import numpy as np
import matplotlib.pyplot as plt
import os

file_name = 'test-img-matrix.png'
path_file = os.getcwd() + '/' + file_name

a = np.arange(10000).reshape(100, 100)


print(a)
plt.imshow(a) #Needs to be in row,col order
plt.show()
plt.savefig(path_file)
