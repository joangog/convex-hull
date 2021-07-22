from math import sqrt, pow, acos, pi, degrees
from itertools import combinations
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import convex_hull_2d as ch2d


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.on_hull = False  # if the point is on the hull or not


class Polyhedron:
    def __init__(self, points, edges):
        self.points = points
        self.edges = edges  # list of edges (edge is a set() of Points)
        self.n = len(edges)  # number of edges in polygon

    def plot(self, ax):
        for edge in self.edges:
            x = []
            y = []
            z = []
            for point in edge:
                x.append(point.x)
                y.append(point.y)
                z.append(point.z)
            ax.plot(x, y, z, 'b',linewidth=0.5)


def plot_convex_hull(point_set, polyhedron):
    x = []
    y = []
    z = []
    for point in point_set:
        x.append(point.x)
        y.append(point.y)
        z.append(point.z)
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.gca(projection='3d')
    polyhedron.plot(ax)  # plot polyhedron
    ax.plot(x, y, z, 'ro', markersize=2)  # plot points
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    return ax


def dot(vec1, vec2=None):  # dot product
    if vec2 is None:
        vec2 = vec1
    return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z


def cross(vec1, vec2):  # cross product
    return Point(vec1.y * vec2.z - vec1.z * vec2.y, vec1.z * vec2.x - vec1.x - vec2.z, vec1.x * vec2.y - vec1.y * vec2.x)


def vectorize(edge):  # find normalized vector from an edge / segment (a,b)
    (a, b) = edge
    vector = Point(
        b.x - a.x,
        b.y - a.y,
        b.z - a.z)
    vector_len = sqrt(pow(vector.x, 2) + pow(vector.y, 2) + pow(vector.z, 2))
    vector = Point(vector.x / vector_len, vector.y / vector_len, vector.z / vector_len)
    return vector


def giftwrap_angle(p, p1, p2, p3):
    # calculates the angle of rotation of the support plane (formed by the three points p1, p2, p3) to reach the
    # potential new point p to be added to the convex hull.

    # points p2 and p3 are optional because in the first two steps of the algorithm we have less than three points
    # in the hull.
    if p2 is None:
        p2 = Point(p1.x + 0, p1.y + 1, p1.z + 0)
    if p3 is None:
        p3 = Point(p1.x + 0, p1.y + 0, p1.z + 1)

    # find the normal vector of the support plane (cross product)
    normal_vector = cross(vectorize((p1,p3)), vectorize((p1,p2)))

    # find the normal vector of the rotated support plane (rotation axis: edge (p1,p2)
    rotated_normal_vector = cross(vectorize((p1, p)), vectorize((p1, p2)))

    # calculate rotation angle
    angle = acos(round(dot(rotated_normal_vector, normal_vector) / (sqrt(dot(normal_vector)) * sqrt(dot(rotated_normal_vector))),8))  # round to avoid flop error

    if angle < 0:  # if angle is negative convert to positive (e.x. -30 -> 330)
        angle = 2 * pi + angle
    elif angle > 2 * pi:  # if angle is over a full rotation, remove a full rotation (e.x. 370 -> 10)
        angle = angle - 2 * pi

    return degrees(angle)


def giftwrap(p1, p2, p3, points, poly_points, poly_edges):  # rotates support plane around edge p1-p2 to find new points to be added to the convex hull

    # terminate algorithm when the giftwrap closes (algorithm reaches initial points)
    # if len(poly_edges) > 3 and ([p1, p2, p3] in [poly_points[0], poly_points[1], poly_points[2]]):
    #     print('done')

    # sort points based on rotation angle of support plane (point1, point2, point3)
    other_points = [point for point in points if point not in [p1, p2, p3]]
    sorted_points = sorted(other_points, key=lambda p: giftwrap_angle(p, p1, p2, p3))

    # add smallest angle point p' to the convex hull if the new point p is not p1, p2 or p3
    p = sorted_points[0]  # new point p
    poly_points.add(p)
    poly_edges.add((p1,p))
    if p2: poly_edges.add((p2,p))

    test_key = giftwrap_angle(p, p1, p2, p3)
    test_keys = [giftwrap_angle(p, p1, p2, p3) for p in sorted_points]

    # test lines
    matplotlib.use("TkAgg")
    plt.ion()
    ax = plot_convex_hull(points,Polyhedron(poly_points,poly_edges))
    if p2 is None:
        p2_ = Point(p1.x + 0, p1.y + 1, p1.z + 0)
    else:
        p2_ = p2
    if p3 is None:
        p3_ = Point(p1.x + 0, p1.y + 0, p1.z + 1)
    else:
        p3_ = p3
    # define line parameters  a*x + b*y + c*z + d
    normal_vector = cross(vectorize((p1,p3_)), vectorize((p1,p2_)))
    a = normal_vector.x
    b = normal_vector.y
    c = normal_vector.z
    d = -(a * p1.x + b * p1.y + c * p1.z)
    if c != 0:
        xx, yy = np.meshgrid([p1.x,p2_.x], [p1.y,p2_.y])
        zz = - (d + b*yy + a*xx) / c
    else:
        yy, zz = np.meshgrid([0,1], [0,1])
        xx = - (d + c*zz + b*yy) / a

    ax.plot_surface(xx, yy, zz, alpha=0.2)
    plt.waitforbuttonpress(timeout=-1)

    # rotate support plane around new edges p1-p and p2-p recursively
    if p3:
        giftwrap(p, p1, p2, points, poly_points, poly_edges)
        giftwrap(p2, p, p1, points, poly_points, poly_edges)
    else:
        giftwrap(p1, p, None, points, poly_points, poly_edges)


def brute_hull(point_set):  # brute force convex hull
    # checks for every trio of points if the plane created by the points separates
    # the point space into two sets where one is empty and the other contains all other points.
    # if it does, add the trio of points to the convex hull polyhedron


    poly_points = set()  # set of points to be added to the convex hull polyhedron
    poly_edges = set()  # set of edges to be added to the convex hull polyhedron

    planes = combinations(point_set, 3)  # define all point trios

    for plane in planes:
        point1 = plane[0]
        point2 = plane[1]
        point3 = plane[2]

        # define plane parameters  a*x + b*y + c*z + d
        a = (point2.y - point1.y) * (point3.z - point1.z) - (point3.y - point1.y) * (point2.z - point1.z)
        b = (point2.z - point1.z) * (point3.x - point1.x) - (point3.z - point1.z) * (point2.x - point1.x)
        c = (point2.x - point1.x) * (point3.y - point1.y) - (point3.x - point1.x) * (point2.y - point1.y)
        d = -(a * point1.x + b * point1.y + c * point1.z)

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
            poly_edges.add((point1, point2))
            poly_edges.add((point1, point3))
            poly_edges.add((point2, point3))

    # poly_points = clockwise_sort(poly_points)  # sort points in clockwise order
    return Polyhedron(poly_points, poly_edges)  # return convex hull Polygon


def convex_hull(points):

    poly_points = set()  # set of points to be added to the convex hull polyhedron
    poly_edges = set()  # set of edges to be added to the convex hull polyhedron

    # initialize support plane with initial trio of points
    p1 = sorted(points, key=lambda pt: pt.x)[-1]  # initialize first point on convex hull as rightmost point in x axis
    poly_points.add(1)  # add point in hull
    p2 = None
    p3 = None

    giftwrap(p1, p2, p3, points, poly_points, poly_edges)


    # return brute_hull(point_set)
    # if len(point_set) < 6000:  # if the set has less than n points just do brute hull
    #     return brute_hull(point_set)
    #
    # point_set1, point_set2 = ch2d.divide(point_set)  # divide into two sets
    #
    # # generate convex hull polygons for each set
    # if len(point_set1) != 0:
    #     poly1 = convex_hull(point_set1)
    # if len(point_set2) != 0:
    #     poly2 = convex_hull(point_set2)
    #
    # # merge the two polygons
    # if len(point_set1) != 0 and len(point_set2) != 0:  # if point sets are not empty
    #     return merge(poly1, poly2)
    # elif len(point_set1) == 0:  # if only the second point set isn't empty then return polygon 2
    #     return poly2
    # else:
    #     return poly1
