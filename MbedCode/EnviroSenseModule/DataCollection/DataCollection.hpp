#ifndef _DataCollection_H
#define _DataCollection_H


#include "mbed.h"

// Correct These to their actual values
#define BMESDAPin D4
#define BMESCLPin D5

#define SoilMoisturePin PA_7

// Other Defines
#define SIZE 10

// Class Function
class DataCollection{
    private:
        float BME280Input, SoilMoistureInput;
        // Address for the I2C Device buses
        const int BMEAddr = 0x76;

        // Buffers
        float AntiSampleJittering[SIZE];

    protected:
    public:
        // Value Structure
        typedef struct {
            float BME;
            float SM;
        } Values;

        // Average Result
        DataCollection::Values AvgResult;

        // Constructor

        // Functions
        void BME280RecieveData();
        void SoilMoistureRecieveData();
        float RollingAverage(float InputVal);
        DataCollection::Values ReturnValues();
        void REBOOT();      
};

#endif /* _DataCollection_H */