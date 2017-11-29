import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def possibility(img):

    # cnt represent times each number appear
    cnt = np.zeros(256, dtype=int)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            cnt[img[x][y]] = cnt[img[x][y]] + 1

    # p represent the possibility for each number
    p = [float(x/img.size) for x in cnt]

    return p


def print_hist(sourceImg, tarImg):
    
    sourceP = possibility(sourceImg)
    tarP = possibility(tarImg)

    plt.subplot(211)
    plt.bar(range(256), sourceP, label='Source Histogram')
    plt.title('Source(Top) And Target(Down) Histogram')    
    
    
    plt.subplot(212)
    plt.bar(range(256), tarP, label='Target Histogram')

    plt.show()

def equalize_hist(img):

    p = possibility(img)
    cdf = 0
    mapping = []

    # get the mapping relationship
    for each in range(256):
        cdf = cdf + p[each]
        mapping.append(np.floor(256*cdf))

    # change the grey level and generate the newImage
    newImg = np.zeros((img.shape[0], img.shape[1]), dtype=img.dtype)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            newImg[x][y] = mapping[img[x][y]]
    return newImg

def start():

    sourceImg = np.array(Image.open('22.png'))
    tarImg = equalize_hist(sourceImg)

    # show histogram
    print_hist(sourceImg, tarImg)

    # show two image
    plt.subplot(121)
    plt.imshow(sourceImg, cmap='gray')
    plt.title('SourceImage')

    plt.subplot(122)
    plt.imshow(tarImg, cmap='gray')
    plt.title('ResultImage')
    Image.fromarray(tarImg).save('Histogram.png')

    plt.show()
    print ('GoodBye!\n')
    return


if __name__ == '__main__':
    start()