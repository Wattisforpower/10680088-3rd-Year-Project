#ifndef Acquisition_H
#define Acquisition_H

#include "mbed.h"
#include "LoRa.h"

class Acquisition{
    private:
        bool ConnectedFlag = false;
    
    public:
        void RapidPoll();
        bool returnflag();

};

#endif