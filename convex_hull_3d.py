from math import sqrt, pow, acos, pi, degrees
from itertools import combinations
import matplotlib.pyplot as plt
import convex_hull_2d as ch2d


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


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


def dot(vec1, vec2):
    return vec1.x * vec2.x + vec1.y + vec2.y + vec1.z + vec2.z


def giftwrap_angle(vector, support_vector,
                   giftwrap_vector):  # calculates angle between polyhedron edge and giftwrap plane

    # project vector of polyhedron edge to the perpendicular plane of the giftwrap plane (its plane normal vector is the support vector)
    projected_vector = Point(
        vector.x - support_vector.x * dot(vector, support_vector) / dot(support_vector, support_vector),
        vector.y - support_vector.y * dot(vector, support_vector) / dot(support_vector, support_vector),
        vector.z - support_vector.z * dot(vector, support_vector) / dot(support_vector, support_vector))

    # calculate angle between projected vector and giftwrap plane (its plane normal vector is the giftwrap vector)
    angle = acos(abs(dot(vector, giftwrap_vector) / (sqrt(dot(vector)) * sqrt(dot(giftwrap_vector)))))

    if angle < 0:  # if angle is negative convert to positive (e.x. -30 -> 330)
        angle = 2 * pi + angle
    elif angle > 2 * pi:  # if angle is over a full rotation, remove a full rotation (e.x. 370 -> 10)
        angle = angle - 2 * pi

    return degrees(angle)


def giftwrap_sort(edges, support_vector,
                  giftwrap_vector):  # sort edges based on angle between giftwrap plane (minimum first)
    return 0


def merge(polyhedron1, polyhedron2):
    points = []  # points of merged convex hull
    edges = []  # edges of merged convex hull

    # find left and right polyhedron
    x1 = []  # x coordinates for every point in polyhedron1
    x2 = []  # x coordinates for every point in polyhedron2
    for point in polyhedron1.points:
        x1.append(point.x)
    for point in polyhedron2.points:
        x2.append(point.x)
    if max(x1) <= min(x2):  # if polyhedron1 is left and polyhedron2 is right
        polyhedronL = polyhedron1
        polyhedronR = polyhedron2
    else:
        polyhedronL = polyhedron2
        polyhedronR = polyhedron1

    # project polyhedrons on x-y plane (2d) to find upper tangent of resulting polygons (is also the tangent of polyhedrons)
    polygonL_points = list()
    polygonR_points = list()
    for point in polyhedronL.points:
        polygonL_points.append(ch2d.Point(point.x, point.y))
    for point in polyhedron2.points:
        polygonR_points.append(ch2d.Point(point.x, point.y))
    polygonL = ch2d.Polygon(polygonL_points)
    polygonR = ch2d.Polygon(polygonR_points)

    # find upper tangent of polygons
    upper_tangent, (upper_left_point_idx, upper_right_point_idx), _, _ = ch2d.tangents(polygonL, polygonR)
    upper_left_point = polyhedronL.points[upper_left_point_idx]
    upper_right_point = polygonR.points[upper_right_point_idx]

    points.extend([upper_left_point, upper_right_point])
    edges.extend((upper_left_point, upper_right_point))

    # get the upper tangent vector (support vector)
    support_vector = Point(
        upper_right_point.x - upper_left_point.x,
        upper_right_point.y - upper_left_point.y,
        upper_right_point.z - upper_left_point.z)
    support_vector_len = sqrt(pow(support_vector.x, 2) + pow(support_vector.y, 2))
    support_vector = Point(support_vector.x / support_vector_len, support_vector.y / support_vector_len)

    # do gift wrapping using support plane (giftwrap plane) to find convex hull faces:
    # get the plane normal vector (giftwrap vector) of the giftwrap plane,
    # calculated as the cross product (a x b) of the z axis and the support vector

    # z axis (vector a)
    ax = 0
    ay = 0
    az = 1
    # support vector (vector b)
    bx = support_vector.x
    by = support_vector.y
    bz = support_vector.z

    giftwrap_vector = Point(ay * bz - az * by, az * bx - ax - bz, ax * by - ay * bx)  # cross product (a x b)

    # initial A and B -> tangent A and B
    # repeat:
    # sort edges to A and B neighbors by angle to giftwrap plane
    # find edge with smallest angle to neighbor C and add edge and point to convex hull
    # to gift wrapping
    # if C neighbor of A: C -> A else C -> B
    # stop when A and B are tangent A and B again


    # neighborsA =

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
    if len(point_set) < 6000:  # if the set has less than n points just do brute hull
        return brute_hull(point_set)

    point_set1, point_set2 = ch2d.divide(point_set)  # divide into two sets

    # generate convex hull polygons for each set
    if len(point_set1) != 0:
        poly1 = convex_hull(point_set1)
    if len(point_set2) != 0:
        poly2 = convex_hull(point_set2)

    # merge the two polygons
    if len(point_set1) != 0 and len(point_set2) != 0:  # if point sets are not empty
        return merge(poly1, poly2)
    elif len(point_set1) == 0:  # if only the second point set isn't empty then return polygon 2
        return poly2
    else:
        return poly1
