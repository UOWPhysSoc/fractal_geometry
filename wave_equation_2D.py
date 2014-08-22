from visual import *
from math import *

height = []
vel = []

fixed_ends = False

#Number of position subdivisions
N = 20
#Speed of wave
c = 0.5
#Position, time subdivisions (position divisions are redundant at this stage)
dx = 1
dt = 0.05

if fixed_ends == True:
    A = 1
    B = N-1
else:
    A = 0
    B = N

#Generate initial distribution
for n in range(0,N):
    height.append([])
    for m in range(0,N):
        height[n].append(3*exp(-0.1*((n - N/2)**2 + (m - N/2)**2)))
        vel.append(0)
        
#Fix edges to zero
if fixed_ends == True:
    for n in range(0,N):
        height[0][n] = 0
        height[n][0] = 0
        height[N-1][n] = 0
        height[n][N-1] = 0


#List of point objects
p = []

#Give initial conditions
for i in range(0,N):
    p.append([])
    for j in range(0,N):
        x = vector(i-N/2, j - N/2, height[i][j])
        p[i].append(points(pos = x, vel = vel[i]))


#Loop the wavyness

sleep(2)
while True:
    rate(100)
    #Update acceleration and velocity all at once
   
    for n in range(A,B):  # iterate over x
        for m in range(A,B): # iterate over y
            acc_x = (p[n][(m+1)%N].pos[0][2] - 2*p[n][m].pos[0][2] + p[n][(m-1)%N].pos[0][2])/dx**2
            acc_y = (p[(n+1)%N][m].pos[0][2] - 2*p[n][m].pos[0][2] + p[(n-1)%N][m].pos[0][2])/dx**2             
            p[n][m].vel += c**2 * (acc_x + acc_y)*dt

    #Update positions
    for n in range(A,B):
        for m in range(A,B):
            p[n][m].pos[0][2] += p[n][m].vel*dt
