import cv2
import numpy as np

from typing import Optional, Tuple

import pyk4a
from pyk4a import Config, PyK4A

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
    # fileName = input('file name plz\n')
    # framesN = int(input('how many frames? int only plz\n'))

    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.OFF,
            depth_mode=pyk4a.DepthMode.WFOV_UNBINNED,
            synchronized_images_only=False,
            camera_fps=pyk4a.FPS.FPS_15
        )
    )
    k4a.start()

    # with open(f'{fileName}.txt', 'w') as f:
    #     for _ in range(framesN):
    #         capture = k4a.get_capture()
    #         if np.any(capture.depth):
    #             f.write(capture.depth.tobytes())
    #         f.write('???')

    capture = k4a.get_capture()
    if np.any(capture.depth):
        print(np.shape(capture.depth))
            
    k4a.stop()

if __name__ == "__main__":
    main()
