#include "Acquisition.h"
#include <string>

LoRa Bluetooth;

void Acquisition::RapidPoll(){
    const char* desired = "YES\r\n";
    while (this->ConnectedFlag == false){
        Bluetooth.Send("ACK\r\n");

        Bluetooth.Recieve();
        char* Received = Bluetooth.RtnBuf();

        if (Received == desired){
            this->ConnectedFlag = true;
        }
    }
}

bool Acquisition::returnflag(){
    return this->ConnectedFlag;
}
