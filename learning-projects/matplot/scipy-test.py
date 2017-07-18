import scipy.misc
import os

file_name = 'test-img-matrix.jpg'
path_file = os.getcwd() + '/' + file_name

image_array = [[0 for x in range(50)] for y in range(50)]

scipy.misc.toimage(image_array, cmin=0.0, cmax=0.1).save(path_file)