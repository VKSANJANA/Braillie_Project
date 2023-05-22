const unsigned int pi_zero = 2;
const unsigned int power = 3;
const unsigned int fet = 4;

unsigned int status = 0;  // status 1 when pi zero is off

void setup()
{
  Serial.begin(115200);
  pinMode(power, INPUT);
  pinMode(pi_zero, OUTPUT);
  pinMode(fet, OUTPUT);

  digitalWrite(fet, HIGH);
  digitalWrite(pi_zero, HIGH);
  status = 0;
}

void loop()
{
  if(digitalRead(power))
  {
    if(status)
    {
      digitalWrite(fet, HIGH);
      digitalWrite(pi_zero, HIGH); 
      status = 0;
    }
  }
  else
  {
    digitalWrite(pi_zero, LOW);
    delay(5000);
    digitalWrite(fet, LOW);
    status = 1;
  }
}
