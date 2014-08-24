"""

Takes a uniform distribution on cos(theta) and phi,
and propogates waves through the surface.

!!! DOES NOT HAVE POLES SO THINGS GET WEIRD THERE !!!
(I think each pole is coupled to the other)

"""


from visual import *
#from math import *

class Point():
    def __init__(self, N, i, j):

        #Grid of cos(theta) and phi

        self.u = 2*float(i)/N - 1
        self.v = float(j)/N*(2*pi)
        self.R = 1

        self.vel = 0
        self.acc = 0

        self.rec_to_sph()
        self.vis()

        #Integration infinitesimals

        self.dt = 0.01
        self.du = 2.0/N
        self.dv = 2*pi/N

    #Maps the grid to a sphere in (x,y,z)

    def rec_to_sph(self):
        self.x = self.R * sqrt(1 - self.u**2) * cos(self.v)
        self.y = self.R * sqrt(1 - self.u**2) * sin(self.v)
        self.z = self.R * self.u

    def vis(self):
        self.p = points(pos = (self.x, self.y, self.z))

    def update(self):
        self.p.pos = (self.x, self.y, self.z)
        self.rec_to_sph()

    #Use acc to update the position of the points

    def integrate(self):
        self.euler_v()
        self.euler_r()
        self.update()
    
    def euler_v(self):
        self.vel += self.acc*self.dt

    def euler_r(self):
        self.R += self.vel*self.dt



# Laplacian part for cos(theta)
def laplace_u(p, a, b, c):
    #a is f(n+1), b is f(n), c is f(n-1)
    #p is the Point class in question
    d1 = -2 * p.u * (a - b)/(2 * p.du)
    d2 = (1 - p.u**2) * (a - 2 * b + c)/(p.du**2)
    return d1 + d2

#Laplacian for phi
def laplace_v(p, a, b, c):
    return 1/(1 - p.u**2) * (a - 2 * b + c)/(p.dv**2)


########### PROGRAM STARTS HERE ############

data = []

N = 10
c = 0.5

#Generate the points uniformly on cos(theta) and phi

for i in range(1,N):
    data.append([])
    for j in range (0,N):
        data[i-1].append(Point(N, i, j))

#Create pertubation to start wave

data[N/2][0].R += 0.1
data[N/2][0].update()

#Time to see the initial conditions
sleep(5)

#Go!
while True:
    rate(100)
    n = 0
    for i in data:
        m = 0
        for j in i:
            # This mess is because the Points class doesn't have neightbour data
            j.acc = c**2 * (laplace_u(j, data[(n+1)%(N-1)][m].R, j.R, data[(n-1)%(N-1)][m].R) +
                             laplace_v(j, data[n][(m+1)%(N-1)].R, j.R, data[n][(m-1)%(N-1)].R))
            m += 1
        n += 1

    for i in data:
        for j in i:
            j.integrate()
