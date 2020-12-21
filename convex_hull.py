import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment:
    def __init__(self, point1, point2):
        # define parameters (a,b) in y=ax+b
        self.point1 = point1
        self.point2 = point2
        self.a = (self.point1.y - self.point2.y) / (self.point1.x - self.point2.x)  # (y1 - y2) / (x1 - x2)
        self.b = self.point1.y - self.a * self.point1.x  # y1 - a * x1

    def crosses_seg(self, segment):  # returns true if the line extension of the segment crosses the target segment
        if self.a == segment.a or np.any(np.in1d([self.point1, self.point2], [segment.point1, segment.point2])):
            return False # return false if the line and segment are parallel or if the line crosses the segment at its end points
        else:
            # solve linear system to find the intersection point between the line extensions of the segments
            # y = a1x + b1 => a1x - y = -b1
            # y = a2x + b2 => a2x - y = -b2
            A = [[self.a, -1], [segment.a, -1]]
            b = [-self.b, -segment.b]
            x, y = np.linalg.solve(A, b)
            if min(segment.point1.y, segment.point2.y) < y < max(segment.point1.y, segment.point2.y):  # if the intersection point is contained in the target segment
                return True
            return False

    def crosses_poly(self, poly):  # returns true if the line extension of the segment crosses the target polygon
        for segment in poly.segments:
            if self.crosses_seg(segment):
                return True
        return False

    def crosses(self, shape):  # wrapper for the above functions
        if type(shape).__name__ == 'Polygon': return self.crosses_poly(shape)
        elif type(shape).__name__ == 'Segment': return self.crosses_seg(shape)


class Polygon:
    def __init__(self, segments):
        self.segments = segments
        self.n = len(segments)  # number of segments in polygon


def tangents(polyL, polyR):

    # find rightmost point of left polygon
    left_rightmost_point = polyL.segments[0].point1  # set first point of left polygon as rightmost point
    left_rightmost_point_idx = 0  # index of rightmost point in left polygon
    for i, segment in enumerate(polyL.segments[1:]):
        if left_rightmost_point.x < segment.point1.x:
            left_rightmost_point = segment.point1
            left_rightmost_point_idx = i + 1 # we add 1 because we enumerate from the segment list skipping the first element

    # find leftmost point of right polygon
    right_leftmost_point = polyR.segments[0].point1  # set first point of left polygon as rightmost point
    right_leftmost_point_idx = 0  # index of leftmost point in right polygon
    for i, segment in enumerate(polyR.segments[1:]):
        if right_leftmost_point.x > segment.point1.x:
            right_leftmost_point = segment.point1
            right_leftmost_point_idx = i + 1  # we add 1 because we enumerate from the segment list skipping the first element

    upper_tangent = Segment(left_rightmost_point, right_leftmost_point)
    lower_tangent = Segment(left_rightmost_point, right_leftmost_point)

    # find upper tangent
    left_point = left_rightmost_point  # current point of left polygon
    right_point = right_leftmost_point  # current point of right polygon
    i = right_leftmost_point_idx  # current point index of right polygon
    j = left_rightmost_point_idx  # current point index of left polygon
    while upper_tangent.crosses(polyL) or lower_tangent.crosses(polyR):
        while upper_tangent.crosses(polyR):
            # go up in right polygon by moving current point to next point (segments are stored clockwise)
            i = (i + 1) % polyR.n
            right_point = polyR.segments[i].point1
            upper_tangent = Segment(upper_tangent.point1,right_point)
        while upper_tangent.crosses(polyL):
            # go up in left polygon by moving current point to previous point (segments are stored clockwise)
            j = (j - 1) % polyL.n
            left_point = polyL.segments[j].point1
            upper_tangent = Segment(left_point,upper_tangent.point2)
    upper_tangent_idx = (i,j) # indices of each point of the upper tangent in the respective polygon

    # find lower tangent
    left_point = left_rightmost_point  # current point of left polygon
    right_point = right_leftmost_point  # current point of right polygon
    i = right_leftmost_point_idx  # current point index of right polygon
    j = left_rightmost_point_idx  # current point index of left polygon
    while lower_tangent.crosses(polyL) or lower_tangent.crosses(polyR):
        while lower_tangent.crosses(polyR):
            # go down by moving current point to previous point (points are stored clockwise)
            i = (i - 1) % polyR.n
            right_point = polyR.segments[i].point1
            lower_tangent = Segment(upper_tangent.point1,right_point)
        while lower_tangent.crosses(polyL):
            # go down by moving current point to next point (points are stored clockwise)
            j = (j + 1) % polyL.n
            left_point = polyL.segments[j].point1
            lower_tangent = Segment(left_point,upper_tangent.point2)
    lower_tangent_idx = (i, j)  # indices of each point of the upper tangent in the respective polygon

    return upper_tangent, upper_tangent_idx, lower_tangent_idx, lower_tangent_idx


def merge(poly1,poly2):

    if poly1.segments[0].point1.x < poly2.segments[0].point1.x:  # if poly1 is left and poly2 is right
        polyL = poly1
        polyR = poly2
    else:
        polyL = poly2
        polyR = poly1

    # find upper and lower tangent of polygons
    upper_tangent, upper_tangent_idx, lower_tangent, lower_tangent_idx = tangents(polyL,polyR)
    upper_left_idx, upper_right_idx = upper_tangent_idx
    lower_left_idx, lower_right_idx = lower_tangent_idx

    segments = []
    segments.append(upper_tangent) # add the upper tangent as a segment of the merged polygon

    # add the rightside segments of the right polygon to the merged polygon
    i = upper_right_idx
    while i != lower_right_idx:
        segments.append(polyR.segments[i])
        i = (i + 1) % polyR.n

    # add the leftside segments of the left polygon to the merged polygon
    i = lower_right_idx
    while i != upper_left_idx:
        segments.append(polyL.segments[i])
        i = (i + 1) % polyL.n

    return Polygon(segments)


def divide():
    # kmeans maybe?
    return True
