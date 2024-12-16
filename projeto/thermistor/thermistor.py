import serial  # Biblioteca para comunicação serial 
import json
import datetime
import time

# Configuração da porta serial
SERIAL_PORT = "/dev/ttyACM0"  # Altere para a porta correta do Arduino
BAUD_RATE = 9600
TIMEOUT = 2  # Timeout para a comunicação serial

# Caminho do arquivo onde os dados serão armazenados
DATA_FILE = "/tmp/temperature_data.json"

# Função para carregar dados do arquivo JSON
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Retorna uma lista vazia caso o arquivo não exista ou esteja corrompido

# Função para salvar dados no arquivo JSON
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Função principal para monitorar a temperatura
def monitor_temperature():
    try:
        # Inicia a comunicação serial
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
            print(f"Conectado à porta serial {SERIAL_PORT} com baud rate {BAUD_RATE}.")
            while True:
                try:
                    # Lê uma linha da porta serial
                    line = ser.readline().decode("utf-8").strip()

                    # Tenta converter a linha para float
                    try:
                        temperature = float(line)

                        # Verifica o status com base na temperatura
                        status = "Normal" if 25 <= temperature <= 30 else "Alerta"

                        # Armazena os dados
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        new_entry = {
                            "time": current_time,
                            "temperature": temperature,
                            "status": status
                        }

                        # Carrega os dados existentes, adiciona a nova entrada e salva
                        data = load_data()
                        data.append(new_entry)
                        save_data(data)

                        # Exibe os dados no console (para fins de depuração)
                        print(f"[{current_time}] Temperatura: {temperature:.2f}°C | Status: {status}")

                    except ValueError:
                        # Se a conversão falhar, trata o erro e continua
                        print(f"Erro: Valor recebido '{line}' não é um número válido.")

                except ValueError:
                    # Ignora linhas que não possam ser convertidas para float
                    print("Erro: Valor recebido não é um número válido.")
                time.sleep(1)  # Intervalo de 1 segundo entre as leituras

    except serial.SerialException as e:
        print(f"Erro na comunicação serial: {e}")

if __name__ == "__main__":
    monitor_temperature()
