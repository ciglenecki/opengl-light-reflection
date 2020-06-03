import copy
import time
from lib.Drawer import Drawer
from lib.Polygon import *
from lib.Vertex import Vertex, Light
from lib.ObjLoader import obj_loader
from pathlib import Path, PurePath
import numpy as np
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from lib.Obj import Obj
from lib.Scene import Scene
text = pyglet.text.Label('Matej Ciglenečki',
                         font_name='Consolas',
                         font_size=10,
                         x=10, y=10)
# PATHS ###################################################

project_path = Path.cwd()
object_name = "teapot"
object_path = Path(project_path, "obj", object_name+".obj")

# PYGLET ###################################################

window = pyglet.window.Window(resizable=True)
drawer = Drawer(window)

# BEIZER ###################################################

poly_control = Polygon([Vertex(0, 0, 2), Vertex(1, 1, 2), Vertex(2, -1, 2), Vertex(3, 0, 2)])
poly_beizer = BeizerPolygon(poly_control)

control = Obj(polygons=[poly_control])
beizer = Obj(polygons=[poly_beizer])

n_control = copy.deepcopy(control).normalize()
n_beizer = copy.deepcopy(beizer).normalize()

# OBJECT ###################################################

obj = Obj(filename=object_path)
n_obj = copy.deepcopy(obj).normalize(scale=0.5)

# SCENE ###################################################

scene = Scene(G=Vertex(0, 0, 0), O=Vertex(1, 1, 1), light=Light(1, 1, 1, ia=255, ka=0.1, ii=255, kd=1))


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.Z:
        window.clear()
    if symbol == key.X:
        window.clear()
        on_draw()
    if symbol == key.C:
        on_draw()


i = -1
@window.event
def on_draw():
    for i in range(len(poly_beizer.vertices)-1):
        window.clear()

        new_O = poly_beizer.vertices[i]
        scene.set_GO(O=new_O)

        trans_n_obj = copy.deepcopy(n_obj)
        scene.prepare_obj(trans_n_obj, intensity_type='polygon')

        text.draw()

        drawer.draw_obj(trans_n_obj)
        window.flip()


@window.event
def on_show():
    on_draw()


# def update(dt):
#     window.flip()
#     global i
#     if i < len(poly_beizer.vertices)-1:
#         i += 1
# pyglet.clock.schedule_interval(update, 0.5)
pyglet.app.run()
