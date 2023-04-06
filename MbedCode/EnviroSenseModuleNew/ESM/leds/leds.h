#ifndef leds_H
#define leds_H

#include "mbed.h"

class led{
    private:

        enum Ecodes{WatchDog};
    public:
        void PowerOn();
        void PowerOff();
        void Communication();
        void Error();
};


#endif