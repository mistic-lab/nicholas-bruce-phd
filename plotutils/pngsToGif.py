"""
Save .GIF made from folder of .PNG images. Saves as movie.gif
in current directory.

Arguements
----------
filespath : string
    Path to the folder which contains the .PNGs
"""

# import matplotlib.pyplot as plt
# import imageio
# import sys
# import os

# filespath = sys.argv[1]

# images = []
# for f in os.listdir(filespath):
#     if f.endswith('.png'):
#         images.append(imageio.imread(f))

# imageio.mimsave('./movie.gif', images, duration=0.5)

import imageio
images = []
for i in range(297):
    images.append(imageio.imread("./figures/{}.png".format(i)))
imageio.mimsave("./5_04MHz-5min-navg100.gif", images, duration=0.2)
