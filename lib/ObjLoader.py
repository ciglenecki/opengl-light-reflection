from .Polygon import Polygon
from .Vertex import Vertex
import sys


def obj_loader(obj_path):
    vertices = []
    polygons = []
    vertices_objects = []

    with obj_path.open() as file:
        for line in file:
            line = line.rstrip()

            if(line.startswith('v')):
                x, y, z = (float(x) for x in line[2:].split(" "))
                vertices.append([x, y, z])

            if(line.startswith('f')):

                v1, v2, v3 = (int(x) for x in line[2:].split(" "))
                v1 = Vertex(vertices[v1-1][0], vertices[v1-1][1], vertices[v1-1][2])
                v2 = Vertex(vertices[v2-1][0], vertices[v2-1][1], vertices[v2-1][2])
                v3 = Vertex(vertices[v3-1][0], vertices[v3-1][1], vertices[v3-1][2])

                polygon = Polygon([v1, v2, v3])
                polygons.append(polygon)

                vertices_objects.append(v1.add_parent_polygon(polygon))
                vertices_objects.append(v2.add_parent_polygon(polygon))
                vertices_objects.append(v3.add_parent_polygon(polygon))

    return polygons, vertices_objects
