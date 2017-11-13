import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def divide(tar_matrix, size):
    for i in range(tar_matrix.shape[0]):
        for j in range(tar_matrix.shape[1]):
            tar_matrix[i][j] = np.floor(tar_matrix[i][j]/(size**2))
    return tar_matrix

def filter2d_freq(sourceImage, filter):
    M = sourceImage.shape[0]
    N = sourceImage.shape[1]
    P = 2*M
    Q = 2*N

    # padding sourceImage and centralization
    padding_image_matrix = np.zeros((P, Q), dtype=int)
    padding_image_matrix[0:M, 0:N] = sourceImage
    for i in range(P):
        for j in range(Q):
            padding_image_matrix[i][j] = padding_image_matrix[i][j]*(-1)**(i+j)

    # padding filter and centralization
    padding_filter_matrix = np.zeros((P, Q), dtype=int)
    padding_filter_matrix[0:filter.shape[0], 0:filter.shape[1]] = filter
    for i in range(P):
        for j in range(Q):
            padding_filter_matrix[i][j] = padding_filter_matrix[i][j]*(-1)**(i+j)

    dft_image_matrix = dft2d(padding_image_matrix, 0)
    dft_filter_matrix = dft2d(padding_filter_matrix, 0)
    ret_freq_matrix = dft_image_matrix*dft_filter_matrix

    temp = dft2d(ret_freq_matrix, 1)

    for i in range(P):
        for j in range(Q):
            temp[i][j] = temp[i][j]*(-1)**(i+j)

    result = np.array((M, N), dtype=int)
    result = temp[0:M, 0:N]

    return result

def visible(dft_matrix):
    height = dft_matrix.shape[0]
    width = dft_matrix.shape[1]
    pattern = np.zeros((height, width), dtype=int)
    for x in range(dft_matrix.shape[0]):
        for y in range(dft_matrix.shape[1]):
            pattern[x][y] = np.floor(np.sqrt(dft_matrix[x][y].real**2 + dft_matrix[x][y].imag**2))
            # log transform using ret = 1 + log(|F(u, v)|)
            pattern[x][y] = 1 + np.log(pattern[x][y])

    # calibration using ret = K*(f-f_min)/(f_max-f_min) with K is the grey level maximun
    pattern_min = pattern.min()
    pattern_max = pattern.max()
    f_max = pattern_max-pattern_min
    ret = np.zeros((pattern.shape[0], pattern.shape[1]), dtype=int)
    for x in range(pattern.shape[0]):
        for y in range(pattern.shape[1]):
            ret[x][y] = np.floor(255*((pattern[x][y]-pattern_min)/f_max))

    return ret


def dft_matrix(N, flags):
    i, j = np.meshgrid(np.arange(N), np.arange(N))
    if flags is 0:
        omega = np.exp(-2*1J*np.pi/N)
    elif flags is 1:
        omega = np.exp(2*1J*np.pi/N)
    ret = np.power(omega, i*j)
    return ret

def dft2d(sourceImage, flags):
    height = sourceImage.shape[0]
    width = sourceImage.shape[1]

    # dft
    if flags is 0:
        output = np.zeros((height, width), dtype=complex)
        # centralization
        shift_image =  np.zeros((height, width), dtype=int)
        for x in range(height):
            for y in range(width):
                shift_image[x][y] = sourceImage[x][y] * (-1)**(x+y)
        output = dft_matrix(height, 0).dot(shift_image).dot(dft_matrix(width, 0))

    # idft
    elif flags is 1:
        output = np.zeros((height, width), dtype=int)
        calculate_matrix = np.zeros((height, width), dtype=complex)
        calculate_matrix = dft_matrix(height, 1).dot(sourceImage).dot(dft_matrix(width, 1))
        for x in range(height):
            for y in range(width):
                output[x][y] = np.floor(calculate_matrix[x][y].real*(-1)**(x+y)/(height*width))

    return output


def start():
    sourceImage = np.array(Image.open('22.png'))

    # DFT
    dft_matrix = dft2d(sourceImage, 0)
    visible_dft_matrix = visible(dft_matrix)

    # IDFT
    idft_matrix = dft2d(dft_matrix, 1)

    plt.subplot(131)
    plt.title('Original Image')
    plt.imshow(sourceImage, cmap='gray')

    plt.subplot(132)
    plt.title('freq Image after visualization')
    plt.imshow(visible_dft_matrix, cmap='gray')

    plt.subplot(133)
    plt.title('recover from freq using IDFT')
    plt.imshow(idft_matrix, cmap='gray')
    plt.show()

    # Filtering
    smooth3_matrix = divide(filter2d_freq(sourceImage, np.ones((3, 3), dtype=int)), 3)
    smooth7_matrix = divide(filter2d_freq(sourceImage, np.ones((7, 7), dtype=int)), 7)
    smooth11_matrix = divide(filter2d_freq(sourceImage, np.ones((11, 11), dtype=int)), 11)
    Laplace_matrix = sourceImage - filter2d_freq(sourceImage, np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=int))

    for i in range(Laplace_matrix.shape[0]):
        for j in range(Laplace_matrix.shape[1]):
            if Laplace_matrix[i][j] < 0:
                Laplace_matrix[i][j] = 0
            elif Laplace_matrix[i][j] > 255:
                Laplace_matrix[i][j] = 255

    plt.subplot(221)
    plt.title('Soomthing-3*3Filter')
    plt.imshow(smooth3_matrix, cmap='gray')

    plt.subplot(222)
    plt.title('Smoothing-7*7Filter')
    plt.imshow(smooth7_matrix, cmap='gray')

    plt.subplot(223)
    plt.title('Soomthing-11*11Filter')
    plt.imshow(smooth11_matrix, cmap='gray')

    plt.subplot(224)
    plt.title('Laplace-Filter')
    plt.imshow(Laplace_matrix, cmap='gray')
    plt.show()

if __name__ == '__main__':
    start()
