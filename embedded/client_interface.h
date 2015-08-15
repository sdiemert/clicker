#ifndef CLIENT_INTERFACE_H
#define CLIENT_INTERFACE_H

#include <HardwareSerial.h>
#include <stdint.h>

#include "const.h"
#include "types.h"
#include "Time.h"

/**
 * A class that communicates events to an external client. 
 */
class ClientInterface{
    public:
        ClientInterface(HardwareSerial * serial);
        uint8_t send_events(time_t *events, uint8_t count);
    private:
        uint8_t check_available();
        uint8_t send_end();
        void send_packet(packet_t * p);
        void init_packet(packet_t * p);
        HardwareSerial * hw;
        unsigned long rate;
        uint8_t seq;
        void reset();
};

#endif 
