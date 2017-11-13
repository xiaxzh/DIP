import numpy as np
from PIL import Image
import cv2

def extendBorder(img):
    width = img.shape[0]
    height = img.shape[1]
    tar_img = np.zeros((width+2, height+2), dtype=img.dtype)
    tar_img[1:width+1, 1:height+1] = img
    tar_img[0, 1:height+1] = img[0,:]
    tar_img[width+1, 1:height+1] = img[width-1,:]
    tar_img[1:width+1, 0] = img[:, 0]
    tar_img[1:width+1, height+1] = img[:, height-1]
    tar_img[0,0] = img[0, 0]
    tar_img[0, height+1] = img[0, height-1]
    tar_img[width+1, 0] = img[width-1, 0]
    tar_img[width+1, height+1] = img[width-1, height-1]
    return tar_img

def scale(img, size):
    arraySize = (size[1], size[0])
    zmfx = float(arraySize[0]/img.shape[0])
    zmfy = float(arraySize[1]/img.shape[1])
    #print ('size[0] : ', arraySize[0], 'img.shape[0] : ', img.shape[0], 'zmfx : ', zmfx)
    #print ('size[1] : ', arraySize[1], 'img.shape[1] : ', img.shape[1], 'zmfy : ', zmfy)
    dst = np.zeros(arraySize, dtype=img.dtype)
    tar_img = extendBorder(img)
    #print ("extendBorder 's size : ", tar_img.shape)
    #print ('arraySize : ', arraySize)
    for dstx in range(arraySize[0]):
        for dsty in range(arraySize[1]):
            x = dstx/zmfx
            y = dsty/zmfy
            i = np.floor(x)
            u = float(x-i)
            j = np.floor(y)
            v = float(y-j)
            i = int(i)
            j = int(j)
            dst[dstx,dsty] = (1-u)*(1-v)*tar_img[i,j] + (1-u)*v*tar_img[i,j+1] + u*(1-v)*tar_img[i+1,j] + u*v*tar_img[i+1,j+1]
    return dst

def quantize(img, level):
    segment = int(255/(level-1))
    tag = [0] + [segment*(x+1) for x in range(level-2)] + [255]
    # print (tag)
    
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            for k in range(len(tag)):
                if img[x][y]>tag[k] and img[x][y]<tag[k+1]:
                    if abs(img[x][y]-tag[k]) < abs(img[x][y]-tag[k+1]):
                        img[x][y] = tag[k]
                    else:
                        img[x][y] = tag[k+1]
    print (img)
    return img

def scalingMode(sourceImg):
    print ('\n\n')    
    while 1:
        op = int(input("Enter 1 if you want to generate 8 required images.\nEnter 2 to specify the size you want to scale.\nPlease enter : "))
        if op is 1 :
            toDoList = [(192, 128), (96, 64), (48, 32), (24, 16), (12, 8), (300, 200), (450, 300), (500, 200)]
            for size in (toDoList):
                scalingImg = scale(sourceImg, size)
                nameFormat = "%d X %d.png" %(size[0], size[1])
                Image.fromarray(scalingImg).save(nameFormat)
                cv2.imshow(nameFormat, scalingImg)
            cv2.waitKey()
            cv2.destroyAllWindows()
            print ("You can find 8 scaled images in this local folder.")
            break

        elif op is 2 :
            scalingWidth = int(input('Enter the width : '))
            scalingHeight = int(input('Enter the height : '))
            print ("\n\n")
            size = (scalingWidth, scalingHeight)
            scalingImg = scale(sourceImg, size)
            print ("sourceImage's grey array:\n", sourceImg, "\n\n")
            print ("scalingImage's grey array:\n", scalingImg, "\n\n")
            Image.fromarray(scalingImg).save('specifyScaledImg.png')
            cv2.imshow('scaling', scalingImg)
            cv2.waitKey()
            cv2.destroyAllWindows()
            print ("You can find this specified scaled image in this local folder.")
            break

        else:
                print ("you could not enter other number unless 1 and 2\n\n\n")


def quantizeMode(sourceImg):
    print ('\n\n')    
    while 1:
        op = int(input("Enter 1 if you want to generate 5 required images.\nEnter 2 to specify the size you want to scale.\nPlease enter : "))    
        if op is 1:
            toDoList = [128, 32, 8, 4, 2]
            for greyLevel in toDoList:
                quantizationImg = quantize(sourceImg, greyLevel)
                nameFormat = "%d-level.png" %greyLevel
                Image.fromarray(quantizationImg).save(nameFormat)
                cv2.imshow(nameFormat,quantizationImg)
            cv2.waitKey()
            cv2.destroyAllWindows()
            print ("You can find 4 scaled images in this local folder.")
            break

        elif op is 2:
            level = int(input("Enter the grey level you want "))
            print ("\n\n")
            quantizationImg = quantize(sourceImg, level)
            print ("quantizationImg's grey array:\n", quantizationImg, "\n\n")
            Image.fromarray(quantizationImg).save('quantizationImg.png')
            cv2.imshow('quantizationImg', quantizationImg)
            cv2.waitKey()
            cv2.destroyAllWindows()
            print ("You can find this specified grey level image in this local folder.")            
            break

        else:
                print ("you could not enter other number unless 1 and 2\n\n\n")


def start():
    sourceImg = np.array(Image.open('22.png'))
    print ("sourceImage's size: %d X %d\n\n"  %(sourceImg.shape[1], sourceImg.shape[0]))
    
    while 1:
        op = int(input("Enter 0 and quit this program\nEnter 1 to use the scale function if you want\nWhile enter 2 to use the quantize function\nPlease enter : "))
        if op is 0:
            print ("GoodBye!\n")
            break
        elif op is 1:
            scalingMode(sourceImg)
            print ("GoodBye!\n")
            break
        elif op is 2:
            quantizeMode(sourceImg)
            print ("GoodBye!\n")
            break
        else:
            print ("you could not enter other number unless 0, 1 and 2\n")

if __name__ == '__main__':
    start() 