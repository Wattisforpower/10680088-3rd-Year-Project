

void setup() {
  // put your setup code here, to run once:
  pinMode(A7, OUTPUT);
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  float val = analogRead(A7);
  Serial.println(val);
  delay(1000);
}
