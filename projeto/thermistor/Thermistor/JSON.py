import serial
import json
import datetime
import time
import logging

# Configurações
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600
TIMEOUT = 2
DATA_FILE = "/tmp/temperature_data.json"
MAX_ENTRIES = 1000

# Configuração de logs
logging.basicConfig(
    filename="/var/log/temperature_monitor.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Funções para carregar e salvar dados
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Monitoramento da temperatura
def monitor_temperature():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
            print(f"Conectado à porta serial {SERIAL_PORT} com baud rate {BAUD_RATE}.")
            while True:
                try:
                    # Lê e tenta interpretar os dados
                    line = ser.readline().decode("utf-8").strip()
                    try:
                        temperature = float(line)
                    except ValueError:
                        print("Erro: Valor recebido não é um número válido.")
                        continue

                    # Avalia status
                    status = "Normal" if 25 <= temperature <= 30 else "Alerta"

                    # Registra a leitura
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_entry = {
                        "time": current_time,
                        "temperature": temperature,
                        "status": status,
                    }

                    # Atualiza o histórico
                    data = load_data()
                    if len(data) >= MAX_ENTRIES:
                        data.pop(0)  # Remove o registro mais antigo
                    data.append(new_entry)
                    save_data(data)

                    # Log e console
                    logging.info(f"Temperatura: {temperature:.2f}°C | Status: {status}")
                    print(f"[{current_time}] Temperatura: {temperature:.2f}°C | Status: {status}")

                except ValueError:
                    print("Erro: Linha recebida não pôde ser processada.")
                time.sleep(1)

    except serial.SerialException as e:
        logging.error(f"Erro na comunicação serial: {e}")
        print(f"Erro na comunicação serial: {e}")

if __name__ == "__main__":
    monitor_temperature()
