import numpy as np
import zmq
import plotly.express as px
import pickle
import zlib
import time

# Consumer has to bind because DRAO cannot
def consumer():
    # output = []

    # context = zmq.Context()
    # zmq_socket_SUB = context.socket(zmq.SUB)
    # zmq_socket_SUB.setsockopt(zmq.SUBSCRIBE, b"")
    # zmq_socket_SUB.connect("tcp://127.0.0.1:5558")


    i=1
    while True:
        print(f"Checking for new data: {i}")
        ts = recv_zmq()
        print(ts)
        # with create_zmq_socket() as zmq_socket_SUB:
        #     # try:

        #     # context = zmq.Context()
        #     # zmq_socket_SUB = context.socket(zmq.SUB)
        #     # zmq_socket_SUB.setsockopt(zmq.SUBSCRIBE, b"")
        #     # zmq_socket_SUB.connect("tcp://127.0.0.1:5558")

        #     # zmq_socket_SUB = connect_zmq_socket()
        #     try:
        #         msg = zmq_socket_SUB.recv(zmq.NOBLOCK)
        #         p = zlib.decompress(msg)
        #         data = pickle.loads(p)
        #         spec = data[:-1]
        #         timestamp = data[-1]
        #         # zmq_socket_SUB.disconnect()
        #         print(f"-- Received something")

        #     except zmq.error.Again:
        #         print("-- Nothing to receive")

        time.sleep(0.5)
        i+=1
    

def create_zmq_socket():
    context = zmq.Context()
    zmq_socket_SUB = context.socket(zmq.SUB)
    zmq_socket_SUB.setsockopt(zmq.SUBSCRIBE, b"")
    zmq_socket_SUB.connect("tcp://127.0.0.1:5558") 

    return zmq_socket_SUB

def recv_zmq():
    with create_zmq_socket() as zmq_socket_SUB:
        try:
            msg = zmq_socket_SUB.recv(zmq.NOBLOCK)
            p = zlib.decompress(msg)
            data = pickle.loads(p)
            timestamp = data[-1]
            # print(timestamp)
            return timestamp
        except zmq.error.Again:
            

consumer()



