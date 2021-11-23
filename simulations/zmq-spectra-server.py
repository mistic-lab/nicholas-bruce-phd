import zmq
import numpy as np
import h5py
import time
import zlib
import pickle

import datetime
from dateutil import tz


# def producer():
#     context = zmq.Context()
#     zmq_socket = context.socket(zmq.PUB)
#     # zmq_socket.connect("tcp://206.12.93.193:5557")
#     zmq_socket.connect("tcp://127.0.0.1:5557")

#     with h5py.File('/Users/nsbruce/Documents/RFI/rfind-monitor/data.h5','r') as h5f:
#         modlen = len(h5f['times'])

#         i=0
#         while True:
#             print(f"Trying to send iteration {i}")
#             spec = np.array(h5f['spec'][i % modlen]).tolist()
#             timestamp = h5f['times'][i % modlen]
#             spec.append(timestamp)
#             p = pickle.dumps(spec,protocol=-1)
#             msg = zlib.compress(p)
#             try:
#                 zmq_socket.send(msg, zmq.NOBLOCK)
#                 print("-- Succeeded")
#             except zmq.error.Again:
#                 print("-- Failed")
#             i+=1
#             time.sleep(1)
#* This is what the h5 rfind data is stored as, float64. They are all integers but very large (~1e13 was the largest I saw).
#* Because math is easier in python and everyone will want to see it in dB we can do that now and then truncate down to
#* a float16. The first two values here are the largest and smallest in some integration from the h5.

test_arr = np.array([721247464550.0, 387079.0, 5000000.0, 68298723497.0], dtype='<f8')
test_arr = 10.*np.log10(test_arr).astype('float32')




def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUB)
    zmq_socket.connect('tcp://127.0.0.1:5557')
    # while True:
    #     try:
    #         print(test_arr.tobytes())
    #         print(test_arr)
    #         zmq_socket.send_multipart([b"testTopic", test_arr.tobytes()])
    #         print("-- Succeeded")
    #     except zmq.error.Again:
    #         print("-- Failed")
    #     time.sleep(1)
    with h5py.File('/Users/nsbruce/Documents/RFI/rfind-monitor/data.h5','r') as h5f:
        modlen = len(h5f['times'])
        i=0
        while True:
            print(f"Trying to send iteration {i}")
            spec = 10.*np.log10(h5f['spec'][i % modlen]).astype('float32')
            ts = str(datetime.datetime.now().timestamp())
            topic = bytes(ts, 'utf-8')
            try:
                zmq_socket.send_multipart([topic, spec.tobytes()], zmq.NOBLOCK)
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

