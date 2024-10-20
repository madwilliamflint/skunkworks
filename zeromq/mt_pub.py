import zmq
import random
import time
from multiprocessing import Process

a = ['one', 'two', 'three', 'four', 'five']
b = [10, 20, 30, 40, 50]
d = dict(zip(a, b))

def pub001():
    port = "5100"
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    while True:
        for i, x in d.items():
            topic = x
            number = random.randrange(1, 215)
            print(topic, number)
            socket.send_string("%d %d" % (topic, number))
            print("Data published to topic:", topic)
            time.sleep(10)

if __name__ == "__main__":
    a = Process(target=pub001, args=())
    a.start()
