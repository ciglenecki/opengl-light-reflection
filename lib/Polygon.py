from pyglet.window import key, mouse
from pyglet.gl import *
import pyglet
import numpy as np
from math import factorial, sqrt
from .Vertex import *
import numpy as np
from math import factorial, sqrt
from functools import reduce


class Polygon():
    def __init__(self, vertices=None):
        self.vertices = vertices  # [(2,3,4),(4,2,5)]
        self.intensity = None

    def normalize(self, M, center):
        for v in self.vertices:
            v.normalize(M=M, center=center)

        if (len(self.vertices) >= 3):

            self.center = self.get_center()

            v1, v2, v3 = self.vertices[0], self.vertices[1], self.vertices[2]
            vector1 = np.array(v2 - v1)
            vector2 = np.array(v3 - v2)

            norm = np.cross(vector1, vector2)
            norm = norm/np.linalg.norm(norm)
            
            self.norm = norm

        return self

    def offset(self, center):
        for v in self.vertices:
            v.offset(center=center)
        return self

    def get_avg_z(self):
        return sum(v.z for v in self.vertices) / len(self.vertices)

    def get_center(self):
        x = (sum(v.x for v in self.vertices)) / 3
        y = (sum(v.y for v in self.vertices)) / 3
        z = (sum(v.z for v in self.vertices)) / 3

        return Vertex(x, y, z)

    def __repr__(self):
        return str(self.vertices)

    def contains_vertex(self, vertex):
        """Returns true/false if point is contained inside of
        polygon
        """
        x, y, z = vertex
        a, b, c, d = self.get_abcd()
        return bool(a*x+b*y+c*z < 0)

    def get_vertices(self):
        v1, v2, v3 = self.vertices
        return v1, v2, v3

    def get_abcd(self):
        v1, v2, v3 = self.get_vertices()
        x1, y1, z1 = v1.get_xyz()
        x2, y2, z2 = v2.get_xyz()
        x3, y3, z3 = v3.get_xyz()
        a = (y2-y1)*(z3-z1)-(z2-z1)*(y3-y1)
        b = -(x2-x1)*(z3-z1)+(z2-z1)*(x3-x1)
        c = (x2-x1)*(y3-y1)-(y2-y1)*(x3-x1)
        d = -x1*a-y1*b-z1*c
        return a, b, c, d


class BeizerPolygon(Polygon):
    def __init__(self, polygon, t_start=0, t_end=1.01, t_step=0.01):

        self.vertices = []
        for t in np.arange(t_start, t_end, t_step).tolist():
            self.vertices.append(self.p(polygon, t))
        super()

    def p(self, polygon, t):

        result = 0

        i = 0
        n = len(polygon.vertices) - 1

        def calc_b(i, n, t):
            return factorial(n) / (factorial(i)*factorial(n-i)) * pow(t, i) * pow(1-t, n-i)

        for v in polygon.vertices:

            r = np.array(v.get_xyz_tuple())
            b = calc_b(i, n, t)

            result = np.add(result, r*b)
            i += 1

        x, y, z = result[0], result[1], result[2]
        return Vertex(x, y, z)
