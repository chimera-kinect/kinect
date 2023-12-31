import numpy as np
import asyncio
from websockets.server import serve
import pyk4a
from pyk4a import Config, PyK4A

def clip_and_crop(
    image: np.ndarray,
) -> np.ndarray:

    return image[y1:y2, x1:x2].clip(500, 1100) # clamps values between min and max

def normalize(
    image: np.ndarray,
) -> np.ndarray:
    normalized_image = (image - 500) / (calibration_depth - 500)
    # OUR PAST PROBLEM
    normalized_image = 1 - np.clip(normalized_image, 0, 1)
    return (normalized_image * 255).astype(np.uint8)

def get_bytes(
    image: np.ndarray,
) -> bytes:
    return image.tobytes(order='C')

x1, y1 = 70, 47
x2, y2 = 1072, 705
push_threshold = 100
calibration_depth = None
k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_720P,
            depth_mode=pyk4a.DepthMode.WFOV_UNBINNED,
            synchronized_images_only=False,
            camera_fps=pyk4a.FPS.FPS_15
        )
    )
counter = 0
async def send_data(websocket):
    global counter
    while True:
        # Send data to the client periodically
        capture = k4a.get_capture()
        if np.any(capture.transformed_depth):
            depth_frame = normalize(clip_and_crop(capture.transformed_depth))
            buf = get_bytes(depth_frame)

        await websocket.send(buf)
        print(counter)
        counter+=1

async def main():
    global calibration_depth

    k4a.start()
    capture = k4a.get_capture()
    if np.any(capture.transformed_depth):
        calibration_depth = clip_and_crop(capture.transformed_depth)

    async with serve(send_data, "localhost", 12345):
        await asyncio.Future()

    k4a.stop()

if __name__ == "__main__":
    asyncio.run(main())
