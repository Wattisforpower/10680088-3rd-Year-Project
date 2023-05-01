#include "mbed.h"

AnalogIn Basic(A6);

// main() runs in its own thread in the OS
int main()
{
    while (true) {
        float val = Basic.read() * 100;
        printf("%f", val);
        wait_us(1000);
    }
}

