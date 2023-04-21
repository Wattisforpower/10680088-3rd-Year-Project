#include "mbed.h"
#include "stdio.h"
#include <cstdarg>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <memory>

#include "sensorread.h"
#include "LoRa.h"
#include "leds.h"
#include "Acquisition.h"

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

// #define NODE_SLAVE

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// INTERVALTIME
#define INTERVALTIME 1s // Testing @1s actual 600s (10mins)


// Classes
SensorRead Sensors;
LoRa DataSend;
led led;
Acquisition AcquireSignal;

// Threads
Thread Data;
Thread Comms;

// Mutex
Mutex DataProtection;

// Function Prototypes
void DataThread();
void CommsThread();
void TriggerWatchdog();

// main() runs in its own thread in the OS
int main()
{
    led.PowerOn();

    AcquireSignal.RapidPoll(); // Rapidly polls "ACK" until signal is acquired from the receiver responding with "YES"

    //DataSend.Initialise();

    Data.start(DataThread);
    wait_us(1000); // wait 1 millisecond before starting the next thread
    Comms.start(CommsThread);

    while (true){
        sleep();
    }
    
    return 0;
}


//////////////////////////////////////
/// Thread Operations
//////////////////////////////////////

void DataThread(){
    while (true) {
        DataProtection.lock();
        Sensors.SoilMoistureSensor();
        Sensors.BME280();
        DataProtection.unlock();

        ThisThread::sleep_for(INTERVALTIME);
    }
}

void CommsThread(){
    while (true){
        DataProtection.trylock();
        string Result = Sensors.ReturnData();
        DataSend.Send(Result);
        printf("%s \n", Result.c_str());
        led.Communication();
        DataProtection.unlock();

        ThisThread::sleep_for(INTERVALTIME);
    }
}
