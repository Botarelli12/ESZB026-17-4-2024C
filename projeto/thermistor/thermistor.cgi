#!/usr/bin/env python3
import cgi
import cgitb
import json
import datetime
import matplotlib.pyplot as plt

# Ativar a depuração de erros CGI
cgitb.enable()

# Caminho do arquivo JSON com os dados registrados
DATA_FILE = "/tmp/temperature_data.json"

# Função para carregar os dados do arquivo JSON
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Função para criar o gráfico de temperatura
def create_temperature_chart(data):
    timestamps = [entry["time"] for entry in data]
    temperatures = [entry["temperature"] for entry in data]
    
    # Configuração do gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, temperatures, marker="o", linestyle="-", color="b")
    plt.xlabel("Horário", fontsize=12)
    plt.ylabel("Temperatura (°C)", fontsize=12)
    plt.title("Medições de Temperatura ao Longo do Tempo", fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    
    # Salva o gráfico como uma imagem
    plt.savefig("/tmp/temperature_chart.png")
    plt.close()

# Geração da página HTML
def generate_html(data):
    # Garante que há dados disponíveis
    if not data:
        return """
        <html>
        <head><title>Relatório de Temperatura</title></head>
        <body>
        <h1>Relatório de Temperatura</h1>
        <p>Sem dados disponíveis no momento.</p>
        </body>
        </html>
        """
    
    # Dados da última medição
    last_entry = data[-1]
    current_temp = last_entry["temperature"]
    current_status = last_entry["status"]
    last_time = last_entry["time"]
    
    # Cria o gráfico atualizado
    create_temperature_chart(data)
    
    # Gera o HTML com os dados e o gráfico
    return f"""
    <html>
    <head>
        <title>Relatório de Temperatura</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>Relatório de Temperatura</h1>
        <p><strong>Horário da última medição:</strong> {last_time}</p>
        <p><strong>Temperatura atual:</strong> {current_temp:.2f} °C</p>
        <p><strong>Status:</strong> {current_status}</p>
        <h2>Gráfico de Temperatura</h2>
        <img src="/tmp/temperature_chart.png" alt="Gráfico de Temperatura">
    </body>
    </html>
    """

# Carregar dados do arquivo JSON
data = load_data()

# Gera a saída HTML
print("Content-type: text/html\n")
print(generate_html(data))
