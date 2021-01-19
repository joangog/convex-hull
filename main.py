from convex_hull import *
import pandas as pd
import timeit # to calculate run time

start = timeit.default_timer()  # start timing

# p1 = Point(-1, 0)
# p2 = Point(-2, 1)
# p3 = Point(-2, 0)
# p4 = Point(2, 0)
# p5 = Point(2, 1)
# p6 = Point(1, 1)
#
# poly3 = convex_hull((p1,p2,p3,p4,p5,p6))
# plot_convex_hull((p1,p2,p3,p4,p5,p6),poly3)

print('Importing file...')

# preproccess dataset
dataset = pd.read_csv('crime.csv').iloc[1:80]
dataset = dataset[dataset['HUNDRED_BLOCK'] != 'OFFSET TO PROTECT PRIVACY']  # keep only uncensored data
dataset = dataset[['X', 'Y']]  # keep only X and Y columns
dataset = dataset.drop_duplicates()  # keep only unique points
# norm_dataset=(dataset-dataset.mean())/dataset.std()  # normalize dataset
# dataset = norm_dataset

# create points from dataset
points = set()
for idx, row in dataset.iterrows():
    points.add(Point(row['X'], row['Y']))

print('Done!')
print('Generating Convex Hull...')

convex_hull = convex_hull(points)  # create convex hull
plot_convex_hull(points,convex_hull)  # plot points and convex hull of the points

stop = timeit.default_timer()  # stop timer

print('Done!')
print(f'Runtime: {int((stop - start)/60)} minutes')

# import winsound
# duration = 500  # milliseconds
# freq = 440  # Hz
# winsound.Beep(freq, duration)

