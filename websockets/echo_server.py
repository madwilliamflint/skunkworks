import asyncio
import websockets
import json


def log(message):
    print(message)

    
async def echo(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        log(json.dumps(message,sort_keys=True,indent=4))
        print(f"Received message: {data['message']}")
        response = json.dumps({"message": data['message']})
        await websocket.send(response)

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
