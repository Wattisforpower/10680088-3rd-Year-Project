import numpy as np

# Testing Different Scenarios

TPressure, THumidity, TTemperature, TSMoisture = 0, 0, 0, 0

TP = np.ones(10) # Pressure Array
TH = np.ones(10) # Humidity Array
TT = np.ones(10) # Temperature Array
TSM = np.ones(10) # Soil Moisture Array
TTM = np.array([0,1,2,3,4,5,6,7,8,9]) # Time Array

###################### Functional Code from main.py ###################################

def CheckGradients(PG, HG, TG, SMG):
    array = [PG, HG, TG, SMG]
    GradArray = ['','','','']

    if PG > 0:
        GradArray[0] = 'POS'
    elif PG == 0:
        GradArray[0] = 'NEU'
    else:
        GradArray[0] = 'NEG'

    if HG > 0:
        GradArray[1] = 'POS'
    elif HG == 0:
        GradArray[1] = 'NEU'
    else:
        GradArray[1] = 'NEG'

    if TG > 0:
        GradArray[2] = 'POS'
    elif TG == 0:
        GradArray[2] = 'NEU'
    else:
        GradArray[2] = 'NEG'

    if SMG > 0:
        GradArray[3] = 'POS'
    elif SMG == 0:
        GradArray[3] = 'NEU'
    else:
        GradArray[3] = 'NEG'

    return GradArray

def FindGradients():
    # DeltaX, DeltaY
    Testing = 0
    global TP, TH, TT, TSM, TTM

    PressureDeltaX = TTM[-1] - TTM[0]
    PressureDeltaY = TP[-1] - TP[0]
    if PressureDeltaX == 0.0:
        PressureGradient = 0.0
    else:
        PressureGradient = PressureDeltaY / PressureDeltaX

    HumidityDeltaX = TTM[-1] - TTM[0]
    HumidityDeltaY = TH[-1] - TH[0]
    if HumidityDeltaX == 0.0:
        HumidityGradient = 0.0
    else:  
        HumidityGradient = HumidityDeltaY / HumidityDeltaX

    TemperatureDeltaX = TTM[-1] - TTM[0]
    TemperatureDeltaY = TT[-1] - TT[0]
    if TemperatureDeltaX == 0.0:
        TemperatureGradient = 0.0
    else:
        TemperatureGradient = TemperatureDeltaY / TemperatureDeltaX

    SoilMoistureDeltaX = TTM[-1] - TTM[0]
    SoilMoistureDeltaY = TSM[-1] - TSM[0]
    if SoilMoistureDeltaX == 0.0:
        SoilMoistureGraient = 0.0
    else:
        SoilMoistureGraient = SoilMoistureDeltaY / SoilMoistureDeltaX

    Gradients = CheckGradients(PressureGradient, HumidityGradient, TemperatureGradient, SoilMoistureGraient)


    # [0] = Pressure, [1] = Humidity, [2] = Temperature, [3] = Soil Moisture
    
    #       NEG             NEG             NEG                 NEG             Rainfall                        Test5
    #       NEG             NEG             NEG                 POS             Rainfall                        Test6
    #       NEG             NEG             POS                 NEG             Rainfall                        Test7
    #       NEG             POS             NEG                 NEG             Rainfall                        Test8
    #       POS             NEG             NEG                 NEG             Rainfall                        Test9
    #       NEG             NEG             POS                 POS             Rainfall                        Test10
    #       NEG             POS             NEG                 POS             Rainfall                        Test11
    #       POS             NEG             NEG                 POS             Watering of Soil                Test12
    #       NEG             POS             POS                 NEG             Rainfall                        Test13
    #       POS             NEG             POS                 NEG             Sunshine                        Test14
    #       POS             POS             NEG                 NEG             Sunshine                        Test15
    #       NEG             POS             POS                 POS             Rainfall                        Test16
    #       POS             NEG             POS                 POS             Sunshine/Watering of Soil       Test17
    #       POS             POS             NEG                 POS             Sunshine                        Test18
    #       POS             POS             POS                 NEG             Sunshine                        Test19
    #       POS             POS             POS                 POS             Sunshine/Watering of Soil       Test20
    #       NEU             NEU             NEU                 NEU             TESTING                         Test21
    #       !!!              Other combinations                 !!!             Unknown

    
    if ((Gradients[0] == 'NEG') and (Gradients[1] == 'NEG') and (Gradients[2] == 'NEG') and (Gradients[3] == 'NEG')): # Test 5
        Testing = 5
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'NEG') and (Gradients[2] == 'NEG') and (Gradients[3] == 'POS')): # Test 6
        Testing = 6
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'NEG') and (Gradients[2] == 'POS') and (Gradients[3] == 'NEG')): # Test 7
        Testing = 7
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'POS') and (Gradients[2] == 'NEG') and (Gradients[3] == 'NEG')): # Test 8
        Testing = 8
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'NEG') and (Gradients[2] == 'NEG') and (Gradients[3] =='NEG')): # Test 9
        Testing = 9
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'NEG') and (Gradients[2] == 'POS') and (Gradients[3] == 'POS')): # Test 10
       Testing = 10
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'POS') and (Gradients[2] == 'NEG') and (Gradients[3] == 'POS')): # Test 11
       Testing = 11
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'NEG') and (Gradients[2] == 'NEG') and (Gradients[3] == 'POS')): # Test 12
       Testing = 12
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'POS') and (Gradients[2] == 'POS') and (Gradients[3] == 'NEG')): # Test 13
       Testing = 13
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'NEG') and (Gradients[2] == 'POS') and (Gradients[3] == 'NEG')): # Test 14
       Testing = 14
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'POS') and (Gradients[2] == 'NEG') and (Gradients[3] == 'NEG')): # Test 15
        Testing = 15
    elif ((Gradients[0] == 'NEG') and (Gradients[1] == 'POS') and (Gradients[2] == 'POS') and (Gradients[3] == 'POS')): # Test 16
        Testing = 16
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'NEG') and (Gradients[2] == 'POS') and (Gradients[3] == 'POS')): # Test 17
        Testing = 17
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'POS') and (Gradients[2] == 'NEG') and (Gradients[3] == 'POS')): # Test 18
        Testing = 18
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'POS') and (Gradients[2] == 'POS') and (Gradients[3] == 'NEG')): # Test 19
        Testing = 19
    elif ((Gradients[0] == 'POS') and (Gradients[1] == 'POS') and (Gradients[2] == 'POS') and (Gradients[3] == 'POS')): # Test 20
        Testing = 20
    elif((Gradients[0] == 'NEU') and (Gradients[1] == 'NEU') and (Gradients[2] == 'NEU') and (Gradients[3] == 'NEU')): # Test 21
        Testing = 21
    #else:
    #    OverallPrediction.config(text = "Unknown Result - Please add to elif Ladder")

    return Testing

#############################################################################################


def StopUnrealisticVals() -> None:
    '''
    This function stops the unrealistic values for each variable from being produced
    '''

    global TPressure, THumidity, TTemperature, TSMoisture

    # Pressure

    if (TPressure <= 0):
        TPressure = 0
    elif (TPressure >= 2000):
        TPressure = 2000

    # Humidity

    if (THumidity <= 0):
        THumidity = 0
    elif (THumidity >= 100):
        THumidity = 100

    # Temperature

    if (TTemperature <= -40): # Not minimum temperature, only minimum operating temperature
        TTemperature = 40
    elif (TTemperature >= 85): # Not maximum temperature, only maximum operating temperature
        TTemperature = 85
    
    # Soil Moisture

    if (TSMoisture <= 0):
        TSMoisture = 0
    elif (TSMoisture >= 100):
        TSMoisture = 100
    

def FunctionalityTestPredefinitions():
    global TPressure, THumidity, TTemperature, TSMoisture

    # Define Normal Values
    TPressure = 1000.0
    THumidity = 20.0
    TTemperature = 21.5
    TSMoisture = 10.0

def TestFive():
    '''
    Testing Conditions 5
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure -= 10
    THumidity -= 1
    TTemperature -= 1
    TSMoisture -= 1

    StopUnrealisticVals()

def TestSix():
    '''
    Testing Conditions 6
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure -= 10
    THumidity -= 1
    TTemperature -= 1
    TSMoisture += 1

    StopUnrealisticVals()

def TestSeven():
    '''
    Testing Conditions 7
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure -= 10
    THumidity -= 1
    TTemperature += 1
    TSMoisture -= 1

    StopUnrealisticVals()

def TestEight():
    '''
    Testing Conditions 8
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure -= 10
    THumidity += 1
    TTemperature -= 1
    TSMoisture -= 1

    StopUnrealisticVals()

def TestNine():
    '''
    Testing Conditions 9
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure += 10
    THumidity -= 1
    TTemperature -= 1
    TSMoisture -= 1

    StopUnrealisticVals()

def TestTen():
    '''
    Testing Conditions 10
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure -= 10
    THumidity -= 1
    TTemperature += 1
    TSMoisture += 1

    StopUnrealisticVals()

def TestEleven():
    '''
    Testing Conditions 11
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure -= 10
    THumidity += 1
    TTemperature -= 1
    TSMoisture += 1

    StopUnrealisticVals()

def TestTwelve():
    '''
    Testing Conditions 12
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure += 10
    THumidity -= 1
    TTemperature -= 1
    TSMoisture += 1

def TestThirteen():
    '''
    Testing Conditions 13
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure -= 10
    THumidity += 1
    TTemperature += 1
    TSMoisture -= 1

    StopUnrealisticVals()

def TestFourteen():
    '''
    Testing Conditions 14
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure += 10
    THumidity -= 1
    TTemperature += 1
    TSMoisture -= 1

    StopUnrealisticVals()

def TestFifteen():
    '''
    Testing Conditions 15
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure += 10
    THumidity += 1
    TTemperature -= 1
    TSMoisture -= 1

    StopUnrealisticVals()

def TestSixteen():
    '''
    Testing Conditions 16
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure -= 10
    THumidity += 1
    TTemperature += 1
    TSMoisture += 1

    StopUnrealisticVals()

def TestSeventeen():
    '''
    Testing Conditions 17
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure += 10
    THumidity -= 1
    TTemperature += 1
    TSMoisture += 1

    StopUnrealisticVals()

def TestEighteen():
    '''
    Testing Conditions 18
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure += 10
    THumidity += 1
    TTemperature -= 1
    TSMoisture += 1

    StopUnrealisticVals()

def TestNineteen():
    '''
    Testing Conditions 19
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure += 10
    THumidity += 1
    TTemperature += 1
    TSMoisture -= 1

    StopUnrealisticVals()

def TestTwente():
    '''
    Testing Conditions 5
    '''
    global TPressure, THumidity, TTemperature, TSMoisture

    TPressure += 10
    THumidity += 1
    TTemperature += 1
    TSMoisture += 1

    StopUnrealisticVals()

def FunctionTestMain():
    '''
    Function that Runs all of the tests to get the appropriate results;
    P = Pressure, H = Humidity, T = Temperature, SM = Soil Moisture;
    N = Negative, P = Positive, NC = No Connection
    '''

    # Functionality Test 1
    # PN, HP, TNC, SMP
    TestPointer = 5
    while (TestPointer <= 20):
        FunctionalityTestPredefinitions()
        TP[0], TH[0], TT[0], TSM[0] = TPressure, THumidity, TTemperature, TSMoisture

        match (TestPointer):
            case 5:
                for i in range(9):
                    TestFive()
                    print(THumidity)
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 6:
                for i in range(9):
                    TestSix()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 7:
                for i in range(9):
                    TestSeven()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 8:
                for i in range(9):
                    TestEight()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 9:
                for i in range(9):
                    TestNine()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 10:
                for i in range(9):
                    TestTen()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 11:
                for i in range(9):
                    TestEleven()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 12:
                for i in range(9):
                    TestTwelve()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 13:
                for i in range(9):
                    TestThirteen()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 14:
                for i in range(9):
                    TestFourteen()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 15:
                for i in range(9):
                    TestFifteen()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 16:
                for i in range(9):
                    TestSixteen()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 17:
                for i in range(9):
                    TestSeventeen()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 18:
                for i in range(9):
                    TestEighteen()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 19:
                for i in range(9):
                    TestNineteen()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            case 20:
                for i in range(9):
                    TestTwente()
                    TP[i+1], TH[i+1], TT[i+1], TSM[i+1] = TPressure, THumidity, TTemperature, TSMoisture
                
                Result = FindGradients()
            

          
        if (TestPointer == 4):
            print("See Test 2")
        elif (Result == TestPointer):
                print("Test " + str(TestPointer) + " Passed")
        else:
            print("Test " + str(TestPointer) + " Failed")
        TestPointer += 1




FunctionTestMain()
