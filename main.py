from convex_hull import *
import pandas as pd
from numpy import abs, random
from scipy import stats
from timeit import default_timer # to calculate run time


start = default_timer()  # start timing

dataset_select = 1  # change dataset selection here

print("Importing dataset...")

# select dataset and preprocess accordingly
if dataset_select == 0:
    # uniform dataset of 10000 points (small)
    dataset = pd.DataFrame(random.uniform(0, 100, size=(10000, 2)), columns=['X', 'Y'])

elif dataset_select == 1:
    # gaussian dataset of 10000 points (small)
    dataset = pd.DataFrame(random.normal(0, 100, size=(10000, 2)), columns=['X', 'Y'])

elif dataset_select == 2:
    # vancouver crime dataset (medium)
    dataset = pd.read_csv('vancouver_crime.csv')
    dataset = dataset[dataset['HUNDRED_BLOCK'] != 'OFFSET TO PROTECT PRIVACY']  # keep only uncensored data
    dataset = dataset[['X', 'Y']]  # keep only X and Y columns
    dataset = dataset.drop_duplicates(subset='X')  # keep only points with unique x coordinates

elif dataset_select == 3:
    # philadelphia crime dataset (big)
    dataset = pd.read_csv('philadelphia_crime.csv')[['Lon', 'Lat']]
    dataset = dataset.dropna() # drop nan data
    dataset = dataset.drop_duplicates(subset='Lon')  # keep only points with unique x coordinates


dataset = dataset[(abs(stats.zscore(dataset)) < 3).all(axis=1)]  # remove outliers

# create points from dataset
points = set()
for idx, row in dataset.iterrows():
    points.add(Point(row[0], row[1]))

print('Done!')
print('Generating Convex Hull...')

convex_hull = convex_hull(points)  # create convex hull
plot_convex_hull(points,convex_hull)  # plot points and convex hull of the points

stop = default_timer()  # stop timer

print('Done!')
print(f'Runtime: {int((stop - start)/60)} minutes')

# import winsound
# duration = 500  # milliseconds
# freq = 440  # Hz
# winsound.Beep(freq, duration)

