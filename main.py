import argparse
from timeit import default_timer  # to calculate run time
import pandas as pd
import numpy as np
from numpy import random
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt
import convex_hull_3d as ch3d
import convex_hull_2d as ch2d


# generate circle / sphere
def sample_spherical(npoints, ndim=3):
    vec = np.random.randn(ndim, npoints)
    vec /= np.linalg.norm(vec, axis=0)
    return vec

# #  import arguments
# parser = argparse.ArgumentParser()
# parser.parse_args()

dim_select = 3  # dimension selection
dataset_select = 0 # dataset selection

print("Importing dataset...")

# select dataset and preprocess accordingly
if dim_select == 2:
    if dataset_select == 0:
        # uniform dataset of 10000 points (small)
        dataset = pd.DataFrame(random.uniform(0, 100, size=(10000, 2)), columns=['x', 'y'])
    elif dataset_select == 1:
        # gaussian dataset of 10000 points (small)
        dataset = pd.DataFrame(random.normal(0, 100, size=(10000, 2)), columns=['x', 'y'])
    elif dataset_select == 2:
        # vancouver crime dataset (medium)
        dataset = pd.read_csv('data/vancouver_crime.csv')
        dataset = dataset[dataset['HUNDRED_BLOCK'] != 'OFFSET TO PROTECT PRIVACY']  # keep only uncensored data
        dataset = dataset[['X', 'Y']]  # keep only X and Y columns
        dataset = dataset.drop_duplicates(subset='X')  # keep only points with unique x coordinates
    elif dataset_select == 3:
        # philadelphia crime dataset (big)
        dataset = pd.read_csv('data/philadelphia_crime.csv')[['Lon', 'Lat']]
        dataset = dataset.dropna() # drop nan data
        dataset = dataset.drop_duplicates(subset='Lon')  # keep only points with unique x coordinates
    elif dataset_select == 4:
        # covid dataset
        dataset = pd.read_csv('data/covid.csv')[['longitude', 'latitude']]
        dataset = dataset.dropna()  # drop nan data
        dataset = dataset.drop_duplicates(subset='longitude')  # keep only points with unique x coordinates
    else:
        raise ValueError('Wrong dataset number')
elif dim_select == 3:
    if dataset_select == 0:
        dataset = pd.DataFrame(columns=['x', 'y', 'z'])
        dataset = dataset.append({'x': 0.1, 'y': -0.2, 'z': 0.2}, ignore_index=True)
        dataset = dataset.append({'x': 0.3, 'y': 0.1, 'z': 0.3}, ignore_index=True)
        dataset = dataset.append({'x': 0.0, 'y': 0.5, 'z': 0.0}, ignore_index=True)
        dataset = dataset.append({'x': 0.5, 'y': 0.0, 'z': 1.0}, ignore_index=True)
        dataset = dataset.append({'x': 0.4, 'y': 0.2, 'z': 0.5},ignore_index=True)
        dataset = dataset.append({'x': 0.2, 'y': 0.7, 'z': 0.7}, ignore_index=True)
        dataset = dataset.append({'x': 0.9, 'y': 0.5, 'z': 0.2}, ignore_index=True)
        # dataset = dataset.append({'x': 0.0, 'y': 0.0, 'z': 0.0}, ignore_index=True)
        # dataset = dataset.append({'x': 0.2, 'y': 0.2, 'z': 0.0}, ignore_index=True)
        # dataset = dataset.append({'x': 0.9, 'y': 0.0, 'z': 0.0}, ignore_index=True)
        # dataset = dataset.append({'x': 0.9, 'y': 0.0, 'z': 0.0}, ignore_index=True)
    elif dataset_select == 1:
        dataset = pd.DataFrame(random.uniform(0, 100, size=(50, 3)), columns=['x', 'y', 'z'])
    elif dataset_select == 2:
        data = np.transpose(sample_spherical(20))
        dataset = pd.DataFrame(data=data, columns=['x', 'y', 'z'])
        print(0)
    else:
        raise ValueError('Wrong dataset number.')
else:
    raise ValueError('Wrong dimension number. Select 2 or 3.')

# dataset = dataset[(abs(stats.zscore(dataset)) < 3).all(axis=1)]  # remove outliers

# create points from dataset
points = set()
if dim_select == 2:
    for idx, row in dataset.iterrows():
        points.add(ch2d.Point(row[0], row[1]))
elif dim_select == 3:
    for idx, row in dataset.iterrows():
        points.add(ch3d.Point(row[0], row[1], row[2]))

print(f'Done!')
print(f'Total points: {len(points)}\n')
print('Generating Convex Hull...')

# create convex hull
start = default_timer()  # start timing
if dim_select == 2:
    convex_hull = ch2d.convex_hull(points)
elif dim_select == 3:
    convex_hull = ch3d.convex_hull(points)
stop = default_timer()  # stop timer

# plot points and convex hull of the points
if dim_select == 2:
    ch2d.plot_convex_hull(points,convex_hull)
elif dim_select == 3:
    matplotlib.use("TkAgg")
    plt.ion()
    ch3d.plot_convex_hull(points, convex_hull)
    plt.pause(0)

print('Done!')
print(f'Runtime: {int((stop - start)/3600)} seconds\n')

# import winsound
# duration = 500  # milliseconds
# freq = 440  # Hz
# winsound.Beep(freq, duration)

