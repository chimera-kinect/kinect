import cv2
import numpy as np

from typing import Optional, Tuple

import pyk4a
from pyk4a import Config, PyK4A

def grayscale(
    image: np.ndarray,
    clipping_range: Tuple[Optional[int], Optional[int]] = (None, None)
) -> np.ndarray:
    if clipping_range[0] or clipping_range[1]:
        img = image.clip(clipping_range[0], clipping_range[1])  # clamps values between min and max
    else:
        img = image.copy()
    
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U) #grayscale
    return img

def colorize(
    image: np.ndarray,
    clipping_range: Tuple[Optional[int], Optional[int]] = (None, None),
    colormap: int = cv2.COLORMAP_HOT,
) -> np.ndarray:
    if clipping_range[0] or clipping_range[1]:
        img = image.clip(clipping_range[0], clipping_range[1])  # clamps values between min and max
    else:
        img = image.copy()
    
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U) #grayscale
    img = cv2.applyColorMap(img, colormap)
    return img

def main():
    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_720P,
            depth_mode=pyk4a.DepthMode.WFOV_UNBINNED,
            synchronized_images_only=False,
            camera_fps=pyk4a.FPS.FPS_15
        )
    )

    k4a.start()

    capture = k4a.get_capture()
    if np.any(capture.transformed_depth):
        img = colorize(capture.transformed_depth, (None, None))
        # correct crop
        cv2.imshow("k4a", cv2.rectangle(img, (70, 47), (1072, 705), (255, 0, 0)))
        key = cv2.waitKey(5000)

    k4a.stop()

if __name__ == "__main__":
    main()