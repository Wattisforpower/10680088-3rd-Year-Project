#define _Sensors_H
#ifndef _Sensors_H

#include "mbed.h"

class Sensors{
    private:
        I2C _BME280;
        I2C _TMP117;
        AnalogIn _SoilMoisture;
    
    protected:
        float BME280Val, TMP117Val, SoilMoistureVal;
    public:
        // Constructor
        Sensors(PinName BMESDA, PinName BMESCL, PinName TMPSDA, PinName TMPSCL, PinNmae SoilMoistureIn) : _BME280(BMESDA, BMESCL), _TMP117(TMPSDA, TMPSCL), _SoilMoisture(SoilMoistureIn);

        // Class Read Functions
        void BMERead();
        void TMPRead();
        void SoilMoistureRead();

        // Class Functions
        void RunningAverage();

        // Class Destructor
        ~Sensors();
};

#endif // _Sensors_H