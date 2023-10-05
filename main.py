import cv2
import numpy as np

import pyk4a
from pyk4a import Config, PyK4A

def clip_and_crop(
    image: np.ndarray,
) -> np.ndarray:

    return image[y1:y2, x1:x2].clip(500, 1100) # clamps values between min and max

def colorize(
    image: np.ndarray,
    colormap: int = cv2.COLORMAP_HOT,
) -> np.ndarray:

    img = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U) #grayscale
    return cv2.applyColorMap(img, colormap)

x1, y1 = 70, 47
x2, y2 = 1072, 705
push_threshold = 100
calibration_depth = None

def test(
    image: np.ndarray,
) -> np.ndarray:
    normalized_image = (image - 500) / (calibration_depth - 500)
    # OUR PAST PROBLEM
    normalized_image = 1 - np.clip(normalized_image, 0, 1)
    return (normalized_image * 255).astype(np.uint8)

def main():
    global calibration_depth

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
        calibration_depth = clip_and_crop(capture.transformed_depth)

    while True:
        capture = k4a.get_capture()
        if np.any(capture.transformed_depth):
            depth_frame = clip_and_crop(capture.transformed_depth)
            cv2.imshow('k4a', test(depth_frame))

            key = cv2.waitKey(10)
            if key != -1:
                cv2.destroyAllWindows()
                break

    k4a.stop()

if __name__ == "__main__":
    main()