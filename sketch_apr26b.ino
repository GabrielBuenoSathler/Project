#include <ESP8266WiFi.h>

#define SSID "NOME DA REDE"
#define PASSWD "SENHA DA REDE"
#define SOCK_PORT 8080
#define ENA   14          // Enable/speed motors Right        GPIO14(D5)
#define ENB   12          // Enable/speed motors Left         GPIO12(D6)
#define IN_1  15          // L298N in1 motors Rightx          GPIO15(D8)
#define IN_2  13          // L298N in2 motors Right           GPIO13(D7)
#define IN_3  2           // L298N in3 motors Left            GPIO2(D4)
#define IN_4  0        
int speedCar = 800;         // 400 - 1023.
int speed_Coeff = 3;// L298N in4 motors Left            GPIO0(D3)



WiFiServer sockServer(SOCK_PORT);


void Forward() 
 {
    
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, speedCar);
      delay(200);
 }

 void  para(){
   digitalWrite(IN_1, LOW);
   digitalWrite(IN_2, LOW);
   digitalWrite(IN_3, LOW);
   digitalWrite(IN_4, LOW);
  
 }

void setup(){
    

    Serial.begin(115200);
    delay(1000);
    WiFi.begin(SSID,PASSWD);
    while (WiFi.status() != WL_CONNECTED){delay(100);}

    Serial.print("IP: ");
    Serial.println(WiFi.localIP());

    sockServer.begin(); //abre a porta 123
     pinMode(ENA, OUTPUT);
     pinMode(ENB, OUTPUT);  
     pinMode(IN_1, OUTPUT);
     pinMode(IN_2, OUTPUT);
     pinMode(IN_3, OUTPUT);
     pinMode(IN_4, OUTPUT); 

}

void loop(){
   uint8_t n1 = 49;
   uint8_t n2 = 50;
   uint8_t n3 = 51;
   uint8_t n4 = 52;
   
    WiFiClient client = sockServer.available();
    if (client){
        while (client.connected()){
            while (client.available() > 0){
                uint8_t c = client.read();
                Serial.write(c);
                if(n1 == c ){
                  Serial.println("Acelera");
                  Forward();
                }
                if (n2 == c ){
              
                   Serial.println("para");
                   para();
                   
                }
               
            }
            delay(10);
        }
        client.stop(); //acabou a leitura dos dados. Finaliza o client.
    }
}
