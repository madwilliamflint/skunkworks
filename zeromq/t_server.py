import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")  # Bind to a specific address

while True:
    topic = b"weather"  # Topic prefix
    message = b"Temperature: 25C"  # Your actual message
    socket.send_multipart([topic, message])
