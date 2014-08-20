from visual import *
from math import *

position = []
vel = []

#Number of position subdivisions
N = 20
#Speed of wave
c = 1
#Position, time subdivisions (position divisions are redundant at this stage)
dx = 1
dt = 0.1


#Generate initial distribution
for n in range(0,N):
    position.append([])
    for m in range(0,N):
        position[n].append(5*exp(-0.05*((n - N/2)**2 + (m - N/2)**2)))
        vel.append(0)
for n in range(0,N):
    position[0][n] = 0
    position[n][0] = 0
    position[N-1][n] = 0
    position[n][N-1] = 0


#List of point objects
p = []

#Give initial conditions
for i in range(0,N):
    p.append([])
    for j in range(0,N):
        x = vector(i-N/2, j - N/2, position[i][j]) #vpython is being a bitch and fucking up the pos object somehow
        p[i].append(points(pos = x, vel = vel[i]))


#Loop the wavyness
while True:
    rate(100)
    #Update acceleration and velocity all at once
    for n in range(1,N-1):  # iterate over x
        for m in range(1,N-1): # iterate over y
            acc_x = (p[n][m+1].pos[0][2] - 2*p[n][m].pos[0][2] + p[n][m-1].pos[0][2])/dx**2
            acc_y = (p[n+1][m].pos[0][2] - 2*p[n][m].pos[0][2] + p[n-1][m].pos[0][2])/dx**2             
            p[n][m].vel += (acc_x + acc_y)*dt

    #Update positions
    for n in range(1,N-1):
        for m in range(1,N-1):
            p[n][m].pos[0][2] += p[n][m].vel*dt
