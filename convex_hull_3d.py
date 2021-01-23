import math
from itertools import combinations
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import convex_hull_2d


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Polyhedron:
    def __init__(self, points, edges):
        self.points = points
        self.edges = edges   # list of edges (edge is a set() of Points)
        self.n = len(edges)  # number of edges in polygon

    def plot(self):
        x = []
        y = []
        z = []

        for edge in self.edges:
            for point in edge:
                x.append(point.x)
                y.append(point.y)
                z.append(point.z)

        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax = fig.gca(projection='3d')
        ax.plot(x, y, z)
        plt.show()


def plot_convex_hull(point_set, polyhedron):
    x = []
    y = []
    z = []
    for point in point_set:
        x.append(point.x)
        y.append(point.y)
        z.append(point.y)
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.gca(projection='3d')
    ax.plot(x, y, 'ro', markersize=1)  # plot points
    polyhedron.plot()  # plot polyhedron
    plt.show()


def clockwise_angle(a,b):  #calculates clockwise angle of vector (a,b)

    if a.x == b.x and a.y == b.y:  # if the segment length is zero return angle = 0
        return 0

    base_vector = Point(0, 1)  # the vector from which we will calculate the angle of the target vector (12 o'clock)

    vector = Point(b.x - a.x, b.y - a.y)  # target vector (basically the end point of a line that starts from (0,0))
    vector_len = math.sqrt(math.pow(vector.x, 2) + math.pow(vector.y, 2))  # length of target vector

    norm_vector = Point(vector.x / vector_len, vector.y / vector_len)  # normalized target vector

    # calculate angle
    dot_prod = norm_vector.x * base_vector.x + norm_vector.y * base_vector.y  # x1 * x2 + y1 * y2
    diff_prod = norm_vector.x * base_vector.y - norm_vector.y * base_vector.x  # x1 * y2 - y1 * x2
    angle = math.atan2(diff_prod, dot_prod)

    if angle < 0:  # if angle is negative convert to positive (e.x. -30 -> 330)
        angle =  2 * math.pi + angle
    elif angle > 2 * math.pi:  # if angle is over a full rotation, remove a full rotation (e.x. 370 -> 10)
        angle = angle - 2 * math.pi

    return math.degrees(angle)


def clockwise_sort(point_set):  # sorts clockwise a set of points

    # find avg of x coordinate of all points
    x = []
    for point in point_set:
        x.append(point.x)
    x_avg = sum(x) / len(x)

    # find avg of y coordinate of all points
    y = []
    for point in point_set:
        y.append(point.y)
    y_avg = sum(y) / len(y)

    # find center of set
    center = Point(x_avg, y_avg)

    # sort points clockwise around center
    return sorted(point_set, key=lambda pt: clockwise_angle(center, pt))  # returns sorted list


def divide(point_set):  # divides a set of points using x axis to two equal sets

    if len(point_set) == 1:  # if the size of the set is 1
        return point_set, set()  # return the set and an empty set

    # sort list of points based on x coordinate
    sorted_point_set = sorted(point_set, key=lambda pt: pt.x)

    # divide space into equal size subsets
    point_set1 = set()
    point_set2 = set()
    for idx, point in enumerate(sorted_point_set):
        if idx < len(sorted_point_set)/2:
            point_set1.add(point)
        else:
            point_set2.add(point)

    return point_set1, point_set2


def orientation(a, b, c):  # calculates orientation of segment (a,b) based on segment (b,c) where a,b,c are points

    # if orientation > 0, the angle between the segments is 0 < angle < 180
    # if orientation < 0, the angle between the segments is 180 < angle < 360
    # if orientation is 0, the angle between the segments is k*180

    return (b.y-a.y)*(c.x-b.x) - (c.y-b.y)*(b.x-a.x)


def tangent(polyL, polyR):  # calculates lower tangent between two polyhedrons

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
    # while upper tangent crosses any polygon
    while not done:
        done = 1
        # while upper tangent crosses right polygon
        while orientation(upper_tangent[0], upper_tangent[1], polyR.points[(i + 1) % polyR.n]) <= 0:
            # move right point of tangent up by moving current point to next point of right polygon (points are stored clockwise)
            i = (i + 1) % polyR.n
            upper_tangent = (upper_tangent[0], polyR.points[i])
        # while upper tangent crosses left polygon
        while orientation(upper_tangent[1], upper_tangent[0], polyL.points[(j - 1) % polyL.n]) >= 0:
            done = 0
            # move left point of tangent up by moving current point to previous point of left polygon
            j = (j - 1) % polyL.n
            upper_tangent = (polyL.points[j], upper_tangent[1])
    upper_tangent_idx = (j, i)  # indices of each point of the upper tangent in the respective polygon

    # find lower tangent
    i = i_leftmost  # index of right polygon
    j = i_rightmost  # index of left polygon
    done = 0
    # while lower tangent crosses any polygon
    while not done:
        done = 1
        # while lower tangent crosses right polygon
        while orientation(lower_tangent[0], lower_tangent[1], polyR.points[(i - 1) % polyR.n]) >= 0:
            #move right point of tangent down by moving current point to previous point of right polygon
            i = (i - 1) % polyR.n
            lower_tangent = (lower_tangent[0], polyR.points[i])
        # while lower tangent crosses left polygon
        while orientation(lower_tangent[1], lower_tangent[0], polyL.points[(j + 1) % polyL.n]) <= 0:
            done = 0
            # move left point of tangent down by moving current point to next point of left polygon
            j = (j + 1) % polyL.n
            lower_tangent = (polyL.points[j], lower_tangent[1])

    lower_tangent_idx = (j, i)

    return upper_tangent, upper_tangent_idx, lower_tangent, lower_tangent_idx


def merge(poly1,poly2):

    #find left and right polyhedron
    x1 = []  # x coordinates for every point in poly1
    x2 = []  # x coordinates for every point in poly2
    for point in poly1.points:
        x1.append(point.x)
    for point in poly2.points:
        x2.append(point.x)
    if max(x1) <= min(x2):  # if poly1 is left and poly2 is right
        polyL = poly1
        polyR = poly2
    else:
        polyL = poly2
        polyR = poly1

    # project polyhedrons in x-y plane to find lower tangent

    # find upper and lower tangent of polygons
    upper_tangent, upper_tangent_idx, lower_tangent, lower_tangent_idx = tangents(polyL,polyR)

    upper_left_idx, upper_right_idx = upper_tangent_idx
    lower_left_idx, lower_right_idx = lower_tangent_idx

    points = []

    # add the upper tangent points to the merged polygon
    points.extend([upper_tangent[0],upper_tangent[1]])

    # add the rightside points of the right polygon to the merged polygon
    if upper_right_idx != lower_right_idx:  # if end of upper tangent != start of lower tangent
        i = (upper_right_idx + 1) % polyR.n
        while i != lower_right_idx:
            points.append(polyR.points[i])
            i = (i + 1) % polyR.n

    # add the lower tangent points to the merged polygon
    if upper_right_idx != lower_right_idx:  # if end of upper tangent != start of lower tangent
        if lower_left_idx != upper_left_idx:  # if end of lower tangent != start of upper tangent
            points.extend([lower_tangent[1], lower_tangent[0]])
        else:
            points.append(lower_tangent[1])
    else:  # if end of upper tangent == start of lower tangent
        if lower_left_idx != upper_left_idx:  # if end of lower tangent != start of upper tangent
            points.append(lower_tangent[0])

    # add the leftside points of the left polygon to the merged polygon
    if lower_left_idx != upper_left_idx:  # if leftside points exist
        i = (lower_left_idx + 1) % polyL.n
        while i != upper_left_idx:
            points.append(polyL.points[i])
            i = (i + 1) % polyL.n

    return Polygon(points)


def brute_hull(point_set):  # brute force convex hull
    # checks for every trio of points if the plane created by the points separates
    # the point space into two sets where one is empty and the other contains all other points.
    # if it does, add the trio of points to the convex hull polyhedron

    poly_points = set()  # set of points to be added to the convex hull polygon
    poly_edges = set()

    planes = combinations(point_set, 3)  # define all point trios

    for plane in planes:
        point1 = plane[0]
        point2 = plane[1]
        point3 = plane[2]

        # define line parameters  a*x + b*y + c*z + d
        a = (point2.y - point1.y) * (point3.z - point1.z) - (point3.y - point1.y) * (point2.z - point1.z)
        b = (point2.z - point1.z) * (point3.x - point1.x) - (point3.z - point1.z) * (point2.x - point1.x)
        c = (point2.x - point1.x) * (point3.y - point1.y) - (point3.x - point1.x) * (point2.y - point1.y)
        d = -(a * point1.x + b * point1.y + c + point1.z)

        point_set1 = set()  # side above the line
        point_set2 = set()  # side below the line

        for point4 in point_set:  # point to be checked in which side of the line it is located
            if point4 != point1 and point4 != point2 and point4 != point3:
                if a * point4.x + b * point4.y + c * point4.z + d < 0:  # if point is below plane
                    point_set1.add(point4)
                elif a * point4.x + b * point4.y + c * point4.z + d > 0:  # if point is above plane
                    point_set2.add(point4)

        if len(point_set1) == 0 or len(point_set2) == 0:  # if any of the sides above or below the line is empty
            # add trio of points to the convex hull
            poly_points.add(point1)
            poly_points.add(point2)
            poly_points.add(point3)
            # add edges of trio to the convex hull
            poly_edges.add((point1,point2))
            poly_edges.add((point1, point3))
            poly_edges.add((point2, point3))

    #poly_points = clockwise_sort(poly_points)  # sort points in clockwise order
    return Polyhedron(poly_points,poly_edges)  # return convex hull Polygon


def convex_hull_3d(point_set):

    if len(point_set) < 6:  # if the set has less than 6 points just do brute hull
        return brute_hull(point_set)

    point_set1, point_set2 = divide(point_set)  # divide into two sets

    # generate convex hull polygons for each set
    if len(point_set1) != 0:
        poly1 = convex_hull_3d(point_set1)
    if len(point_set2) != 0:
        poly2 = convex_hull_3d(point_set2)

    # merge the two polygons
    if len(point_set1) != 0 and len(point_set2) != 0:  # if point sets are not empty
        return merge(poly1, poly2)
    elif len(point_set1) == 0:  # if only the second point set isn't empty then return polygon 2
        return poly2
    else:
        return poly1




