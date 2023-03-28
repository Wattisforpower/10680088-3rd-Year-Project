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

        // Following is for either LoRaWAN or Bluetooth, please choose the appropriate option

        // LoRaWAN
        int CheckResponse(string acknowledgement, int timeout, string command);
        int RecvPrase(void);
        int NodeRecv(uint32_t timeout);
        int NodeSend(void);
        void NodeRecvThenSend(uint32_t timeout);
        void NodeSendThenRecv(uint32_t timeout);

        // Bluetooth
        void Send(string data);
        void Recieve();
        char* RtnBuf();

};

#endif