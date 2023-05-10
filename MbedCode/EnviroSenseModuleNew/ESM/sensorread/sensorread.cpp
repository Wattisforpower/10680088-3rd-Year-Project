#include "sensorread.h"
#include <string>

mbed::AnalogIn SM(A6);
BME280 BME(D4, D5);

void SensorRead::initializeBME280(){
    BME.initialize();
}

void SensorRead::SoilMoistureSensor(){
    this->SoilMositureRAW = SM.read_u16();
    //this->SoilMositurePercentage = (this->SoilMositureRAW / 65535.0) * 100.0;
}

void SensorRead::BME280(){
    this->BMEPres = BME.getPressure();
    this->BMEHumid = BME.getHumidity();
    this->BMETemp = BME.getTemperature();
}

string SensorRead::ReturnData(){
    string BMEPressure = to_string(this->BMEPres);
    string BMEHumidity =   to_string(this->BMEHumid);
    string BMETemperature =   to_string(this->BMETemp);
    //string SoilMoisture =   to_string(this->SoilMositurePercentage);
    string SoilMoisture = to_string(this->SoilMositureRAW);

    string CombinedString =  BMEPressure + "," + BMEHumidity + "," + BMETemperature + "," + SoilMoisture;
    return CombinedString;
}

void SensorRead::AppendData(){
    this->Pressure = to_string(this->BMEPres);
    this->Humidity = to_string(this->BMEHumid);
    this->Temperature = to_string(this->BMETemp);
    this->SoilMoisture = to_string(this->SoilMositurePercentage);
}

float SensorRead::returnSM(){
    return this->SoilMositureRAW;
}