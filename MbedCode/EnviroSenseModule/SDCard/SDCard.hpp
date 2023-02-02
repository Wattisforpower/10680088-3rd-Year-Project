#ifndef _SDCard_H
#define _SDCard_H

#include "mbed.h"

#define SPIMosi PA_6
#define SPIMiso PA_5
#define SPISclk PA_12
#define SPICS   PA_4


class SDCard{
    private:

    public:
        void SendData(float Data);
};

#endif //_SDCard_H