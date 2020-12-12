import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Segment:
    def __init__(self, point1, point2):
        #define parameters (a,b) in y=ax+b
        self.x1, self.y1 = point1
        self.x2, self.y2 = point2
        self.a = (self.y1 - self.y2) / (self.x1 - self.x2)
        self.b = self.y1 - self.a * self.x1

    def crosses(self,segment): #returns true if the line extension of the segment crosses the target segment
        if self.a == segment.a or np.any(np.in1d([self.point1,self.point2], [segment.point1,segment.pont2])) :
            return False
        else:
            #solve linear system to find the intersection point between the line extensions of the segments
            # y = a1x + b1 => a1x - y = -b1
            # y = a2x + b2 => a2x - y = -b2
            A = [[self.a, -1],[segment.a, -1]]
            b = [-self.b,-segment.b]
            x,y = np.linalg.solve(A,b)
            if min(segment.y1,segment.y2) < y < max(segment.y1,segment.y2): #if the intersection point is contained in the target segment
                return True

    def crosses(self,poly): #returns true if the line extension of the segment crosses the polygon
        for segment in poly.segments:
            if self.crosses(segment):
                return True
        return False

class Polygon:
    def __init__(self, segments):
        self.segments = segments

def tangents(poly1, poly2):

    if poly1.segments[0].point1[0]<poly2.segments[0].point1[0]: #if poly1 is left and poly2 is right
        polyL = poly1
        polyR = poly2
    else:
        polyL = poly2
        polyR = poly1



    #find rightmost point of left polygon
    rightmost_pointL = polyL.segments[0].point1 #set first point of left polygon as rightmost point
    rightmost_pointL_i = 0 #index of rightmost point in left polygon
    for i,segment in enumerate(polyL.segments[1:]):
        if rightmost_pointL[0] < segment.point1[0]:
            rightmost_pointL = segment.point1
            rightmost_pointL_i = i

    #find leftmost point of right polygon
    leftmost_pointR = polyR.segments[0].point1  # set first point of left polygon as rightmost point
    leftmost_pointR_i = 0  # index of leftmost point in right polygon
    for i,segment in enumerate(polyR.segments[1:]):
        if leftmost_pointR[0] < segment.point1[0]:
            leftmost_pointR = segment.point1
            leftmost_pointR_i = i

    lower_tangent = Segment(rightmost_pointL,leftmost_pointR)
    upper_tangent = Segment(rightmost_pointL,leftmost_pointR)

    #find lower tangent
    while lower_tangent.crosses(polyL) or lower_tangent.crosses(polyR):
        while lower_tangent.crosses(polyR):
            #move leftmost point of right polygon up
            if leftmost_pointR[1] <= polyR.segment[leftmost_pointR_i+1].point1[1]: #if next point is above current point
                leftmost_pointR = polyR.segment[leftmost_pointR_i+1].point1
                leftmost_pointR_i = leftmost_pointR_i+1
            else:
                leftmost_pointR = polyR.segment[leftmost_pointR_i-1].point1
                leftmost_pointR_i = leftmost_pointR_i-1
            lower_tangent = Segment(rightmost_pointL, leftmost_pointR)

        while lower_tangent.crosses(polyL):
            #move rightmost point of left polygon up
            if rightmost_pointL[1] <= polyL.segment[rightmost_pointL_i+1].point1[1]:  # if next point is below current point
                rightmost_pointL = polyL.segment[rightmost_pointL_i+1].point1
                rightmost_pointL_i = rightmost_pointL_i+1
            else:
                rightmost_pointL = polyL.segment[rightmost_pointL_i-1].point1
                rightmost_pointL_i = rightmost_pointL_i-1

def merge():
    return True

def divide():
    #kmeans maybe?
    return True
