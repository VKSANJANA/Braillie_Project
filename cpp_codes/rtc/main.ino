#include <DS3231.h>

DS3231  rtc(A4, A5);

void initialize()
{
  rtc.setDOW(SUNDAY);
  rtc.setDate(21, 5, 2023);
  rtc.setTime(18, 4, 3);
}

void setup()
{
  Serial.begin(9600);
  rtc.begin();
  //initialize();
  Serial.println("Initialized");
}

void loop()
{
  Serial.print(rtc.getDOWStr());
  Serial.print(" ");
  Serial.print(rtc.getDateStr());
  Serial.print(" ");
  Serial.println(rtc.getTimeStr());
  delay (1000);
}
