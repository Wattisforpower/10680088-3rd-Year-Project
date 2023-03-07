#include "mbed.h"
#include "bme280.h"
#include <cstdint>

struct bme280_dev dev;
int rslt = BME280_OK;

uint8_t dev_addr = BME280_I2C_ADDR_PRIM;

dev.intf_ptr = &dev_addr


