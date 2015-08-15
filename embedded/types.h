#ifndef TYPES_H
#define TYPES_H

#include <stdint.h>
#include "const.h"

typedef struct {
    uint8_t min;
    uint8_t hour;
    uint8_t day;
    uint8_t month;
    uint32_t year;
} time_packet_t;

typedef struct {
    uint8_t seq;
    uint8_t ack;
    uint8_t type;
    time_packet_t time;
} packet_t;


#endif 
