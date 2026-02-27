import requests
import time
import random

# Santos é quente (30°C) e úmido (40%)
TEMP_AMBIENTE = 30.0
HUM_AMBIENTE = 40
URL_DADOS = "http://127.0.0.1:5000/api/dados"
URL_CONFIG = "http://127.0.0.1:5000/api/config"

temp_atual = TEMP_AMBIENTE
hum_atual = HUM_AMBIENTE

while True:
    try:
        # Busca limites do servidor
        res = requests.get(URL_CONFIG)
        lim = res.json()
        
        # --- SIMULAÇÃO DE FÍSICA REAL (Oscilação) ---
        # Perda de calor natural para o ambiente (Santos)
        temp_atual -= (temp_atual - TEMP_AMBIENTE) * 0.0015
        # Perda/Ganho de umidade para o ambiente
        hum_atual -= (hum_atual - HUM_AMBIENTE) * 0.001
        
        # Controle do Aquecedor
        heater = "OFF"
        if temp_atual < lim['t_min']:
            heater = "ON"
            temp_atual += random.uniform(0.1, 0.2) # Potência do aquecimento
            
        # Controle do Umidificador
        humidifier = "OFF"
        if hum_atual < lim['h_min']:
            humidifier = "ON"
            hum_atual += random.uniform(0.2, 0.5)

        # Envio dos dados
        requests.post(URL_DADOS, json={
            "temp": round(temp_atual, 2), "hum": round(hum_atual, 2),
            "heater": heater, "humidifier": humidifier, "phase": "Simulação Real"
        })
        print(f"Status: Temp:{round(temp_atual,1)} Hum:{round(hum_atual,1)} | Aquecedor:{heater} Humidade:{humidifier}")

    except Exception as e:
        print(f"Conectando ao servidor... {e}")

    time.sleep(5)