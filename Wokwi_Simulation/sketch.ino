int button = 2;
int led = 8;
int buzzer = 9;

unsigned long pressTime = 0;

void setup() {
  pinMode(button, INPUT_PULLUP);
  pinMode(led, OUTPUT);
  pinMode(buzzer, OUTPUT);
}

void loop() {

  if (digitalRead(button) == LOW) {

    if (pressTime == 0) {
      pressTime = millis();
    }

    unsigned long duration = millis() - pressTime;

    if (duration < 2000) {
      // NORMAL
      digitalWrite(led, LOW);
      noTone(buzzer);
    }

    else if (duration < 4000) {
      // DROWSY
      digitalWrite(led, HIGH);
      noTone(buzzer);
    }

    else if (duration < 6000) {
      // WARNING
      digitalWrite(led, HIGH);
      tone(buzzer, 1000);
      delay(500);
      noTone(buzzer);
      delay(500);
    }

    else {
      // CRITICAL
      digitalWrite(led, HIGH);
      tone(buzzer, 2000);
    }

  } else {
    // RESET
    pressTime = 0;
    digitalWrite(led, LOW);
    noTone(buzzer);
  }

}