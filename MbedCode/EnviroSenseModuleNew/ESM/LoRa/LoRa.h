#ifndef LoRa_H
#define LoRa_H

#include "mbed.h"
#include <cstdint>
#include "stdio.h"
#include <string>
#include "sensorread.h"

class LoRa{
    private:
        char Buffer[18];
    public:
        void Initialise(void);
        
        // Bluetooth
        void Send(string data);
        void Recieve();
        char* RtnBuf();

};

#endif