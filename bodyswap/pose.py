"""Pose do corpo (33 pontos) + máscara da pessoa, usando MediaPipe Pose (CPU)."""
from __future__ import annotations

import os

os.environ.setdefault("GLOG_minloglevel", "2")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import cv2
import mediapipe as mp
import numpy as np

# Índices MediaPipe Pose
NOSE, L_EAR, R_EAR = 0, 7, 8
L_SH, R_SH, L_EL, R_EL, L_WR, R_WR = 11, 12, 13, 14, 15, 16
L_IDX, R_IDX = 19, 20
L_HIP, R_HIP, L_KN, R_KN, L_AN, R_AN = 23, 24, 25, 26, 27, 28
L_FT, R_FT = 31, 32


class PoseResult:
    __slots__ = ("pts", "vis", "z", "mask")

    def __init__(self, pts, vis, z, mask):
        self.pts = pts      # (33,2) pixels
        self.vis = vis      # (33,) 0..1
        self.z = z          # (33,) profundidade relativa (menor = mais perto)
        self.mask = mask    # (H,W) float 0..1 – onde está a pessoa


def plausible(p: "PoseResult | None") -> bool:
    """Descarta poses absurdas (ex.: ombros na altura do nariz)."""
    if p is None:
        return False
    q = p.pts
    sw = np.linalg.norm(q[L_SH] - q[R_SH])
    ear = np.linalg.norm(q[L_EAR] - q[R_EAR]) + 1e-3
    return 1.3 * ear < sw < 5 * ear and (q[L_SH, 1] + q[R_SH, 1]) / 2 > q[NOSE, 1] + 0.3 * ear


def _make_pose(static: bool):
    return mp.solutions.pose.Pose(static_image_mode=static, model_complexity=1,
                                  enable_segmentation=True, smooth_segmentation=not static,
                                  smooth_landmarks=not static,
                                  min_detection_confidence=0.4, min_tracking_confidence=0.4)


class PoseDetector:
    """Em modo vídeo usa rastreamento; se a pose ficar absurda, detecta de novo
    do zero e reinicia o rastreador (o MediaPipe às vezes "trava" numa pose errada)."""

    def __init__(self, video_mode: bool = True):
        self.video_mode = video_mode
        self.pose = _make_pose(static=not video_mode)
        self.static = _make_pose(static=True) if video_mode else None

    def close(self):
        for m in (self.pose, self.static):
            try:
                m and m.close()
            except Exception:
                pass

    def __call__(self, bgr: np.ndarray) -> PoseResult | None:
        res = self._run(self.pose, bgr)
        if self.video_mode and not plausible(res):
            alt = self._run(self.static, bgr)
            if plausible(alt):
                self.pose.close()
                self.pose = _make_pose(static=False)  # reinicia o rastreamento
                self._run(self.pose, bgr)
                return alt
        return res

    @staticmethod
    def _run(model, bgr: np.ndarray) -> PoseResult | None:
        h, w = bgr.shape[:2]
        r = model.process(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
        if r.pose_landmarks is None:
            return None
        lm = r.pose_landmarks.landmark
        pts = np.array([(p.x * w, p.y * h) for p in lm], np.float32)
        vis = np.array([p.visibility for p in lm], np.float32)
        z = np.array([p.z for p in lm], np.float32)
        mask = r.segmentation_mask if r.segmentation_mask is not None else np.zeros((h, w), np.float32)
        return PoseResult(pts, vis, z, mask.astype(np.float32))


def detect_image(bgr: np.ndarray) -> PoseResult | None:
    d = PoseDetector(video_mode=False)
    try:
        return d(bgr)
    finally:
        d.close()
