import shapely
import shapely.plotting
import matplotlib.pyplot as plt
import numpy as np

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
            x = np.random.randint(-GRID_SIZE, GRID_SIZE)
            y = np.random.randint(-GRID_SIZE, GRID_SIZE)
            r = round(np.random.uniform(1,5),1)
            obstacles.append(build_circle([x,y],r))
        
        elif shape == "oval":
            x = np.random.randint(-GRID_SIZE, GRID_SIZE)
            y = np.random.randint(-GRID_SIZE, GRID_SIZE)
            w = round(np.random.uniform(0,6),1)
            h = round(np.random.uniform(0,6),1)
            a = np.random.randint(0, 90)
            obstacles.append(build_oval([x,y],w,h,a))
        
        elif shape == "rectangle":
            x = np.random.randint(-GRID_SIZE, GRID_SIZE)
            y = np.random.randint(-GRID_SIZE, GRID_SIZE)
            w = round(np.random.uniform(1,4),1)
            h = round(np.random.uniform(1,7),1)
            a = np.random.randint(0, 90)
            obstacles.append(build_rectangle([x,y],w,h,a))

    return obstacles

