import time
from math import sqrt, pow, atan2, pi, degrees
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim


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


def plot_convex_hull(point_set, polyhedron, title):
    x = []
    y = []
    z = []
    for point in point_set:
        x.append(point.x)
        y.append(point.y)
        z.append(point.z)
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.gca(projection='3d')
    plt.title(title)
    polyhedron.plot(ax)  # plot polyhedron
    ax.plot(x, y, z, 'ro', markersize=2)  # plot points
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    return fig, ax


def save_convex_hull_gif(fig, ax):
    def rotate(angle):
        ax.view_init(azim=angle)
    print("Making animation...Please wait.")
    rot_animation = anim.FuncAnimation(fig, rotate, frames=np.arange(0, 362, 2), interval=100)
    rot_animation.save(f'rotation_{int(time.time())}.gif', dpi=80, writer='imagemagick')


def dot(vec1, vec2=None):  # dot product
    if vec2 is None:
        vec2 = vec1
    return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z


def det(vec1, vec2, vec3):  # determinant
    return vec1.x * (vec2.y * vec3.z - vec3.y * vec2.z) \
           - vec2.y * (vec1.y * vec3.z - vec3.y * vec1.z) \
           + vec3.x * (vec1.y * vec2.z - vec2.y * vec1.z)


def cross(vec1, vec2):  # cross product
    return Point(vec1.y * vec2.z - vec1.z * vec2.y,
                 vec1.z * vec2.x - vec1.x - vec2.z,
                 vec1.x * vec2.y - vec1.y * vec2.x)


def plane_norm_vector(vec1, vec2):  # calculate plane normal vector of plane (formed by two vectors)
    norm_vector = cross(vec1, vec2)
    norm_vector_len = sqrt(dot(norm_vector))
    return Point(norm_vector.x / norm_vector_len, norm_vector.y / norm_vector_len, norm_vector.z / norm_vector_len)


def plane_params(p1, p2 ,p3):  # get plane parameters from point trio
    # plane parameters  a*x + b*y + c*z + d
    a = (p2.y - p1.y) * (p3.z - p1.z) - (p3.y - p1.y) * (p2.z - p1.z)
    b = (p2.z - p1.z) * (p3.x - p1.x) - (p3.z - p1.z) * (p2.x - p1.x)
    c = (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)
    d = -(a * p1.x + b * p1.y + c * p1.z)
    return a, b, c, d


def vectorize(edge):  # find vector of an edge (a,b)
    (a, b) = edge
    vector = Point(
        b.x - a.x,
        b.y - a.y,
        b.z - a.z)
    return vector


def giftwrap_angle(p, p1, p2, p3):
    # calculates the rotation angle of the support plane (formed by the three points p1, p2, p3) needed to reach the
    # potential new point p to be added to the convex hull.

    # points p2 and p3 are optional because in the first two steps of the algorithm we have less than three points
    # in the hull.
    if p2 is None:  # if p2 is none set an imaginary point in the same y line
        p2 = Point(p1.x + 0, p1.y + 10, p1.z + 0)
    if p3 is None:  # if p3 is none set an imaginary point in the same z line
        p3 = Point(p1.x + 0, p1.y + 0, p1.z + 10)

    # vectors
    a = vectorize((p1,p2))
    b = vectorize((p1,p3))
    c = vectorize((p1,p))

    # find the normal vector of the support plane (a x b , where a is p1-p2 and b is p1-p3)
    # because we want the plane normal vector to point outside of the hull
    norm_vector = plane_norm_vector(a,b)

    # find the normal vector of the rotated support plane (a x c, where c is p1-p and rotation axis is vector a)
    rotated_normal_vector = plane_norm_vector(a,c)

    # calculate rotation angle between norm_vector and rotated_normal_vector
    dot_prod = dot(norm_vector, rotated_normal_vector)
    determinant = det(rotated_normal_vector, norm_vector, plane_norm_vector(norm_vector, rotated_normal_vector))
    angle = atan2(determinant, dot_prod)

    if angle < 0:  # if angle is negative convert to positive (e.x. -30 -> 330)
        angle = 2 * pi + angle
    elif angle > 2 * pi:  # if angle is over a full rotation, remove a full rotation (e.x. 370 -> 10)
        angle = angle - 2 * pi

    return degrees(angle)


def giftwrap(p1, p2, p3, points, poly_points, poly_edges, poly_facets):  # rotates support plane around edge p1-p2 to find new points to be added to the convex hull

    # sort points based on rotation angle of support plane (point1, point2, point3)
    other_points = [point for point in points if point not in [p1, p2, p3]]  # point that are not p1, p2 or p3
    sorted_points = sorted(other_points, key=lambda p: giftwrap_angle(p, p1, p2, p3))

    p = sorted_points[0]  # potential new point p (smallest angle)

    # terminate algorithm when the giftwrap closes (algorithm reaches existing facet)
    if len(poly_edges) > 3 and (frozenset([p1, p2, p]) in poly_facets):
        return None

    # add smallest angle point p to the convex hull
    poly_points.add(p)
    # add the new edges (or edge) to the convex hull
    poly_edges.add(frozenset([p1,p]))  # a frozen set is used because a set cannot contain sets (we need a set because the order of points on the edge doesn't matter)
    if p2:
        poly_edges.add(frozenset([p2,p]))
        poly_facets.add(frozenset([p1, p2, p3]))

    # rotate support plane around new edges recursively
    if p2:  # if we have three points (p1, p2 and p)
        # rotate on new edge p1-p
        giftwrap(p1, p, p2, points, poly_points, poly_edges, poly_facets)
        # rotate on new edge p2-p
        giftwrap(p, p1, p2, points, poly_points, poly_edges, poly_facets)
    else:  # if we have only two points  (p1 and p)
        # rotate on new edge p1-p
        giftwrap(p1, p, None, points, poly_points, poly_edges, poly_facets)

    return Polyhedron(poly_points,poly_edges)


def brute_hull(point_set):  # brute force convex hull
    # checks for every trio of points (potential facet) if the plane created by the points separates
    # the point space into two sets where one is empty and the other contains all other points.
    # if it does, add the trio of points to the convex hull polyhedron as a facet


    poly_points = set()  # set of points to be added to the convex hull polyhedron
    poly_edges = set()  # set of edges to be added to the convex hull polyhedron

    planes = combinations(point_set, 3)  # define all point trios

    for plane in planes:
        # point trio
        p1 = plane[0]
        p2 = plane[1]
        p3 = plane[2]

        # define plane parameters  a*x + b*y + c*z + d
        (a, b, c, d) = plane_params(p1, p2, p3)

        point_set1 = set()  # side above the plane
        point_set2 = set()  # side below the plane

        for p4 in point_set:  # point to be checked in which side of the plane it is located
            if p4 != p1 and p4 != p2 and p4 != p3:
                if a * p4.x + b * p4.y + c * p4.z + d < 0:  # if point is below plane
                    point_set1.add(p4)
                elif a * p4.x + b * p4.y + c * p4.z + d > 0:  # if point is above plane
                    point_set2.add(p4)

        if len(point_set1) == 0 or len(point_set2) == 0:  # if any of the sides above or below the plane is empty
            # add trio of points to the convex hull
            poly_points.add(p1)
            poly_points.add(p2)
            poly_points.add(p3)
            # add edges of trio to the convex hull
            poly_edges.add(frozenset([p1, p2]))
            poly_edges.add(frozenset([p1, p3]))
            poly_edges.add(frozenset([p2, p3]))

    return Polyhedron(poly_points, poly_edges)  # return convex hull Polygon


def convex_hull(points):

    poly_points = set()  # set of points of the convex hull polyhedron
    poly_edges = set()  # set of edges of the convex hull polyhedron
    poly_facets = set()  # set of facets of the convex hull polyhedron

    # initialize support plane with initial trio of points
    p1 = sorted(points, key=lambda pt: pt.x)[-1]  # initialize first point on convex hull as rightmost point in x axis
    poly_points.add(1)  # add point in hull
    p2 = None
    p3 = None

    # uncomment the one line below to use giftwrap algorithm
    # return giftwrap(p1, p2, p3, points, poly_points, poly_edges, poly_facets)

    # uncomment the one line below to use brute hull algorithm
    return brute_hull(points)

