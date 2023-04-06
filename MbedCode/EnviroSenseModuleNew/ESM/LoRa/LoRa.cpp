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

int LoRa::CheckResponse(string acknowledgement, int timeout, string command){
    int index = 0;
    int startMillis = 0;

    memset(this->Buffer, 0, sizeof(this->Buffer));

    EndNode.write(command.c_str(), sizeof(command.c_str()));
    printf("%s", command.c_str());

    startMillis = us_ticker_read() / 1000;

    if (command.c_str() == NULL)
    {
        return 0;
    }

    do
    {
        while (EndNode.readable() > 0){
            EndNode.read(this->Buffer, sizeof(this->Buffer));
            index++;
            wait_us(2000);
        }

        if (strstr(this->Buffer, acknowledgement.c_str()) != NULL){
            return 1;
        }
    } while ((us_ticker_read() / 1000) - startMillis < timeout);
        
    return 0;
}

int LoRa::RecvPrase(){
    int index = 0;

    memset(this->Buffer, 0, sizeof(this->Buffer));

    while (EndNode.readable() > 0){
        EndNode.read(this->Buffer, sizeof(this->Buffer));
        index++;
        wait_us(2000);
    }

    if (index){
        char* start = NULL;
        char data[32] = {0};

        int rssi = 0;
        int snr = 0;

        start = strstr(this->Buffer, "+TEST: RX \"5345454544");

        if (start){
            start = strstr(this->Buffer, "5345454544");

            if (start && (1 == sscanf(start, "5345454544%s", data))){
                data[4] = 0;
                printf("%s \r\n", data);
            }

            return 1;
        }
    }
    return 0;
}

int LoRa::NodeRecv(uint32_t timeout){
    this->CheckResponse("+TEST: RXLRPKT", 1000, "AT+TEST=RXLRPKT\r\n");
    int startMillis = us_ticker_read() / 1000;

    do {
        if (RecvPrase()){
            return 1;
        }
    } while ((us_ticker_read() / 1000) - startMillis < timeout);
    return 0;
}

int LoRa::NodeSend(){
    static uint16_t count = 0;
    int ret = 0;
    char data[32];
    char cmd[128];

    memset(data, 0, sizeof(data));
    sprintf(data, "%04X", count);
    sprintf(cmd, "AT+TEST=TXLRPKT, \"5345454544%s\"\r\n", data);

    ret = this->CheckResponse("TX DONE", 2000, cmd);
    if (ret == 1){
        count++;
        printf("Sent Successfully!\r\n");
    }
    else{
        printf("Send Failed!\r\n");
    }
    return ret;
}

void LoRa::NodeRecvThenSend(uint32_t timeout){
    int ret = 0;
    ret = this->NodeRecv(timeout);
    wait_us(100000);

    if (!ret){
        printf("\r\n");
        return;
    }

    this->NodeSend();
    printf("\r\n");
}

void LoRa::NodeSendThenRecv(uint32_t timeout){
    int ret = 0;
    ret = this->NodeSend();

    if (!ret){
        printf("\r\n");
        return;
    }
    if (!NodeRecv(timeout)){
        printf("Recv Timeout!\r\n");
    }
    printf("\r\n");
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