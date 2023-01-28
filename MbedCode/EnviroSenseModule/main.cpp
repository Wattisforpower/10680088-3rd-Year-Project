// Libraries
#include "mbed.h"

// Headers
#include "DataCollection.hpp"

// Threads
Thread Thread_DataAquisition;

// Queues
EventQueue EQ_DataAquisition(1 * EVENTS_QUEUE_SIZE);

// Classes
DataCollection Data;

// Function Prototypes
void DataAquisition();

int main()
{
    EQ_DataAquisition.call_every(1s, DataAquisition); // change to a suitable time after testing

    Thread_DataAquisition.start(callback(&EQ_DataAquisition, &EventQueue::dispatch_forever));
    

    while (true) {
        sleep();
    }
}

// Thread Functions

void DataAquisition(){
    // Recieve Data
    Data.BME280RecieveData();
    Data.TMP117RecieveData();
    Data.SoilMoistureRecieveData();

    // Recieve Values for Rolling Average
    DataCollection::Values InVals;
    InVals = Data.ReturnValues();

    // Rolling Average
    Data.AvgResult.BME = Data.RollingAverage(InVals.BME);
    Data.AvgResult.TMP = Data.RollingAverage(InVals.TMP);
    Data.AvgResult.SM  = Data.RollingAverage(InVals.SM);
}
