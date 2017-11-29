import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def process3(sourceImage, view=False):
    print ('Processing 3:')
    from changeMode import getRGB, HSI_Image, RGB_Image
    rImage, gImage, bImage = getRGB(sourceImage)

    from hw2_histogram import equalize_hist, print_hist
    hsiImage = HSI_Image(rImage, gImage, bImage)
    hsiImage[:,:,2] = equalize_hist(hsiImage[:,:,2])
    retImage = RGB_Image(hsiImage[:,:,0], hsiImage[:,:,1], hsiImage[:,:,2])

    if view:
        from show import show
        show(sourceImage, retImage, 'Convert from HSI to RGB')

def process2(sourceImage, view=False):
    print ('Processing 2:')
    from changeMode import getRGB
    rImage, gImage, bImage = getRGB(sourceImage)

    new_histogram = np.zeros(rImage.shape, dtype=int)
    for x in range(new_histogram.shape[0]):
        for y in range(new_histogram.shape[1]):
            new_histogram[x][y] = int((rImage[x][y] + gImage[x][y] + bImage[x][y])/3)

    # get the mapping function
    from hw2_histogram import possibility
    p = possibility(new_histogram)
    cdf = 0
    mapping = []
    for each in range(256):
        cdf = cdf + p[each]
        mapping.append(np.floor(256*cdf))

    retImage = np.zeros(sourceImage.shape, dtype=sourceImage.dtype)
    retImage[:,:,:] = sourceImage[:,:,:]
    for x in range(retImage.shape[0]):
        for y in range(retImage.shape[1]):
            for k in range(retImage.shape[2]):
                retImage[x][y][k] = mapping[sourceImage[x][y][k]]
    if view:
        from show import show
        show(sourceImage, retImage, "average histogram")

def process1(sourceImage, view=False):
    print ('Processing 1:')
    from changeMode import getRGB
    rImage, gImage, bImage = getRGB(sourceImage)

    from hw2_histogram import equalize_hist, print_hist
    retImage = np.zeros(sourceImage.shape, dtype=sourceImage.dtype)
    retImage[:,:,0] = equalize_hist(rImage)
    retImage[:,:,1] = equalize_hist(gImage)
    retImage[:,:,2] = equalize_hist(bImage)

    if view:
        from show import show
        show(sourceImage, retImage, "respective histogram")

def start():
    sourceImage = np.array(Image.open('../img/22.png'))
    process1(sourceImage, True)
    process2(sourceImage, True)
    process3(sourceImage, True)



if __name__ == '__main__':
    start()
