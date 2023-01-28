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
    EQ_DataAquisition.call_every(1ms, DataAquisition);

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

    DataCollection::Values InVals;
    InVals = Data.ReturnValues();
}
