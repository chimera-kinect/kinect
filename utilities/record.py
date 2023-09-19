import cv2
import numpy as np
import pyk4a
from pyk4a import Config, PyK4A
from typing import Optional, Tuple
import random
from os import path

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

def main():
    while not path.isdir('recordings'):
        print('Please create a folder called "recordings" in the same directory as this script, then press any key to continue.')
        input()
    filePath = f'recordings/{input("File name plz: ")}.npy'
    framesN = int(input('How many frames should I record? '))

    k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.OFF,
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            synchronized_images_only=False,
            camera_fps=pyk4a.FPS.FPS_15
        )
    )
    k4a.start()

    frames = []
    for _ in range(framesN):
        capture = k4a.get_capture()
        if np.any(capture.depth):
            # don't feel like making the clipping range a user input rn, sorry ¯\_(ツ)_/¯ (Love, Bozo)
            frames.append(grayscale(capture.depth, (300, 500)))
            
    k4a.stop()

    np.save(filePath, frames)

    # make sure everything was saved correctly
    loaded_frames = np.load(filePath)
    rndFrame = random.randint(0, framesN - 1)
    rndInShape = random.randint(frames[0][0].shape[0], frames[0][0].shape[0])-1
    assert frames[rndFrame].shape == loaded_frames[rndFrame].shape
    assert frames[rndFrame][rndInShape][rndInShape] == loaded_frames[rndFrame][rndInShape][rndInShape]

    # all good
    print(f'Saved frames in {filePath}, bozo.')

if __name__ == "__main__":
    main()
