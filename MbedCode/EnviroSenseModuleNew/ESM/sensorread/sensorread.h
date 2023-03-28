#ifndef sensorread_H
#define sensorread_H

// Include Libraries
#include "mbed.h"
#include <string>
#include "BME280.h"

class SensorRead{
    protected:
        int SoilMositureRAW;
        long SoilMositurePercentage;
        long BMEPres, BMEHumid, BMETemp;

    public:
        string Pressure, Humidity, Temperature, SoilMoisture;
        void initializeBME280();
        void SoilMoistureSensor();
        void BME280();
        string ReturnData();
        void AppendData();
};

#endif