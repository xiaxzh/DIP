import matplotlib.pyplot as plt

def show4(sourceImage, rets, name):
    plt.subplot(121)
    plt.title('Original Image')
    plt.imshow(sourceImage, cmap='gray')

    plt.subplot(122)
    plt.title('3*3-'+name)
    plt.imshow(rets[0], cmap='gray')
    plt.show()

def show3(sourceImage, rets, name):
    plt.subplot(131)
    plt.title('Original Image')
    plt.imshow(sourceImage, cmap='gray')

    plt.subplot(132)
    plt.title('3*3-'+name)
    plt.imshow(rets[0], cmap='gray')

    plt.subplot(133)
    plt.title('9*9-'+name)
    plt.imshow(rets[1], cmap='gray')
    plt.show()

def show(sourceImage, retImage, name):
    plt.subplot(121)
    plt.title('Original Image')
    plt.imshow(sourceImage, cmap='gray')

    plt.subplot(122)
    plt.title(name)
    plt.imshow(retImage, cmap='gray')
    plt.show()
