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
    def crosses(segment) #returns true if the line extention of the segment crosses another segment

    def crosses(poly): #returns true if the line extention of the segment crosses the polygon
        for segment in poly.segments

class polygon:
    def __init__(self, segments):
        self.segments = segments


def tangents(poly1, poly2)
    #find upper tangent
    #find lower tangent

def merge()

def divide()
