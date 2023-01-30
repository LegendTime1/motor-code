int Pwm1 = 10; //Nodemcu PWM pin
int Pwm2 = 8; //Nodemcu PWM pin

int dir1 = 11;  //Gpio-12 of nodemcu esp8266
int dir2 = 9;  //Gpio-13 of nodemcu esp8266

int dirVal1 = 0 ;
int dirVal2 = 0 ;
int pwmVal1 = 0 ;
int pwmVal2 = 0 ;


String incomingbyte;  
int m1Data = 0;
int m2Data = 0;
int inpSpeed = 0;
//char message;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  //Declaring l293d control pins as Output
  pinMode(dir1, OUTPUT);
  pinMode(dir2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
 // Serial.println(1);
 /*while(true){
  Serial.print(Serial.available());
  Serial.print("\n");
 }*/

  if(Serial.available() > 0){
//    time_t t;
//    time(&t);
//    Serial.print(myTime);
    incomingbyte = Serial.readStringUntil('\n');
    

      
//    inpSpeed = incomingbyte.toInt(); //int() or whatever datatype you neeed toc convert to. Converting ASCII to integer
    //Serial.print("I received : ");
    Serial.println(incomingbyte);
    //analogWrite(6, incomingbyte.toInt());

    m1Data = incomingbyte.substring(0, 4).toInt();
    //Serial.println(m1Data);
    m2Data = incomingbyte.substring(4).toInt();
    //Serial.println(m2Data);
    //Serial.write(message);
   // Serial.println(incomingbyte);
    

    if(m1Data>=0){
        dirVal1 = 1;
        pwmVal1 = m1Data;
        
    }

    else if(m1Data<0){
        dirVal1 = 2;
        pwmVal1 = m1Data*(-1);
    }

    if(m2Data>=0){
        dirVal2 = 1;
        pwmVal2 = m2Data;
    }

    else if(m2Data<0){
        dirVal2 = 2;
        pwmVal2 = m2Data*(-1);
    }
  }

  else{
    dirVal1 = dirVal1;
    dirVal2 = dirVal2;
    pwmVal1 = pwmVal1;
    pwmVal2 = pwmVal2;
  }

  if (dirVal1 == 1)
  {
    digitalWrite(dir1, HIGH);
  }
  else if (dirVal1 == 2)
  {
    digitalWrite(dir1, LOW);
  }

  analogWrite(Pwm1, pwmVal1);

//  digitalWrite(dir1, HIGH);
//  analogWrite(Pwm1, 100);

  if (dirVal2 == 1)
  {
    digitalWrite(dir2, HIGH);
  }
  else if (dirVal2 == 2)
  {
    digitalWrite(dir2, LOW);
  }

  analogWrite(Pwm2, pwmVal2);
//  digitalWrite(dir2, HIGH);
//  analogWrite(Pwm2, 100);


}
