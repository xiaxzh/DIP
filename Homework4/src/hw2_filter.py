import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 
# change the entengImg's dtype from int to float
# change the output of filter2d's dtype from int to float 
# 

def extending(img, filterHeight, filterWidth):
    # extending image
    extendImg = np.zeros((img.shape[0]+(filterHeight-1)*2, img.shape[1]+(filterWidth-1)*2), dtype=float)
    height = extendImg.shape[0]
    width = extendImg.shape[1]
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]

    # extend entity
    extendImg[filterHeight-1:filterHeight-1+imgHeight, filterWidth-1:filterWidth-1+imgWidth] = img

    # extend horizontal border
    extendImg[0:filterHeight-1, filterWidth-1:width-(filterWidth-1)] = img[0, :]
    extendImg[filterHeight-1+img.shape[0]:height, filterWidth-1:width-(filterWidth-1)] = img[img.shape[0]-1, :]

    # extend vetical border
    for i in range(filterHeight-1):
        extendImg[filterHeight-1:filterHeight-1+imgHeight, i] = img[:, 0]
        extendImg[filterHeight-1:filterHeight-1+imgHeight, width-(filterWidth-1)+i] = img[:, img.shape[1]-1]

    # extend cornor
    for i in range(filterHeight-1):
        for j in range(filterWidth-1):
            extendImg[0+i][0+j] = img[0][0]
            extendImg[filterHeight-1+imgHeight+i][0+j] = img[imgHeight-1][0]
            extendImg[0+i][filterWidth-1+imgWidth+j] = img[0][imgWidth-1]
            extendImg[filterHeight-1+imgHeight+i][filterWidth-1+imgWidth+j] = img[imgHeight-1][imgWidth-1]

    return extendImg

def filter2d(img, filter):
    
    # get the extendingImage
    extendImg = extending(img, filter.shape[0], filter.shape[1])
    
    # print ('After extending')
    # print (extendImg)

    height = extendImg.shape[0]
    width = extendImg.shape[1]
    filterHeight = filter.shape[0]
    filterWidth = filter.shape[1]

    # calculating
    correlateImg = np.zeros((height, width), dtype=extendImg.dtype)
    for x in range(height-(filterHeight-1)):
        for y in range(width-(filterWidth-1)):
            sum = 0
            for j in range(filterHeight):
                for k in range(filterWidth):
                    sum = sum + filter[j][k]*extendImg[x+j][y+k]
            correlateImg[x+int((filterHeight-1)/2)][y+int((filterWidth-1)/2)] = sum
    # print ('After calculating')
    # print (correlateImg)

    import math
    # cutting
    tarImg = np.zeros((img.shape[0], img.shape[1]), dtype=int)
    for x in range(tarImg.shape[0]):
        for y in range(tarImg.shape[1]):
            if math.isinf(correlateImg[x+filterHeight-1][y+filterWidth-1]):
                tarImg[x][y] = 255
            else:
                tarImg[x][y] = int((correlateImg[x+filterHeight-1][y+filterWidth-1]))
    # print ('After cutting')
    # print (tarImg)

    return tarImg


def highBoostFiltering(img):
    
    # print ('Before HighBoostFiltering')
    # print (img)
    
    # get the smoothFilteringImage and choose the 3*3 mask's result
    smoothImg = smoothFiltering(img)[0]

    # calculating
    g = np.zeros((img.shape[0], img.shape[1]), dtype=int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            f = int(img[i][j])
            f1 = int(smoothImg[i][j])
            g[i][j] = 2*(f - f1)+f
    
    # calibration
    final = np.zeros((img.shape[0], img.shape[1]), dtype=img.dtype)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if g[i][j] < 0:
                final[i][j] = 0
            elif g[i][j] > 255:
                final[i][j] = 255
            else:
                final[i][j] = g[i][j]
    

    # print ('After HighBoostFiltering')
    # print (final)

    return final


def LaplaceFiltering(img):

    # print ('Before LaplaceFiltering')
    # print (img)

    g = filter2d(img, np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=int))

    # calculating
    retImg = np.zeros((img.shape[0], img.shape[1]), dtype=int)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            retImg[i][j] = int(img[i][j]) - int(g[i][j])

    # calibration
    finalImg = np.zeros((img.shape[0], img.shape[1]), dtype=img.dtype)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if retImg[i][j] < 0:
                finalImg[i][j] = 0
            elif retImg[i][j] > 255:
                finalImg[i][j] = 255
            else:
                finalImg[i][j] = retImg[i][j]


    # print ('After LaplaceFiltering')
    # print (finalImg)

    return finalImg


def smoothFiltering(img):

    filterSizes  = [3, 7, 11]
    finals = []

    for size in filterSizes:

        # calculating
        retImg = filter2d(img, np.ones((size, size), dtype=int))

        # narrowing
        finalImg = np.zeros((img.shape[0], img.shape[1]), dtype=img.dtype)
        for i in range(finalImg.shape[0]):
            for j in range(finalImg.shape[1]):
                finalImg[i][j] = int(retImg[i][j]/(size*size))

        # collecting the results
        finals.append(finalImg)
        
    return finals

def start():
    sourceImg = np.array(Image.open('../img/22.png'))

    while 1:
        
        op = int(input("Enter 0 and quit this program\nEnter 1 to use the smoothFiltering function if you want\nWhile enter 2 to use the LaplaceFiltering function\nEnter 3 to use the highBoostFiltering function\nPlease enter : "))
        
        if op is 0:
            print ("GoodBye!\n")
            break
        elif op is 1:
            rets = smoothFiltering(sourceImg)

            # plot1-sourceImage
            plt.subplot(221)
            plt.title('SourceImage')
            plt.imshow(sourceImg, cmap='gray')

            # plot2-3*3 smoothFilteringImage
            plt.subplot(222)
            plt.title('3*3-SmoothFilteringImage')
            plt.imshow(rets[0], cmap='gray')
            Image.fromarray(rets[1]).save("Smooth3X3.png")

            # plot3-7*7 smoothFilteringImage
            plt.subplot(223)
            plt.title('7*7-SmoothFilteringImage')
            plt.imshow(rets[1], cmap='gray')
            Image.fromarray(rets[1]).save("Smooth7X7.png")

            # plot2-9*9 smoothFilteringImage
            plt.subplot(224)
            plt.title('11*11-SmoothFilteringImage')
            plt.imshow(rets[2], cmap='gray')
            Image.fromarray(rets[2]).save("Smooth11X11.png")

            plt.show()
            print ("GoodBye!\n")
            break
        elif op is 2:
            retImg = LaplaceFiltering(sourceImg)

            # plot1-sourceImage
            plt.subplot(121)
            plt.title('sourceImage')
            plt.imshow(sourceImg, cmap='gray')

            # plot2-LaplaceFilteringImage
            plt.subplot(122)
            plt.title('LaplaceFilteringImage')
            plt.imshow(retImg, cmap='gray')
            Image.fromarray(retImg).save('LaplaceFilteringImage.png')

            plt.show()
            print ("GoodBye!\n")
            break
        elif op is 3:
            retImg = highBoostFiltering(sourceImg)

            # plot1-sourceImage
            plt.subplot(121)
            plt.title('SourceImage')
            plt.imshow(sourceImg, cmap='gray')

            # plot2-highBoostFilteringImage
            plt.subplot(122)
            plt.title('highBoostFilteringImage')
            plt.imshow(retImg, cmap='gray')
            Image.fromarray(retImg).save('highBoostFilteringImage.png')

            plt.show()          
            print("GoodBye!\n")
            break
        else:
            print ("you could not enter other number unless 0, 1 , 2 and 3\n")


if __name__ == '__main__':
    start()
