import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import math
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

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


# ===============================================================
# Neural Network
# ===============================================================

MAXSIZEOFARRAY = 10
HiddenUnits = 10
Points = np.ones((MAXSIZEOFARRAY, 2))
Angles = np.ones((MAXSIZEOFARRAY, 2))


def TrainWeightsStochastic(HiddenUnits, Cycles, Points, Alpha, Training, Bias):
    # Initialize Random Weights
    Weight1 = np.random.rand(HiddenUnits, 3)
    Weight2 = np.random.rand(2, HiddenUnits)

    #print(Weight1)
    #print(Weight2)

    XAugmenter = np.ones((MAXSIZEOFARRAY, 1))

    Error = np.empty(MAXSIZEOFARRAY)

    X = np.concatenate((Points, XAugmenter), axis = 1)

    for cycle in range(1, Cycles):
        print(cycle)

        for Iterative in range(0, MAXSIZEOFARRAY):
            XHat = X[Iterative]
            #XAugmented = Points[Iterative]
            Target = Training[Iterative]

            # Sigma Layer
            net2 = Weight1 * XHat
            Sigma = 1 / (1 + np.exp(-net2))

            BiasArray = np.empty((1, HiddenUnits))
            BiasArray.fill(Bias)

            WeightBias = np.concatenate((Weight2, BiasArray))
            SigmaAugmenter = np.ones((MAXSIZEOFARRAY, 1))
            AugSigma = np.concatenate((Sigma, SigmaAugmenter), axis = 1)

            # Linear Output Layer
            Output = np.matmul(WeightBias, AugSigma)

            # =================
            # Error
            # ================= 
            Error[Iterative] =  np.matmul((Target[1] - Output[1]), (Target[1] - Output[1]).T)

            # =================
            # Back Propogation
            # =================
            Delta3 = -(Target[1] - Output)
            Delta2A = np.matmul(WeightBias.T, Delta3)
            Delta2B = np.matmul(AugSigma.T, (1 - AugSigma))

            Delta2 = np.dot(Delta2A, Delta2B)

            Xhat = np.reshape(XHat, (-1, 1))
            XhatB = np.concatenate( (Xhat, np.ones((1, 1))) , axis = 0)

            DeDW1 = np.matmul(Delta2, XhatB)
            DeDW2 = np.matmul(Delta3, AugSigma.T)

            DeltaW1 = np.dot(Alpha, DeDW1)
            DeltaW2 = np.dot(Alpha, DeDW2)

            Weight1 = Weight1 - DeltaW1
            Weight2 = np.subtract(WeightBias, DeltaW2)
        
    
    return Weight1, Weight2


def NNPredict(Weight1, Weight2, Input, Bias):
    net2 = Weight1 * Input
    Sigma = 1 / (1 + np.exp(-net2))

    BiasArray = np.empty((1, HiddenUnits))
    BiasArray.fill(Bias)

    WeightBias = np.concatenate((Weight2, BiasArray))
    SigmaAugmenter = np.ones((MAXSIZEOFARRAY, 1))
    AugSigma = np.concatenate((Sigma, SigmaAugmenter), axis = 1)

    # Linear Output Layer
    Output = np.matmul(WeightBias, AugSigma)

    return Output


            

#W1, W2 = TrainWeightsStochastic(HiddenUnits, 100, Points, 0.1, Angles, 2)

#In = 32.2

#Out = NNPredict(W1, W2, In, 2)

#print(str(Out) + '\n')


# ==========================================================================
# Forecasting
# ==========================================================================

# Written Using sources in sources.txt

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor

class Forecasting():
    def __init__(self, X, Y):
        self.x = pd.DataFrame(X , columns=['X'])
        self.y = pd.DataFrame(Y, columns=['Y'])
        #DataIn = np.concatenate(self.x, self.y)
        #self.Data = pd.DataFrame(DataIn)

    def PlotData(self):
        Figure = plt.figure(figsize=(12, 6))
        SubPlt = plt.subplot(111)
        SubPlt.plot(self.x, self.y)

        plt.show()
    
    def Modelling(self):
        DataFrames = [self.x, self.y]
        df = pd.concat(DataFrames, axis=1)
        df['yPred'] = df['Y'].shift(-1)

        train = df[:-25]
        test = df[-25:]
        test = test.drop(test.tail(1).index) # removes NaN

        # Baseline Model
        test = test.copy()
        test['BasePred'] = test['Y']

        # Decision Tree
        XTrain = train['Y'].values.reshape(-1, 1)
        YTrain = train['yPred'].values.reshape(-1, 1)
        XTest = test['Y'].values.reshape(-1, 1)

        DTRegression = DecisionTreeRegressor(random_state=42)
        DTRegression.fit(X=XTrain, y=YTrain)

        DTPredictions = DTRegression.predict(XTest)

        test['DTPred'] = DTPredictions

        # Gradient Boosting
        GBR = GradientBoostingRegressor(random_state=42)

        GBR.fit(XTrain, y = YTrain)

        GBRPrediction = GBR.predict(XTest)

        test['GBRPred'] = GBRPrediction

        return test
        
    def MAPE(self, YTrue, YPred):
        return round(np.mean(np.abs((YTrue - YPred) / YTrue)) * 100, 2)

    def windowIO(self, input_length: int, output_length: int, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        print(df)

        i = 1

        while i < input_length:
            df[f'x_{i}'] = df['Y'].shift(-i)
            i = i + 1
        
        j = 0

        while j < output_length:
            df[f'y_{j}'] = df['Y'].shift(-output_length-j)
            j = j + 1



        XCols = [col for col in df.columns if col.startswith('x')]

        return df
    

    


xVal = np.linspace(0, 100)
yVal = np.random.rand(50) * xVal + 0

Forecast = Forecasting(xVal, yVal)

Test = Forecast.Modelling()
print(Test)

seq_df = Forecast.windowIO(25, 25, Test)

print(seq_df)

