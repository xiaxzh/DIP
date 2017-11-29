import numpy as np
from PIL import Image

def process3(sourceImage, view=False):
    print ('Processing 3:')
    from filters import arithmetic_meanProcess, geometric_meanProcess, maxProcess, minProcess, medianProcess
    arithmetic_meanProcess(sourceImage, view)
    geometric_meanProcess(sourceImage, view)
    maxProcess(sourceImage, view)
    minProcess(sourceImage, view)
    medianProcess(sourceImage, view)

def process2(sourceImage, view=False):
    print ('Processing 2:')
    from filters import harmonicProcess, contraHarmonicProcess
    harmonicProcess(sourceImage, view)
    contraHarmonicProcess(sourceImage, -1.5, view)
    contraHarmonicProcess(sourceImage, 1.5, view)

def process1(sourceImage, view=False):
    print ('Processing 1:')
    from filters import arithmetic_meanProcess, geometric_meanProcess, medianProcess
    arithmetic_meanProcess(sourceImage, view)
    geometric_meanProcess(sourceImage, view)
    medianProcess(sourceImage, view)

def start():
    sourceImage = np.array(Image.open('../img/task_2.png'))[:,:,0]

    from noise import GaussionNoise
    GaussionNoiseImage = GaussionNoise(sourceImage, 0, 40)
    process1(GaussionNoiseImage, True)

    from noise import salt_pepperNoise
    salt_pepperNoiseImage = salt_pepperNoise(sourceImage, 0.2)
    process2(salt_pepperNoiseImage, True)

    salt_pepperNoiseImage = salt_pepperNoise(sourceImage, 0.2, 0.2)
    process3(salt_pepperNoiseImage, True)

if __name__ == '__main__':
    start()
