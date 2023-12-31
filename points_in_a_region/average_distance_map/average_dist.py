import numpy as np
import matplotlib.pyplot as plt
import math as mt

def distance_func(point1, point2):
    distance = mt.dist(point1,point2)
    return distance

def average_distance(point, array): #Returns the average distance of points (e.g. [1,2]) from all the points in array.
    distance = 0
    for i in range(len(array)):
        distance += distance_func(point,array[i])
    return distance/len(array)

def average_dist_func(points_count): #Ths square region is divided into many grids and average distance is calcualted for each such grid. This is then used for mapping the avg. dist.

    x_list = []
    y_list = []
    avg_dist_list = []

    randompoint_count = int(points_count)

    # points = np.random.uniform(-5,5, size = [2,randompoint_count])
    points = np.random.triangular(-5,0,5, size = [2,randompoint_count]) #Comment, uncomment as per need

    x_points = points[0]
    y_points = points[1]
    points = [ [points[0][i],points[1][i]] for i in range( int(points.shape[1]) ) ] 



    for i in range(-50,50):
        for j in range(-50,50):
            x = 10*i/100
            y = 10*j/100
            point = [x,y]
            dist = average_distance(point, points)
            x_list.append(x)
            y_list.append(y)
            avg_dist_list.append(dist)
    
    # fig, ax = plt.subplots(111)
    
    plt.scatter(x_list,y_list, c= avg_dist_list,
                cmap='jet'
                )
    plt.colorbar(pad = 0.01)
    plt.title("Average distance from random points in white")
    plt.scatter(x_points,y_points, s = 15, c='w');

average_dist_func(50)
