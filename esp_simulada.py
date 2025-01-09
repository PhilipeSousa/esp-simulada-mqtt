import paho.mqtt.client as mqtt
import time 
import random
import json
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente 
load_dotenv()

try:
    porta = int(os.getenv("PORT"))
    topico = os.getenv("TOPIC")
    if not topico:
        raise ValueError("Topico não definido corretamente")
except Exception as e:
    raise RuntimeError(f"Erro ao carregar varriaveis do .env: {e}")

# Config Broker
broker = "test.mosquitto.org"

#print(f"Conectando ao broker {broker} na porta {porta} e no tópico {topico}")
