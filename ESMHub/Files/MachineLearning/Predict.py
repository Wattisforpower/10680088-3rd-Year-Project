import numpy as np

class predict:
    def __init__(self, X, Y) -> None:
        self.x = np.asarray(X)
        self.y = np.asarray(Y)

    def TrainModel(self) -> None:
        N = len(self.x)

        # Regression Line
        XMean = self.x.mean()
        YMean = self.y.mean()

        B1Numerator = ((self.x - XMean) * (self.y - YMean)).sum()
        B1Denominator = ((self.x - XMean)**2).sum()

        B1 = B1Numerator / B1Denominator

        B0 =  YMean + (B1 * XMean)

        self.B0 = B0
        self.B1 = B1
    
    def Predict(self, Input) -> any:
        if self.B1 != 0:
            return self.B1 * Input + self.B0
        else:
            return self.y[-1]
    
    def PredictArray(self, InputArray) -> any:
        TempArray = [[] for i in range(len(InputArray))]

        if self.B0 != 0:
            for i in range(len(InputArray)):
                TempArray[i] = self.B1 * InputArray[i] + self.B0
        else:
            for i in range(len(InputArray)):
                TempArray[i] = self.y[-1]
        
        return TempArray
    
    def PosNegNeutGrad(self) -> None:
        if (self.B1 > 0):
            print("Positive Gradient")
        elif (self.B1 < 0):
            print("Negative Gradient")
        else:
            print("Neutral Gradient")

#####################################################
# FORECASTING
#####################################################

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import RegressorChain
import pandas as pd
import matplotlib.pyplot as plt

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

        i = 1

        while i < input_length:
            df[f'x_{i}'] = df['Y'].shift(-i)
            i = i + 1
        
        j = 0

        while j < output_length:
            df[f'y_{j}'] = df['Y'].shift(-output_length-j)
            j = j + 1

        df = df.dropna(axis = 0)

        return df

    def ModellingTwo(self, df):
        # Split the Data

        XCols = [col for col in df.columns if col.startswith('x')]
        XCols.insert(0, 'Y')
        YCols = [col for col in df.columns if col.startswith('y')]

        XTraining = df[XCols][:-2].values
        YTraining = df[YCols][:-2].values

        XTesting = df[XCols][-2:].values
        YTesting = df[YCols][-2:].values

        # Decision Tree

        DecisionTreeSequence = DecisionTreeRegressor(random_state=42)
        DecisionTreeSequence.fit(XTraining, YTraining)

        DecisionTreeSequencePrediction = DecisionTreeSequence.predict(XTesting)

        # Gradient Boosting

        GBR = GradientBoostingRegressor(random_state=42)
        ChainedGBR = RegressorChain(GBR)
        ChainedGBR.fit(XTraining, YTraining)

        GBRPrediction = ChainedGBR.predict(XTesting)

        return DecisionTreeSequencePrediction, GBRPrediction, XTesting, YTesting

    def PlotPrediction(self, DTSP, GBRP, XT, YT):
        fig, ax = plt.subplots(figsize=(16, 11))

        ax.plot(np.arange(0, 10, 1), XT[1], 'b-', label = "Input")
        ax.plot(np.arange(10, 21, 1), YT[1], color='blue', label="Actual")
        ax.plot(np.arange(10, 21, 1), DTSP[1], color='green', label="DT")
        ax.plot(np.arange(10, 21, 1), GBRP[1], color='purple', label="GB")

        plt.show() 