import convex_hull_3d as ch3d
import convex_hull_2d as ch2d
import pandas as pd
from numpy import random
from scipy import stats
from timeit import default_timer # to calculate run time
import argparse

#  import arguments
parser = argparse.ArgumentParser()
parser.parse_args()


start = default_timer()  # start timing

dataset = pd.DataFrame(columns=['x', 'y', 'z'])
dataset = dataset.append({'x': 0, 'y': 0, 'z': 0},ignore_index=True)
dataset = dataset.append({'x': 0, 'y': 0, 'z': 1},ignore_index=True)
dataset = dataset.append({'x': 0, 'y': 1, 'z': 0},ignore_index=True)
dataset = dataset.append({'x': 1, 'y': 0, 'z': 0},ignore_index=True)

# create points from dataset
points = []
for idx, row in dataset.iterrows():
    points.append(ch3d.Point(row[0],row[1],row[2]))

poly = ch3d.convex_hull(points)
poly.plot()

# dataset_select = 1  # change dataset selection here
#
# print("Importing dataset...")
#
# # select dataset and preprocess accordingly
# if dataset_select == 0:
#     # uniform dataset of 10000 points (small)
#     dataset = pd.DataFrame(random.uniform(0, 100, size=(10000, 2)), columns=['x', 'y'])
#
# elif dataset_select == 1:
#     # gaussian dataset of 10000 points (small)
#     dataset = pd.DataFrame(random.normal(0, 100, size=(10000, 2)), columns=['x', 'y'])
#
# elif dataset_select == 2:
#     # vancouver crime dataset (medium)
#     dataset = pd.read_csv('vancouver_crime.csv')
#     dataset = dataset[dataset['HUNDRED_BLOCK'] != 'OFFSET TO PROTECT PRIVACY']  # keep only uncensored data
#     dataset = dataset[['X', 'Y']]  # keep only X and Y columns
#     dataset = dataset.drop_duplicates(subset='X')  # keep only points with unique x coordinates
#
# elif dataset_select == 3:
#     # philadelphia crime dataset (big)
#     dataset = pd.read_csv('philadelphia_crime.csv')[['Lon', 'Lat']]
#     dataset = dataset.dropna() # drop nan data
#     dataset = dataset.drop_duplicates(subset='Lon')  # keep only points with unique x coordinates
#
#
# dataset = dataset[(abs(stats.zscore(dataset)) < 3).all(axis=1)]  # remove outliers
#
# # create points from dataset
# points = set()
# for idx, row in dataset.iterrows():
#     points.add(Point(row[0], row[1]))
#
# print('Done!')
# print('Generating Convex Hull...')
#
# convex_hull = convex_hull_2d(points)  # create convex hull
# plot_convex_hull(points,convex_hull)  # plot points and convex hull of the points

stop = default_timer()  # stop timer

print('Done!')
print(f'Runtime: {int((stop - start)/60)} minutes')

# import winsound
# duration = 500  # milliseconds
# freq = 440  # Hz
# winsound.Beep(freq, duration)

