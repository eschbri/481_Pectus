from matplotlib import pyplot as plt


class Slice(object):
    # given the line segmentations representation
    # find the ordered vertices representation of a slice
    def __init__(self, lines):

        self.lines = lines
        self.vertices = []

        self.point_dict = {}
        visited = {}
        for l in lines:
            if l[0] not in self.point_dict:
                self.point_dict[l[0]] = []
                visited[l[0]] = 0
            if l[1] not in self.point_dict:
                self.point_dict[l[1]] = []
                visited[l[1]] = 0
            self.point_dict[l[0]].append(l[1])
            self.point_dict[l[1]].append(l[0])

        curr = lines[0][0]
        visited[curr] = 1
        self.vertices.append(curr)
        next = self.point_dict[curr][0]
        for i in range(len(self.point_dict)):
            if visited[next] == 0:
                visited[next] = 1
                self.vertices.append(next)
                connected = self.point_dict[next]
                if visited[connected[0]] == 0:
                    curr = next
                    next = connected[0]
                elif len(connected) >= 2 and visited[connected[1]] == 0:
                    curr = next
                    next = connected[1]
                else:
                    curr = next
                    min_dist = 999999999999999999
                    for p, v in visited.iteritems():
                        if v == 0:
                            dist = (curr[0] - p[0]) * (curr[0] - p[0]) + (curr[1] - p[1]) * (curr[1] - p[1])
                            if dist < min_dist:
                                min_dist = dist
                                next = p
                    if min_dist > 0.01:
                        if len(self.vertices) < len(lines)/3:
                            self.vertices = []
                            for p, v in visited.iteritems():
                                if v == 0:
                                    curr = p
                                    break
                            visited[curr] = 1
                            self.vertices.append(curr)
                            next = self.point_dict[curr][0]
                        else:
                            break
            else:
                print "!!!!!"
        '''
        print len(self.vertices), len(lines)
        print "AreaChest:", self.areaChest()
        #plt.plot([0, 0.5], [0.075, 0.07])
        #print "AreaDefect:", self.areaDefect(0, 0.075, 0.5, 0.07)
        print "AreaLeft", self.areaLeft(0.33)
        '''
        '''
        x_list = [x for [x, y] in self.vertices]
        y_list = [y for [x, y] in self.vertices]
        plt.plot(x_list, y_list)
        plt.show()
        '''

    # Return the original lines
    def getLines(self):
        lines = []

        for i in range(len(self.vertices) - 1):
            lines.append((self.vertices[i], self.vertices[i+1]))

        lines.append((self.vertices[len(self.vertices) - 1],self.vertices[0]))

        return lines

    def sign(self, n):
        if n > 0:
            return 1
        elif n < 0:
            return -1
        else:
            return 0

    def determine(self, p1, p2, p):
        return self.sign( (p2[0] - p1[0])*(p[1] - p1[1]) - (p2[1] - p1[1])*(p[0] - p1[0]) )

    # Chop off a portion of the lines
    def chop(self, p1, p2, p3):
        o = self.determine(p1, p2, p3)

        rList = []

        for i in range(len(self.vertices)):
            c = self.determine(p1, p2, self.vertices[i])
            if c == o or c == 0: # If point is on the erase side of line
                rList.append(i)
                #self.vertices.pop(i)

        for i in range(len(rList)-1,0,-1):
            self.vertices.pop(rList[i])

    #calculate the defect/chest ratio
    def defectRatio(self, x0, y0, x1, y1):
        return self.areaDefect(x0, y0, x1, y1)/self.areaChest()

    #calculate the left/right ratio
    def asymmetryRatio(self, x0):
        areaLeft = self.areaLeft(x0) 
        areaRight = self.areaChest() - areaLeft
        if areaRight == 0:
            return 0
        return areaLeft / areaRight

    def areaChest(self):
        return areaPolygon(self.vertices)

    #line : y = kx + b
    def areaDefect(self, x0, y0, x1, y1):
        k = (y1 - y0) / (x1 - x0) 
        b = y1 - k * x1

        point_lists = []

        point_list = []
        for i in range(len(self.vertices)):
            v = self.vertices[i]
            prev_v = self.vertices[i-1]
            #below the line
            if v[1] < k * v[0] + b and len(point_list) > 0:
                x, y = findIntersection(prev_v[0], prev_v[1], v[0], v[1], x0, y0, x1, y1)
                point_list.append((x, y))
                point_lists.append(point_list)
                point_list = []
            #above the line
            elif v[1] >= k * v[0] + b:
                if len(point_list) == 0:
                    x, y = findIntersection(prev_v[0], prev_v[1], v[0], v[1], x0, y0, x1, y1)
                    point_list.append((x, y))
                point_list.append(v)

        if len(point_lists) == 0:
            return -1
        elif self.vertices[0][1] >= k * self.vertices[0][0] + b and self.vertices[-1][1] >= k * self.vertices[-1][0] + b:
            point_lists[0] += point_lists[-1]
            point_lists = point_lists[:-1]

        if len(point_lists) == 0:
            return -1

        defect_vertices_index = 0
        min_num_vertices = len(point_lists[0])
        for i in range(1, len(point_lists)):
            if len(point_lists[i]) < min_num_vertices:
                min_num_vertices = len(point_lists[i])
                defect_vertices_index = i
        '''
        x_list = [x for [x, y] in point_lists[defect_vertices_index]]
        y_list = [y for [x, y] in point_lists[defect_vertices_index]]
        plt.plot(x_list, y_list)
        plt.show()
        '''
        return areaPolygon(point_lists[defect_vertices_index])

    #calculate the area of chest left to x=x0
    def areaLeft(self, x0):

        point_list = []
        for i in range(len(self.vertices)):
            v = self.vertices[i]
            prev_v = self.vertices[i-1]
            #right side
            if v[0] > x0 and prev_v[0] <= x0:
                x, y = findIntersection(prev_v[0], prev_v[1], v[0], v[1], x0, 0, x0, 1)
                point_list.append((x, y))
            #left side
            elif v[0] <= x0:
                if prev_v[0] > x0:
                    x, y = findIntersection(prev_v[0], prev_v[1], v[0], v[1], x0, 0, x0, 1)
                    point_list.append((x, y))
                point_list.append(v)

        if len(point_list) == 0:
            return 0
        '''
        x_list = [x for [x, y] in point_list]
        y_list = [y for [x, y] in point_list]
        plt.plot(x_list, y_list)
        plt.show()
        '''
        return areaPolygon(point_list)

    #the function assumes that the slice has a standard concave 
    #this function also assumes that self.vertices is correct, and the arms are "cut off"
    #might need to modify function to handle a slice without standard concave
    def hallerIndex(self):
        point_list = []
        two_lowest_z_peaks = [(1,1),(1,1)]
        left_lung_x = (1,1)
        right_lung_x = (0,0)
        lowest_point = (1,1)

        self.new_point_dict = {}
        for l in range(len(self.vertices)-1):
            if self.vertices[l] not in self.new_point_dict:
                self.new_point_dict[self.vertices[l]] = []

            self.new_point_dict[self.vertices[l]].append(self.vertices[l+1])
            self.new_point_dict[self.vertices[l]].append(self.vertices[l-1])

        if self.vertices[len(self.vertices)-1] not in self.new_point_dict:
            self.new_point_dict[self.vertices[len(self.vertices)-1]] = []
        self.new_point_dict[self.vertices[len(self.vertices)-1]].append(self.vertices[0])
        self.new_point_dict[self.vertices[len(self.vertices)-1]].append(self.vertices[len(self.vertices)-2])

        #find the two outer side horizontal points
        for i in range(len(self.vertices)):
            if left_lung_x[0] > self.vertices[i][0]:
                left_lung_x = self.vertices[i]
            if right_lung_x[0] < self.vertices[i][0]:
                right_lung_x = self.vertices[i]
            if lowest_point[1] > self.vertices[i][1]:
                lowest_point = self.vertices[i]

        midLine = (left_lung_x[0] + right_lung_x[0]) / 2
        firstQuarterLine = midLine * .75
        thirdQuarterLine = midLine * 1.25

        #find left_peak to the left of midline, and the right peak to the right of midline
        curr = left_lung_x
        left_peak = (1,1)
        right_peak = (1,1)
        visited = {}

        for l in range(len(self.vertices)):
            if self.vertices[l][1] < left_peak[1] and self.vertices[l][0] < midLine:
                left_peak = self.vertices[l]
            elif self.vertices[l][1] < right_peak[1] and self.vertices[l][0] > midLine:
                right_peak = self.vertices[l]

        #the sternum is marked at the highest point z axis between the two lowest z peaks
        curr = left_peak
        sternum_point = (0,0)
        visited = {}
        while curr[0] < midLine:
            if curr not in visited:
                visited[curr] = True
            else:
                break

            if curr[1] > sternum_point[1] and curr[0] > firstQuarterLine:
                sternum_point = curr

            if self.new_point_dict[curr][0][0] < self.new_point_dict[curr][1][0]:
                curr = self.new_point_dict[curr][1]
            else:
                curr = self.new_point_dict[curr][0]

        
        #the sternum is marked at the highest point z axis between the two lowest z peaks
        curr = right_peak
        visited = {}
        while curr[0] > midLine:
            if curr not in visited:
                visited[curr] = True
            else:
                break

            if curr[1] > sternum_point[1] and curr[0] < thirdQuarterLine:
                sternum_point = curr

            if self.new_point_dict[curr][0][0] > self.new_point_dict[curr][1][0]:
                curr = self.new_point_dict[curr][1]
            else:
                curr = self.new_point_dict[curr][0]

        #find the point that intercepts the x of the sternum for the vertebre point
        vertebre_point = (0,0)
        for i in range(len(self.vertices)):
            if self.vertices[i-1][0] == sternum_point[0] and self.vertices[i-1][1] > sternum_point[1]:
                vertebre_point = self.vertices[i-1]
                break
            elif self.vertices[i-1][0] <= sternum_point[0] and self.vertices[i][0] >= sternum_point[0]:
                if self.vertices[i-1][1] > sternum_point[1] and self.vertices[i][1] > sternum_point[1]:
                    vertebre_point = hallerIntersection(self.vertices[i-1], self.vertices[i], sternum_point)
                    break
            elif self.vertices[i-1][0] >= sternum_point[0] and self.vertices[i][0] <= sternum_point[0]:
                if self.vertices[i-1][1] > sternum_point[1] and self.vertices[i][1] > sternum_point[1]:
                    vertebre_point = hallerIntersection(self.vertices[i-1], self.vertices[i], sternum_point)
                    break

        retList = []
        retList.append((right_lung_x[0] - left_lung_x[0]) / (vertebre_point[1] - sternum_point[1]))
        retList.append(vertebre_point)
        retList.append(sternum_point)
        retList.append(right_lung_x)
        retList.append(left_lung_x)
        retList.append(lowest_point)
        return retList

#calcualte the area given vertices using Shoelace formula
def areaPolygon(vertices):
    area = 0.0
    for i in range(len(vertices) - 1):
        area += vertices[i][0] * vertices[i+1][1]
        area -= vertices[i][1] * vertices[i+1][0]
    area += vertices[len(vertices) - 1][0] * vertices[0][1]
    area -= vertices[len(vertices) - 1][1] * vertices[0][0]
    if area < 0:
        area = 0 - area
    area = 0.5 * area
    return area

#find the intersection of two lines given 4 points
def findIntersection(x0, y0, x1, y1, x2, y2, x3, y3):
    if x1 == x0 and x3 == x2:
        return (x0, y0)
    if x1 == x0:
        x = x0
        k1 = (y3 - y2) / (x3 - x2) 
        b1 = y3 - k1 * x3
        y = k1 * x + b1
    elif x3 == x2:
        x = x2
        k0 = (y1 - y0) / (x1 - x0) 
        b0 = y1 - k0 * x1
        y = k0 * x + b0
    else: 
        k0 = (y1 - y0) / (x1 - x0) 
        b0 = y1 - k0 * x1
        k1 = (y3 - y2) / (x3 - x2) 
        b1 = y3 - k1 * x3
        x = (b1 - b0)/(k0 - k1)
        y = k0 * x + b0
    return (x, y) 

def hallerIntersection(p1, p2, p3):
    k = (p1[1] - p2[1]) / (p1[0] - p2[0])
    x = p3[0]
    b = p1[1] - (k * p1[0])
    z = (k * p3[0]) + b
    return (x, z)
