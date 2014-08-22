__author__ = 'Matt Griffiths, James Archer, Matt Sanderson'
from visual import *
from random import gauss
from math import *


class Square():
    def __init__(self, corners, order=0, chaos=0):
        """
        Data structure for squares in the Diamond Square Algorithm

        :param a: Top left corner height
        :param b: Top right corner height
        :param c: Bottom left corner height
        :param d: Bottom right corner height
        :param order: Order of recursion depth
        :param chaos: Amount of chaos to induce
        """
        #Square data
        self.order = order
        self.chaos = chaos
        self.heights = list(map(float, corners))
        self.sub_squares = []

        #Stochastic variables
        self.random = gauss(0, 5)
        self.random_scalar = self.chaos / (1 + self.order ** 2)

        #Recursion handler
        if self.order < iterations:
            self.sub_square_generation()
        else:
            final_squares.append(self.heights)

    def sub_square_generation(self):

        # Top left square generation
        self.sub_squares.append(Square(
            [self.heights[0],
            0.5 * (self.heights[0] + self.heights[1]),
            0.5 * (self.heights[0] + self.heights[2]),
            0.25 * sum(self.heights) + (self.random_scalar * self.random)],
            self.order + 1,
            self.chaos
        ))

        # Top right square generation
        self.sub_squares.append(Square(
            [0.5 * (self.heights[0] + self.heights[1]),
            self.heights[1],
            0.25 * sum(self.heights) + (self.random_scalar * self.random),
            0.5 * (self.heights[1] + self.heights[3])],
            self.order + 1,
            self.chaos
        ))

        # Bottom left square generation
        self.sub_squares.append(Square(
            [0.5 * (self.heights[0] + self.heights[2]),
            0.25 * sum(self.heights) + (self.random_scalar * self.random),
            self.heights[2],
            0.5 * (self.heights[2] + self.heights[3])],
            self.order + 1,
            self.chaos
        ))

        # Bottom right square generation
        self.sub_squares.append(Square(
            [0.25 * sum(self.heights) + (self.random_scalar * self.random),
            0.5 * (self.heights[1] + self.heights[3]),
            0.5 * (self.heights[2] + self.heights[3]),
            self.heights[3]],
            self.order + 1,
            self.chaos
        ))


class Generator():
    def __init__(self, c):

        """
        Generate fractal landscape using DSA

        :param c: Chaos factor of fractal
        """
        #Repository for final height map
        self.map_array = []
        #Generate Terrain
        self.terrain = Square([0,0,0,0], chaos=c)
        #Collect final data from external variable
        self.final_squares = final_squares
        for i in range(iterations):
            self.combine_list()
        self.construct_map()

    def combine_squares(self, a, b, c, d):
        temp = []
        for row in range(0, int(sqrt(len(a)))):
            for column in range(0, int(sqrt(len(a)))):
                temp.append(a[row * int(sqrt(len(a))) + column])
            column = 0
            while column < sqrt(len(b)):
                if column != 0:
                    temp.append(b[row * int(sqrt(len(b))) + column])
                column += 1
        for row in range(0, int(sqrt(len(c)))):
            column = 0
            while column < sqrt(len(c)):
                if row != 0:
                    temp.append(c[row * int(sqrt(len(c))) + column])
                column += 1

            column = 0
            while column < sqrt(len(d)):
                if column != 0 and row != 0:
                    temp.append(d[row * int(sqrt(len(d))) + column])
                column += 1

        return temp

    def combine_list(self):
        temp = []
        i = 0
        while i < len(self.final_squares) / 4:
            temp.append(self.combine_squares(self.final_squares[i * 4],
                                             self.final_squares[i * 4 + 1],
                                             self.final_squares[i * 4 + 2],
                                             self.final_squares[i * 4 + 3]))
            i += 1
        self.final_squares = temp

    def construct_map(self):
        for i in range(int(sqrt(len(self.final_squares[0])))):
            self.map_array.append([])
        for i in range(len(self.final_squares[0])):
            self.map_array[int(i / len(self.map_array))].append(self.final_squares[0][i])

    def __str__(self):
        temp_str = ''
        for i in self.map_array:
            temp_str = temp_str + str(i) + '\n'
        return temp_str

    def dump(self):
        return self.map_array


class Waves():
    def __init__(self, initdata, c=1):
        self.dt = 0.1
        self.dx = 1
        self.initdata = initdata
        self.xdim = len(self.initdata)
        self.ydim = len(self.initdata[0])
        self.points = []
        self.gen_grid()

    def gen_grid(self):
        for i in range(self.xdim):
            temp = []
            for j in range(self.ydim):
                temp.append(sphere(pos=(i-self.xdim/2, j-self.ydim/2, self.initdata[i][j]), vel=0, radius = 0.1))
            self.points.append(temp)

    def acc_update(self):
        for i in range(1, self.xdim-1):
            for j in range(1, self.ydim-1):
                accx = (self.points[i][j+1].pos.z - 2*self.points[i][j].pos.z +self.points[i][j-1].pos.z)/self.dx**2
                accy = (self.points[i+1][j].pos.z - 2*self.points[i][j].pos.z +self.points[i-1][j].pos.z)/self.dx**2
                self.points[i][j].vel += (accx + accy)*self.dt

    def pos_update(self):
        for i in self.points:
            for j in i:
                j.pos.z += j.vel*self.dt

    def step(self):
        self.acc_update()
        self.pos_update()


if __name__ == '__main__':
    iterations = 5
    final_squares = []
    gen = Generator(1.3)
    sim = Waves(gen.dump())
    while True:
        rate(100)
        sim.step()
