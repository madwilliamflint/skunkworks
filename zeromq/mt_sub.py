import zmq

def log(message):
    print(message)

def run():
    context = zmq.Context()
    sub = context.socket(zmq.SUB)

    try:
        result = sub.connect("tcp://127.0.0.1:5100")
        sub.setsockopt(zmq.SUBSCRIBE, b'two')  # Subscribe to the topic "two"
        print("Result [{0}]".format(result))

        while True:
            try:
                message = sub.recv_string()
                topic, number = message.split()
                print(f"Received data from topic {topic}: {number}")
            except zmq.ZMQError as e:
                log("ZMQ Error: [{0}]".format(e))
    except KeyboardInterrupt:
        log("Keyboard interrupt received.  Exiting.")

if __name__ == '__main__':
    run()
