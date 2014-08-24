from visual import *
import numpy as np
import random
<<<<<<< HEAD
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

class Mesh():
    def __init__(self, corners, iter_max = 2, chaos=1, h_init = [[0,0],[0,0]]):
=======

class Mesh():
    def __init__(self, corners, iter_max = 2, h_init = [[0,0],[0,0]]):
>>>>>>> origin/master
        """
        format of corners:
        [[upper left, upper right],
         [lower left, lower right]]
        """
        self.corners = corners
        self.heights = h_init
        self.mesh = [[],[]]     # first create an empty array that will be filled with points
        self.locs = [(0,0), (0,1), (1,0), (1,1)]    # a list to be iterated through to get corners in correct order
        for loc in self.locs:
            # a point object the correct coordinates at the correct location in self.mesh (looks messy I know...)
            self.mesh[loc[0]].append(Point((corners[loc[0]][loc[1]][0], corners[loc[0]][loc[1]][1], h_init[loc[0]][loc[1]])))
        self.dims = len(self)
        self.iter_level = 0         # intial level of iteration (increases to self.iter_max)
        self.iter_max = iter_max
<<<<<<< HEAD
        self.chaos = chaos
        random.seed()
=======
>>>>>>> origin/master

    def create_midpoints(self, pts):
        # pts are the points we are finding the midpoint of
        # this method assumes the region is at least rectangular for simplicity
        
        # first generate center point
        p_C = Point((0.5*(pts[0].x + pts[1].x), 0.5*(pts[0].y + pts[2].y), None))

        # now generate edge points
        p_N = Point((0.5*(pts[0].x + pts[1].x), pts[0].y, None))
        p_W = Point((pts[0].x, 0.5*(pts[0].y + pts[2].y), None))
        p_E = Point((pts[1].x, 0.5*(pts[1].y + pts[3].y), None))
        p_S = Point((0.5*(pts[2].x + pts[3].x), pts[2].y, None))
        return {'N':p_N, 'W':p_W, 'E':p_E, 'S':p_S, 'C':p_C}

    def expand_mesh(self):
        # this will take the current mesh and expand it to a mesh with appropriate size for the next iteration
        for row in self.mesh:
            # we want to insert self.dims - 1 extra points in each row, then add self.dims - 1 rows inbetween each of these rows
            # also, we will want to insert the rows and points from the back so that the indexing is easier
            for i in range(self.dims - 1, 0, -1):
                row.insert(i, None)    # just put a None in for now as a place holder then add in the particles later
        for i in range(self.dims - 1, 0, -1):
            self.mesh.insert(i, [None]*(2*self.dims - 1))
        self.dims = len(self)

    def give_neighbors(self):
        # this will iterate through self.mesh to give all the new points the correct neighbors
        for x in range(2, self.dims, 2):
            for y in range(2, self.dims, 2):
                # central pt
                curr_pt = self.mesh[y-1][x-1]
                curr_pt.neighbors['NW'] = self.mesh[y-2][x-2]
                curr_pt.neighbors['NE'] = self.mesh[y-2][x]
                curr_pt.neighbors['SW'] = self.mesh[y][x-2]
                curr_pt.neighbors['SE'] = self.mesh[y][x]
<<<<<<< HEAD
                curr_pt.set_height(self.iter_level, self.chaos)
=======
                curr_pt.set_height(self.iter_level)
>>>>>>> origin/master
                # outer points:
                for coord in [(-1,-2), (-2,-1), (0,-1), (-1, 0)]:
                    curr_pt = self.mesh[y+coord[1]][x+coord[0]]
                    try:
                        curr_pt.neighbors['N'] = self.mesh[y+coord[1]-1][x+coord[0]]
                    except:
                        pass
                    try:
                        curr_pt.neighbors['W'] = self.mesh[y+coord[1]][x+coord[0]-1]
                    except:
                        pass
                    try:
                        curr_pt.neighbors['E'] = self.mesh[y+coord[1]][x+coord[0]+1]
                    except:
                        pass
                    try:
                        curr_pt.neighbors['S'] = self.mesh[y+coord[1]+1][x+coord[0]]
                    except:
                        pass
<<<<<<< HEAD
                    curr_pt.set_height(self.iter_level, self.chaos)
=======
                    curr_pt.set_height(self.iter_level)
>>>>>>> origin/master
                        

    def fill_points(self):
        for x in range(2, self.dims, 2):
            for y in range(2, self.dims, 2):
                corners = [self.mesh[y-2][x-2], self.mesh[y-2][x], self.mesh[y][x-2], self.mesh[y][x]]
                new_points = self.create_midpoints(corners)
                self.mesh[y-2][x-1] = new_points['N']
                self.mesh[y-1][x-2] = new_points['W']
                self.mesh[y-1][x-1] = new_points['C']
                self.mesh[y-1][x] = new_points['E']
                self.mesh[y][x-1] = new_points['S']

    def iterate(self):
        # this is the method that is actually called externally
        while self.iter_level < self.iter_max:
            # first, expand mesh:
            self.expand_mesh()

            # now fill the gaps with new points
            self.fill_points()

            # give the new points their neighbors (this also gives the heights as it is more convenient to do within this function
            self.give_neighbors()

            self.iter_level += 1

    def create_spheres(self):
<<<<<<< HEAD
        # creates the sphere generated in vpython (note: calling this will cause vpython to run!)
=======
>>>>>>> origin/master
        for x in range(self.dims):
            for y in range(self.dims):
                self.mesh[y][x].gen_sphere()

<<<<<<< HEAD
    def get_heights(self):
        # returns an array with just height values
        h_map = []
        i = 0
        for row in self.mesh:
            h_map.append([])
            for point in row:
                h_map[i].append(point.z)
            i += 1
        return h_map

    def plot(self, mode):
        fig = plt.figure()
        
        if mode == 'flat':
            im = plt.imshow(self.get_heights(), extent = (self.corners[0][0][0], self.corners[0][1][0], self.corners[0][0][1], self.corners[1][0][1]),
                            origin='lower', cmap=plt.cm.RdBu)
            plt.colorbar(im)
        elif mode == '3D':
            x_range = np.linspace(self.corners[0][0][0], self.corners[0][1][0], self.dims)
            y_range = np.linspace(self.corners[0][0][1], self.corners[1][0][1], self.dims)
            X, Y = np.meshgrid(x_range, y_range)
            ax = fig.add_subplot(111, projection='3d')
            surf = ax.plot_surface(X, Y, self.get_heights(), cmap=plt.cm.RdBu, antialiased=False, linewidth=0, rstride=1, cstride=1)    # change/remove rstride & cstride for i_max > about 5
            fig.colorbar(surf, shrink=0.5, aspect=5)
        fig.show()
        
=======
>>>>>>> origin/master
    def __call__(self):
        return self.mesh

    def __str__(self):
        rep = '[\n'
        for row in self.mesh:
            for pt in row:
                rep += str(pt) + ', '
            rep += '\n'
        rep += ']'
        return rep

    def __len__(self):
        return(len(self.mesh[0]))

class Point():
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]

        self.neighbors = {'NW':None, 'N':None, 'NE':None,
                          'W':None, 'E':None,
                          'SW':None, 'S':None, 'SE':None}

<<<<<<< HEAD
    def set_height(self, i, h):
        # i is the number of the iteration, h is a modifier to set how much variation there is in the random numbers
        rand = random.uniform(-h*2**(-i), h*2**(-i))
=======
    def set_height(self, i):
        # i is the number of the iteration
        rand = random.uniform(-2**(-i), 2**(-i))
>>>>>>> origin/master
        val = 0
        count = 0
        for direc in self.neighbors:
            if self.neighbors[direc] != None:
                if self.neighbors[direc].z != None:
                    val += self.neighbors[direc].z
                    count += 1
        try:
            self.z = val/count + rand
        except ZeroDivisionError:
            pass

    def gen_sphere(self):
        # this will create a sphere object at the location of the point
        self.sphere = sphere(pos=(self.x, self.y, self.z), vel=0, radius=0.01)

    def __str__(self):
        return "Point at: ({0}, {1}, {2})".format(self.x, self.y, self.z)

    def __call__(self):
        return (self.x, self.y, self.z)

<<<<<<< HEAD
i_max = 5
plotter = 'mpl'
c = [[(-1,1), (1,1)], [(-1,-1), (1,-1)]]
a = Mesh(c, iter_max=i_max, chaos=0.8)
a.iterate()
if plotter == 'mpl':
    a.plot('3D')
elif plotter == 'vpython':
    a.create_spheres()
=======

c = [[(0,1), (1,1)], [(0,0), (1,0)]]
a = Mesh(c, iter_max=4)
a.iterate()
a.create_spheres()
>>>>>>> origin/master
