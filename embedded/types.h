#ifndef TYPES_H
#define TYPES_H

#include <stdint.h>
#include "const.h"

typedef struct {
  uint8_t seq;
  uint8_t ack; 
  signal_t type;
  char * bytes;  
  uint8_t length;  
}packet_t; 

#endif 
