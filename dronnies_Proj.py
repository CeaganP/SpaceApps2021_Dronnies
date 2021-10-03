import numpy as np
import matplotlib.pyplot as plt

from skimage import io
from sklearn.cluster import KMeans

def plot(img, title):
    """
    using the title and image provide plot the image and display it to the user with the custom title
    """
    plt.figure()
    plt.title(title)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def plot_quantize_special(img, k, t):
    """
    img - image being used, k is the number of clusters, t is the method the image is being modified by
    Perform quantization on the image using KMeans, modify the original
        image by the quantized image for different representations
    """
    shape = img.shape
    img_orig = img
    #create list of values
    img = img.reshape(shape[0] * shape[1], shape[2])

    km = KMeans(n_init=20, n_clusters=k).fit(img)

    #create an array that's the same length as predict, for each point in the data, the center it is closest to
    img = km.cluster_centers_[km.predict(img)]
    img = np.round(img, 0).astype(int)
    img = img.reshape(shape[0], shape[1], shape[2])

    if t==0:
        img = (img_orig * img);
    elif t==2:
            img = abs(img_orig - img);
    elif t==3:
            img = img_orig / img;


    plot(img, "K " + str(k) + "T " + str(t))

imgVeg = io.imread("vegetation.png")

def loadData(file):
    data = []
    width = 0
    height = 0
    with open(file) as file:
        for line in file:
            row = line.strip().split(",")
            width = len(row)
            for i in range(0, len(row)):
                floatval = np.float(row[i])
                if floatval != 99999 and floatval > 60:
                    data += [floatval, 0, 0, 0]
                elif floatval < 30:
                    data += [0, 0, floatval, 0]
                elif floatval < 60:
                    data += [floatval / 2, floatval / 2, floatval / 2, 0]
                else:
                    data += [0, 0, 0, 0]
                #data+=[nr[:-1]]

            height += 1
    data = np.array(data, np.uint8)
    data = np.round(data, 0)
    data = np.reshape(data, (height, width, 4)) #convert to image format

    return data


imgAerosol = loadData("aerosol.csv")
#img = imgAerosol + np.reshape(np.append(imgTrue, np.zeros((720, 1440))), (720, 1440, 4))
#img = imgAerosol + imgVeg
img = imgVeg + (imgAerosol)
img = np.clip(0,255,img)

plot(img, "TRUE+AEROSOL")

# image from file
#image2 = io.imread("monoxide.png")
#image3 = io.imread("temperature.png")
#image = image1 + image3

#plot(data, "AEROSOL")
#plot(image3, "image 3 - default")
#plot_quantize_other(image1, image3, 7)
