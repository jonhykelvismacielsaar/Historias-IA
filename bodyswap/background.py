"""Apaga a pessoa original do vídeo ("clean plate").

Para cada quadro, a região onde a pessoa está é preenchida com pixels de
outros quadros (onde aquele pedaço do fundo aparecia), alinhados por
homografia para compensar movimento/zoom da câmera. O que nunca aparece é
preenchido por inpainting.
"""
from __future__ import annotations

import cv2
import numpy as np


class BackgroundFiller:
    def __init__(self, frames: list[np.ndarray], masks: list[np.ndarray], n_neighbors: int = 10):
        self.frames = frames
        self.masks = masks  # uint8 0/255, pessoa (dilatada)
        self.n = len(frames)
        self.k = n_neighbors
        self.orb = cv2.ORB_create(1500)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.feats = []
        for f, m in zip(frames, masks):
            g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            kp, des = self.orb.detectAndCompute(g, cv2.bitwise_not(m))
            self.feats.append((np.float32([k.pt for k in kp]) if kp else np.zeros((0, 2), np.float32), des))
        self._H: dict[tuple[int, int], np.ndarray | None] = {}
        self.static = self._detect_static()

    def _detect_static(self) -> bool:
        """Câmera parada? (compara alguns pares de quadros)"""
        if self.n < 3:
            return True
        idx = np.linspace(0, self.n - 1, min(6, self.n)).astype(int)
        for a, b in zip(idx[:-1], idx[1:]):
            H = self._homography(a, b)
            if H is None:
                return False
            corners = np.float32([[0, 0], [1, 0], [1, 1], [0, 1]]) * self.frames[0].shape[1::-1]
            moved = cv2.perspectiveTransform(corners[None], H)[0]
            if np.abs(moved - corners).max() > 3.0:
                return False
        return True

    def _homography(self, src: int, dst: int):
        key = (src, dst)
        if key in self._H:
            return self._H[key]
        (p1, d1), (p2, d2) = self.feats[src], self.feats[dst]
        H = None
        if d1 is not None and d2 is not None and len(p1) > 20 and len(p2) > 20:
            ms = self.bf.match(d1, d2)
            if len(ms) > 20:
                a = p1[[m.queryIdx for m in ms]]
                b = p2[[m.trainIdx for m in ms]]
                H, inl = cv2.findHomography(a, b, cv2.RANSAC, 3.0)
                if H is None or inl.sum() < 15:
                    H = None
        self._H[key] = H
        return H

    def fill(self, t: int) -> np.ndarray:
        frame, hole = self.frames[t], self.masks[t]
        if hole.max() == 0:
            return frame
        h, w = hole.shape
        # vizinhos espalhados no tempo (longe primeiro = pessoa em outro lugar)
        cand = np.unique(np.linspace(0, self.n - 1, min(self.n, self.k * 3)).astype(int))
        cand = sorted((c for c in cand if c != t), key=lambda c: -abs(c - t))[: self.k * 2]
        stack, valid = [], []
        need = hole > 0
        for j in cand:
            if self.static:
                wf, wm = self.frames[j], self.masks[j]
            else:
                H = self._homography(j, t)
                if H is None:
                    continue
                wf = cv2.warpPerspective(self.frames[j], H, (w, h), flags=cv2.INTER_LINEAR,
                                         borderMode=cv2.BORDER_CONSTANT)
                wm = cv2.warpPerspective(self.masks[j], H, (w, h), flags=cv2.INTER_NEAREST,
                                         borderMode=cv2.BORDER_CONSTANT, borderValue=255)
            ok = need & (wm == 0)
            if ok.any():
                stack.append(wf)
                valid.append(ok)
            if len(stack) >= self.k:
                break
        out = frame.copy()
        remaining = need.copy()
        if stack:
            S = np.stack(stack).astype(np.float32)
            Vd = np.stack(valid)
            S[~Vd] = np.nan
            with np.errstate(all="ignore"):
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    med = np.nanmedian(S[:, need], axis=0)  # (K, 3) -> (N,3)
            got = ~np.isnan(med[:, 0])
            coords = np.nonzero(need)
            out[coords[0][got], coords[1][got]] = med[got].astype(np.uint8)
            remaining[coords[0][got], coords[1][got]] = False
        if remaining.any():
            # inpainting em meia resolução (rápido) para o que nunca apareceu
            small = cv2.resize(out, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
            rm = cv2.resize(remaining.astype(np.uint8) * 255, (w // 2, h // 2), interpolation=cv2.INTER_NEAREST)
            rm = cv2.dilate(rm, np.ones((3, 3), np.uint8))
            inp = cv2.inpaint(small, rm, 5, cv2.INPAINT_TELEA)
            inp = cv2.resize(inp, (w, h), interpolation=cv2.INTER_LINEAR)
            out[remaining] = inp[remaining]
        # borda suave entre original e preenchido
        soft = cv2.GaussianBlur(hole, (0, 0), 3).astype(np.float32)[..., None] / 255.0
        return (out * soft + frame * (1 - soft)).astype(np.uint8)
