import pyglet
from pyglet.gl import *


class Drawer():
    def __init__(self, window):
        self.window = window

    def scale_vertex_window(self, vertex):

        w = self.window.width
        h = self.window.height
        return (vertex.x+1)*w/2, (vertex.y+1)*h/2

    def draw_scene(self, scene, point_size=1, draw_label=False, color=None):
        for obj in scene.objs:
            self.draw_obj(obj, point_size, draw_label, color)

    def draw_obj(self, obj, point_size=1, draw_label=False, color=None):
        print(len(obj.polygons))
        for polygon in obj.polygons:
            self.draw_polygon(polygon, point_size, draw_label, color, obj)

    def draw_polygon(self, polygon, point_size=1, draw_label=False, color=None, obj=None):

        # average_color = polygon.get_avg_z()/obj.get_max_z()

        glPointSize(point_size)
        glBegin(GL_TRIANGLES)

        if polygon.intensity is not None:
            i = polygon.intensity
            glColor3f(i, i, i)

        for v in polygon.vertices:

            if v.intensity is not None:
                i = v.intensity
                glColor3f(i, i, i)

            x, y = self.scale_vertex_window(v)

            glVertex2f(x, y)
        glEnd()

    def draw_lines(self, obj, point_size=1, draw_label=False, color=None):
        """
        Obj
            Polygon1:
                (x1,y1,z1)
                (x2,y2,y2)
                ...
            ...
        """

        for polygon in obj.polygons:
            for i in range(len(polygon.vertices)-1):
                x1, y1 = self.scale_vertex_window(polygon.vertices[i])
                x2, y2 = self.scale_vertex_window(polygon.vertices[i+1])

                pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                     ('v2f', (x1, y1, x2, y2))
                                     )

    def draw_vertex(self, vertex):
        x, y = self.scale_vertex_window(vertex)
        glPointSize(10)
        glColor3f(1, 1, 1)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

        # pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
        #                      ('v2f', (x, y))
        #                      )
        return
