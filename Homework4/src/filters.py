import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from show import show, show3, show4

def contraHarmonicFilting(sourceImage, view=False):
    """ContraharmonicFilting using filters-shape [3,3] and [9,9]
       Using Q only respective -1.5

        Args:
            sourceImage:    The original image
            view:           The flag to decided to show the result image
                            Set to False default

        Returns:
            rets:           The list contains the filted images
    """
    filters = [np.ones((3,3), dtype=int), np.ones((9, 9), dtype=int)]
    Q = -1.5

    from hw2_filter import filter2d
    rets=[]
    for item in filters:
        temp1 = filter2d(sourceImage**(Q+1), item)
        temp2 = filter2d(sourceImage**Q, item)
        ret = np.ones(sourceImage.shape, dtype=int)
        for x in range(ret.shape[0]):
            for y in range(ret.shape[1]):
                if temp2[x][y] == 0.0:
                    ret[x][y] = 255
                else:
                    ret[x][y] = int(temp1[x][y]/temp2[x][y])

        rets.append(ret)

    if view:
        show3(sourceImage, rets, 'contraHarmonic')

    return rets

def harmonicFilting(sourceImage, view=False):
    """HarmonicFilting using filters-shape [3,3] and [9,9]

        Args:
            sourceImage:    The original image
            view:           The flag to decided to show the result image
                            Set to False default

        Returns:
            rets:           The list contains the filted images
    """
    from hw2_filter import extending
    filter_size = [3, 9]
    rets = []
    for size in filter_size:
        # extending
        extendingImage = extending(sourceImage, size, size)
        height, width = extendingImage.shape

        import math
        # calculating
        correlateImage = np.zeros((height, width), dtype=extendingImage.dtype)
        for x in range(height-(size-1)):
            for y in range(width-(size-1)):
                sum = 0
                for j in range(size):
                    for k in range(size):
                        if extendingImage[x+j][y+k] == 0.0:
                            sum = sum + math.inf
                        else:
                            sum = sum + 1/(extendingImage[x+j][y+k])
                correlateImage[x+int((size-1)/2)][y+int((size-1)/2)] = 1/sum

        # cutting
        tarImage = np.zeros(sourceImage.shape, dtype=float)
        for x in range(tarImage.shape[0]):
            for y in range(tarImage.shape[1]):
                tarImage[x][y] = int((correlateImage[x+size-1][y+size-1]))

        ret = np.zeros(sourceImage.shape, dtype=int)
        for x in range(ret.shape[0]):
            for y in range(ret.shape[1]):
                if math.isinf(tarImage[x][y]):
                    ret[x][y] = 255
                else:
                    ret[x][y] = int(size*size*tarImage[x][y])
        rets.append(ret)

    if view:
       show3(sourceImage, rets, "harmonic")

    return rets

def harmonicProcess(sourceImage, view=False):
    """HarmonicProcess using filter only shape [3,3]

        Args:
            sourceImage:    The original image
            view:           The flag to decided to show the result image
                            Set to False default

        Returns:
            rets:           The list contains the filted image
    """
    from hw2_filter import extending
    filter_size = [3]
    rets = []
    for size in filter_size:
        # extending
        extendingImage = extending(sourceImage, size, size)
        height, width = extendingImage.shape

        import math
        # calculating
        correlateImage = np.zeros((height, width), dtype=extendingImage.dtype)
        for x in range(height-(size-1)):
            for y in range(width-(size-1)):
                sum = 0
                for j in range(size):
                    for k in range(size):
                        if extendingImage[x+j][y+k] == 0.0:
                            sum = sum + math.inf
                        else:
                            sum = sum + 1/(extendingImage[x+j][y+k])
                correlateImage[x+int((size-1)/2)][y+int((size-1)/2)] = 1/sum

        # cutting
        tarImage = np.zeros(sourceImage.shape, dtype=float)
        for x in range(tarImage.shape[0]):
            for y in range(tarImage.shape[1]):
                tarImage[x][y] = int((correlateImage[x+size-1][y+size-1]))

        ret = np.zeros(sourceImage.shape, dtype=int)
        for x in range(ret.shape[0]):
            for y in range(ret.shape[1]):
                if math.isinf(tarImage[x][y]):
                    ret[x][y] = 255
                else:
                    ret[x][y] = int(size*size*tarImage[x][y])
        rets.append(ret)

    if view:
       show4(sourceImage, rets, "harmonic")

    return rets

def contraHarmonicProcess(sourceImage, Q=-1.5, view=False):
    """ContraharmonicProcess using filter only shape [3,3]
       Providing changeable Q to process filting
        Args:
            sourceImage:    The original image
            Q:              The Q factor using to process filting
                            Set to False default
            view:           The flag to decided to show the result image
                            Set to False default

        Returns:
            rets:           The list contains the filted image
    """
    filters = [np.ones((3,3), dtype=int)]
    from hw2_filter import filter2d
    rets=[]
    for item in filters:
        temp1 = filter2d(sourceImage**(Q+1), item)
        temp2 = filter2d(sourceImage**Q, item)
        ret = np.ones(sourceImage.shape, dtype=int)
        for x in range(ret.shape[0]):
            for y in range(ret.shape[1]):
                if temp2[x][y] == 0.0:
                    ret[x][y] = 255
                else:
                    ret[x][y] = int(temp1[x][y]/temp2[x][y])
        rets.append(ret)

    if view:
        show4(sourceImage, rets, 'contraHarmonic')

    return rets

def arithmeticFilting(sourceImage, view=False):
    """ArithmeticFilting using filters-shape [3,3] and [9,9]

        Args:
            sourceImage:    The original image
            view:           The flag to decided to show the result image
                            Set to False default

        Returns:
            rets:           The list contains the filted images
    """
    filters = [np.ones((3, 3), dtype=int), np.ones((9, 9), dtype=int)]
    from hw2_filter import filter2d
    rets = []
    for item in filters:
        temp = filter2d(sourceImage, item)
        for x in range(temp.shape[0]):
            for y in range(temp.shape[1]):
                temp[x][y] = int(temp[x][y] / (item.shape[0]*item.shape[1]))
        rets.append(temp)

    if view:
        show3(sourceImage, rets, "arithmetic")

    return rets

def arithmetic_meanProcess(image, view=False):
    """Arithmetic_meanProcess using filter only shape [3,3]

        Args:
            image:  The original image
            view:   The flag to decided to show the result image
                    Set to False default

        Returns:
            rets:   The list contains the filted image
    """
    from hw2_filter import filter2d
    retImage = filter2d(image, np.ones((3,3), dtype=int))
    for x in range(retImage.shape[0]):
        for y in range(retImage.shape[1]):
            retImage[x][y] = int(retImage[x][y]/9)

    if view:
       show(image, retImage, "arithmetic_mean")

    return retImage

def geometric_meanProcess(image, view=False):
    """Geometic_meanProcess using filter only shape [3,3]

        Args:
            image:  The original image
            view:   The flag to decided to show the result image
                    Set to False default

        Returns:
            rets:   The list contains the filted image
    """
    from hw2_filter import extending
    extendingImage = extending(image, 3, 3)

    height = extendingImage.shape[0]
    width = extendingImage.shape[1]
    filterHeight = 3
    filterWidth = 3

    correlateImg = np.zeros((height, width), dtype=extendingImage.dtype)
    for x in range(height-(filterHeight-1)):
        for y in range(width-(filterWidth-1)):
            sum = 1
            for j in range(filterHeight):
                for k in range(filterWidth):
                    sum = sum * extendingImage[x+j][y+k]
            correlateImg[x+int((filterHeight-1)/2)][y+int((filterWidth-1)/2)] = sum

    # import math
    tarImage = np.zeros((image.shape[0], image.shape[1]), dtype=int)
    for x in range(tarImage.shape[0]):
        for y in range(tarImage.shape[1]):
            tarImage[x][y] = int(pow(correlateImg[x+filterHeight-1][y+filterWidth-1], 1/9))

    if view:
        show(image, tarImage, "geometric_mean")

    return tarImage

def medianProcess(image, view=False):
    """MedianProcess using filter only shape [3,3]
       Using the median value of neighborhood as the filting result

        Args:
            image:  The original image
            view:   The flag to decided to show the result image
                    Set to False default

        Returns:
            rets:   The list contains the filted image
    """
    from hw2_filter import extending
    extendingImage = extending(image, 3, 3)

    height = extendingImage.shape[0]
    width = extendingImage.shape[1]
    filterHeight = 3
    filterWidth = 3

    correlateImage = np.zeros((height, width), dtype=int)
    for x in range(height-(filterHeight-1)):
        for y in range(width-(filterWidth-1)):
            myList = [extendingImage[x+i][y+j] for i in range(filterHeight) for j in range(filterWidth)]
            retList = sorted(myList)
            correlateImage[x+int((filterHeight-1)/2)][y+int((filterWidth-1)/2)] = int(retList[int((filterHeight+filterWidth)/2)])

    if view:
        show(image, correlateImage, "medianProcess")
    return correlateImage

def maxProcess(image, view=False):
    """MaxProcess using filter only shape [3,3]
       Using the maximal value of neighborhood as the filting result

        Args:
            image:  The original image
            view:   The flag to decided to show the result image
                    Set to False default

        Returns:
            rets:   The list contains the filted image
    """
    from hw2_filter import extending
    extendingImage = extending(image, 3, 3)

    height = extendingImage.shape[0]
    width = extendingImage.shape[1]
    filterHeight = 3
    filterWidth = 3

    correlateImage = np.zeros((height, width), dtype=int)
    for x in range(height-(filterHeight-1)):
        for y in range(width-(filterWidth-1)):
            myList = [extendingImage[x+i][y+j] for i in range(filterHeight) for j in range(filterWidth)]
            retList = sorted(myList)
            correlateImage[x+int((filterHeight-1)/2)][y+int((filterWidth-1)/2)] = int(retList[-1])

    if view:
        show(image, correlateImage, "maxProcess")

    return correlateImage

def minProcess(image, view=False):
    """MinProcess using filter only shape [3,3]
       Using the minimal value of neighborhood as the filting result

        Args:
            image:  The original image
            view:   The flag to decided to show the result image
                    Set to False default

        Returns:
            rets:   The list contains the filted image
    """
    from hw2_filter import extending
    extendingImage = extending(image, 3, 3)

    height = extendingImage.shape[0]
    width = extendingImage.shape[1]
    filterHeight = 3
    filterWidth = 3

    correlateImage = np.zeros((height, width), dtype=int)
    for x in range(height-(filterHeight-1)):
        for y in range(width-(filterWidth-1)):
            myList = [extendingImage[x+i][y+j] for i in range(filterHeight) for j in range(filterWidth)]
            retList = sorted(myList)
            correlateImage[x+int((filterHeight-1)/2)][y+int((filterWidth-1)/2)] = int(retList[0])

    if view:
        show(image, correlateImage, "minProcess")
        
    return correlateImage

def start():
    from noise import salt_pepperNoise
    sourceImage = np.array(Image.open('task_2.png'))[:,:,0]
    noiseImage = salt_pepperNoise(sourceImage, 0.2, 0.2, True)
    medianProcess(noiseImage, True)

if __name__ == '__main__':
    start()
