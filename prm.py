import shapely
import shapely.plotting
from shapely.geometry import Point, Polygon, LineString
import matplotlib.pyplot as plt
import numpy as np
from queue import PriorityQueue

from utils import get_random_map, sovle_map

GRID_SIZE = 20
NUM_SAMPLES = 150

# get map
obstacles = get_random_map()

plt.ion()
fig,axs = plt.subplots(1,1,figsize=(8,8))
axs.set_ylim(-GRID_SIZE,GRID_SIZE)
axs.set_xlim(-GRID_SIZE,GRID_SIZE)

# plot obstacles
for obs in obstacles:
    shapely.plotting.plot_polygon(obs, axs, color='black', add_points=False, alpha=0.5)
plt.draw()
plt.pause(2)

# sample points
scat = axs.scatter([],[])
points = np.random.uniform(-GRID_SIZE, GRID_SIZE, (NUM_SAMPLES, 2))
scat.set_offsets(points)
plt.draw()
plt.pause(2)

# remove invalid points
invalid = []
for i in range(NUM_SAMPLES):
    p = Point(points[i,0], points[i,1])
    for obs in obstacles:
        if p.intersects(obs):
            invalid.append(i)
            break
points = np.delete(points, invalid, axis=0)
points = np.vstack([np.array([-GRID_SIZE,-GRID_SIZE]), points, np.array([GRID_SIZE,GRID_SIZE])])
scat.set_offsets(points)
plt.draw()
plt.pause(2)

ret = sovle_map(points, obstacles)

# draw path
lines = []
for i in range(1,len(ret)):
    l = LineString([Point(points[ret[i],0],points[ret[i],1]), Point(points[ret[i-1],0],points[ret[i-1],1])])
    lines.append(l)

# plot lines
for l in lines:
    shapely.plotting.plot_line(l, axs, color='black', add_points=False)

plt.ioff()
plt.show()


