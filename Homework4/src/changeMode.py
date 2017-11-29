import numpy as np
from PIL import Image

def RGB_Image(hImage, sImage, iImage, view=False):
    """Change the color mode from HSI to RGB

    Given a HSI color mode image, and change it into GRB color
    mode image

    Args:
        hImage: The H tunnel of the HSI color mode image
                0.0 <= hImage's items <= 1.0
        sImage: The S tunnel of the HSI color mode image
                0.0 <= sImage's items <= 1.0
        iImage: The I tunnel of the HSI color mode image
                0.0 <= iImage's items <= 1.0
        view:   The flag to decided to show the result image
                Set to False default

    Returns:
        retImage: The processed RGB color mode image
    """
    rImage = np.zeros(hImage.shape, dtype=float)
    gImage = np.zeros(hImage.shape, dtype=float)
    bImage = np.zeros(hImage.shape, dtype=float)

    normal_hImage = np.zeros(hImage.shape, dtype=float)
    normal_sImage = np.zeros(hImage.shape, dtype=float)
    normal_iImage = np.zeros(hImage.shape, dtype=float)

    normal_hImage = hImage/255*(2*np.pi)
    normal_sImage = sImage/255
    normal_iImage = iImage/255

    import math
    for x in range(normal_hImage.shape[0]):
        for y in range(normal_hImage.shape[1]):
            if normal_hImage[x][y] < 2*np.pi/3:
                bImage[x][y] = normal_iImage[x][y]*(1-normal_sImage[x][y])
                numerator = normal_sImage[x][y]*math.cos(normal_hImage[x][y])
                denominator = math.cos(np.pi/3-normal_hImage[x][y])
                rImage[x][y] = normal_iImage[x][y]*(1+numerator/denominator)
                gImage[x][y] = 3*normal_iImage[x][y]-(rImage[x][y]+bImage[x][y])

            elif normal_hImage[x][y] < 4*np.pi/3:
                numerator = normal_sImage[x][y]*math.cos(normal_hImage[x][y]-2*np.pi/3)
                denominator = math.cos(np.pi-normal_hImage[x][y])
                rImage[x][y] = normal_iImage[x][y]*(1-normal_sImage[x][y])
                gImage[x][y] = normal_iImage[x][y]*(1+numerator/denominator)
                bImage[x][y] = 3*normal_iImage[x][y]-(rImage[x][y] + gImage[x][y])
            elif normal_hImage[x][y] < 2*np.pi:
                gImage[x][y] = normal_iImage[x][y]*(1-normal_sImage[x][y])
                numerator = normal_sImage[x][y]*math.cos(normal_hImage[x][y]-4*np.pi/3)
                denominator = math.cos(5*np.pi/3-normal_hImage[x][y])
                bImage[x][y] = normal_iImage[x][y]*(1+numerator/denominator)
                rImage[x][y] = 3*normal_iImage[x][y] - (gImage[x][y] + bImage[x][y])


    retImage = np.zeros((hImage.shape[0], hImage.shape[1], 3), dtype=np.uint8)
    retImage[:,:,0] = rImage[:,:]*255
    retImage[:,:,1] = gImage[:,:]*255
    retImage[:,:,2] = bImage[:,:]*255

    if view:
        plt.subplot(131)
        plt.title('R tunnel Image')
        plt.imshow(rImage, cmap='gray')

        plt.subplot(132)
        plt.title('G tunnel Image')
        plt.imshow(gImage, cmap='gray')

        plt.subplot(133)
        plt.title('B tunnel Image')
        plt.imshow(bImage, cmap='gray')
        plt.show()

    return retImage

def HSI_Image(rImage, gImage, bImage, view=False):
    """Change the color mode from RGB to HSI

    Given a RGB color mode image, and change it into HSI color
    mode image

    Args:
        rImage: The R tunnel of the RGB color mode image
                0.0 <= rImage's items <= 1.0
        gImage: The G tunnel of the RGB color mode image
                0.0 <= gImage's items <= 1.0
        bImage: The B tunnel of the RGB color mode image
                0.0 <= bImage's items <= 1.0
        view:   The flag to decided to show the result image
                Set to False default

    Returns:
        retImage: The processed HSI color mode image
    """
    hImage = np.zeros((rImage.shape[0], rImage.shape[1]), dtype=float)
    sImage = np.zeros((rImage.shape[0], rImage.shape[1]), dtype=float)
    iImage = np.zeros((rImage.shape[0], rImage.shape[1]), dtype=float)

    normal_rImage = rImage/255
    normal_gImage = gImage/255
    normal_bImage = bImage/255

    iImage = (normal_rImage+normal_gImage+normal_bImage)/3

    import math
    for x in range(rImage.shape[0]):
        for y in range(rImage.shape[1]):
            den = (normal_rImage[x][y]+normal_gImage[x][y]+normal_bImage[x][y])
            if den == 0.0:
                den = np.spacing(1e6)
            sImage[x][y] = 1-3/den*min([normal_rImage[x][y], normal_gImage[x][y], normal_bImage[x][y]])
            if sImage[x][y] == 0.0:
                hImage[x][y] = 0.0
            else:
                numerator = 0.5*((normal_rImage[x][y]-normal_gImage[x][y])+(normal_rImage[x][y]-normal_bImage[x][y]))
                denominator = np.sqrt((normal_rImage[x][y]-normal_gImage[x][y])**2 + (normal_rImage[x][y]-normal_bImage[x][y])*(normal_gImage[x][y]-normal_bImage[x][y]))
                theta = np.arccos(numerator/(denominator+np.spacing(1e6)))
                hImage[x][y] = theta/(2*np.pi) if normal_bImage[x][y] <= normal_gImage[x][y] else (2*np.pi-theta)/(2*np.pi)

    retImage = np.zeros((rImage.shape[0], rImage.shape[1], 3), dtype=int)
    retImage[:,:,0] = hImage[:,:]*255
    retImage[:,:,1] = sImage[:,:]*255
    retImage[:,:,2] = iImage[:,:]*255

    if view:
        plt.subplot(131)
        plt.title('H tunnel Image')
        plt.imshow(hImage, cmap='gray')

        plt.subplot(132)
        plt.title('S tunnel Image')
        plt.imshow(sImage, cmap='gray')

        plt.subplot(133)
        plt.title('I tunnel Image')
        plt.imshow(iImage, cmap='gray')
        plt.show()

    return retImage

def getRGB(sourceImage):
    """get the R, G, B tunnel from a colorful Image

    Args:
        sourceImage: A colorful Image instance

    Returns:
        R tunnel, G tunnel, B tunnel of the sourceImage
    """
    rImage = np.zeros((sourceImage.shape[0], sourceImage.shape[1]), dtype=int)
    gImage = np.zeros((sourceImage.shape[0], sourceImage.shape[1]), dtype=int)
    bImage = np.zeros((sourceImage.shape[0], sourceImage.shape[1]), dtype=int)

    rImage[:,:] = sourceImage[:,:,0]
    gImage[:,:] = sourceImage[:,:,1]
    bImage[:,:] = sourceImage[:,:,2]
    return rImage, gImage, bImage
