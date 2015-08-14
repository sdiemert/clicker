#include <stdint.h>
#include "Time.h"
#include "const.h"
#include "types.h"
#include "client_interface.h"

int BUTTON1 = 4;
int BUTTON2 = 3;
int BUTTON3 = 2; 

int prev_button_1_state = HIGH; 
int prev_button_2_state = HIGH; 
int prev_button_3_state = HIGH; 

int LED1 = 11; 
int LED2 = 10; 
int LED3 = 9; 

time_t events[150]; 
int events_count = 0; 

ClientInterface * client; 

void setup() {

  //Set up some pins here. 
  pinMode(BUTTON1, INPUT_PULLUP);
  pinMode(BUTTON2, INPUT_PULLUP);
  pinMode(BUTTON3, INPUT_PULLUP);

  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT); 

  setTime(12, 30, 30, 15, 10, 2015);

  Serial.begin(9600);

  client = new ClientInterface(&Serial);
 
}

void loop() {

  if(digitalRead(BUTTON1) == LOW){

    //button is depressed. 

    if(prev_button_1_state == LOW){

        //no change. 
      
    }else if(prev_button_1_state == HIGH){

        //they have just pressed the button.
        events[events_count] = now();
        events_count++;
        delay(200); //this delay helps reduce noisey presses. 
        //Serial.println(events_count);
        
    }

    prev_button_1_state = LOW; 
    digitalWrite(LED1, HIGH);
    
  }else{

    //buttton is not pressed (HIGH).
    prev_button_1_state = HIGH;
    
    digitalWrite(LED1, LOW);   
  
  }

  
  if(digitalRead(BUTTON2) == LOW){

    digitalWrite(LED2, HIGH); 

          
  }else{
    
    digitalWrite(LED2, LOW);
  
  }

    packet_t packet;
    packet.bytes = "abcd";
    packet.length = 5; 
    packet.seq = 0;
    packet.ack = 0; 
    packet.type = INIT; 

  if(Serial.available()>0){

    //there is a byte waiting on the Serial input.

     digitalWrite(LED2, HIGH);

     for(int i = 0; i < events_count; i++){

        client->send_packet(&packet); 

         /*
        Serial.print(year(events[i]));
        Serial.print("-");
        Serial.print(month(events[i]));
        Serial.print("-");
        Serial.print(day(events[i]));
        Serial.print("_");
        Serial.print(hour(events[i]));
        Serial.print(":");
        Serial.print(minute(events[i]));
        Serial.print(":");
        Serial.println(second(events[i]));
        */
        
      }
  
      events_count = 0;
    
  }else{
    digitalWrite(LED2, LOW);
  }

}
