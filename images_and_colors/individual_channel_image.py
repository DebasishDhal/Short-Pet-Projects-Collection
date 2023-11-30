#This will take an image array and re-plot the image considering only one channel at once

def individual_channel_image(img_arr, channel= 'r', ax=None):
  img_arr = img_arr[:,:,0:3]
  
  if channel in ['r','red','Red']:
    plot_arr = img_arr[:,:,2]
    channel_name = 'Red'
    cmap = 'Reds'
  if channel in ['g','green','Green']:
    plot_arr = img_arr[:,:,1]
    channel_name = 'Green'
    cmap = 'Greens'
  if channel in ['b','blue','Blue']:
    plot_arr = img_arr[:,:,0]
    channel_name = 'Blue'
    cmap = 'Blues'
  
  if channel not in ['r','red','Red','g','green','Green','b','blue','Blue']:
    plot_arr = img_arr 
    channel_name = 'Original'

  if ax is None:
    if channel_name == 'Original':
      plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    else:
      plt.imshow(plot_arr)
      plt.colorbar(orientation= 'vertical', shrink = 0.7, pad = 0.01)
      plt.title('Image in the {} channel'.format(channel_name))
      plt.show()

  if ax is not None:
    if channel_name == 'Original':
      ax.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    else:
      plot = ax.imshow(plot_arr, cmap = cmap)
      plt.colorbar(plot, orientation= 'vertical', ax = ax)
      # plt.colorbar(orientiation= 'vertical', shrink = 0.7, pad = 0.1)
      ax.set_title('Image in the {} channel'.format(channel_name))



if __name__ == "__main__": 
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
  
  individual_channel_image(img, channel='r', ax=ax1)
  individual_channel_image(img, channel='g', ax=ax2)
