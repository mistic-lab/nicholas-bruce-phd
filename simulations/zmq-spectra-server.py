import zmq
import numpy as np
import h5py
import time
import zlib
import pickle

import datetime
from dateutil import tz


def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.connect("tcp://206.12.93.193:5557")
    # zmq_socket.connect("tcp://127.0.0.1:5557")

    with h5py.File('/Users/nsbruce/Documents/RFI/web-spectra-explorer/data.h5','r') as h5f:
        modlen = len(h5f['times'])

        i=0
        while True:
            print(f"Trying to send iteration {i}")
            spec = np.array(h5f['spec'][i % modlen]).tolist()
            timestamp = h5f['times'][i % modlen]
            spec.append(timestamp)
            p = pickle.dumps(spec,protocol=-1)
            msg = zlib.compress(p)
            try:
                zmq_socket.send(msg, zmq.NOBLOCK)
                print("-- Succeeded")
            except zmq.error.Again:
                print("-- Failed")
            i+=1
            time.sleep(1)

# # Works with 4edc6464789d3c4d78d904c8b85ae57b7dc4232d
# def producer():
#     context = zmq.Context()
#     zmq_socket = context.socket(zmq.PUSH)
#     zmq_socket.connect("tcp://206.12.93.193:5557")

#     with h5py.File('/Users/nsbruce/Documents/RFI/web-spectra-explorer/data.h5','r') as h5f:
#         modlen = len(h5f['times'])

#         i=0
#         while True:
#             print(f"Trying to send iteration {i}")
#             spec = np.array(h5f['spec'][i % modlen])
#             p = pickle.dumps(spec,protocol=-1)
#             msg = zlib.compress(p)
#             try:
#                 zmq_socket.send(msg, zmq.NOBLOCK)
#                 print("-- Succeeded")
#             except zmq.error.Again:
#                 print("-- Failed")
#             i+=1
#             time.sleep(0.4)

producer()

