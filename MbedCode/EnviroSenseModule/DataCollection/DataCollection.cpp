#include "DataCollection.hpp"

// I2C Device Setup
I2C BME(BMESDAPin, BMESCLPin);
I2C TMP(TMPSDAPin, TMPSCLPin);
AnalogIn SM(SoilMoisturePin);

// Class Functions
void DataCollection::BME280RecieveData(){
    char BMEInputTemp[2];
    BMEInputTemp[0] = 0x01;
    BMEInputTemp[1] = 0x00;
    BME.read(this->BMEAddr, BMEInputTemp, 2);

    this->BME280Input = (float((BMEInputTemp[0] << 8) | BMEInputTemp[1])/ 256.0);
}

void DataCollection::TMP117RecieveData(){
    char TMPInputTemp[2];
    TMPInputTemp[0] = 0x01;
    TMPInputTemp[1] = 0x00;

    BME.read(this->TMPAddr, TMPInputTemp, 2);
    this->TMP117Input = (float((TMPInputTemp[0] << 8) | TMPInputTemp[1]) / 256.0);
}

void DataCollection::SoilMoistureRecieveData(){
    this->SoilMoistureInput = SM;
}

float DataCollection::RollingAverage(float InputVal){
    float Total = 0, Avg = 0;

    for (int i = 0; i < SIZE; i++){
        AntiSampleJittering[i] = AntiSampleJittering[i+1];
    }
    AntiSampleJittering[SIZE-1] = InputVal;

    for (int i = 0; i < SIZE; i++){
        Total += AntiSampleJittering[i];
    }

    return Total / SIZE;
}

DataCollection::Values DataCollection::ReturnValues(){
    DataCollection::Values Output;
    Output.BME = this->BME280Input;
    Output.TMP = this->TMP117Input;
    Output.SM = this->SoilMoistureInput;

    return Output;
} 
