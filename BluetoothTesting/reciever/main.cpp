#include "mbed.h"

BufferedSerial Bluetooth(D1, D0);
char Buffer[18];

Thread Receive;

void ReceivingThread();
void RapidPoll();

#define TIMEVAL 1s

int main()
{
    RapidPoll();

    while (true) {
        if (Bluetooth.readable() > 0){
            Bluetooth.read(Buffer, sizeof(Buffer));

            printf("%s", Buffer);
        }
    }
}

bool connected = false;

void RapidPoll(){
    const char* desired = "ACK\r\n";
    const char* Return = "YES\r\n";

    while (connected == false){
        if (Bluetooth.readable() > 0){
            Bluetooth.read(Buffer, sizeof(Buffer));

            printf("%s", Buffer);
        }

        if (Buffer == desired){
            connected = true;
            Bluetooth.write(Return, sizeof(strlen(Return)))
        }
    }
}