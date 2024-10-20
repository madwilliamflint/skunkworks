import socket

# Server-side code
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
server_socket.listen(1)

print("Listening on port 5000...")

downstream_socket, downstream_address = server_socket.accept()

print("Connection received.  Connecting the upstream")

while True:
    data = downstream_socket.recv(512)
    if not data:
        break

    # Log received data
    print(f"Received: {data.decode()}")

    # Forward data back to the client
    client_socket.send(data)

    # Log sent data
    print(f"Sent: {data.decode()}")

client_socket.close()
server_socket.close()

# Client-side code
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

while True:
    user_input = input("Enter data to send (or 'q' to quit): ")
    if user_input.lower() == 'q':
        break

    client_socket.send(user_input.encode())
    response = client_socket.recv(512)
    print(f"Received from server: {response.decode()}")

client_socket.close()
