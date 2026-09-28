"""Personagem 2D "rigado": transforma a FOTO de corpo inteiro em uma marionete
controlada pelo esqueleto da pessoa do vídeo.

1. Recorta o personagem da foto (máscara do MediaPipe refinada com GrabCut,
   ou o canal alfa se a foto for um PNG transparente).
2. Cobre o personagem com uma malha de triângulos.
3. Liga cada vértice aos ossos mais próximos (cabeça, pescoço, tronco,
   braços, antebraços, mãos, coxas, canelas, pés) – "skinning".
4. Em cada quadro do vídeo, calcula como cada osso se moveu e deforma a malha
   (linear blend skinning), desenhando os membros mais distantes primeiro.
"""
from __future__ import annotations

import cv2
import numpy as np

from .pose import (L_AN, L_EAR, L_EL, L_FT, L_HIP, L_IDX, L_KN, L_SH, L_WR, NOSE,
                   R_AN, R_EAR, R_EL, R_FT, R_HIP, R_IDX, R_KN, R_SH, R_WR, PoseResult,
                   detect_image)

LIMBS = [  # (nome, a, b)
    ("braco_e", L_SH, L_EL), ("antebraco_e", L_EL, L_WR), ("mao_e", L_WR, L_IDX),
    ("braco_d", R_SH, R_EL), ("antebraco_d", R_EL, R_WR), ("mao_d", R_WR, R_IDX),
    ("coxa_e", L_HIP, L_KN), ("canela_e", L_KN, L_AN), ("pe_e", L_AN, L_FT),
    ("coxa_d", R_HIP, R_KN), ("canela_d", R_KN, R_AN), ("pe_d", R_AN, R_FT),
]
TORSO = [L_SH, R_SH, R_HIP, L_HIP]
HEAD_PTS = [NOSE, 2, 5, L_EAR, R_EAR]  # nariz, olhos, orelhas
BONES = ["tronco", "cabeca", "pescoco"] + [n for n, _, _ in LIMBS]
NB = len(BONES)


class NoPersonError(RuntimeError):
    pass


def _mid(p, i, j):
    return (p[i] + p[j]) / 2


def _head_center(p):
    return p[[NOSE, L_EAR, R_EAR]].mean(0)


def _torso_len(p):
    return float(np.linalg.norm(_mid(p, L_SH, R_SH) - _mid(p, L_HIP, R_HIP))) + 1e-3


def _seg_dist(x, a, b):
    ab = b - a
    t = np.clip(((x - a) @ ab) / (ab @ ab + 1e-6), 0, 1)
    return np.linalg.norm(x - (a + t[:, None] * ab), axis=1)


def _limb_affine(A, B, A2, B2, s):
    """Afim que leva o osso A->B em A2->B2: estica ao longo do osso pela razão
    de comprimento e na largura pela escala global s (membros não afinam)."""
    d, d2 = B - A, B2 - A2
    L, L2 = np.linalg.norm(d) + 1e-6, np.linalg.norm(d2) + 1e-6
    u, u2 = d / L, d2 / L2
    v, v2 = np.array([-u[1], u[0]]), np.array([-u2[1], u2[0]])
    r = max(L2 / L, 0.35 * s)
    R = r * np.outer(u2, u) + s * np.outer(v2, v)  # 2x2
    t = A2 - R @ A
    return np.hstack([R, t[:, None]]).astype(np.float32)


def refine_mask(bgr: np.ndarray, soft: np.ndarray, pose: PoseResult | None = None) -> np.ndarray:
    """Máscara da pessoa (0-255) mais nítida com GrabCut. O esqueleto entra
    como semente: braços/mãos que o recorte automático perde são recuperados."""
    m = np.full(soft.shape, cv2.GC_PR_BGD, np.uint8)
    m[soft < 0.02] = cv2.GC_BGD
    if pose is not None:
        q, v = pose.pts, pose.vis
        sw = float(np.linalg.norm(q[L_SH] - q[R_SH]))
        region = np.zeros(soft.shape, np.uint8)
        seed = np.zeros(soft.shape, np.uint8)
        for _, a, b in LIMBS[:6]:  # braços e mãos
            if min(v[a], v[b]) > 0.4:
                pa, pb = tuple(q[a].astype(int)), tuple(q[b].astype(int))
                cv2.line(region, pa, pb, 255, max(6, int(sw * 0.45)))
                cv2.line(seed, pa, pb, 255, max(2, int(sw * 0.05)))
        m[region > 0] = cv2.GC_PR_FGD
        m[seed > 0] = cv2.GC_FGD
    m[soft > 0.15] = cv2.GC_PR_FGD
    m[soft > 0.85] = cv2.GC_FGD
    if (m == cv2.GC_FGD).sum() < 100:
        return (soft > 0.5).astype(np.uint8) * 255
    try:
        bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
        cv2.grabCut(bgr, m, None, bgd, fgd, 4, cv2.GC_INIT_WITH_MASK)
        out = np.where((m == cv2.GC_FGD) | (m == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    except cv2.error:
        out = (soft > 0.5).astype(np.uint8) * 255
    # mantém só o maior pedaço
    n, lab, stats, _ = cv2.connectedComponentsWithStats(out)
    if n > 2:
        big = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        out = np.where(lab == big, 255, 0).astype(np.uint8)
    return cv2.morphologyEx(out, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))


def skeleton_mask(Q: PoseResult, shape, vis_min: float = 0.5) -> np.ndarray:
    """Máscara grosseira do corpo desenhada a partir do esqueleto."""
    h, w = shape
    m = np.zeros((h, w), np.uint8)
    q, v = Q.pts, Q.vis
    sw = float(np.linalg.norm(q[L_SH] - q[R_SH]))
    ear = float(np.linalg.norm(q[L_EAR] - q[R_EAR]))
    thick = max(4, int(max(sw * 0.35, ear * 0.6)))
    if min(v[TORSO]) > vis_min:
        cv2.fillConvexPoly(m, cv2.convexHull(q[TORSO].astype(np.int32)), 255)
    cv2.circle(m, tuple(_head_center(q).astype(int)), int(max(ear * 0.95, sw * 0.3)), 255, -1)
    cv2.line(m, tuple(_mid(q, L_SH, R_SH).astype(int)), tuple(_head_center(q).astype(int)), 255, thick)
    cv2.line(m, tuple(q[L_SH].astype(int)), tuple(q[R_SH].astype(int)), 255, thick)
    for _, a, b in LIMBS:
        if min(v[a], v[b]) > vis_min:
            cv2.line(m, tuple(q[a].astype(int)), tuple(q[b].astype(int)), 255, thick)
    return m


class Character:
    def __init__(self, image: np.ndarray):
        alpha = None
        if image.ndim == 3 and image.shape[2] == 4:
            alpha = image[:, :, 3]
            bgr = image[:, :, :3].copy()
            bgr[alpha < 10] = 255
        else:
            bgr = image
        h, w = bgr.shape[:2]
        s = min(1.0, 1400 / max(h, w))
        if s < 1:
            bgr = cv2.resize(bgr, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
            if alpha is not None:
                alpha = cv2.resize(alpha, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        pose = detect_image(bgr)
        if pose is None:
            raise NoPersonError("Não encontrei uma pessoa/personagem de corpo na FOTO. "
                                "Use uma foto de corpo inteiro (ou da cintura para cima), de frente.")
        mask = alpha if alpha is not None else refine_mask(bgr, pose.mask, pose)
        ys, xs = np.nonzero(mask > 127)
        if len(xs) < 500:
            raise NoPersonError("Não consegui recortar o personagem da foto.")
        pad = 10
        x0, y0 = max(0, xs.min() - pad), max(0, ys.min() - pad)
        x1, y1 = min(bgr.shape[1], xs.max() + pad), min(bgr.shape[0], ys.max() + pad)
        self.img = np.ascontiguousarray(bgr[y0:y1, x0:x1])
        self.alpha = np.ascontiguousarray(mask[y0:y1, x0:x1])
        self.P = pose.pts - [x0, y0]
        self.vis = pose.vis
        self.full_bgr, self.offset = bgr, (x0, y0)
        self._build_mesh()
        self._build_weights()

    # ------------------------------------------------------------------ malha
    def _build_mesh(self):
        h, w = self.alpha.shape
        step = max(4, int(max(h, w) / 70))
        inside = cv2.erode((self.alpha > 127).astype(np.uint8), np.ones((3, 3), np.uint8))
        gy, gx = np.mgrid[step // 2:h:step, step // 2:w:step]
        grid = np.stack([gx.ravel(), gy.ravel()], 1)
        grid = grid[inside[grid[:, 1], grid[:, 0]] > 0]
        cnts, _ = cv2.findContours((self.alpha > 127).astype(np.uint8), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_NONE)
        border = []
        for c in cnts:
            c = c[:, 0, :]
            if len(c) > 10:
                border.append(c[:: max(1, step // 2)])
        pts = np.vstack([grid] + border).astype(np.float32) if border else grid.astype(np.float32)
        # remove duplicados próximos
        _, keep = np.unique(np.round(pts / 2), axis=0, return_index=True)
        pts = pts[np.sort(keep)]
        subdiv = cv2.Subdiv2D((0, 0, w + 1, h + 1))
        for x, y in pts:
            subdiv.insert((float(x), float(y)))
        tri_xy = subdiv.getTriangleList().reshape(-1, 3, 2)
        # mapeia coordenadas -> índice
        index = {(round(float(x), 1), round(float(y), 1)): i for i, (x, y) in enumerate(pts)}
        tris = []
        solid = (self.alpha > 60).astype(np.uint8)
        for t in tri_xy:
            ids = [index.get((round(float(x), 1), round(float(y), 1))) for x, y in t]
            if None in ids:
                continue
            c = t.mean(0).astype(int)
            if not (0 <= c[0] < w and 0 <= c[1] < h) or not solid[c[1], c[0]]:
                continue
            # descarta triângulos que atravessam "buracos" (ex.: entre braço e tronco)
            mids = ((t + np.roll(t, 1, 0)) / 2).astype(int)
            mids[:, 0] = np.clip(mids[:, 0], 0, w - 1)
            mids[:, 1] = np.clip(mids[:, 1], 0, h - 1)
            if solid[mids[:, 1], mids[:, 0]].sum() < 2:
                continue
            tris.append(ids)
        self.V = pts
        self.T = np.array(tris, np.int32)
        a = self.V[self.T]
        self.tri_len = np.max(np.linalg.norm(a - np.roll(a, 1, 1), axis=2), axis=1)

    # --------------------------------------------------------------- skinning
    def _bone_dists(self) -> np.ndarray:
        P, V = self.P, self.V
        D = np.full((len(V), NB), np.inf, np.float32)
        tl = _torso_len(P)
        poly = P[TORSO].astype(np.float32).reshape(-1, 1, 2)
        D[:, 0] = [max(0.0, -cv2.pointPolygonTest(poly, (float(x), float(y)), True)) for x, y in V]
        hc = _head_center(P)
        hr = max(np.linalg.norm(P[L_EAR] - P[R_EAR]) * 0.5, tl * 0.12)
        D[:, 1] = np.maximum(0, np.linalg.norm(V - hc, axis=1) - hr)
        D[:, 2] = _seg_dist(V, _mid(P, L_SH, R_SH), hc) + tl * 0.05
        for k, (_, a, b) in enumerate(LIMBS):
            if min(self.vis[a], self.vis[b]) < 0.2:  # osso não aparece na foto
                continue
            D[:, 3 + k] = _seg_dist(V, P[a], P[b])
        return D

    def _build_weights(self):
        D = self._bone_dists()
        eps = _torso_len(self.P) * 0.04
        W = 1.0 / (D + eps) ** 4
        W[~np.isfinite(D)] = 0
        # mantém os 3 ossos mais fortes
        idx = np.argsort(-W, axis=1)[:, 3:]
        np.put_along_axis(W, idx, 0, axis=1)
        W /= W.sum(1, keepdims=True) + 1e-12
        self.W = W.astype(np.float32)
        self.dom = np.argmax(W, 1)

    # --------------------------------------------------------------- por quadro
    def scale_candidates(self, Q: PoseResult) -> dict:
        P, q = self.P, Q.pts
        c = {"ombros": np.linalg.norm(q[L_SH] - q[R_SH]) / (np.linalg.norm(P[L_SH] - P[R_SH]) + 1e-3),
             "cabeca": np.linalg.norm(q[L_EAR] - q[R_EAR]) / (np.linalg.norm(P[L_EAR] - P[R_EAR]) + 1e-3)}
        if min(Q.vis[L_HIP], Q.vis[R_HIP]) > 0.5 and min(self.vis[L_HIP], self.vis[R_HIP]) > 0.5:
            c["tronco"] = _torso_len(q) / _torso_len(P)
        return {k: float(v) for k, v in c.items()}

    def robust_scale(self, Q: PoseResult) -> float:
        """Mediana das escalas (ombros, cabeça, tronco): resiste a um ponto errado."""
        c = list(self.scale_candidates(Q).values())
        if len(c) == 2:  # sem tronco: média geométrica
            return float(np.sqrt(c[0] * c[1]))
        return float(np.median(c))

    def bone_transforms(self, Q: PoseResult, s: float | None = None):
        P, q = self.P, Q.pts
        if s is None:
            s = self.robust_scale(Q)
        T = np.zeros((NB, 2, 3), np.float32)
        st = self.scale_candidates(Q).get("tronco")
        hips_ok = st is not None and 0.7 < st / s < 1.4  # quadris coerentes com o resto?
        M = cv2.estimateAffine2D(P[TORSO], q[TORSO])[0] if hips_ok else None
        if M is not None:  # evita tronco achatado/cisalhado demais
            sv = np.linalg.svd(M[:, :2], compute_uv=False)
            if sv.min() < 0.55 * s or sv.max() > 1.8 * s:
                M = None
        if M is None:
            # quadris fora do quadro: tronco segue a linha dos ombros (rotação + escala s)
            a, b, a2, b2 = P[R_SH], P[L_SH], q[R_SH], q[L_SH]
            ang = np.arctan2(*(b2 - a2)[::-1]) - np.arctan2(*(b - a)[::-1])
            R = s * np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
            c, c2 = (a + b) / 2, (a2 + b2) / 2
            M = np.hstack([R, (c2 - R @ c)[:, None]]).astype(np.float32)
        T[0] = M
        Hm, _ = cv2.estimateAffinePartial2D(P[HEAD_PTS], q[HEAD_PTS])
        if Hm is None:
            Hm = M
        else:
            hs = np.sqrt(abs(np.linalg.det(Hm[:, :2])))
            hs_c = np.clip(hs, 0.8 * s, 1.25 * s)
            Hm[:, :2] *= hs_c / (hs + 1e-6)
            # mantém o centro da cabeça no lugar certo
            c = _head_center(P)
            Hm[:, 2] += _head_center(q) - (Hm[:, :2] @ c + Hm[:, 2])
        T[1] = Hm
        T[2] = _limb_affine(_mid(P, L_SH, R_SH), _head_center(P), _mid(q, L_SH, R_SH), _head_center(q), s)
        depth = np.zeros(NB, np.float32)
        hidden = np.zeros(NB, bool)
        depth[0] = Q.z[TORSO].mean()
        depth[1] = depth[2] = Q.z[[NOSE, L_EAR, R_EAR]].mean()
        for k, (_, a, b) in enumerate(LIMBS):
            T[3 + k] = _limb_affine(P[a], P[b], q[a], q[b], s)
            depth[3 + k] = (Q.z[a] + Q.z[b]) / 2
            hidden[3 + k] = min(Q.vis[a], Q.vis[b]) < 0.3
        return T, depth, hidden, s

    def render(self, Q: PoseResult, frame_shape, hide_occluded: bool = True, s: float | None = None):
        """Devolve (rgb, alpha) do personagem já posicionado no quadro."""
        H, W_ = frame_shape[:2]
        T, depth, hidden, s = self.bone_transforms(Q, s)
        Vh = np.hstack([self.V, np.ones((len(self.V), 1), np.float32)])  # V,3
        per_bone = np.einsum("bij,vj->vbi", T, Vh)  # V,B,2
        V2 = np.einsum("vb,vbi->vi", self.W, per_bone)

        tris = self.T
        dom = self.dom[tris]  # T,3
        tri_bone = np.array([np.bincount(r, minlength=NB).argmax() for r in dom])
        keep = np.ones(len(tris), bool)
        # remove triângulos muito esticados (pele "grudada" entre partes)
        a = V2[tris]
        new_len = np.max(np.linalg.norm(a - np.roll(a, 1, 1), axis=2), axis=1)
        keep &= new_len < np.maximum(self.tri_len * s * 3.0, 6)
        if hide_occluded:
            keep &= ~hidden[tri_bone]
        tris, tri_bone = tris[keep], tri_bone[keep]
        if len(tris) == 0:
            return None, None
        order = np.argsort(-depth[tri_bone], kind="stable")  # mais longe primeiro
        tris = tris[order]

        x0, y0 = np.floor(V2[tris].reshape(-1, 2).min(0)).astype(int) - 2
        x1, y1 = np.ceil(V2[tris].reshape(-1, 2).max(0)).astype(int) + 2
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W_), min(y1, H)
        if x1 - x0 < 4 or y1 - y0 < 4:
            return None, None
        local = V2 - [x0, y0]
        idx_map = np.zeros((y1 - y0, x1 - x0), np.int32)
        poly = np.round(local[tris] * 4).astype(np.int32)
        for t in range(len(tris)):
            cv2.fillConvexPoly(idx_map, poly[t], t + 1, lineType=cv2.LINE_8, shift=2)
        D = np.concatenate([local[tris], np.ones((len(tris), 3, 1), np.float32)], 2)
        M = np.linalg.pinv(D) @ self.V[tris]  # destino -> origem
        ys, xs = np.nonzero(idx_map)
        m = M[idx_map[ys, xs] - 1]
        map_x = np.full(idx_map.shape, -1, np.float32)
        map_y = np.full(idx_map.shape, -1, np.float32)
        map_x[ys, xs] = xs * m[:, 0, 0] + ys * m[:, 1, 0] + m[:, 2, 0]
        map_y[ys, xs] = xs * m[:, 0, 1] + ys * m[:, 1, 1] + m[:, 2, 1]
        rgb = cv2.remap(self.img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        al = cv2.remap(self.alpha, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                       borderValue=0)
        al[idx_map == 0] = 0
        full_rgb = np.zeros((H, W_, 3), np.uint8)
        full_a = np.zeros((H, W_), np.uint8)
        full_rgb[y0:y1, x0:x1] = rgb
        full_a[y0:y1, x0:x1] = al
        return full_rgb, full_a
