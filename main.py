from timeit import default_timer  # to calculate run time
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
import matplotlib
import matplotlib.pyplot as plt
import convex_hull_3d as ch3d
import convex_hull_2d as ch2d

# parameters
dim_select = 2  # dimension selection (2 or 3)
dataset_select = 0  # dataset selection (2D: [0-4], 3D: [0-2])
percent_select = 100  # percentage of dataset to use
save_3d_gif = False  # set to True to save an animated gif of the 3D convex hull

print("Importing dataset...")

# select dataset
if dim_select == 2:
    if dataset_select == 0:
        # uniform dataset of 10000 points (very small)
        dataset_name = "2D Uniform Dataset"
        dataset = pd.DataFrame(np.random.uniform(0, 1, size=(10000, 2)), columns=['x', 'y'])
    elif dataset_select == 1:
        # gaussian dataset of 100000 points (small)
        dataset_name = "2D Gaussian Dataset"
        dataset = pd.DataFrame(np.random.normal(0, 1, size=(100000, 2)), columns=['x', 'y'])
    elif dataset_select == 2:
        # vancouver crime dataset (medium)
        dataset_name = "2D Vancouver Crime Dataset"
        dataset = pd.read_csv('data/vancouver_crime.csv')
        dataset = dataset[dataset['HUNDRED_BLOCK'] != 'OFFSET TO PROTECT PRIVACY']  # keep only uncensored data
        dataset = dataset[['X', 'Y']]  # keep only X and Y columns
        dataset = dataset[(abs(stats.zscore(dataset)) < 3).all(axis=1)]  # remove outliers (there is a random point out of map)
    elif dataset_select == 3:
        # philadelphia crime dataset (big)
        dataset_name = "2D Philadelphia Crime Dataset"
        dataset = pd.read_csv('data/philadelphia_crime.csv')[['Lon', 'Lat']]
    elif dataset_select == 4:
        # covid dataset (huge)
        dataset_name = "2D Covid Dataset"
        dataset = pd.read_csv('data/covid.csv')[['longitude', 'latitude']]
    else:
        raise ValueError('Wrong dataset number')
    dataset.columns = ['x', 'y']  # rename columns

elif dim_select == 3:
    if dataset_select == 0:
        dataset_name = "3D Handmade Dataset"
        dataset = pd.DataFrame(columns=['x', 'y', 'z'])
        # convex hull points
        dataset = dataset.append({'x': 0.5, 'y': 0.5, 'z': 0.5}, ignore_index=True)
        dataset = dataset.append({'x': 0.5, 'y': 0.5, 'z': -0.5}, ignore_index=True)
        dataset = dataset.append({'x': 0.5, 'y': -0.5, 'z': 0.5}, ignore_index=True)
        dataset = dataset.append({'x': 0.5, 'y': -0.5, 'z': -0.5}, ignore_index=True)
        dataset = dataset.append({'x': -0.5, 'y': 0.5, 'z': 0.5},ignore_index=True)
        dataset = dataset.append({'x': -0.5, 'y': 0.5, 'z': -0.5}, ignore_index=True)
        dataset = dataset.append({'x': -0.5, 'y': -0.5, 'z': 0.5}, ignore_index=True)
        dataset = dataset.append({'x': -0.5, 'y': -0.5, 'z': -0.5}, ignore_index=True)
        dataset = dataset.append({'x': 0, 'y': 0, 'z': 0.75}, ignore_index=True)
        dataset = dataset.append({'x': 0, 'y': 0, 'z': -0.75}, ignore_index=True)
        dataset = dataset.append({'x': 0, 'y': 0.75, 'z': 0}, ignore_index=True)
        dataset = dataset.append({'x': 0, 'y': -0.75, 'z': 0}, ignore_index=True)
        dataset = dataset.append({'x': 0.75, 'y': 0, 'z': 0}, ignore_index=True)
        dataset = dataset.append({'x': -0.75, 'y': 0, 'z': 0}, ignore_index=True)
        # inner points
        dataset = dataset.append({'x': 0.3, 'y': 0.1, 'z': 0.3}, ignore_index=True)
        dataset = dataset.append({'x': -0.1, 'y': -0.3, 'z': -0.3}, ignore_index=True)
        dataset = dataset.append({'x': 0.3, 'y': -0.3, 'z': 0.1}, ignore_index=True)
        dataset = dataset.append({'x': -0.3, 'y': -0.1, 'z': -0.3}, ignore_index=True)
        dataset = dataset.append({'x': 0.1, 'y': 0.3, 'z': 0.3}, ignore_index=True)
        dataset = dataset.append({'x': -0.3, 'y': 0.3, 'z': -0.1}, ignore_index=True)
    elif dataset_select == 1:
        dataset_name = "3D Uniform Dataset"
        dataset = pd.DataFrame(np.random.uniform(0, 1, size=(50, 3)), columns=['x', 'y', 'z'])
    elif dataset_select == 2:
        dataset_name = "3D Gaussian Dataset"
        dataset = pd.DataFrame(np.random.uniform(0, 1, size=(200, 3)), columns=['x', 'y', 'z'])
    else:
        raise ValueError('Wrong dataset number.')
    dataset.columns = ['x', 'y', 'z']  # rename columns
else:
    raise ValueError('Wrong dimension number. Select 2 or 3.')

# preprocess
dataset = dataset.dropna() # drop nan data
dataset = dataset[:int(len(dataset)*percent_select/100)]  # select percentage of dataset
dataset = pd.DataFrame(MinMaxScaler().fit_transform(dataset.values))  # scale data
if dataset_select > 1 and dim_select == 2:  # if dataset is from a downloaded 2D dataset
    np.random.seed(0)  # make the random seed the same for every run
    dataset = dataset + np.random.normal(0,0.0001,(len(dataset),dim_select)) # add tiny gaussian noise to data to avoid points with the same y coordinate (bad for x-axis slices)

# create points from dataset
points = set()
if dim_select == 2:
    for idx, row in dataset.iterrows():
        points.add(ch2d.Point(row[0], row[1]))
elif dim_select == 3:
    for idx, row in dataset.iterrows():
        points.add(ch3d.Point(row[0], row[1], row[2]))

print('Done!')
print(f'Dataset: {dataset_name}')
print(f'Total points: {len(points)}\n')
print('Generating Convex Hull...')

# create convex hull
start = default_timer()  # start timing
if dim_select == 2:
    convex_hull = ch2d.convex_hull(points)
elif dim_select == 3:
    convex_hull = ch3d.convex_hull(points)
stop = default_timer()  # stop timer

print('Done!')
print(f'Algorithm Runtime: {round(stop - start,2)} seconds\n')

print('Printing Convex Hull...')

# plot points and convex hull of the points
if dim_select == 2:
    ch2d.plot_convex_hull(points,convex_hull, title=dataset_name)
elif dim_select == 3:
    matplotlib.use("TkAgg")
    plt.ion()
    fig, ax = ch3d.plot_convex_hull(points, convex_hull, title=dataset_name)
    if save_3d_gif:
        ch3d.save_convex_hull_gif(fig, ax)
    plt.pause(0)

print('Done!')

# Play sound when done
# import winsound
# duration = 500  # milliseconds
# freq = 440  # Hz
# winsound.Beep(freq, duration)

