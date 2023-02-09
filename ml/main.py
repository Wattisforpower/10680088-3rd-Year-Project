import numpy as np

class Predict:
    def __init__(self, InputX, InputY):
        self.x = np.asarray(InputX)
        self.y = np.asarray(InputY)
    
    def TrainModel(self):
        N = len(self.x)
        # Regression Line
        XMean = self.x.mean()
        YMean = self.x.mean()

        B1Numerator = ((self.x - XMean) * (self.y - YMean)).sum()
        B1Denominator = ((self.x - XMean)**2).sum()
        B1 = B1Numerator / B1Denominator

        B0 = YMean = (B1*XMean)

        regressionLine = f'y = {B0} + {round(B1, 3)}'

        # Correlation Coefficient
        Numerator = (N * (self.x * self.y).sum()) - (self.x.sum() * self.y.sum())
        Denominator = np.sqrt((N * (self.x**2).sum() - self.x.sum()**2) * (N * (self.y**2).sum() - self.y.sum()**2))

        Coefficient = Numerator / Denominator

        self.B0 = B0
        self.B1 = B1
        return regressionLine, Coefficient, B0, B1
    
    def Predict(self, Input):
        if self.B1 != 0:
            return self.B1 * Input + self.B0
        else:
            return self.y[-1]
    
    def PredictArray(self, InputArray):
        TempArray = [[] for i in range(len(InputArray))]
        if self.B1 != 0:
            for i in range(len(InputArray)):
                TempArray[i] = self.B1 * InputArray[i] + self.B0
        else:
            for i in range(len(InputArray)):
                TempArray[i] = self.y[-1]
        
        return TempArray
    
    def PosNegGrad(self):
        if (self.B1 > 0):
            print("Positive Gradient")
        elif (self.B1 < 0):
            print("Negative Gradient")
        else:
            print("Neutral Gradient")


def main():
    XList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    YList = [0, 1, 1, 2, 2, 3, 2, 4, 3, 5]

    YList2 = [10, 10, 9, 8, 6, 5, 4, 3, 2, 2]
    YList3 = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

    Test = Predict(XList, YList3)

    Test.TrainModel()

    prediction = Test.Predict(10)

    Array = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    predarray = Test.PredictArray(Array)

    Test.PosNegGrad()

    print(prediction)
    print(predarray)
    


if __name__ == "__main__":
    main()