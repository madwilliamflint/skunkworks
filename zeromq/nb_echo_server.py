import socket




def main():
    HOST = "127.0.0.1"  # Use your desired IP address or hostname
    PORT = 65432       # Choose an available port (non-privileged)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Server listening on {HOST}:{PORT}")

        # Set the socket to non-blocking mode
        s.setblocking(0)

        while True:
            try:
                conn, addr = s.accept()
                print(f"Connected by {addr}")

                # Set the accepted connection to non-blocking mode
                conn.setblocking(0)

                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        conn.sendall(data)  # Echo back the received data
                    except BlockingIOError:
                        pass  # No data available, continue listening
                    except Exception as e:
                        print(f"Error: {e}")
                        break

                conn.close()
                print(f"Connection closed by {addr}")

            except BlockingIOError:
                pass  # No incoming connections, continue listening
            except KeyboardInterrupt:
                print("\nServer stopped by user.")
                break

if __name__ == "__main__":
    main()