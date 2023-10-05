import asyncio
from websockets.server import serve

async def send_data(websocket):
    while True:
        # Send data to the client periodically
        data_to_send = "Hello from the server!"
        await websocket.send(data_to_send)
        await asyncio.sleep(1)

async def main():
  async with serve(send_data, "localhost", 12345):
    await asyncio.Future()  # run forever

asyncio.run(main())