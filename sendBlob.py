"""
Sends the "blob.jpg" image as a frame over a websocket.
Blob was created using this Figma plugin: https://www.figma.com/community/plugin/739208439270091369/blobs
and exported in a 1002*658 image with a black background
"""
import numpy as np
import asyncio
from websockets.server import serve
from PIL import Image

blob = None

def get_bytes(image: np.ndarray) -> bytes:
  return image.tobytes(order='C')

async def send_data(websocket):
  global blob
  while True:
    await websocket.send(blob)

async def main():
  im = Image.open('blob.jpg')
  pix = im.load()
  width, height = im.size
  red_channel = np.zeros((height, width), dtype=np.uint8)

  for y in range(height):
    for x in range(width):
      red_channel[y, x] = pix[x, y][0]

  global blob
  blob = get_bytes(red_channel)

  async with serve(send_data, "localhost", 12345):
    await asyncio.Future()

if __name__ == "__main__":
  asyncio.run(main())