#include "Thermistor.h" //INCLUSÃO DA BIBLIOTECA

#define LED 9
#define BUZ 8
#define limite 30

Thermistor temp(2); //VARIÁVEL DO TIPO THERMISTOR, INDICANDO O PINO ANALÓGICO (A2) EM QUE O SENSOR ESTÁ CONECTADO
void setup() {
  Serial.begin(9600); //INICIALIZA A SERIAL
  delay(1000); //INTERVALO DE 1 SEGUNDO
  pinMode(LED, OUTPUT);
  pinMode(BUZ, OUTPUT);
}
void loop() {
  float temperature = temp.getTemp(); //VARIÁVEL DO TIPO INTEIRO QUE RECEBE O VALOR DE TEMPERATURA CALCULADO PELA BIBLIOTECA
  Serial.print("Temperatura: "); //IMPRIME O TEXTO NO MONITOR SERIAL
  Serial.print(temperature); //IMPRIME NO MONITOR SERIAL A TEMPERATURA MEDIDA
  Serial.println("*C"); //IMPRIME O TEXTO NO MONITOR SERIAL
  
  if (temperature >= limite){
    digitalWrite(LED, HIGH);
    digitalWrite(BUZ, HIGH);
  }
  else{
    digitalWrite(LED, LOW);
    digitalWrite(BUZ, LOW);
  }
  delay(100); //INTERVALO DE 1 SEGUNDO
}
