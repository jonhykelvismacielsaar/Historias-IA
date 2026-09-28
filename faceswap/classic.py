"""Motor CLÁSSICO de troca de rosto (sem rede neural de troca).

Como funciona:
  1. Pega os 468 pontos do rosto da FOTO e os 468 pontos do rosto em cada
     quadro do VÍDEO (MediaPipe).
  2. Divide o rosto em ~900 triângulos e "estica" cada triângulo da foto até a
     posição correspondente no vídeo (deformação por partes / piecewise affine).
     Assim o rosto novo acompanha a boca, os olhos e a pose da pessoa do vídeo.
  3. Ajusta a cor/iluminação para bater com o vídeo e mistura as bordas.
  4. O interior da boca do vídeo original é preservado (dentes/língua reais).

Vantagem: roda em qualquer CPU e não precisa de download.
Limitação: é menos realista que o motor com IA (inswapper) e sofre com
rostos muito de perfil.
"""
from __future__ import annotations

import cv2
import numpy as np

from .landmarks import FACE_OVAL, INNER_LIPS, LEFT_EYE, RIGHT_EYE, OUTER_LIPS


def _delaunay(points: np.ndarray, w: int, h: int) -> np.ndarray:
    rect = (0, 0, w + 1, h + 1)
    subdiv = cv2.Subdiv2D(rect)
    pts = np.clip(points, 0, [w, h]).astype(np.float32)
    lookup = {}
    for i, (x, y) in enumerate(pts):
        subdiv.insert((float(x), float(y)))
        lookup.setdefault((round(float(x), 2), round(float(y), 2)), i)
    tris = []
    for t in subdiv.getTriangleList():
        ids = []
        for k in range(3):
            key = (round(float(t[2 * k]), 2), round(float(t[2 * k + 1]), 2))
            if key not in lookup:
                # busca pelo mais próximo (erros de arredondamento)
                d = np.sum((pts - [t[2 * k], t[2 * k + 1]]) ** 2, axis=1)
                j = int(np.argmin(d))
                if d[j] > 1.0:
                    break
                ids.append(j)
            else:
                ids.append(lookup[key])
        if len(ids) == 3 and len(set(ids)) == 3:
            tris.append(ids)
    return np.array(tris, dtype=np.int32)


def _signed_area(p: np.ndarray, tris: np.ndarray) -> np.ndarray:
    a, b, c = p[tris[:, 0]], p[tris[:, 1]], p[tris[:, 2]]
    return (b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (c[:, 0] - a[:, 0]) * (b[:, 1] - a[:, 1])


class ClassicSwapper:
    name = "classico"

    def __init__(self, source_bgr: np.ndarray, source_landmarks: np.ndarray,
                 blend: str = "seamless", keep_mouth: bool = True):
        # Limita o tamanho da foto para ficar rápido
        h, w = source_bgr.shape[:2]
        s = min(1.0, 1280 / max(h, w))
        if s < 1.0:
            source_bgr = cv2.resize(source_bgr, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
            source_landmarks = source_landmarks * s
        self.src = source_bgr
        self.src_pts = source_landmarks[:468].astype(np.float32)
        hh, ww = self.src.shape[:2]
        self.tris = _delaunay(self.src_pts, ww, hh)
        self.src_area_sign = np.sign(_signed_area(self.src_pts, self.tris))
        self.blend = blend
        self.keep_mouth = keep_mouth
        self.shrink = 0.9
        self.src_skin = self._skin_mask(self.src, self.src_pts)
        self._color_state: dict[int, tuple[np.ndarray, np.ndarray]] = {}

    # ------------------------------------------------------------ skin mask
    @staticmethod
    def _skin_mask(img: np.ndarray, pts: np.ndarray) -> np.ndarray:
        """Máscara (0-255) do que é PELE no rosto da foto. Remove cabelo,
        óculos escuros, mãos ou fundo que invadem o contorno do rosto."""
        lab = cv2.cvtColor(cv2.GaussianBlur(img, (5, 5), 0), cv2.COLOR_BGR2LAB).astype(np.float32)
        sample = np.zeros(img.shape[:2], np.uint8)
        c = pts[[1, 6, 168, 197]].mean(0)
        inner = c + (pts[FACE_OVAL] - c) * 0.6
        cv2.fillConvexPoly(sample, cv2.convexHull(inner.astype(np.int32)), 255)
        for eye in (LEFT_EYE, RIGHT_EYE):  # olhos/sobrancelhas não são pele
            cv2.fillConvexPoly(sample, cv2.convexHull(pts[eye].astype(np.int32)), 0)
        cv2.fillPoly(sample, [pts[OUTER_LIPS].astype(np.int32)], 0)
        px = lab[sample > 0]
        if len(px) < 100:
            return np.full(img.shape[:2], 255, np.uint8)
        mean = px.mean(0)
        cov = np.cov(px.T) + np.diag([10.0, 1.0, 1.0])
        inv = np.linalg.inv(cov)
        d = lab.reshape(-1, 3) - mean
        m = np.sqrt(np.einsum("ij,jk,ik->i", d, inv, d)).reshape(img.shape[:2])
        skin = np.clip((3.2 - m) / 1.0, 0, 1)  # 1 = pele, 0 = não-pele
        # tudo que está dentro do rosto interno conta como pele (olhos, boca)
        core = np.zeros(img.shape[:2], np.uint8)
        cv2.fillConvexPoly(core, cv2.convexHull((c + (pts[FACE_OVAL] - c) * 0.72).astype(np.int32)), 255)
        skin = np.maximum(skin, core / 255.0)
        skin = cv2.morphologyEx((skin * 255).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        return cv2.GaussianBlur(skin, (9, 9), 0)

    # ------------------------------------------------------------------ warp
    def _warp(self, dst_pts: np.ndarray, frame_shape) -> tuple[np.ndarray, np.ndarray, tuple]:
        H, W = frame_shape[:2]
        x0, y0 = np.floor(dst_pts.min(0)).astype(int) - 2
        x1, y1 = np.ceil(dst_pts.max(0)).astype(int) + 2
        x0, y0 = max(x0, 0), max(y0, 0)
        x1, y1 = min(x1, W), min(y1, H)
        bw, bh = x1 - x0, y1 - y0
        if bw < 8 or bh < 8:
            return None, None, None

        local = dst_pts - [x0, y0]
        # descarta triângulos "virados" (lado escondido do rosto)
        sign = np.sign(_signed_area(local, self.tris))
        keep = sign == self.src_area_sign
        tris = self.tris[keep]
        if len(tris) == 0:
            return None, None, None

        # Mapa de índice de triângulo (qual triângulo cobre cada pixel)
        idx_map = np.zeros((bh, bw), dtype=np.int32)
        poly = np.round(local[tris] * 4).astype(np.int32)  # subpixel (shift=2)
        for t in range(len(tris)):
            cv2.fillConvexPoly(idx_map, poly[t], t + 1, lineType=cv2.LINE_8, shift=2)

        # Afins destino->origem de cada triângulo (vetorizado)
        D = np.concatenate([local[tris], np.ones((len(tris), 3, 1), np.float32)], axis=2)  # T,3,3
        S = self.src_pts[tris]  # T,3,2
        M = np.linalg.pinv(D) @ S  # T,3,2

        ys, xs = np.nonzero(idx_map)
        tid = idx_map[ys, xs] - 1
        m = M[tid]  # K,3,2
        sx = xs * m[:, 0, 0] + ys * m[:, 1, 0] + m[:, 2, 0]
        sy = xs * m[:, 0, 1] + ys * m[:, 1, 1] + m[:, 2, 1]
        map_x = np.full((bh, bw), -1, np.float32)
        map_y = np.full((bh, bw), -1, np.float32)
        map_x[ys, xs] = sx
        map_y[ys, xs] = sy
        warped = cv2.remap(self.src, map_x, map_y, cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_REPLICATE)
        skin = cv2.remap(self.src_skin, map_x, map_y, cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        covered = np.where(idx_map > 0, skin, 0).astype(np.uint8)
        return warped, covered, (x0, y0, x1, y1)

    # ------------------------------------------------------------------ mask
    def _mask(self, dst_pts: np.ndarray, box, covered: np.ndarray) -> np.ndarray:
        x0, y0, x1, y1 = box
        local = (dst_pts - [x0, y0]).astype(np.int32)
        mask = np.zeros(covered.shape, np.uint8)
        # encolhe o contorno em direção ao centro do rosto (evita puxar
        # cabelo/fundo da foto que ficam colados na borda do rosto)
        oval = local[FACE_OVAL].astype(np.float32)
        center = local[[1, 6, 168, 197]].mean(0)  # nariz / entre os olhos
        oval = center + (oval - center) * self.shrink
        hull = cv2.convexHull(oval.astype(np.int32))
        cv2.fillConvexPoly(mask, hull, 255)
        mask = np.minimum(mask, covered)
        face_size = max(8, int(np.sqrt(cv2.contourArea(hull) + 1)))
        if self.keep_mouth:
            mouth = local[INNER_LIPS]
            mh = np.ptp(mouth[:, 1])
            if mh > face_size * 0.025:  # boca aberta -> mostra a boca real
                mouth_mask = np.zeros_like(mask)
                cv2.fillPoly(mouth_mask, [mouth], 255)
                k = max(1, face_size // 80)
                mouth_mask = cv2.dilate(mouth_mask, np.ones((k, k), np.uint8))
                mask[mouth_mask > 0] = 0
        k = max(3, face_size // 25)
        mask = cv2.erode(mask, np.ones((k, k), np.uint8))
        b = max(3, face_size // 12) | 1
        mask = cv2.GaussianBlur(mask, (b, b), 0)
        return mask

    # ----------------------------------------------------------------- color
    def _color_match(self, warped, target, core, face_id: int):
        sel = core > 200
        if sel.sum() < 50:
            return warped
        wl = cv2.cvtColor(warped, cv2.COLOR_BGR2LAB).astype(np.float32)
        tl = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype(np.float32)
        ws, ts = wl[sel], tl[sel]
        w_mean, w_std = ws.mean(0), ws.std(0) + 1e-3
        t_mean, t_std = ts.mean(0), ts.std(0) + 1e-3
        gain = np.clip(t_std / w_std, 0.6, 1.6)
        shift = t_mean - w_mean * gain
        # suaviza no tempo para não piscar
        if face_id in self._color_state:
            pg, ps = self._color_state[face_id]
            gain = 0.8 * pg + 0.2 * gain
            shift = 0.8 * ps + 0.2 * shift
        self._color_state[face_id] = (gain, shift)
        out = wl * gain + shift
        return cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)

    # ------------------------------------------------------------------ main
    def swap_face(self, frame: np.ndarray, dst_landmarks: np.ndarray, face_id: int = 0) -> np.ndarray:
        dst = dst_landmarks[:468].astype(np.float32)
        warped, covered, box = self._warp(dst, frame.shape)
        if warped is None:
            return frame
        x0, y0, x1, y1 = box
        target = frame[y0:y1, x0:x1]
        mask = self._mask(dst, box, covered)
        core = cv2.erode(mask, np.ones((5, 5), np.uint8))
        warped = self._color_match(warped, target, core, face_id)

        if self.blend == "seamless":
            try:
                bin_mask = (mask > 30).astype(np.uint8) * 255
                pad = 4
                big_t = cv2.copyMakeBorder(target, pad, pad, pad, pad, cv2.BORDER_REFLECT)
                big_w = cv2.copyMakeBorder(warped, pad, pad, pad, pad, cv2.BORDER_REFLECT)
                big_m = cv2.copyMakeBorder(bin_mask, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
                ys, xs = np.nonzero(big_m)
                if len(xs):
                    center = (int((xs.min() + xs.max()) / 2), int((ys.min() + ys.max()) / 2))
                    cloned = cv2.seamlessClone(big_w, big_t, big_m, center, cv2.NORMAL_CLONE)
                    warped = cloned[pad:-pad, pad:-pad]
            except cv2.error:
                pass

        a = (mask.astype(np.float32) / 255.0)[..., None]
        out = frame.copy()
        out[y0:y1, x0:x1] = (warped * a + target * (1 - a)).astype(np.uint8)
        return out
