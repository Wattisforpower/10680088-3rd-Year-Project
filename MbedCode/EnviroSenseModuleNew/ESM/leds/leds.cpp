#include "leds.h"

DigitalOut PowerLED(D6);
DigitalOut ErrorLED(D3);
DigitalOut CommsSDLED(D9);

void led::PowerOn(){
    PowerLED = 1;
}

void led::PowerOff(){
    PowerLED = 0;
}

void led::Communication(){
    CommsSDLED = 1;
    wait_us(1000);
    CommsSDLED = 0;
}

void led::Error(){
    
}