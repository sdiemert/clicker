#ifndef CLIENT_INTERFACE_H
#define CLIENT_INTERFACE_H

#include "const.h"
#include "types.h"
#include <HardwareSerial.h>

class ClientInterface{
    public:
        ClientInterface(HardwareSerial * serial);
        void send_packet(packet_t * p); 
    private:
        HardwareSerial * hw; 

};

#endif 
