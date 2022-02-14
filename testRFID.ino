#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define L_GRANTED 8
#define L_DENIED 7
MFRC522 mfrc522(SS_PIN, RST_PIN);
byte actualUID[4];
byte authorizedCard1[4] = {0x9A, 0xC5, 0x4E, 0xBF} ;
//byte authorizedCard2[4] = {};

//Available cards
//blue one 
//37 190 17 83

//white card
//160 39 112 55

//https://circuitdigest.com/microcontroller-projects/login-to-windows-computers-using-rc522-rfid-tag-and-arduino

void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT);
  pinMode(7,OUTPUT);
  SPI.begin();                                                                                            
  mfrc522.PCD_Init();
  //Serial.println("RFID Reader Initialized");
}
void loop() {
  //Turn off leds to start clean implementation
  digitalWrite(L_DENIED,LOW);
  digitalWrite(L_GRANTED,LOW);
  int decrypt_data = 0;
  int temp_decrypt_data = -1;

  if(! mfrc522.PICC_IsNewCardPresent())
  return;
  if(!  mfrc522.PICC_ReadCardSerial())
  return;

  for(byte i=0; i < mfrc522.uid.size; i++){
    //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    //Serial.print(mfrc522.uid.uidByte[i], HEX);
    actualUID[i] = mfrc522.uid.uidByte[i];
  } 
  if( compareArray(actualUID, authorizedCard1 )){
    //Dummy test to check read of card
    //Serial.println("Access granted");
    decrypt_data = 1;
    digitalWrite(L_DENIED,LOW);
    digitalWrite(L_GRANTED,HIGH);
    //Serial.print('ID:');
    //send_tag_val(rfid.serNum);
    //Serial.println(' ');
    //Serial.println(rfidCard);
    Serial.write(decrypt_data);
  }
  else{
    //Dummy test to check read of card
    decrypt_data = 0;
    digitalWrite(L_GRANTED,LOW);
    //Serial.println("AccessDenied");
    digitalWrite(L_DENIED,HIGH);
    //Serial.println(' ');
    //Serial.println(rfidCard);
    Serial.write(decrypt_data);
  }
   mfrc522.PICC_HaltA();
}

void send_tag_val (byte *buff, byte bufferSize)
{
   Serial.print("ID:");
   String rfidCard = " ";

   byte byteArray[bufferSize];
   strcpy((char *)byteArray, buff);
   String rfiCard = String((char *)byteArray);
   //Serial.print(rfiCard);
   for (byte i = 0; i < bufferSize; i++)
  {
     
     //Serial.print(rfidCard);
     //Serial.print(" ");
   
  }
   //Serial.print(0, DEC);
   //Serial.print(card);
   //Serial.print(">");
}


//Función para comparar dos vectores
 boolean compareArray(byte array1[],byte array2[])
{
  if(array1[0] != array2[0])return(false);
  if(array1[1] != array2[1])return(false);
  if(array1[2] != array2[2])return(false);
  if(array1[3] != array2[3])return(false);
  return(true);
}
