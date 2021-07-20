from math import sqrt, pow, acos, pi, degrees
from itertools import combinations
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


def giftwrap_angle(new_point, point1, point2, point3):
    # calculates the angle of rotation of the support plane (formed by the three points) to reach the potential new
    # point to be added to the convex hull.

    # point2 and point3 are optional because in the first two steps of the algorithm we have less than three points
    # in the hull.
    if point2 is None:
        point2 = Point(0,1,0)
    if point3 is None:
        point3 = Point(1,0,0)

    # find the normal vector of the support plane (cross product)
    normal_vector = cross(vectorize((point1,point2)),vectorize((point1,point3)))

    # find the normal vector of the rotated support plane (rotation axis: edge (point1,point2)
    rotated_normal_vector = cross(vectorize((point1, new_point)), vectorize((point1, point2)))

    # calculate rotation angle
    angle = acos(dot(normal_vector, rotated_normal_vector) / (sqrt(dot(normal_vector)) * sqrt(dot(rotated_normal_vector))))

    if angle < 0:  # if angle is negative convert to positive (e.x. -30 -> 330)
        angle = 2 * pi + angle
    elif angle > 2 * pi:  # if angle is over a full rotation, remove a full rotation (e.x. 370 -> 10)
        angle = angle - 2 * pi

    return degrees(angle)


def giftwrap(points):  # rotates support plane to find new points to be added to the convex hull

    poly_points = set()  # set of points to be added to the convex hull polyhedron
    poly_edges = set()  # set of edges to be added to the convex hull polyhedron

    start_point1 = sorted(points, key=lambda pt: pt.x)[0] # initialize first point on convex hull as rightmost point in x axis
    start_point2 = None

    # initialize support plane
    point1 = start_point1
    poly_points.add(point1)  # add point in hull
    point2 = None
    point3 = None

    while True:
        # sort points based on rotation angle of support plane (point1, point2, point3)
        sorted_points = sorted(points, key=lambda potential_point: giftwrap_angle(potential_point, point1, point2, point3))

        # add smallest angle point to the convex hull if the new point is not
        if not sorted_points[0] in [point1, point2, point3]:
            new_point = sorted_points[0]
        else:
            new_point = sorted_points[1]
        poly_points.add(new_point)
        poly_edges.add((point1,new_point))
        if point2: poly_edges.add((point2,new_point))

        # update current points
        if point2: point3 = point2
        if not start_point2:  start_point2 = new_point  #  when the initial point 2 is found, save it
        point2 = new_point

        # test lines
        if len(poly_points) != 0 and len(poly_edges) != 0:
            matplotlib.use("TkAgg")
            plt.ion()
            plot_convex_hull(points,Polyhedron(poly_points,poly_edges))
            plt.waitforbuttonpress(timeout=-1)


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

        # define line parameters  a*x + b*y + c*z + d
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


def convex_hull(point_set):
    return brute_hull(point_set)
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
