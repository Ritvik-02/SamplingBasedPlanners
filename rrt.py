import shapely
import shapely.plotting
from shapely.geometry import Point, Polygon, LineString
import matplotlib.pyplot as plt
import numpy as np
from queue import PriorityQueue

from build_map import get_random_map

GRID_SIZE = 20
GOAL_BIAS = 0.1
STEP_SIZE = 5
GOAL_POINT = [GRID_SIZE,GRID_SIZE]

def sample_point():
    if np.random.rand() <= GOAL_BIAS:
        return GOAL_POINT
    while True:
        sample = [np.random.uniform(-GRID_SIZE,GRID_SIZE), np.random.uniform(-GRID_SIZE,GRID_SIZE)]
        p = Point(sample[0], sample[1])
        collide = False
        for obs in obstacles:
            if p.intersects(obs):
                collide = True
                break
        if not collide:
            return sample

def find_nearest(points, newpoint):
    dists = []
    for p in points:
        d = np.sqrt((p[0] - newpoint[0])**2 + (p[1] - newpoint[1])**2)
        dists.append(d)
    dists = np.array(dists)
    i = np.argmin(dists)
    theta = np.arctan2(newpoint[1]-points[i][1], newpoint[0]-points[i][0])
    newx = points[i][0] + STEP_SIZE*np.cos(theta)
    newy = points[i][1] + STEP_SIZE*np.sin(theta)
    
    return i, [newx, newy]

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

for i in range(10):
    newpoint = sample_point()
    i, addpoint = find_nearest(points, newpoint)
    l = LineString([Point(points[i][0],points[i][1]), Point(addpoint[0],addpoint[1])])
    collide = False
    for obs in obstacles:
        if l.intersects(obs):
            collide = True
            break
    if not collide:
        lines.append(l)
        points.append(addpoint)

# plot lines
for l in lines:
    shapely.plotting.plot_line(l, axs, color='black', add_points=False)

# plot points
points = np.array(points)
axs.scatter(points[:,0], points[:,1])

plt.show()


