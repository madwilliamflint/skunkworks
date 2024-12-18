import asyncio
import websockets
import json

async def echo_client():
    uri = ""
    try:
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            message = input("Enter a message to send: ")
            envelope = json.dumps({"message": message})
            await websocket.send(envelope)
            response = await websocket.recv()
            data = json.loads(response)
            print(f"Received from server: {data['message']}")
    except ConnectionRefusedError as e:
        print("Failed to connect to [{0}]".format(uri))
    

asyncio.get_event_loop().run_until_complete(echo_client())

