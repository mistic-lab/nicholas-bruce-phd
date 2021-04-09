import zmq
import numpy as np
import h5py
import time
import zlib
import pickle

# Producer has to connect not bind because DRAO

def producer():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.connect("tcp://127.0.0.1:5557")

    with h5py.File('/Users/nsbruce/Documents/RFI/web-spectra-explorer/data.h5','r') as h5f:
        modlen = len(h5f['times'])

        
        i=0
        while True:
            print(f"Trying to send iteration {i}")
            spec = np.array(h5f['spec'][i % modlen])
            p = pickle.dumps(spec,protocol=-1)
            msg = zlib.compress(p)
            try:
                zmq_socket.send(msg, zmq.NOBLOCK)
                print("-- Succeeded")
            except zmq.error.Again:
                print("-- Failed")
            i+=1
            time.sleep(1)

producer()

