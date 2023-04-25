#include "mbed.h"

BufferedSerial Bluetooth(D1, D0);
char Buffer[18];

Thread Receive;

void ReceivingThread();

#define TIMEVAL 1s

int main()
{
    while (true) {
        if (Bluetooth.readable() > 0){
            Bluetooth.read(Buffer, sizeof(Buffer));

            printf("%s", Buffer);
        }
    }
}
