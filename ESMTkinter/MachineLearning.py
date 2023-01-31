import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import math
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
import pandas as pd

def InitXY(InputXArray, InputYArray):
    X = np.asarray(InputXArray)
    Y = np.asarray(InputYArray)
    return X, Y

def TrainModel(InputX, InputY):
    N = len(InputX)
    # Regression Line
    XMean = InputX.mean()
    YMean = InputY.mean()

    B1Numerator = ((InputX - XMean) * (InputY - YMean)).sum()
    B1Denominator = ((InputX - XMean)**2).sum()
    B1 = B1Numerator / B1Denominator

    B0 = YMean = (B1*XMean)

    regressionLine = f'y = {B0} + {round(B1, 3)}'

    # Correlation Coefficient
    Numerator = (N * (InputX * InputY).sum()) - (InputX.sum() * InputY.sum())
    Denominator = np.sqrt((N * (InputX**2).sum() - InputX.sum()**2) * (N * (InputY**2).sum() - InputY.sum()**2))

    Coefficient = Numerator / Denominator


    return regressionLine, Coefficient, B0, B1
    



def Predict(B0, B1, InputDataX):
    y = B1 * InputDataX + B0

    return y


