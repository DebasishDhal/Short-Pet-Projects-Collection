def which_channel_dominates(img_arr, original_image_plot = 'yes', original_image_opacity = 0.3, channel_opacity = 0.7):
    cmap = mcolors.ListedColormap(['red', 'green', 'blue', 'white', 'black', 'gray'])
    img_arr = img_arr[:,:,:3]

    red_channel = img_arr[:,:,2]
    green_channel = img_arr[:,:,1]
    blue_channel = img_arr[:,:,0]


    print(np.max(red_channel), np.max(green_channel), np.max(blue_channel))

    if original_image_plot == 'yes':
        plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB), alpha=original_image_opacity)

    which_channel_dominates = np.zeros((img_arr.shape[0],img_arr.shape[1]))

    red_greater_green = np.greater(red_channel,green_channel)
    red_greater_blue = np.greater(red_channel,blue_channel)
    green_greater_blue = np.greater(green_channel,blue_channel)

    #Red is greatest if red is greater than green and blue

    which_channel_dominates[(red_greater_green & red_greater_blue)] = 1
    which_channel_dominates[green_greater_blue & (~red_greater_green)] = 2
    which_channel_dominates[~green_greater_blue & (~red_greater_blue)] = 3

    which_channel_dominates[(red_channel == green_channel) & (red_channel == blue_channel)] = 6
    which_channel_dominates[(red_channel == 255) & (blue_channel == 255) & (green_channel == 255)] = 4
    which_channel_dominates[(red_channel == 0) & (blue_channel == 0) & (green_channel == 0)] = 5

    print(np.unique(which_channel_dominates))

    #Map the color code to the image
    plot = plt.imshow(which_channel_dominates, cmap=cmap, alpha=channel_opacity)

    #Customize the ticks of the colorbar
    plt.colorbar(plot, orientation='vertical', 
                #  ticks=[1,2,3,4,5,6],
                ticks = [],
                label='Dominant Color Channel'
                )
    
    text = "Which channel dominates in the image below?\nWhite : R=G=B=255, Black : R=G=B=0\nGray : 0 < R=G=B< 255"
    plt.title(text)
    
