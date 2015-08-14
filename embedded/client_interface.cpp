#include "client_interface.h"

ClientInterface::ClientInterface(HardwareSerial * hw){

    this->hw = hw; 

}

void ClientInterface::send_packet(packet_t * p){

    //sends a packet to the client over the serial interface.

    this->hw->println(p->bytes); 

}
