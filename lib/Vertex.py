class Vertex(object):
    def __init__(self, x=None, y=None, z=None, xyz=None):
        if xyz is not None:
            x, y, z = xyz
        self.x = x
        self.y = y
        self.z = z
        self.norm = None
        self.intensity = None
        self.parent_polygon = []

    def get_xyz(self):
        return self.x, self.y, self.z

    def get_xyz_tuple(self):
        return ((self.x, self.y, self.z))

    def get_xyz_list(self):
        return [self.x, self.y, self.z]

    def add_parent_polygon(self, parent_polygon):
        self.parent_polygon.append(parent_polygon)
        return self

    def set_xyz(self, sample):
        x, y, z = sample
        self.x = x
        self.y = y
        self.z = z
        return self

    def offset(self, center):
        xc, yc, zc = center.get_xyz()

        self.x = self.x-xc
        self.y = self.y-yc
        self.z = self.z-zc

    def normalize(self, M, center):

        xc, yc, zc = center.get_xyz()
        self.x = (self.x - xc)*2/M
        self.y = (self.y - yc)*2/M
        self.z = (self.z - zc)*2/M
        return self

    def __sub__(self, vertex):
        return [self.x-vertex.x, self.y - vertex.y, self.z - vertex.z]

    def get_one_zero(self):

        def calc(value):
            return (value+2)
        return calc(self.x), calc(self.y), calc(self.z)

    def __repr__(self):
        return str((self.x, self.y, self.z))


class Light(Vertex):
    def __init__(self, x=None, y=None, z=None, xyz=None, ia=255, ka=0.5, ii=255, kd=0.5):
        super().__init__(x, y, z)
        self.ia = ia
        self.ka = ka
        self.ii = ii
        self.kd = kd
        self.ambience = None
        self.partital_difuse = None

    def get_ambience(self):
        if self.ambience is None:
            self.ambience = self.ia * self.ka
        return self.ambience

    def get_difuse(self, LN):
        if self.partital_difuse is None:
            self.partital_difuse = self.ii * self.kd
        return self.partital_difuse * max(0, LN)
