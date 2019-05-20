from sketchno import Webcam

def fun(x):
    print(x.shape)
    return x

Webcam('Sketchno').start(fun)

