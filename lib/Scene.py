from .Vertex import Vertex
import numpy as np
import numpy.linalg as LA
from math import factorial, sqrt
from functools import reduce


class Scene:
    def __init__(self, G=Vertex(0, 0, 0), O=Vertex(1, 1, 3), light=None, v_point=None):
        self.G = G
        self.O = O
        self.light = light
        self.update_TP()
        self.v_point = v_point

    def prepare_obj(self, obj, intensity_type=None):
        self.transform_obj(obj)
        if self.light is not None:
            self.intensity_obj(obj)

    def intensity_obj(self, obj, intensity_type=None):

        if intensity_type == 'polygon':
            for polygon in obj.polygons:
                light_vector = self.light - polygon.center
                scalar_product = np.dot(polygon.norm, light_vector)/LA.norm(light_vector)/LA.norm(polygon.norm)
                polygon.intensity = (self.light.get_ambience() + self.light.get_difuse(scalar_product))/255

        else:
            for v in obj.obj_vertices:
                total = np.zeros(3)
                for p in v.parent_polygon:
                    total += p.norm
                v.norm = total/len(v.parent_polygon)
                light_vector = self.light - v
                scalar_product = np.dot(v.norm, light_vector)/LA.norm(light_vector)/LA.norm(v.norm)
                v.intensity = (self.light.get_ambience() + self.light.get_difuse(scalar_product))/255

    def transform_obj(self, obj):
        for polygon in list(obj.polygons):
            if not self.hide_polygon(polygon):
                for vertex in polygon.vertices:
                    x, y, z = vertex.get_xyz()

                    A0 = np.array([x, y, z, 1])
                    App = reduce(np.matmul, [A0, self.T, self.P])

                    xpp, ypp, zpp, hpp = App[0], App[1], App[2], App[3]
                    xp = xpp/hpp
                    yp = ypp/hpp

                    vertex.set_xyz((xp, yp, z))
            else:
                obj.polygons.remove(polygon)

    def hide_polygon(self, polygon):

        a, b, c, d = polygon.get_abcd()
        x, y, z = self.O.get_xyz()
        if ((x*a + y*b + z*c + d) <= 0):
            return True
        return False

    def set_GO(self, G=None, O=None):

        if G is not None:
            self.G = G
        if O is not None:
            self.O = O

        self.update_TP()

    def update_TP(self):
        O = np.array(self.O.get_xyz_list())
        G = np.array(self.G.get_xyz_list())

        xg, yg, zg = G[0], G[1], G[2]
        x0, y0, z0 = O[0], O[1], O[2]

        T1 = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [-x0, -y0, -z0, 1]
            ]
        )

        xg1 = xg-x0
        yg1 = yg-y0
        zg1 = zg-z0

        G1 = np.array([xg1, yg1, zg1])
        sina = yg1/(sqrt(pow(xg1, 2)+pow(yg1, 2)))
        cosa = xg1/(sqrt(pow(xg1, 2)+pow(yg1, 2)))

        if np.isnan(sina):
            sina = 0
        if np.isnan(cosa):
            cosa = 1

        T2 = np.array(
            [
                [cosa, -sina, 0, 0],
                [sina, cosa, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        )
        xg2 = sqrt(pow(xg1, 2)+pow(yg1, 2))
        yg2 = 0
        zg2 = zg1

        G2 = np.array([xg2, yg2, zg2])

        sinb = xg2/(sqrt(pow(xg2, 2)+pow(zg2, 2)))
        cosb = zg2/(sqrt(pow(xg2, 2)+pow(zg2, 2)))
        if np.isnan(sina):
            sina = 0
        if np.isnan(cosa):
            cosa = 1
        T3 = np.array(
            [
                [cosb, 0, sinb, 0],
                [0, 1, 0, 0],
                [-sinb, 0, cosb, 0],
                [0, 0, 0, 1]
            ]
        )

        xg3 = 0
        yg3 = 0
        zg3 = sqrt(pow(xg2, 2)+pow(zg2, 2))

        G3 = np.array([xg3, yg3, zg3])

        T4 = np.array(
            [
                [0, -1, 0, 0],
                [1, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        )
        T5 = np.array(
            [
                [-1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        )
        xpp, ypp, zpp, hpp = App[0], App[1], App[2], App[3]
        xp = xpp/hpp
        yp = ypp/hpp

        vertex.set_xyz((xp, yp, z))

    def hide_polygon(self, polygon):

        a, b, c, d = polygon.get_abcd()
        x, y, z = self.O.get_xyz()
        if ((x*a + y*b + z*c + d) <= 0):
            return True
        return False

    def set_GO(self, G=None, O=None):

        if G is not None:
            self.G = G
        if O is not None:
            self.O = O

        self.update_TP()

    def update_TP(self):
        O = np.array(self.O.get_xyz_list())
        G = np.array(self.G.get_xyz_list())

        xg, yg, zg = G[0], G[1], G[2]
        x0, y0, z0 = O[0], O[1], O[2]

        T1 = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [-x0, -y0, -z0, 1]
            ]
        )

        xg1 = xg-x0
        yg1 = yg-y0
        zg1 = zg-z0

        G1 = np.array([xg1, yg1, zg1])
        sina = yg1/(sqrt(pow(xg1, 2)+pow(yg1, 2)))
        cosa = xg1/(sqrt(pow(xg1, 2)+pow(yg1, 2)))

        if np.isnan(sina):
            sina = 0
        if np.isnan(cosa):
            cosa = 1

        T2 = np.array(
            [
                [cosa, -sina, 0, 0],
                [sina, cosa, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        )
        xg2 = sqrt(pow(xg1, 2)+pow(yg1, 2))
        yg2 = 0
        zg2 = zg1

        G2 = np.array([xg2, yg2, zg2])

        sinb = xg2/(sqrt(pow(xg2, 2)+pow(zg2, 2)))
        cosb = zg2/(sqrt(pow(xg2, 2)+pow(zg2, 2)))
        if np.isnan(sina):
            sina = 0
        if np.isnan(cosa):
            cosa = 1
        T3 = np.array(
            [
                [cosb, 0, sinb, 0],
                [0, 1, 0, 0],
                [-sinb, 0, cosb, 0],
                [0, 0, 0, 1]
            ]
        )

        xg3 = 0
        yg3 = 0
        zg3 = sqrt(pow(xg2, 2)+pow(zg2, 2))

        G3 = np.array([xg3, yg3, zg3])

        T4 = np.array(
            [
                [0, -1, 0, 0],
                [1, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        )
        T5 = np.array(
            [
                [-1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        )

        T = reduce(np.matmul, [T1, T2, T3, T4, T5])
        H = zg3

        P = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 1/H],
                [0, 0, 0, 0]
            ]
        )
        self.T = T
        self.P = P
        return self

    def __repr__(self):
        return str(self.objs)
