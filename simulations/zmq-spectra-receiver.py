import numpy as np
import zmq
import plotly.express as px
import pickle
import zlib

# Consumer has to bind because DRAO cannot
def consumer():
    output = []

    context = zmq.Context()
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.bind("tcp://127.0.0.1:5557")

    should_continue = True
    while should_continue:
        print("loopin")
        msg = consumer_receiver.recv()
        if msg == b"Done":
            should_continue=False
        else:
            p = zlib.decompress(msg)
            spec = pickle.loads(p)
            output.append(spec)
    
    output = np.array(output)
    # np.save('output.npy', output)
    # fig=px.imshow(output, height=1000, width=1000)
    fig = px.heatmap(output)
    fig.show()

consumer()



