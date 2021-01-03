from convex_hull import *

p1 = Point(-2, -2)
p2 = Point(-1, -5)
p3 = Point(-4, -9)
p4 = Point(-7, -5)
p5 = Point(-6, -1)
p6 = Point(5, 1)
p7 = Point(4, -5)
p8 = Point(2, -6)
p9 = Point(1, -4)
p10 = Point(2, -1)



poly3 = convex_hull((p1,p2,p3,p4,p5,p6,p7,p8,p9,p10))
plot_convex_hull((p1,p2,p3,p4,p5,p6,p7,p8,p9,p10),poly3)

