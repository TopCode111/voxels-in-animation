import sys
import fileinput
import os
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

path="points"

ma = []

n = 0

def LineMatrix(path):
    global ma
    linematrix = []
    for lines in fileinput.input(path):
        lines = lines.rstrip().split()
        for line in lines:
            linematrix.append( line)

    n = int( str(linematrix[0]))
    linematrix.remove ( linematrix[0])
    rlt = []
    tmp = []
    for i in range ( n):
        I = float(linematrix[i*4+3])
        tmp.append ( I)
    minv, maxv = min ( tmp), max ( tmp)
    for ele in tmp:
        elev = (ele - minv)/(maxv-minv)
        rlt.append ( elev)
    for i in range ( n):
        xy = int(i % 1600)
        yy = int(xy/40)
        xx = xy % 40
        zz = int(i/1600)
        ma[zz][yy][xx] += rlt[i]
    return rlt



N1 = 40
N2 = 40
N3 = 40
ma = np.zeros([N1, N2, N3])
rlt_arr = []
file_num =1


colors = np.empty(ma.shape, dtype=object)
#colors[ma[1]] = 'red'


fig = plt.figure()
ax = fig.gca(projection='3d')
#ax.set_aspect('equal')

ax.voxels(ma,  edgecolor="k")

print(ma)
plt.show()
