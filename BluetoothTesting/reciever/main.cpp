#include "mbed.h"

// main() runs in its own thread in the OS
BufferedSerial Bluetooth(D1, D0);
char Buffer[18];

int main()
{

    while (true) {
        if (Bluetooth.readable() > 0){
            Bluetooth.read(Buffer, sizeof(Buffer));

            printf("%s", Buffer);
        }
    }
}

