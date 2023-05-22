#include <Arduino.h>  // Comment line if using arduino ide or .ino file 

#define clk 3
#define data_l 7
#define data_r 6
#define oe_l 8
#define oe_r 9
#define strobe_l 5
#define strobe_r 4

byte in_r = 0b11110000;
byte in_l = 0b00001111;
boolean state = true;

void setup() 
{
  Serial.begin(9600);

  pinMode(clk, OUTPUT);
  pinMode(data_l, OUTPUT);
  pinMode(data_r, OUTPUT);
  pinMode(oe_l, OUTPUT);
  pinMode(oe_r, OUTPUT);
  pinMode(strobe_l, OUTPUT);
  pinMode(strobe_r, OUTPUT);

  digitalWrite(data_l, LOW);
  digitalWrite(data_r, LOW);
  digitalWrite(strobe_l, HIGH);
  digitalWrite(strobe_r, HIGH);
  digitalWrite(oe_l, HIGH);
  digitalWrite(oe_r, HIGH);
  digitalWrite(clk, LOW);
}

byte swap(int pos_1, int pos_2, byte data)
{
  byte mask = ~((1<<pos_1) | (1<<pos_2));
  byte temp_1 = data & 1<<pos_1;
  byte temp_2 = data & 1<<pos_2;
  int diff = pos_1 - pos_2;
  data &= mask;
  if(diff>0)
  {
    data |= (temp_1>>diff) | (temp_2<<diff);
  }
  else
  {
    diff = -diff;
    data |= (temp_1<<diff) | (temp_2>>diff);
  }
  return data;
}

byte correct_data(int position[], byte data)
{
  byte correction = 0b00000000;
  for(int i = 0; i < 3; i++)
  {
    correction |= (1<<position[i]);
  }
  return data ^ correction;
}

byte map(byte data)
{
  int map_array[] = {7, 5, 3, 6, 4, 2, 1, 0};
  byte data_mapped = 0b00000000;
  for(int i=0; i<8; i++)
    data_mapped |= ((data>>i)&1)<<map_array[i];
  return data_mapped;
}


void loop() 
{
  if(state == true)
  {
    in_r = map(in_r);
    in_l = map(in_l);
    in_l = swap(0, 1, in_l);
    in_l = swap(2, 3, in_l);

    digitalWrite(strobe_l, LOW);
    shiftOut(data_l, clk, LSBFIRST, in_r);
    shiftOut(data_l, clk, LSBFIRST, in_l);
    digitalWrite(strobe_l, HIGH);
  
    digitalWrite(strobe_r, LOW); 
    shiftOut(data_r, clk, LSBFIRST, ~(in_r));
    shiftOut(data_r, clk, LSBFIRST, ~(in_l));
    digitalWrite(strobe_r, HIGH);

    for(int i = 3; i >0; i--)
    {
      delay(5);
      digitalWrite(oe_l, LOW);
      digitalWrite(oe_r, LOW);
      delay(15);
      digitalWrite(oe_l, HIGH);
      digitalWrite(oe_r, HIGH);
    }
    state = false;
  }
}

/*
void loop() 
{
  //in_r = map(in_r);
  //in_l = map(in_l);
  in_l = swap(0, 1, in_l);
  in_l = swap(2, 3, in_l);

  digitalWrite(strobe_l, LOW);
  shiftOut(data_l, clk, LSBFIRST, in_r);
  shiftOut(data_l, clk, LSBFIRST, in_l);
  digitalWrite(strobe_l, HIGH);

  digitalWrite(strobe_r, LOW); 
  shiftOut(data_r, clk, LSBFIRST, ~(in_r));
  shiftOut(data_r, clk, LSBFIRST, ~(in_l));
  digitalWrite(strobe_r, HIGH);
  for(int i = 3; i >0; i--)
  {
    delay(5);
    digitalWrite(oe_l, LOW);
    digitalWrite(oe_r, LOW);
    delay(15);
    digitalWrite(oe_l, HIGH);
    digitalWrite(oe_r, HIGH);
  }

  delay(2000);
  in_r = ~ in_r;
  in_l = ~ in_l;
}*/
