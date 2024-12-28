import shapely
import shapely.plotting
import matplotlib.pyplot as plt
import numpy as np

from build_map import get_random_map

GRID_SIZE = 20
NUM_SAMPLES = 100

# get map
obstacles = get_random_map()

# sample points
points = np.random.uniform(-GRID_SIZE, GRID_SIZE, (NUM_SAMPLES, 2))

# remove invalid points
invalid = []
for i in range(NUM_SAMPLES):
    p = shapely.geometry.Point(points[i,0], points[i,1])
    for obs in obstacles:
        if p.intersects(obs):
            invalid.append(i)
            break
# print(points)
points = np.delete(points, invalid, axis=0)
# print(points)

fig,axs = plt.subplots(1,1,figsize=(8,8))

# plot obstacles
for obs in obstacles:
    shapely.plotting.plot_polygon(obs, axs, color='black', add_points=False, alpha=0.5)

# plot samples
axs.scatter(points[:,0], points[:,1])

axs.set_ylim(-GRID_SIZE,GRID_SIZE)
axs.set_xlim(-GRID_SIZE,GRID_SIZE)
plt.show()


