import shapely
import shapely.plotting
from shapely.geometry import Point, Polygon, LineString
import matplotlib.pyplot as plt
import numpy as np
from queue import PriorityQueue

from build_map import get_random_map

GRID_SIZE = 20
GOAL_BIAS = 0.1
GOAL_POINT = [GRID_SIZE,GRID_SIZE]

def sample_point():
    if np.random.rand() <= GOAL_BIAS:
        return GOAL_POINT
    while True:
        sample = [np.random.uniform(-GRID_SIZE,GRID_SIZE), np.random.uniform(-GRID_SIZE,GRID_SIZE)]
        p = Point(sample[0], sample[1])
        flag = True
        for obs in obstacles:
            if p.intersects(obs):
                flag = False
                break
        if flag:
            return sample

def find_nearest(points, newpoint):
    dists = []
    for p in points:
        d = np.sqrt((p[0] - newpoint[0])**2 + (p[1] - newpoint[1])**2)
        dists.append(d)
    dists = np.array(dists)
    return np.argmin(dists)

# get map
obstacles = get_random_map()

points = [[-GRID_SIZE,-GRID_SIZE]]




fig,axs = plt.subplots(1,1,figsize=(8,8))
axs.set_ylim(-GRID_SIZE,GRID_SIZE)
axs.set_xlim(-GRID_SIZE,GRID_SIZE)

# plot obstacles
for obs in obstacles:
    shapely.plotting.plot_polygon(obs, axs, color='black', add_points=False, alpha=0.5)

lines = []

newpoint = sample_point()
i = find_nearest(points, newpoint)
l = LineString([Point(points[i][0],points[i][1]), Point(newpoint[0],newpoint[1])])
lines.append(l)
points.append(newpoint)

# plot lines
for l in lines:
    shapely.plotting.plot_line(l, axs, color='black', add_points=False)

# plot points
points = np.array(points)
axs.scatter(points[:,0], points[:,1])

plt.show()


