"""Simple matshow() example."""
"""""
import matplotlib.pyplot as plt
import numpy as np


def samplemat(dims):
    
    aa = np.zeros(dims)
    for i in range(min(dims)):
        aa[i, i] = i
    return aa


# Display matrix
plt.matshow(samplemat((15, 35)))

plt.show()
"""""

import matplotlib.pyplot as plt
import os
file_name = 'test-img-matrix.png'
path_file = os.getcwd() + '/' + file_name

image_array = [[0 for x in range(50)] for y in range(50)]
for i in range(50):
    for j in range(50):
        image_array[i][j] = i+j


plt.imshow(image_array) #Needs to be in row,col order
plt.savefig(path_file)

