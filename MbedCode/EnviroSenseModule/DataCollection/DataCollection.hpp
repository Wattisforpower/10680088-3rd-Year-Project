#ifndef _DataCollection_H
#define _DataCollection_H


#include "mbed.h"

// Correct These to their actual values
#define BMESDAPin PG_10
#define BMESCLPin PG_11

#define TMPSDAPin PG_12
#define TMPSCLPin PG_13

#define SoilMoisturePin PG_14

// Other Defines
#define SIZE 10

// Class Function
class DataCollection{
    private:
        float BME280Input, TMP117Input, SoilMoistureInput;
        // Address for the I2C Device buses
        const int BMEAddr = 0x76;
        const int TMPAddr = 0x48;

        // Buffers
        float AntiSampleJittering[SIZE];

    protected:
    public:
        typedef struct {
            float BME;
            float TMP;
            float SM;
        } Values;

        DataCollection();
        void BME280RecieveData();
        void TMP117RecieveData();
        void SoilMoistureRecieveData();
        float RollingAverage(float InputVal);
        DataCollection::Values ReturnValues();        
};

#endif /* _DataCollection_H */