#include "mbed.h"
#include "sensorread.h"
#include "stdio.h"
#include "lorawan/LoRaWANInterface.h"
#include "lorawan/system/lorawan_data_structures.h"
#include <LoRaWan.h>
#include <cstdarg>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <memory>

// The following is used to mitage the errors given about the following missing
extern "C"{
   wchar_t* wmemcpy (wchar_t* destination, const wchar_t* source, size_t num){return nullptr;}
   wchar_t* wmemset (wchar_t* ptr, wchar_t wc, size_t num){return nullptr;}
   int __ARM_snprintf ( char * s, size_t n, const char * format, ... ){return 0;}
   int __ARM_vasprintf (char **ret, const char *format, va_list ap){return 0;}
   int __ARM_vsnprintf (char * s, size_t n, const char * format, va_list arg ){return 0;}
   int __ARM_vsscanf ( const char * s, const char * format, va_list arg ){return 0;}
   size_t _mbsnrtowcs ( wchar_t * restrict_dest, const char** restrict_src, size_t nms, size_t len, mbstate_t* restrict_ps){return 0;}
   size_t _wcsnrtombs(char *restrict_dest, const wchar_t **restrict_src, size_t nwc, size_t len, mbstate_t * restrict_ps){return 0;}
   wint_t btowc (int c){return 0;}
   int iswalpha( wint_t ch ){return 0;}
   int  iswcntrl( wint_t ch ){return 0;}
   int  iswdigit( wint_t ch ){return 0;}
   int  iswlower( wint_t ch ){return 0;}
   int  iswprint( wint_t ch ){return 0;}
   int  iswpunct( wint_t ch ){return 0;}
   int  iswspace( wint_t ch ){return 0;}
   int  iswupper( wint_t ch ){return 0;}
   int  iswxdigit( wint_t ch ){return 0;}
   size_t mbrlen (const char* pmb, size_t max, mbstate_t* ps){return 0;}
   size_t mbsrtowcs (wchar_t* dest, const char** src, size_t max, mbstate_t* ps){return 0;}
   int mbtowc (wchar_t* pwc, const char* pmb, size_t max){return 0;}
   wint_t towlower ( wint_t c ){return 0;}
   wint_t towupper ( wint_t c ){return 0;}
   int wcscoll (const wchar_t* wcs1, const wchar_t* wcs2){return 0;}
   size_t wcsxfrm (wchar_t* destination, const wchar_t* source, size_t num){return 0;}
   int wctob (wint_t wc){return 0;}
   int __2swprintf (wchar_t* ws, size_t len, const wchar_t* format, ...){return 0;}
   size_t wcslen( const wchar_t *str ){return 0;}
   long int wcstol (const wchar_t* str, wchar_t** endptr, int base){return 0;}
   unsigned long int wcstoul (const wchar_t* str, wchar_t** endptr, int base){return 0;}
   unsigned long long int wcstoull (const wchar_t* str, wchar_t** endptr, int base){return 0;}
   double __wcstod_int( const wchar_t* str, wchar_t** str_end ){return 0;}
   float __wcstof_int( const wchar_t* str, wchar_t** str_end ){return 0;}
   wchar_t* wmemchr (const wchar_t* ptr, wchar_t wc, size_t num){return 0;}
   int wmemcmp (const wchar_t* ptr1, const wchar_t* ptr2, size_t num){return 0;}
   wchar_t* wmemmove (wchar_t* destination, const wchar_t* source, size_t num){return nullptr;}
   int iswblank (wint_t c){return 0;}
   long long int strtoll (const char* str, char** endptr, int base){return 0;}
   long long int wcstoll (const wchar_t* str, wchar_t** endptr, int base){return 0;}
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

SensorRead Sensors;
/*
UnbufferedSerial LoRa(D1, D0);

const int addr8bit = 0x76 << 1;
*/

// #define NODE_SLAVE

string startconfig = "AT+ID\r\n";
string LocConfig = "AT+DR=EU868\r\n";
string ModeConfig = "AT+MODE=LWOTAA";
string DevEUIConfig = "AT+ID=DevEui,\"70B3D57ED005B898\"\r\n";
string AppEUIConfig = "AT+ID=AppEui,\"0809101112131415\"\r\n";
string Appkeyconfig = "AT+KEY=APPSKEY\"AB5F958A27F5BD301C2B4F8846D8F10E\"\r\n";
string PortConfig = "AT+PORT=125\r\n";
string JoinConfig = "AT+JOIN\r\n";
static bool Exists = false;


#define BUFFERSIZE 128

static BufferedSerial LoRa(D1, D0);

char buffer[BUFFERSIZE] = {0};

char InStream[BUFFERSIZE] = {0};

static char RecvBuf[512];
static bool is_exist = false;
static bool is_join = false;


// Function Protypes
void SendData(string Inputstream);
static int ATSendCheckResponse(string p_ack, int timeout_ms, string p_cmd);
static int RecvPrase();
static int NodeRecv(uint32_t timeout_ms);
static int NodeSend();
static void NodeRecvThenSend(uint32_t timeout);
static void NodeSendThenRecv(uint32_t timout);

// main() runs in its own thread in the OS
int main()
{
    LoRa.set_baud(9600);
    LoRa.set_format(8, BufferedSerial::None, 1); // 8 Bits of Data, no parity and 1 stop bit
    memset(InStream, 0, sizeof(InStream));

    wait_us(1500000); // wait 1.5 seconds for connection
    /*
    SendData("AT+MODE=TEST\r\n");
    SendData("AT+TEST=RFCFG, 866, SF12, 125, 12, 15, 14, ON, OFF, OFF\r\n");
    */

    string ATMode = "AT+MODE=TEST\r\n";
    string ATTestSetup = "AT+TEST=RFCFG, 866, SF12, 125, 12, 15, 14, ON, OFF, OFF\r\n";

    if (ATSendCheckResponse("+AT: OK", 100, "AT\r\n")){
        Exists = true;
        ATSendCheckResponse("+ID: AppEUI", 1000, "AT+ID\r\n");
        wait_us(200000);
    }

    while (true) {
        memset(InStream, 0, sizeof(InStream));
        Sensors.SoilMoistureSensor();
        Sensors.BME280();
        string Result = Sensors.ReturnData();

        printf("%s \n", Result.c_str());
        /*
        string send = "AT+TEST=TXLRSTR,\"" + Result + "\"\r\n";
        
        printf("%s \n", send.c_str());
        LoRa.write(send.c_str(), sizeof(send.c_str()));

        if (LoRa.readable() > 0){
            LoRa.read(InStream, sizeof(InStream));
        }

        printf("%s", InStream);

        //SendData(send);
        */
        wait_us(1000000);
    }

    return 0;
}


void SendData(string Inputstream){
    LoRa.write(Inputstream.c_str(), sizeof(Inputstream.c_str()));
    
    while (LoRa.readable() > 0) {
        LoRa.read(InStream, sizeof(InStream));
    }

    printf("%s \n", InStream);
}

/*
 * Source for the following code can be found at: https://wiki.seeedstudio.com/Grove_LoRa_E5_New_Version/
 * Last Accessed: 14 March 2023 @ 11:09am
*/

static int ATSendCheckResponse(string p_ack, int timeout_ms, string p_cmd){
    int startMillis = 0;
    
    // Print command to LoRa and Terminal
    memset(RecvBuf, 0, sizeof(RecvBuf)); // Set memory in RecvBuf to 0
    LoRa.write(p_cmd.c_str(), sizeof(p_cmd.c_str()));
    printf("%s", p_cmd.c_str());

    wait_us(200000); // wait 200 miliseconds

    startMillis = us_ticker_read() / 1000;

    if (p_ack.c_str() == NULL){
        return 0;
    }

    do {
        LoRa.read(RecvBuf, sizeof(RecvBuf));
        printf("%s", RecvBuf);

        if (strstr(RecvBuf, p_ack.c_str()) != NULL){
            return 1;
        }
    }while((us_ticker_read() / 1000) - startMillis < timeout_ms);
    return 0;
}

static int RecvPrase(){
    memset(RecvBuf, 0, sizeof(RecvBuf));
    int ch = LoRa.read(RecvBuf, sizeof(RecvBuf));

    if (ch){
        return 1;
    }
    else{
        return 0;
    }
}

static int NodeRecv(uint32_t timeout_ms){
    ATSendCheckResponse("+TEST: RXLRPKT", 1000, "AT+TEST=RXLRPKT\r\n");
    int startMillis = us_ticker_read() / 1000;
    do{
        if (RecvPrase()){
            return 1;
        }
    } while((us_ticker_read() / 1000) - startMillis < timeout_ms);
    return 0;
}

static int NodeSend(){
    static uint16_t count = 0;
    int ret = 0;
    char data[32];
    char cmd[128];

    memset(data, 0, sizeof(data));
    sprintf(data, "%04X", count);
    sprintf(cmd, "AT+TEST=TXLRPKT,\"5325454544\"\r\n", data);

    ret = ATSendCheckResponse("TX DONE", 2000, cmd);

    if (ret == 1){
        count++;
        printf("Sent Successfully! \r\n");
    }
    else{
        printf("Send Failed \r\n");
    }
    return ret;
}

static void NodeRecvThenSend(uint32_t timeout){
    int ret = 0;
    ret = NodeRecv(timeout);
    wait_us(100000);
    if(!ret){
        printf("\r\n");
        return;
    }
    NodeSend();
    printf("\r\n");
}

static void NodeSendThenRecv(uint32_t timeout){
    int ret = 0;
    ret = NodeSend();
    if (!ret){
        printf("\r\n");
        return;
    }
    if(!NodeRecv(timeout)){
        printf("recv timout!\r\n");
    }
    printf("\r\n");
}

