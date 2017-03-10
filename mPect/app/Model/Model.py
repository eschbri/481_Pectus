import matplotlib.pyplot as plt
from Vertex import *
from VertexNormal import *
from Face import *
from matplotlib import collections as mc

class Model(object):

    def __init__(self):
        # init the points
        self.vertices = []
        self.vertexNormals = []
        self.faces = []

        # init the bounding box
        self.minx, self.miny, self.minz = 99999,99999,99999
        self.maxx, self.maxy, self.maxz = -99999, -99999, -99999

        # Init constraints. Right now, just use the same points

    def initialize(self, filename):
        # init the filename
        self.filename = filename

        # populate it all
        self.readIn()

        self.cVertices = range(1,len(self.vertices))
        self.cFaces    = range(1,len(self.faces))

    def readIn(self):
        with open(self.filename) as f:
            content = f.readlines()

        content = [x.strip("\n") for x in content]

        for c in content:
            if len(c) > 0 and c[0] == '#':
                # It's a comment, ignore it
                continue

            line = c.split(' ')

            if len(line) < 2:
                # TODO: maybe throw an error?
                continue

            if line[0] == "v":
                # Vertex
                x = float(line[1])
                y = float(line[2])
                z = float(line[3])

                self.vertices.append(Vertex(x, y, z))

                # Figure out bounding boxes
                if x < self.minx:
                    self.minx = x
                if x > self.maxx:
                    self.maxx = x
                if y < self.miny:
                    self.miny = y
                if y > self.maxy:
                    self.maxy = y
                if z < self.minz:
                    self.minz = z
                if z > self.maxz:
                    self.maxz = z

            elif line[0] == "vn":
                # Vector normal

                if line[1] == "nan" or line[2] == "nan" or line[3] == "nan":
                    self.vertexNormals.append(VertexNormal(0,0,0))

                self.vertexNormals.append(VertexNormal(float(line[1]), float(line[2]), float(line[3])))
            elif line[0] == "f":
                # Face
                x = line[1].split('/')
                y = line[2].split('/')
                z = line[3].split('/')

                if len(x) < 3 or len(y) < 3 or len(z) < 3:
                    raise Exception("Invalid Face Format")

                self.faces.append(Face(int(x[0])-1,int(x[2])-1,int(y[0])-1,int(y[2])-1,int(z[0])-1,int(z[2])-1))

    def flip(self, flipx, flipy, flipz):
        for i in range(len(self.vertices)):
            if flipx:
                self.vertices[i].x = self.maxx - self.vertices[i].x
            if flipy:
                self.vertices[i].y = self.maxy - self.vertices[i].y
            if flipz:
                self.vertices[i].z = self.maxz - self.vertices[i].z

        self.calculateBounding()

    def calculateBounding(self):
        self.minx, self.miny, self.minz = 99999,99999,99999
        self.maxx, self.maxy, self.maxz = -99999, -99999, -99999

        for v in self.vertices:
            x = v.x
            y = v.y
            z = v.z

            if x < self.minx:
                self.minx = x
            if x > self.maxx:
                self.maxx = x
            if y < self.miny:
                self.miny = y
            if y > self.maxy:
                self.maxy = y
            if z < self.minz:
                self.minz = z
            if z > self.maxz:
                self.maxz = z



    def get2D(self, plane, fig, sliceAction):
        if len(plane) != 2 or plane not in ["xy","yz","xz"]:
            raise Exception("Invalid plane.\n\tValid planes are [\"xy\",\"yz\",\"xz\"")

        # Use contraints
        xs = [self.vertices[i].x for i in self.cVertices]
        ys = [self.vertices[i].y for i in self.cVertices]
        zs = [self.vertices[i].z for i in self.cVertices]

        fig.clf()

        axes = fig.add_subplot(111)
        axes.set_axis_off()

        if plane == "xy":
            axes.scatter(xs, ys, c=zs, s=100, cmap='gray')
        elif plane == "yz":
            axes.scatter(ys, zs, c=xs, s=100, cmap='gray')
        elif plane == "xz":
            axes.scatter(xs, zs, c=ys, s=100, cmap='gray')


        onclick = sliceAction(axes)

        cid = fig.canvas.mpl_connect('button_press_event', onclick)

        #fig.canvas.mpl_disconnect(cid)

        #return constraints

    def drawConstraints(self, plane):
        if len(plane) != 2 or plane not in ["xy","yz","xz"]:
            raise Exception("Invalid plane.\n\tValid planes are [\"xy\",\"yz\",\"xz\"")

        xs = [self.vertices[i].x for i in self.cVertices]
        ys = [self.vertices[i].y for i in self.cVertices]
        zs = [self.vertices[i].z for i in self.cVertices]

        fig = plt.figure()

        if plane == "xy":
            plt.scatter(xs, ys, c=zs, s=100, cmap='gray')
        elif plane == "yz":
            plt.scatter(ys, zs, c=xs, s=100, cmap='gray')
        elif plane == "xz":
            plt.scatter(xs, zs, c=ys, s=100, cmap='gray')

        plt.show()

    def drawXY(self):
        xs = [x.x for x in self.vertices]
        ys = [x.y for x in self.vertices]
        zs = [x.z for x in self.vertices]

    def constrain(self, axis, gt, lt):
        if type(axis) is not str or axis not in ["x","y","z"]:
            raise Exception("Improper axis given")

        if (type(gt) is not int and type(gt) is not float) or (type(lt) is not int and type(lt) is not float):
            raise ValueError("Must use float or integer as constraints; given " + str(type(gt)) + " and " + str(type(lt)))

        if axis == "x":
            self.cVertices = [i for i in self.cVertices if self.vertices[i].x > gt and self.vertices[i].x < lt]
            self.cFaces = [i for i in self.cFaces if self.vertices[self.faces[i].v1].x > gt and self.vertices[self.faces[i].v1].x < lt and self.vertices[self.faces[i].v2].x > gt and self.vertices[self.faces[i].v2].x < lt and self.vertices[self.faces[i].v3].x > gt and self.vertices[self.faces[i].v3].x < lt]
        elif axis == "y":
            self.cVertices = [i for i in self.cVertices if self.vertices[i].y > gt and self.vertices[i].y < lt]
            self.cFaces = [i for i in self.cFaces if self.vertices[self.faces[i].v1].y > gt and self.vertices[self.faces[i].v1].y < lt and self.vertices[self.faces[i].v2].y > gt and self.vertices[self.faces[i].v2].y < lt and self.vertices[self.faces[i].v3].y > gt and self.vertices[self.faces[i].v3].y < lt]
        elif axis == "z":
            self.cVertices = [i for i in self.cVertices if self.vertices[i].z > gt and self.vertices[i].z < lt]
            self.cFaces = [i for i in self.cFaces if self.vertices[self.faces[i].v1].z > gt and self.vertices[self.faces[i].v1].z < lt and self.vertices[self.faces[i].v2].z > gt and self.vertices[self.faces[i].v2].z < lt and self.vertices[self.faces[i].v3].z > gt and self.vertices[self.faces[i].v3].z < lt]

    # Slicing
    def iPlane(self, f, y):
        points = [self.vertices[f.v1], self.vertices[f.v2], self.vertices[f.v3]]

        # ensure the triangle intersects the plane
        above = False
        below = False
        on    = False

        for p in points:
            if p.y > y:
                above = True
            if p.y == y:
                on = True
            if p.y < y:
                below = True

        # TODO: Handle the case where only one point of the triangle is on the plane

        if not (above and below):
            return False

        return True

    # sliceFByY
    # Gets the intersection of a plane and a face
    # returns a tuple with the two points that define the intersection
    def sliceFByY(self, f, y):
        if not self.iPlane(f, y):
            raise Exception("Triangle does not intersect plane")

        points = [self.vertices[f.v1], self.vertices[f.v2], self.vertices[f.v3]]

        combs = [(0,1), (0,2), (1,2)]
        results = []

        for c in combs:
            if len(results) >= 2:
                break

            # only care about the combinations that intersect the plane
            if (points[c[0]].y >= y and points[c[1]].y < y) or (points[c[0]].y < y and points[c[1]].y >= y):
                t0 = points[c[0]]
                t1 = points[c[1]]

                factor = (y - t0.y) / (t1.y - t0.y)

                x = t0.x + (t1.x - t0.x) * factor
                z = t0.z + (t1.z - t0.z) * factor
                
                results.append((x,z))

        if len(results) < 2:
            raise Exception("Not enough intersection points")

        return results

    def sliceY(self, y):
        # Get all the faces that intersect our plane
        faces = [x for x in self.faces if self.iPlane(x, y)]

        results = []

        #linking list connecting points from 2d slice
        #not sure about the white spaces until cropping is complete but 
        #for now just do a simple dictionary match with each specfic point 
        #having its own list of connecting points
        linkingListSlice = {}

        for f in faces:
            points = self.sliceFByY(f, y)
            #results.append(points[0])
            #results.append(points[1])
            
            if points[0] not in linkingListSlice:
                linkingListSlice[points[0]] = [points[1]]
            else:
                linkingListSlice[points[0]].append(points[1])

            if points[1] not in linkingListSlice:
                linkingListSlice[points[1]] = [points[0]]
            else:
                linkingListSlice[points[1]].append(points[0])

            results.append((points[0], points[1]))

        return results

    def printStats(self):
        print "Total vertices: " + str(len(self.vertices))
        print "Total vertnorms: " + str(len(self.vertexNormals))
        print "Total faces: " + str(len(self.faces))
        print "Bounding Box:"
        print "\tX: " + str(self.minx) + " " + str(self.maxx)
        print "\tY: " + str(self.miny) + " " + str(self.maxy)
        print "\tZ: " + str(self.minz) + " " + str(self.maxz)
