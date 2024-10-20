import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")  # Connect to the publisher

# Subscribe to all topics (empty string means all)
socket.setsockopt_string(zmq.SUBSCRIBE, "")

while True:
    topic, message = socket.recv_multipart()
    print(f"Received: {topic.decode()} - {message.decode()}")
