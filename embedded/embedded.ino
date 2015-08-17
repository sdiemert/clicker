#include <Arduino.h>
#include <HardwareSerial.h>
#include <stdint.h>
#include "Time.h"
#include "const.h"
#include "types.h"
#include "client_interface.h"

uint8_t BUTTON1 = 4;
uint8_t BUTTON2 = 3;
uint8_t BUTTON3 = 2;

uint8_t prev_button_1_state = HIGH;
uint8_t prev_button_2_state = HIGH;
uint8_t prev_button_3_state = HIGH;

uint8_t LED1 = 11;
uint8_t LED2 = 10;
uint8_t LED3 = 9;

time_t events[150];
uint8_t events_count = 0;

packet_t sync_packet;

ClientInterface *client;

void setup() {

    //Set up some pins here.
    pinMode(BUTTON1, INPUT_PULLUP);
    pinMode(BUTTON2, INPUT_PULLUP);
    pinMode(BUTTON3, INPUT_PULLUP);

    pinMode(LED1, OUTPUT);
    pinMode(LED2, OUTPUT);
    pinMode(LED3, OUTPUT);

    setTime(12, 30, 30, 15, 10, 2015);

    client = new ClientInterface(&Serial);

}

void loop() {

    digitalWrite(LED3, HIGH);

    if(client->send_events(events, events_count, &sync_packet)){

        events_count = 0;

        //syncronize the embedded clock with the host.
        setTime(sync_packet.time.hour,sync_packet.time.min, 0, sync_packet.time.day, sync_packet.time.month, (int)sync_packet.time.year);

    }

    digitalWrite(LED3, LOW);


    if (digitalRead(BUTTON1) == LOW) {

        //button is depressed.

        if (prev_button_1_state == LOW) {

            //no change.

        } else if (prev_button_1_state == HIGH) {

            //they have just pressed the button.
            events[events_count] = now();
            events_count++;
            delay(200); //this delay helps reduce noisey presses.
            //Serial.println(events_count);

        }

        prev_button_1_state = LOW;
        digitalWrite(LED1, HIGH);

    } else {

        //buttton is not pressed (HIGH).
        prev_button_1_state = HIGH;
        digitalWrite(LED1, LOW);

    }


    if (digitalRead(BUTTON2) == LOW) {

        digitalWrite(LED2, HIGH);


    } else {

        digitalWrite(LED2, LOW);

    }


}
