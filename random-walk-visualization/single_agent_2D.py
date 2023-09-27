import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd

def generate_random_walk(iters, step_size = 1, random_seed = None):
    # random.seed(random_seed)
    iters = int(iters)
    directions = ['east', 'north', 'west', 'south']
    start_point = [0, 0]

    if random_seed is None:
        random_seed = random.randint(1, 100000)
    else:
        random_seed = random_seed

    random.seed(random_seed)
    
    def distance_from_start(final_coord, start_coord, round_to=2):
        return round(np.sqrt((final_coord[0] - start_coord[0])**2 + (final_coord[1] - start_coord[1])**2), round_to)
    
    def step_addition(old_coord, step):
        return [sum(x) for x in zip(old_coord, step)]
    
    def step_determination():
        direction = random.choice(directions)
        if direction == 'east':
            return [1*step_size, 0]
        elif direction == 'west':
            return [-1*step_size, 0]
        elif direction == 'north':
            return [0, 1*step_size]
        elif direction == 'south':
            return [0, -1*step_size]
    
    coordinate_list = [start_point]
    
    for i in range(iters):
        new_step = step_determination()
        new_coordinate = step_addition(coordinate_list[-1], new_step)
        coordinate_list.append(new_coordinate)
    
    x = [i[0] for i in coordinate_list]
    y = [i[1] for i in coordinate_list]
    df = pd.DataFrame({'x':x,'y':y})
    csv_file = "2d_random_walk_coordinates.csv"
    df.to_csv(csv_file, index=False)
    
    fig, ax = plt.subplots(1)
    
    base_marker_size = 10
    markersize = base_marker_size / np.sqrt(iters)
    
    ax.plot(x, y, marker='o', markersize=markersize, linestyle='None')
    
    ax.plot(x[0], y[0], marker='o', markersize=5, color="red")
    ax.plot(x[-1], y[-1], marker='o', markersize=5, color="orange")
    
    ax.text(start_point[0], start_point[1], 'Start', color='red')
    ax.text(x[-1], y[-1], 'End', color='orange')
    
    x_max_index = x.index(max(x))
    x_min_index = x.index(min(x))
    y_max_index = y.index(max(y))
    y_min_index = y.index(min(y))
    
    info_text = 'Start point=' + str(start_point) + '\n'  +'End point=' + str([x[-1],y[-1]]) + '\n' +'Displacement =' + str(distance_from_start([x[-1], y[-1]], start_point)) + '\n' +'Max x = ' + str(max(x)) + '\n' + 'Min x = ' + str(min(x)) + '\n' + 'Max y = ' + str(max(y)) + '\n' + 'Min y = ' + str(min(y)) 
    ax.legend([info_text], loc='best', handlelength=0, handletextpad=0, fancybox=True, fontsize=8)
    
    plt.title( '2D Random Walk\nsteps=' + str(iters)+', step size='+ str(step_size)+ ', seed = '+str((random_seed)) )
    plt.grid()
    
    fig.canvas.draw()
    image_array = np.array(fig.canvas.renderer.buffer_rgba())

    
    return image_array, csv_file