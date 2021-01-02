import numpy as np
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Polygon:
    def __init__(self, points):
        self.points = points
        self.n = len(points)  # number of segments in polygon

    def plot(self):
        x = []
        y = []
        for point in self.points:
            x.append(point.x)
            y.append(point.y)
        # repeat the first point to create a closed polygon shape
        x.append(self.points[0].x)
        y.append(self.points[0].y)
        plt.figure()
        plt.plot(x, y)
        plt.show()


def orientation(a, b, c):  # calculate orientation of segment (a,b) based on segment (b,c) where a,b,c are points

    # if orientation > 0, the angle between the segments is < 180
    # if orientation < 0, the angle between the segments is > 180
    # if orientation is 0, the angle between the segments is 180
    return (b.y-a.y)*(c.x-b.x) - (c.y-b.y)*(b.x-a.x)


def tangents(polyL, polyR):

    # find rightmost point of left polygon
    i_rightmost = 0  # index of rightmost point in left polygon (init with first point)
    for i in range(1, len(polyL.points)):  # for every point in the polygon
        if polyL.points[i_rightmost].x < polyL.points[i].x:  # if rightmost point is left of the current point
            i_rightmost = i  # set current point as new rightmost point

    # find leftmost point of right polygon
    i_leftmost = 0
    for i in range(1, len(polyR.points)):
        if polyR.points[i_leftmost].x > polyR.points[i].x:
            i_leftmost = i

    # init tangents with line connecting the rightmost and leftmost point of left and right polygon respectively
    upper_tangent = lower_tangent = (polyL.points[i_rightmost], polyR.points[i_leftmost])

    # find upper tangent
    i = i_leftmost  # current point index of right polygon (init with leftmost point of right polygon)
    j = i_rightmost  # current point index of left polygon (init with rightmost point of left polygon)
    done = 0
    while not done:  # while upper tangent crosses any polygon
        done = 1
        while orientation(upper_tangent[0], upper_tangent[1], polyR.points[(i + 1) % polyR.n]) < 0:  # while upper tangent crosses right polygon
            # move right point of tangent up by moving current point to next point of right polygon (points are stored clockwise)
            i = (i + 1) % polyR.n
            upper_tangent = (upper_tangent[0], polyR.points[i])
        while orientation(polyL.points[(j - 1) % polyL.n], upper_tangent[1], upper_tangent[0]) > 0:  # while upper tangent crosses left polygon
            done = 0
            # move left point of tangent up by moving current point to previous point of left polygon (points are stored clockwise)
            j = (j - 1) % polyL.n
            upper_tangent = (polyL.points[j], upper_tangent[1])
    upper_tangent_idx = (j, i)  # indices of each point of the upper tangent in the respective polygon

    # find lower tangent
    i = i_leftmost
    j = i_rightmost
    done = 0
    while not done:
        done = 1
        while orientation(lower_tangent[0], lower_tangent[1], polyR.points[(i - 1) % polyR.n]) > 0:  # while lower tangent crosses right polygon
            #move right point of tangent down by moving current point to previous point of right polygon (points are stored clockwise)
            i = (i - 1) % polyR.n
            lower_tangent = (lower_tangent[0], polyR.points[i])
        while orientation(polyL.points[(j + 1) % polyL.n], lower_tangent[1], lower_tangent[0]) < 0:  # while lower tangent crosses left polygon
            done = 0
            # move left point of tangent down by moving current point to next point of left polygon (points are stored clockwise)
            j = (j + 1) % polyL.n
            lower_tangent = (polyL.points[j], lower_tangent[1])
    lower_tangent_idx = (j, i)

    return upper_tangent, upper_tangent_idx, lower_tangent, lower_tangent_idx


def merge(poly1,poly2):

    if poly1.points[0].x < poly2.points[0].x:  # if poly1 is left and poly2 is right
        polyL = poly1
        polyR = poly2
    else:
        polyL = poly2
        polyR = poly1

    # find upper and lower tangent of polygons
    upper_tangent, upper_tangent_idx, lower_tangent, lower_tangent_idx = tangents(polyL,polyR)
    upper_left_idx, upper_right_idx = upper_tangent_idx
    lower_left_idx, lower_right_idx = lower_tangent_idx

    points = []
    points.extend([upper_tangent[0],upper_tangent[1]]) # add the upper tangent points to the merged polygon

    # add the rightside points of the right polygon to the merged polygon
    i = (upper_right_idx + 1) % polyR.n
    while i != lower_right_idx:
        points.append(polyR.points[i])
        i = (i + 1) % polyR.n

    points.extend([lower_tangent[1],lower_tangent[0]])  # add the lower tangent points to the merged polygon

    # add the leftside points of the left polygon to the merged polygon
    i = (lower_right_idx + 1) % polyL.n
    while i != upper_left_idx:
        points.append(polyL.points[i])
        i = (i + 1) % polyL.n

    return Polygon(points)


def divide():
    #find median of x coordinate of all points
    #divide space using median x
    #start appending segment from uppermost y of each polygon
    return True
