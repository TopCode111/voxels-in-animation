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
        d,h,w = matrix.shape
        
        min_new_x = 0
        max_new_x = 0
        min_new_y = 0
        max_new_y = 0
        min_new_z = 0
        max_new_z = 0
        new_coords = []
        
        angle = radians(deg_angle)
        sinth = sin(angle)
        costh = cos(angle)

        for z in range(d):
            for y in range(h):
                for x in range(w):

                    if axis == "x":
                        new_x = x
                        new_y = int(round(y*costh - z*sinth))
                        new_z = int(round(y*sinth + z*costh))
                    elif axis == "y":
                        new_x = int(round(z*sinth + x*costh))
                        new_y = y
                        new_z = int(round(z*costh - x*sinth))
                    else : # axis == "z":
                        new_x = int(round(x*costh - y*sinth))
                        new_y = int(round(x*sinth + y*costh))
                        new_z = z
                    
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

        new_width = max_new_x - min_new_x
        new_height = max_new_y - min_new_y
        new_depth = max_new_z - min_new_z

        rotated = np.empty((new_depth + 1, new_height + 1, new_width + 1))
        rotated.fill(0)
        
        global frameNum
        frameNum +=1
        with open ( 'frames/frame_{}.txt'.format(frameNum), 'w') as f:

            for coord in new_coords:
                    val = coord[0]
                    x = coord[1]
                    y = coord[2]
                    z = coord[3]

                    new_z = new_z_offset + z
                    new_y = new_y_offset + y
                    new_x = new_x_offset + x

                    rotated[new_z][new_y][new_x] = val

                    print(val,new_x,new_y,new_z,file=f)


        return rotated
x_angle = []
y_angle = []
z_angle = []
def Rotate2Video(xa,xs,ya,ys,za,zs) :
    
    #writer = animation.writers['ffmpeg'](fps=20)
    #with writer.saving(fig, "voxelRotate.mp4", 100):

            # x-rotation
            for angle in range(0,xa+xs,xs):
                #x_angle = [angle]
                x_angle.append(angle)
                #print('x-axis : {} degrees'.format(angle))

                ax.clear()
                ra = RotateMatrix(ma, angle, 'x')
                ax.voxels(ra,  edgecolor="k")
                
                # Write video frame
               # writer.grab_frame()

            print(x_angle)
            print(ra)
            
            # y-rotation
            for angle in range(0, ya + ys, ys):
                y_angle.append(angle)

                #print('y-axis : {} degrees'.format(angle))
                ax.clear()
                ra = RotateMatrix(ma, angle, 'y')
                ax.voxels(ra,  edgecolor="k")
                
                # Write video frame
               # writer.grab_frame()
            print(y_angle)
            print(ra)
            # z-rotation
            for angle in range(0,za+zs,zs):
                z_angle.append(angle)

                #print('z-axis : {} degrees'.format(angle))
                ax.clear()
                ra = RotateMatrix(ma, angle, 'z')
                ax.voxels(ra,  edgecolor="k")
                
                # Write video frame
                #writer.grab_frame()
            

            print(z_angle)
            print(ra)


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

#plt.show()
xAngle = 90
xStep = 10

yAngle = 90
yStep = 10

zAngle = 90
zStep = 10

#plt.rcParams['animation.ffmpeg_path'] =r'ffmpeg\bin\ffmpeg.exe'
frameNum = 0

Rotate2Video(xAngle,xStep,yAngle,yStep,zAngle,zStep)


