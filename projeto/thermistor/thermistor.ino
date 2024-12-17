#include "Thermistor.h" // Inclusão da biblioteca para leitura do termistor

#define LED 9           // Pino digital do LED
#define BUZ 8           // Pino digital do buzzer
#define LIMITE_SUP 30   // Limite superior da faixa de temperatura
#define LIMITE_INF 25   // Limite inferior da faixa de temperatura

Thermistor temp(2);     // Objeto Thermistor no pino analógico A2

bool buzzer_ativado = false; // Variável para controlar o estado do buzzer

void setup() {
  Serial.begin(9600);   // Inicializa a comunicação serial
  delay(1000);          // Espera 1 segundo para estabilizar
  pinMode(LED, OUTPUT);
  pinMode(BUZ, OUTPUT);
}

void loop() {
  float temperature = temp.getTemp(); // Lê a temperatura do sensor
  //Serial.print("Temperatura: ");
  Serial.println(temperature);
  //Serial.println("°C");

  // Verifica se a temperatura está fora da faixa aceitável
  if (temperature <= LIMITE_INF || temperature >= LIMITE_SUP) {
    //Serial.println("Alerta! Temperatura fora da faixa aceitável.");
    digitalWrite(LED, HIGH); // Liga o LED
    
    // Emite um único bip se o buzzer ainda não foi ativado
    if (!buzzer_ativado) {
      digitalWrite(BUZ, HIGH);
      delay(200);          // Duração do bip
      digitalWrite(BUZ, LOW);
      buzzer_ativado = true; // Marca que o buzzer já foi ativado
    }
  } else {
    // Temperatura está normal
    //Serial.println("Temperatura normal.");
    digitalWrite(LED, LOW);   // Desliga o LED
    buzzer_ativado = false;   // Reseta o estado do buzzer
  }

  delay(100); // Intervalo de 1 segundo
}
