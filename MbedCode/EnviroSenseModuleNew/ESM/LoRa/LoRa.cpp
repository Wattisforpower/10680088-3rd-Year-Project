#include "LoRa.h"
#include <cstdint>
#include <cstdio>
#include <cstring>

BufferedSerial EndNode(D1, D0);


void LoRa::Initialise(){
    EndNode.set_baud(38400);
    EndNode.set_format(
        8, // Bits
        BufferedSerial::None, // Parity
        1 // Stop Bit
    );
}

void LoRa::Send(string data){
    memset(this->Buffer, 0, sizeof(this->Buffer));
    
    sprintf(this->Buffer, "%s\r\n", data.c_str());

    EndNode.write(this->Buffer, sizeof(Buffer));
}


void LoRa::Recieve(){
    EndNode.read(this->Buffer, sizeof(this->Buffer));
    printf("Recieved Data!");
}

char* LoRa::RtnBuf(){
    return this->Buffer;
}