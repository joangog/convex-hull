import numpy as np

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class segment:
    def __init__(self, point1, point2):
        #define parameters (a,b) in y=ax+b
        self.x1, self.y1 = point1
        self.x2, self.y2 = point2
        self.a = (self.y1 - self.y2) / (self.x1 - self.x2)
        self.b = self.y1 - self.a * self.x1

    def crosses(segment): #returns true if the line extention of the segment crosses the target segment
        if self.a == segment.a or np.any(np.in1d([self.point1,self.point2], [segment.point1,segment.pont2])) :
            return False
        else:
            #solve linear system to find the intersection point between the line extentions of the segments
            # y = a1x + b1 => a1x - y = -b1
            # y = a2x + b2 => a2x - y = -b2
            A = [[self.a, -1],[segment.a, -1]]
            b = [-self.b,-segment.b]
            x,y = np.linalg.solve(A,b)
            if min(segment.y1,segment.y2) < y < max(segment.y1,segment.y2): #if the intersection point is contained in the target segment
                return True

    def crosses(poly): #returns true if the line extention of the segment crosses the polygon
        for segment in poly.segments:
            if self.crosses(segment):
                return True
        return False

class polygon:
    def __init__(self, segments):
        self.segments = segments


def tangents(poly1, poly2):
    #find upper tangent
    #find lower tangent
    return True

def merge():
    return True

def divide():
    return True
