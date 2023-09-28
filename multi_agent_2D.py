import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

#single_random_walk takes a single particle and plots its trajectory on the axis passed to it
def single_random_walk(iters, agent_number, ax, step_size = 1, random_seed = None):
    if random_seed: 
        random.seed(random_seed)

    iters = int(iters) #Because for some reason, the input from Gradio input components is in float
    directions = ['east', 'north', 'west', 'south']
    start_point = [0, 0]
    
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
    
    for _ in range(iters): #Key part that decides the trajectory of the agent
        new_step = step_determination()
        new_coordinate = step_addition(coordinate_list[-1], new_step)
        coordinate_list.append(new_coordinate)
    
    x = [i[0] for i in coordinate_list]
    y = [i[1] for i in coordinate_list]
    df = pd.DataFrame({'x':x,'y':y})
    
    #This to determine the markersize. This is is only a makeshift solution.
    base_marker_size = 10
    markersize = base_marker_size / np.sqrt(iters)

    #Plot on the axis passed, do not make a new figure.
    plot = ax.plot(x, y, marker='o', markersize=markersize, linestyle='None', alpha=0.5, label = 'Agent {i}'.format(i=agent_number+1))
    color = plot[0].get_color() #Get the color so that we can add label with proper colors later
    ax.plot(x[-1], y[-1], marker='o', markersize=5, color = 'black')
    ax.text(x[-1], y[-1], 'End {i}'.format(i=agent_number+1), color = 'black', alpha=1.0)
    
    return ax, df, color


#multi_agent_walk iteratively calls the single_random_walk function to plot different trajectories on the same axis.
def multi_agent_walk(agent_count, iters, step_size = 1, random_seed = None):
    assert agent_count >= 1, "Number of agents must be >= than 1"
    agent_count = int(agent_count)
    iters = int(iters)
    
    def displacement_calc(df):
        x1,y1 = df.iloc[0]
        x2,y2 = df.iloc[-1]
        return np.round(np.sqrt((x2-x1)**2 + (y2-y1)**2),1)

    if random_seed is None:
        random_seed = random.randint(0,1000000)

    random_seed = int(random_seed)
    assert type(random_seed) == int, "Random seed must be an integer"
    #Generates a list of random seeds for each agent
    random.seed(random_seed)
    random_numbers = [random.randint(0,100000) for _ in range(agent_count)]

    
    fig, ax = plt.subplots(figsize=(8,8))
    color_list = []

    for i in range(agent_count):
        if i == 0:
            ax, df, color = single_random_walk(iters=iters, ax=ax, step_size=step_size, agent_number=i, random_seed=random_numbers[i])
            color_list.append(color)
            
        else:
            ax, df_new, color = single_random_walk(iters=iters, ax=ax, step_size=step_size, agent_number=i, random_seed=random_numbers[i])
            df = pd.concat([df,df_new], axis=1)
            x_columns = [f'x{i}' for i in range(1, i+2)]
            y_columns = [f'y{i}' for i in range(1, i+2)]
            new_column_names = [val for pair in zip(x_columns, y_columns) for val in pair] 
            df.columns = new_column_names
            color_list.append(color)

    ax.plot(0,0, marker='X', markersize=8, color='black')
    ax.text(0, 0, 'Start (0,0)')

    plt.grid()
    plt.title('Random 2D Walk with {} agents\n #Steps = {}, Step size = {}, random seed = {}\nAll agents start from the origin'.format(agent_count, iters, step_size, random_seed))
    
    displacement = [displacement_calc(df.iloc[:,[i,i+1]]) for i in range(0,agent_count*2,2)]
    end_point = [(df.iloc[-1,i]) for i in range(0,agent_count*2,2)]

    end_point = [(df.iloc[-1,i], df.iloc[-1,i+1]) for i in range(0,agent_count*2,2)]
    
    agent_number = [i+1 for i in range(agent_count)]
    legend_df = pd.DataFrame({'#':agent_number, 'dis.':displacement, 'End Point':end_point, })
    info_box = legend_df.to_string(index=False)

    ax.text(0.01, 0.99, info_box, 
            transform=ax.transAxes, 
            verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.5)
           )
    
    lines = []
    for i in range(len(color_list)):
        lines.append(Line2D([0], [0], color=color_list[i], lw=9, linestyle=':'))

    labels = [f'Agent {i+1}' for i in range(len(color_list))]
    plt.legend(lines, labels, 
               loc='best', 
               handlelength=1.01, 
               handletextpad=0.21, 
               fancybox=True, 
               fontsize=10,
               )
    
    fig.canvas.draw()
    image_array = np.array(fig.canvas.renderer.buffer_rgba())
    csv_file = "2d_random_walk_coordinates.csv"
    df.to_csv(csv_file, index=False)
    
    try:
        return image_array, csv_file
    except:
        return image_array, None


# _, df = multi_agent_walk(agent_count=9, iters=1e5, step_size=1, random_seed=123);

            