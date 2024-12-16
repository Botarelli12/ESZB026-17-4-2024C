#!/usr/bin/env python3
import cgi
import cgitb
import json
import datetime
import matplotlib.pyplot as plt

# Ativar a depuração de erros CGI
cgitb.enable()

DATA_FILE = "/tmp/temperature_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def create_temperature_chart(data):
    timestamps = [entry["time"] for entry in data]
    temperatures = [entry["temperature"] for entry in data]
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, temperatures, marker="o", linestyle="-", color="b")
    plt.xlabel("Horário", fontsize=12)
    plt.ylabel("Temperatura (°C)", fontsize=12)
    plt.title("Medições de Temperatura ao Longo do Tempo", fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("/tmp/temperature_chart.png")
    plt.close()

def generate_html(data):
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
    last_entry = data[-1]
    current_temp = last_entry["temperature"]
    current_status = last_entry["status"]
    last_time = last_entry["time"]
    create_temperature_chart(data)
    rows = "".join(
        f"<tr><td>{entry['time']}</td><td>{entry['temperature']:.2f}</td><td>{entry['status']}</td></tr>"
        for entry in data[-10:]
    )
    return f"""
    <html>
    <head>
        <title>Relatório de Temperatura</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            p, table {{ font-size: 14px; line-height: 1.6; }}
            img {{ max-width: 100%; height: auto; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
            th {{ background-color: #f4f4f4; }}
        </style>
    </head>
    <body>
        <h1>Relatório de Temperatura</h1>
        <p><strong>Horário da última medição:</strong> {last_time}</p>
        <p><strong>Temperatura atual:</strong> {current_temp:.2f} °C</p>
        <p><strong>Status:</strong> {current_status}</p>
        <h2>Gráfico de Temperatura</h2>
        <img src="/tmp/temperature_chart.png" alt="Gráfico de Temperatura">
        <h2>Últimas 10 Medições</h2>
        <table>
            <tr>
                <th>Horário</th>
                <th>Temperatura (°C)</th>
                <th>Status</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

data = load_data()
print("Content-type: text/html\n")
print(generate_html(data))

