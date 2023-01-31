import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import math
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression

def InitXY(InputXArray, InputYArray):
    X = InputXArray
    Y = InputYArray
    return X, Y

def TrainModel(InputX, InputY):
    X_train, X_test, Y_train, Y_test = model_selection.train_test_split(InputX, InputY, test_size=0.2)
    clf = LinearRegression(n_jobs=1)

    clf.fit(X_train, Y_train)
    confidence = clf.score()

    return clf, confidence 


def Predict(clf, InputDataX):
    Forecast = clf.predict(InputDataX)

    return Forecast


