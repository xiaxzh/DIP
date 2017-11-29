import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from show import show, show3

def GaussionNoise(sourceImage, mean, segma, view=False):
    """GaussionNoise add a additive Gaussion Noise with respective
       Mean and Segma to a image

        Args:
            sourceImage:    original image
            mean:           respective mean of the Gaussion noise
            segma:          respective segma of the Gaussion noise
            view:           The flag to decided to show the result image
                            Set to False default

        Returns:
            retImage:       a image polluted by a Gaussion noise
    """
    retImage = sourceImage + segma*np.random.randn(sourceImage.shape[0], sourceImage.shape[1])+mean
    for x in range(retImage.shape[0]):
        for y in range(retImage.shape[1]):
            if retImage[x][y] > 255:
                retImage[x][y] = 255
            elif retImage[x][y] < 0:
                retImage[x][y] = 0
            else:
                retImage[x][y] = int(retImage[x][y])

    if view:
        show(sourceImage, retImage, "GaussionNoise")

    return retImage

def salt_pepperNoise(sourceImage, saltP=0, pepperP=0, view=False):
    """salt_pepperNoise add a possible Noise with respective
       saltP and pepperP to a image

        Args:
            sourceImage:    original image
            saltP:          possibility of salt noise
            pepperP:        possibility of pepper noise
            view:           The flag to decided to show the result image
                            Set to False default

        Returns:
            retImage:       a image polluted by a salt_pepper noise
    """
    retImage = np.zeros(sourceImage.shape, dtype=sourceImage.dtype)
    retImage[:,:] = sourceImage[:,:]

    if saltP != 0:
        count = int(retImage.size * saltP)
        xHigh = retImage.shape[0]-1
        yHigh = retImage.shape[1]-1
        for i in range(count):
            x = np.random.random_integers(0, xHigh)
            y = np.random.random_integers(0, yHigh)
            retImage[x][y] = 255

    if pepperP != 0:
        count = int(retImage.size * pepperP)
        xHigh = retImage.shape[0]-1
        yHigh = retImage.shape[1]-1
        for i in range(count):
            x = np.random.random_integers(0, xHigh)
            y = np.random.random_integers(0, yHigh)
            retImage[x][y] = 0

    if view:
       show(sourceImage, retImage, "salt_pepperNoise")

    return retImage

def start():
    sourceImage = np.array(Image.open('task_2.png'))[:,:,0]
    noiseImage = saltNoise(sourceImage, 0.2, 0.2)

if __name__ == '__main__':
    start()
