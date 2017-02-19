class Vertex(object):

    def __init__(self, x, y , z):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, rhs):
        return dot(self, rhs)

def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z