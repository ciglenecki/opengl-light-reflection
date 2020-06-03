from .ObjLoader import obj_loader
import sys
from .Vertex import Vertex


class Obj():

    def __init__(self, filename=None, polygons=None, center=Vertex(0, 0, 0), scale=1):
        if filename is not None:
            self.polygons, self.obj_vertices = obj_loader(filename)

        elif polygons is not None:
            self.polygons = polygons

        self.center = center

    def offset(self, center):
        for p in self.polygons:
            p.offset(center=center)

    def normalize(self, scale=1):

        M, un_center = self.calc_extremes()

        for p in self.polygons:
            p.normalize(M=M/scale, center=un_center)

        return self

    def get_max_z(self):
        return max(v.z for p in self.polygons for v in p.vertices)

    def calc_extremes(self):
        xmin = ymin = zmin = sys.maxsize
        xmax = ymax = zmax = - sys.maxsize - 1

        for p in self.polygons:
            for v in p.vertices:
                x, y, z = v.get_xyz()
                if(x < xmin):
                    xmin = x
                if (x > xmax):
                    xmax = x
                if (y < ymin):
                    ymin = y
                if (y > ymax):
                    ymax = y
                if (z < zmin):
                    zmin = z
                if (z > zmax):
                    zmax = z

        M = max(xmax - xmin, ymax - ymin, zmax - zmin)
        un_center = Vertex((xmax+xmin)/2, (ymax+ymin)/2, (zmax+zmin)/2)
        return M, un_center

    def contains_vertex(self, vertex):
        """
        Returns true/false if vertex are contained inside of object = (x,y,z)
        """

        for polygon in self.polygons:
            if not (polygon.contains_vertex(point)):
                return False
        return True

    def __repr__(self):
        return str(self.polygons)
