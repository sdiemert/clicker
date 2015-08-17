#include "client_interface.h"
#include "types.h"

ClientInterface::ClientInterface(HardwareSerial *hw) {

    this->hw = hw;
    this->rate = 9600;
    this->seq = 0;

    this->hw->begin(this->rate);
}

void ClientInterface::reset() {
    this->seq = 0;
}

uint8_t ClientInterface::send_packet(packet_t *p) {

    //sends a packet to the client over the serial interface.

    p->seq = this->seq;

    this->hw->write((char *) p, sizeof(packet_t));

    this->seq++;

    return 1;

}

uint8_t ClientInterface::send_events(time_t *events, uint8_t count, packet_t * sync) {

    if (!this->check_available()) {
        return 0;
    }

    uint8_t x = 0;

    //reset the seq number
    this->reset();

    packet_t p;

    for (uint8_t i = 0; i < count; i++) {

        p.seq = 0;
        p.ack = 0;
        p.type = (uint8_t) DATA;
        p.time.min = (uint8_t) minute(events[i]);
        p.time.hour = (uint8_t) hour(events[i]);
        p.time.day = (uint8_t) day(events[i]);
        p.time.month = (uint8_t) month(events[i]);
        p.time.year = (uint32_t) year(events[i]);

        x = this->send_packet(&p);

        if (!x) {
            return 0;
        }

    }

    x = this->send_end_of_data();

    if(!x){
        return 0;
    }

    //read the incoming time sync packet from the
    //host. Put the data into the sync variable
    x = this->read_packet(&p);

    if(!x){
        return 0;
    }else{
        sync->time.min = p.time.min;
        sync->time.hour = p.time.hour;
        sync->time.day = p.time.day;
        sync->time.month = p.time.month;
        sync->time.year = p.time.year;
    }

    x = this->send_end();

    if(!x){
        return 0;
    }

    return 1;
}

uint8_t ClientInterface::send_end_of_data() {

    packet_t p;
    int x = 0;

    x = this->init_packet(&p);

    if(!x){

        return 0;

    }

    p.type = DONE;

    x = this->send_packet(&p);

    if(!x){

        return 0;

    }

    return 1;

}

uint8_t ClientInterface::read_packet(packet_t *p) {

    //packets have 11 bytes:
    // - seq (char)
    // - ack (char)
    // - type (char)
    // - min (char)
    // - hour (char)
    // - day (char)
    // - month (char)
    // - year (int, 4 bytes)

    uint8_t buffer[11];

    int num_bytes = this->hw->readBytes(buffer, (int)sizeof(packet_t));

    if (num_bytes != 11) {

        return 0;

    } else {

        p->seq = buffer[0];
        p->ack = buffer[1];
        p->type = buffer[2];
        p->time.min = buffer[3];
        p->time.hour = buffer[4];
        p->time.day = buffer[5];
        p->time.month = buffer[6];
        p->time.year = (buffer[10] << 24) | (buffer[9] << 16) | (buffer[8] << 8) | (buffer[7]);

        return 1;

    }

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

    return 1;
}

uint8_t ClientInterface::init_packet(packet_t *p) {

    p->seq = NULL;
    p->ack = NULL;
    p->type = NULL;
    p->time.min = 0;
    p->time.hour = 0;
    p->time.day = 0;
    p->time.month = 0;
    p->time.year = 0;

    return 1;

}
