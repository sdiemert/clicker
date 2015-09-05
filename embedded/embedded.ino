#include <Arduino.h>
#include <HardwareSerial.h>
#include <stdint.h>
#include "Time.h"
#include "const.h"
#include "types.h"
#include "client_interface.h"

uint8_t BUTTON1 = 9;
uint8_t BUTTON2 = 10;
uint8_t BUTTON3 = 12;

int LED = 7;

uint8_t prev_button_1_state = HIGH;
uint8_t prev_button_2_state = HIGH;
uint8_t prev_button_3_state = HIGH;

event_t events[150];
event_t tmp_event;
uint8_t events_count = 0;

packet_t sync_packet;

ClientInterface *client;

void setup() {

    //Set up some pins here.
    pinMode(BUTTON1, INPUT_PULLUP);
    pinMode(BUTTON2, INPUT_PULLUP);
    pinMode(BUTTON3, INPUT_PULLUP);

    //Set up output
    pinMode(LED, OUTPUT);
    digitalWrite(LED, LOW);

    setTime(12, 30, 30, 15, 10, 2015);

    //Serial.begin(9600);

    client = new ClientInterface((HardwareSerial *)&Serial);

}

void loop() {

    if(client->send_events(events, events_count, &sync_packet)){

        events_count = 0;

        //syncronize the embedded clock with the host.
        setTime(sync_packet.time.hour,sync_packet.time.min, 0, sync_packet.time.day, sync_packet.time.month, (int)sync_packet.time.year);

    }

    if (digitalRead(BUTTON1) == LOW) {

        //button is depressed.

        if (prev_button_1_state == LOW) {

            //no change.

        } else if (prev_button_1_state == HIGH) {

            //they have just pressed the button.
            events[events_count].time = now();
            events[events_count].action = 1;
            events_count++;
            delay(200); //this delay helps reduce noisey presses.
            //Serial.println(events_count);

        }

        prev_button_1_state = LOW;

    } else {

        //buttton is not pressed (HIGH).
        prev_button_1_state = HIGH;

    }


    if (digitalRead(BUTTON2) == LOW) {

        //button is depressed.

        if (prev_button_2_state == LOW) {

            //no change.

        } else if (prev_button_2_state == HIGH) {

            //they have just pressed the button.
            events[events_count].time = now();
            events[events_count].action = 2;
            events_count++;
            delay(200); //this delay helps reduce noisey presses.
            //Serial.println(events_count);

        }

        prev_button_2_state = LOW;

    } else {

        prev_button_2_state = HIGH;

    }

    if (digitalRead(BUTTON3) == LOW) {

        //button is depressed.

        if (prev_button_3_state == LOW) {

            //no change.

        } else if (prev_button_3_state == HIGH) {

            //they have just pressed the button.
            events[events_count].time = now();
            events[events_count].action = 3;
            events_count++;
            delay(200); //this delay helps reduce noisey presses.
            //Serial.println(events_count);

        }

        prev_button_3_state = LOW;


    } else {

        prev_button_3_state = HIGH;

    }

}
