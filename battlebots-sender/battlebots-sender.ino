#include <RadioHead.h>
#include <RH_ASK.h>
#ifdef RH_HAVE_HARDWARE_SPI
#include <SPI.h> // Not actually used but needed to compile
#endif

RH_ASK driver(1900, 13, 12, 0);


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(100);

  {
    if (!driver.init())
#ifdef RH_HAVE_SERIAL
      Serial.println("init failed");
#else
      ;
#endif
  }

}

void loop() {
  if (Serial.available()) {
    String data = getData();
    commands(data);
    sendData(data);
  }
}

String getData() {
  String data = Serial.readStringUntil('\n');
  return data;
}

void sendData(String data) {
  data += " ";
  byte buf[50];
  data.getBytes(buf, data.length());

  driver.send((uint8_t *)buf, data.length());
  driver.waitPacketSent();
  Serial.println("sent: " + data);
}

void commands(String data) {
  if (data == "on") {
    digitalWrite(LED_BUILTIN, HIGH);
  } else if (data == "off") {
    digitalWrite(LED_BUILTIN, LOW);
  }
}
