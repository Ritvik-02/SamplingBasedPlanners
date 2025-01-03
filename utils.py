import shapely
import shapely.plotting
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon, LineString
from queue import PriorityQueue

GRID_SIZE = 20
NUM_OBS = 8

def build_circle(center, radius):
    circle = shapely.geometry.Point(center[0],center[1]).buffer(radius)
    return circle

def build_oval(center, w, h, angle):
    circle = build_circle(center, 1)
    ellipse = shapely.affinity.scale(circle, w, h)
    oval = shapely.affinity.rotate(ellipse, angle)
    return oval

def build_rectangle(center, w, h, angle):
    coords = np.array([[center[0]-w/2, center[1]+h/2],
                       [center[0]+w/2, center[1]+h/2],
                       [center[0]+w/2, center[1]-h/2],
                       [center[0]-w/2, center[1]-h/2]])
    rec = shapely.geometry.Polygon(coords)
    rectangle = shapely.affinity.rotate(rec, angle)
    return rectangle

def get_random_map():
    shapes = ["circle", "oval", "rectangle"]

    obstacles = []
    choice = np.random.choice(shapes, NUM_OBS)
    for shape in choice:
        if shape == "circle":
            x = np.random.randint(-GRID_SIZE+5, GRID_SIZE-5)
            y = np.random.randint(-GRID_SIZE+5, GRID_SIZE-5)
            r = round(np.random.uniform(1,5),1)
            obstacles.append(build_circle([x,y],r))
        
        elif shape == "oval":
            x = np.random.randint(-GRID_SIZE+5, GRID_SIZE-5)
            y = np.random.randint(-GRID_SIZE+5, GRID_SIZE-5)
            w = round(np.random.uniform(0,6),1)
            h = round(np.random.uniform(0,6),1)
            a = np.random.randint(0, 90)
            obstacles.append(build_oval([x,y],w,h,a))
        
        elif shape == "rectangle":
            x = np.random.randint(-GRID_SIZE+5, GRID_SIZE-5)
            y = np.random.randint(-GRID_SIZE+5, GRID_SIZE-5)
            w = round(np.random.uniform(1,4),1)
            h = round(np.random.uniform(1,7),1)
            a = np.random.randint(0, 90)
            obstacles.append(build_rectangle([x,y],w,h,a))

    return obstacles

def sovle_map(points, obstacles):
    adj = {}
    for i in range(len(points)):
        neigbors = []
        for j in range(len(points)):
            if j == i:
                continue
            l = LineString([Point(points[i,0],points[i,1]), Point(points[j,0],points[j,1])])
            collide = False
            for obs in obstacles:
                if l.intersects(obs):
                    collide = True
                    break
            if not collide:
                neigbors.append(j)
        adj[i] = neigbors

    ret = sovle_map2(points, adj)

    return ret

def sovle_map2(points, adj):

    # solving using Dijkstra
    pqueue = PriorityQueue()  # cost, (curnode, path)
    visited = {0}
    ret = []
    pqueue.put((0, (0, [0])))

    while not pqueue.empty():
        (cost, (curidx,path)) = pqueue.get()

        if curidx == len(points)-1:
            ret = path
            break
        
        neighbors = adj[curidx]
        for nodeidx in neighbors:
            if nodeidx not in visited:
                visited.add(nodeidx)
                ctg = np.sqrt((points[curidx][0] - points[nodeidx][0])**2 + (points[curidx][1] - points[nodeidx][1])**2)
                pqueue.put((cost+ctg, (nodeidx, path+[nodeidx])))

    return ret

