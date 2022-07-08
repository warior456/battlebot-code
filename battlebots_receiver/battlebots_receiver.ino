#include <RH_ASK.h>
#include <SPI.h> // Not actualy used but needed to compile

RH_ASK driver(1900, 13, 12, 0);
int led = LED_BUILTIN;
int vbql = 0;
int inPin = 11;

int links_v = 5;
int links_a = 3;
int rechts_v = 11;
int rechts_a = 6;

int packet_led = 4;

int safety_distance = 20;

char vooruit;

#define echoPin 8 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 7 //attach pin D3 Arduino to pin Trig of HC-SR04

long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement


void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  pinMode(pled, OUTPUT);

  if (!driver.init())
    Serial.println("init failed");

  pinMode(inPin, INPUT);

  Serial.println("started");

}

void loop() {

  // check if data is available
  if (Serial.available() > 0) {
    // read the incoming byte:
    byte incomingByte = Serial.read();
    // prints the received data
    Serial.print("I received: ");
    Serial.println((char)incomingByte);
  }
  data_receive();

}

void data_receive() {

  uint8_t buf[RH_ASK_MAX_MESSAGE_LEN];
  uint8_t buflen = sizeof(buf);

  if (driver.recv(buf, &buflen)) { // Non-blocking
    String message = (char*)buf;



    // Message with a good checksum received, dump it.
    Serial.print("Received: ");
    Serial.println((char*)buf);
    message = message.substring(0, buflen);
    pled(message);
    controls(message);
  }

}

void pled(String message) {

  digitalWrite(packet_led, HIGH);
  delay(5);
  digitalWrite(packet_led, LOW);

  if (message == "on") {
    digitalWrite(packet_led, HIGH);
  } else if (message == "off") {
    digitalWrite(packet_led, LOW);
  }
}

void controls(String message) {

  vooruit = message[0];
  char achteruit = message[1];
  char links = message[2];
  char rechts = message[3];
  String speed_s = message.substring(4, 7);
  uint8_t speed = speed_s.toInt();


  if (check_distance() != true) {
    Serial.println("stop");
    vooruit = '0';
  }
  //analogWrite(10, speed);
  if (vooruit == '1' && links == '0' && rechts == '0' && achteruit == '0') { //vooruit 1000
    analogWrite(links_v, speed);
    analogWrite(rechts_v, speed);
    analogWrite(links_a, 0);
    analogWrite(rechts_a, 0);
  }
  else if (achteruit == '1' && vooruit == '0' && links == '0' && rechts == '0') { //achteruit 0100
    analogWrite(links_a, speed);
    analogWrite(rechts_a, speed);
    analogWrite(links_v, 0);
    analogWrite(rechts_v, 0);
  }

  else if (links == '1' && vooruit == '0' && rechts == '0' && achteruit == '0') { //scherp links 0010
    analogWrite(links_a, 0);
    analogWrite(rechts_v, speed);
    analogWrite(links_v, 0);
    analogWrite(rechts_a, 0);
  }

  else if (rechts == '1' && links == '0' && vooruit == '0' && achteruit == '0') { //scherp rechts 0001
    analogWrite(rechts_a, 0);
    analogWrite(links_v, speed);
    analogWrite(rechts_v, 0);
    analogWrite(links_a, 0);
  }
  else if (links == '1' && vooruit == '1' && achteruit == '0' && rechts == '0') { //links vooruit 1010
    analogWrite(links_v, (int) (speed * 0.5));
    analogWrite(rechts_v, speed);
    analogWrite(links_a, 0);
    analogWrite(rechts_a, 0);
  }
  else if (rechts == '1' && vooruit == '1' && links == '0' && achteruit == '0') { //rechts vooruit 1001
    analogWrite(rechts_v, (int) (speed * 0.5));
    analogWrite(links_v, speed);
    analogWrite(rechts_a, 0);
    analogWrite(links_a, 0);
  }
  else if (links == '1' && achteruit == '1' && rechts == '0' && vooruit == '0') { //links achteruit 0110
    analogWrite(rechts_a, speed);
    analogWrite(links_a, (int) (speed * 0.5));
    analogWrite(rechts_v, 0);
    analogWrite(links_v, 0);
  }
  else if (rechts == '1' && achteruit == '1' && links == '0' && vooruit == '0') { //rechts achteruit 0101
    analogWrite(links_a, speed);
    analogWrite(rechts_a, (int) (speed * 0.5));
    analogWrite(links_v, 0);
    analogWrite(rechts_v, 0);
  }
  else if (vooruit == '1' && achteruit == '1' && links == '0' && rechts == '0') { //stop 1100
    analogWrite(rechts_v, 0);
    analogWrite(rechts_a, 0);
    analogWrite(links_v, 0);
    analogWrite(links_a, 0);
  }
  else if (vooruit == '0' && achteruit == '0' && rechts == '0' && links == '0') { // stop 0000
    analogWrite(rechts_v, 0);
    analogWrite(rechts_a, 0);
    analogWrite(links_v, 0);
    analogWrite(links_a, 0);
  }
}

bool check_distance() {
  bool x;
  int distance_check = distancemeter();
  Serial.println(distance_check);
  if (distance_check > safety_distance) {
    x = true;
  } else {
    x = false;
  }
  return x;
}


int distancemeter() {
  // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
  //Serial.println(distance);
  return distance;
}
