#include "SDCard.hpp"
#include <mutex>

SPI SDcard(SPIMosi, SPIMiso, SPISclk);
DigitalOut SDCardSelect(SPICS);

void SDCard::SendData(float Data){
    // Select SDCard SPI Bus
    SDcard.select();
    SDcard.lock();
    SDCardSelect = 0;
    
    SDcard.write(Data);

    SDCardSelect = 1;
    SDcard.unlock();
}
