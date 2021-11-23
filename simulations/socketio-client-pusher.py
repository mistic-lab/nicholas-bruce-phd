import socketio
import numpy as np
import h5py
import datetime
import time

sio = socketio.Client()

sio.connect('http://localhost:4001')

test_arr = np.array([721247464550.0, 387079.0, 5000000.0, 68298723497.0], dtype='<f8')
test_arr = 10.*np.log10(test_arr).astype('float32')

with h5py.File('/Users/nsbruce/Documents/RFI/rfind-monitor/data.h5','r') as h5f:
    modlen = len(h5f['times'])
    i=0
    while True:
        print(f"Trying to send iteration {i}")
        spec = 10.*np.log10(h5f['spec'][i % modlen]).astype('float32')
        ts = str(datetime.datetime.now().timestamp())
        # topic = bytes(ts, 'utf-8')
        try:
            sio.emit('spec', spec.tobytes())
            print("-- Succeeded")
        except :
            print("-- Failed")
        i+=1
        time.sleep(1)
