#include <Servo.h>

Servo feed;
Servo camX;
Servo camY;

const String CMD_FEED = "FEED";
const String CMD_CAM = "CAM";

void setup() {
  feed.attach(9);
  camX.attach(10);
  camY.attach(11);
  Serial.begin(9600);
  while (!Serial);
}

void loop() {
  if (Serial.available() > 0) {
    String raw = Serial.readString();
    String cmd = toCmd(raw);
    if (cmd == CMD_CAM) {
      int x = toCamCtlX(raw);
      int y = toCamCtlY(raw);
      camX.write(x);
      camY.write(y);
      char res[3];
      sprintf(res, "%d,%d", x, y);
      Serial.println(res);
    } else if (cmd == CMD_FEED) {
      int from = raw.indexOf(":") + 1;
      int d = raw.substring(from, raw.length()).toInt();
      feed.write(d);
      Serial.println(d);
    }
  }
}

String toCmd(String raw) {
  return raw.substring(0, raw.indexOf(":"));
}

int toCamCtlX(String raw) {
  int from = raw.indexOf(":") + 1;
  int to = raw.indexOf(",");
  return raw.substring(from, to).toInt();
}

int toCamCtlY(String raw) {
  int from = raw.indexOf(",") + 1;
  return raw.substring(from, raw.length()).toInt();
}
