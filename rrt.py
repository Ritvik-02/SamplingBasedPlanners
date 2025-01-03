import shapely
import shapely.plotting
from shapely.geometry import Point, Polygon, LineString
import matplotlib.pyplot as plt
import numpy as np
from queue import PriorityQueue

from utils import get_random_map, sovle_map2

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
count = 0
while True:
    newpoint = sample_point()
    i, addpoint = find_nearest(points, newpoint)
    l = LineString([Point(points[i][0],points[i][1]), Point(addpoint[0],addpoint[1])])
    collide = False
    for obs in obstacles:
        if l.intersects(obs):
            collide = True
            break
    if not collide:
        points.append(addpoint)
        count += 1
        lines.append((l,i,count))
        # distance to the goal point
        d = np.sqrt((GOAL_POINT[0] - addpoint[0])**2 + (GOAL_POINT[1] - addpoint[1])**2)
        if d <= STEP_SIZE:
            break

points.append(GOAL_POINT)
count += 1
lines.append((LineString([Point(points[-2][0],points[-2][1]), Point(GOAL_POINT[0],GOAL_POINT[1])]), len(points)-2, count))

# build adjacency list
adj = {}
for i in range(len(points)):
    adj[i] = []
for i in range(len(lines)):
    (l,j,c) = lines[i]
    adj[j].append(c)
    adj[c].append(j)

ret = sovle_map2(points, adj)

# plot lines
for (l,i,c) in lines:
    shapely.plotting.plot_line(l, axs, color='black', add_points=False)

pathLines = []
for i in range(1,len(ret)):
    l = LineString([Point(points[ret[i]][0],points[ret[i]][1]), Point(points[ret[i-1]][0],points[ret[i-1]][1])])
    pathLines.append(l)
for l in pathLines:
    shapely.plotting.plot_line(l, axs, color='red', add_points=False)

# plot points
points = np.array(points)
axs.scatter(points[:,0], points[:,1])

plt.show()


