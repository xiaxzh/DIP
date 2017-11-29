import numpy as np
from PIL import Image


def process1(sourceImage, view=False):
    print ('Processing 1:')
    from filters import arithmeticFilting
    arithmeticFilting(sourceImage, view)

def process2(sourceImage, view=False):
    print ('Processing 2:')
    from filters import harmonicFilting
    harmonicFilting(sourceImage, view)

def process3(sourceImage, view=False):
    print ('Processing 3:')
    from filters import contraHarmonicFilting
    contraHarmonicFilting(sourceImage, view)

def start():
    sourceImage = np.array(Image.open('../img/task_1.png'))
    process1(sourceImage, True)
    process2(sourceImage, True)
    process3(sourceImage, True)

if __name__ == '__main__':
    start()
