#include "client_interface.h"
#include "types.h"

ClientInterface::ClientInterface(HardwareSerial *hw) {

    this->hw = hw;
    this->rate = 9600;
    this->seq = 0;

    this->hw->begin(this->rate);
}

void ClientInterface::reset(){
    this->seq = 0;
}

void ClientInterface::send_packet(packet_t *p) {

    //sends a packet to the client over the serial interface.

    p->seq = this->seq;

    this->hw->write((char *)p, sizeof(packet_t));

    this->seq++;

}

uint8_t ClientInterface::send_events(time_t *events, uint8_t count) {

    if(!this->check_available()){
        return 0;
    }

    //reset the seq number
    this->reset();

    packet_t p;

    for (uint8_t i = 0; i < count; i++) {

        p.seq = 0;
        p.ack = 0;
        p.type = (uint8_t) DATA;
        p.time.min      = (uint8_t) minute(events[i]);
        p.time.hour     = (uint8_t) hour(events[i]);
        p.time.day      = (uint8_t) day(events[i]);
        p.time.month    = (uint8_t) month(events[i]);
        p.time.year     = (uint32_t) year(events[i]);

        this->send_packet(&p);

    }

    this->send_end();

    return 1;
}

uint8_t ClientInterface::check_available() {

    //expect sequence: $ to start

    int x = this->hw->available();

    int chars = 0;
    int c = NULL;

    if (x >= 1) {

        c = this->hw->read();

        if (c == '$') {

            return 1;

        } else {

            return 0;

        }

    } else {

        return 0;

    }

}

uint8_t ClientInterface::send_end() {

    packet_t p;

    //get an empty packet.
    this->init_packet(&p);

    p.seq = 0;
    p.ack = 0;
    p.type = TERM;
    this->send_packet(&p);

    return 0;
}

void ClientInterface::init_packet(packet_t * p) {

    p->seq = NULL;
    p->ack = NULL;
    p->type = NULL;
    p->time.min = 0;
    p->time.hour = 0;
    p->time.day = 0;
    p->time.month = 0;
    p->time.year = 0;

}
