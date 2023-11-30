#Plot the distribution of pixel values in all the 3 channels, alongside the original image.
def channel_distribution_plotter(img_array):

    img_array = img_array[:,:,:3] #Not considering the A channel, if it's a RGBA image.

    plt.subplot(2,2,1)
    plt.hist(img_array[:,:,2].ravel(),bins=256,color='red');
    plt.title("Red Channel")

    plt.subplot(2,2,2)
    plt.hist(img_array[:,:,1].ravel(),bins=256,color='green');
    plt.title("Green Channel")

    plt.subplot(2,2,3)
    plt.hist(img_array[:,:,1].ravel(),bins=256,color='blue');
    plt.title("Blue Channel")

    plt.subplot(2,2,4)
    plt.imshow(cv2.cvtColor(img_array,cv2.COLOR_BGR2RGB))
    plt.title("Original Image")

    plt.suptitle("Pixel values distribution in each channel\nx-axis: pixel values, y-axis: number of pixels")
    plt.tight_layout()

    plt.show()

channel_distribution_plotter(img)
