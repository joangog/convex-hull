from convex_hull import *

p1 = Point(-4.3, 7)
p2 = Point(-1.5, 5.5)
p3 = Point(-2.2, 2)
p4 = Point(-6.1, 1)
p5 = Point(-7.4, 5)

p6 = Point(1.8, 6)
p7 = Point(3.96, 5.35)
p8 = Point(5.14, -0.5)
p9 = Point(1.7, 0.84)
p10 = Point(1, 3.5)

s1 = Segment(p1, p2)
s2 = Segment(p2, p3)
s3 = Segment(p3, p4)
s4 = Segment(p4, p5)
s5 = Segment(p5, p1)

s6 = Segment(p6, p7)
s7 = Segment(p7, p8)
s8 = Segment(p8, p9)
s9 = Segment(p9, p10)
s10 = Segment(p10, p6)

poly1 = Polygon([s1, s2, s3, s4, s5])
poly2 = Polygon([s6, s7, s8, s9, s10])

merge(poly1,poly2)
