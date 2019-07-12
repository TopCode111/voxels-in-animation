import sys
import fileinput
import os

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from  math import radians, cos, sin



def LineMatrix(path):
    global ma, linematrix
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



def RotateMatrix(matrix, deg_angle, axis):
        d = len(matrix)
        h = len(matrix[0])
        w = len(matrix[0][0])
        min_new_x = 0
        max_new_x = 0
        min_new_y = 0
        max_new_y = 0
        min_new_z = 0
        max_new_z = 0
        new_coords = []
        angle = radians(deg_angle)

        for z in range(d):
            for y in range(h):
                for x in range(w):

                    new_x = None
                    new_y = None
                    new_z = None

                    if axis == "x":
                        new_x = int(round(x))
                        new_y = int(round(y*cos(angle) - z*sin(angle)))
                        new_z = int(round(y*sin(angle) + z*cos(angle)))
                    elif axis == "y":
                        new_x = int(round(z*sin(angle) + x*cos(angle)))
                        new_y = int(round(y))
                        new_z = int(round(z*cos(angle) - x*sin(angle)))
                    elif axis == "z":
                        new_x = int(round(x*cos(angle) - y*sin(angle)))
                        new_y = int(round(x*sin(angle) + y*cos(angle)))
                        new_z = int(round(z))

                    val = matrix.item((z, y, x))
                    new_coords.append((val, new_x, new_y, new_z))
                    if new_x < min_new_x: min_new_x = new_x
                    if new_x > max_new_x: max_new_x = new_x
                    if new_y < min_new_y: min_new_y = new_y
                    if new_y > max_new_y: max_new_y = new_y
                    if new_z < min_new_z: min_new_z = new_z
                    if new_z > max_new_z: max_new_z = new_z

        new_x_offset = abs(min_new_x)
        new_y_offset = abs(min_new_y)
        new_z_offset = abs(min_new_z)

        new_width = abs(min_new_x - max_new_x)
        new_height = abs(min_new_y - max_new_y)
        new_depth = abs(min_new_z - max_new_z)

        rotated = np.empty((new_depth + 1, new_height + 1, new_width + 1))
        rotated.fill(0)
        for coord in new_coords:
            val = coord[0]
            x = coord[1]
            y = coord[2]
            z = coord[3]

            if rotated[new_z_offset + z][new_y_offset + y][new_x_offset + x] == 0:
                rotated[new_z_offset + z][new_y_offset + y][new_x_offset + x] = val

        return rotated


def Rotate2Video(xa,xs,ya,ys,za,zs) :
    

    writer = animation.writers['ffmpeg'](fps=20)
    frameNum = 0
    
    with writer.saving(fig, "voxelRotate.mp4", 200):

            # x-rotation
            for angle in range(0,xa+xs,xs):
                print('x-axis : {} degrees'.format(angle))
                ax.clear() 
                ra = RotateMatrix(ma, angle, 'x')
                ax.voxels(ra,  edgecolor="k")
                
                # Write video frame
                writer.grab_frame()
                
                # Write data set to text
                frameNum +=1
                with open ( 'frames/frame_{}.txt'.format(frameNum), 'w') as f:
                    for i in ra.ravel() :
                        print(i,file=f)
                
            
            # y-rotation:
            for angle in range(0,ya+ys,ys):
                print('y-axis : {} degrees'.format(angle))
                ax.clear()
                ra = RotateMatrix(ma, angle, 'y')
                ax.voxels(ra,  edgecolor="k")
                
                # Write video frame
                writer.grab_frame()
                
                # Write data set to text
                frameNum +=1
                with open ( 'frames/frame_{}.txt'.format(frameNum), 'w') as f:
                    for i in ra.ravel() :
                        print(i,file=f)
            
            
            # z-rotation:
            for angle in range(0,za+zs,zs):
                print('z-axis : {} degrees'.format(angle))
                ax.clear() 
                ra = RotateMatrix(ma, angle, 'z')
                ax.voxels(ra,  edgecolor="k")
                
                # Write video frame:
                writer.grab_frame()

                # Write data set to text:
                frameNum +=1
                with open ( 'frames/frame_{}.txt'.format(frameNum), 'w') as f:
                    for i in ra.ravel() :
                        print(i,file=f)
    

    

path="points"
ma = []
n = 0

N1 = 40
N2 = 40
N3 = 40
ma = np.zeros([N1, N2, N3])
rlt_arr = []
file_num =1
for i in range (file_num):
    arr = []
    real_path = path + str(i+1)+".txt"
    arr = LineMatrix(real_path)
    rlt_arr.append(arr)

with open ( 'result.txt', 'w') as f:
    for i in range ( 64000):
        for j in range (file_num):
            f.write("%f " % rlt_arr[j][i])
        f.write('\n')
f.close()

colors = np.empty(ma.shape, dtype=object)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(ma,  edgecolor="k")



plt.show()



xAngle = 90
xStep = 10

yAngle = 90
yStep = 10

zAngle = 90
zStep = 10

plt.rcParams['animation.ffmpeg_path'] =r'ffmpeg\bin\ffmpeg.exe'

Rotate2Video(xAngle,xStep,yAngle,yStep,zAngle,zStep)


