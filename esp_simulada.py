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

# Funções de callback do client mqtt 

def se_conectou(client, userdata, flags, rc):
    print(f"Conectado com o codigo rc {rc}")
    client.subscribe(topico)

def nova_mensagem_foi_recebida(client, userdata, msg):
    print(f"Uma mensagem foi recebida no topico {msg.topico}: {msg.payload.decode()}")



# Simulando dados vindos de sensores conectados na ESP

def gera_dados_sensores():
    data = {
        "Temperatura Ambiente": round(random.uniform(20.0, 40.0), 1),
        "Temperatura de Água": round(random.uniform(20.0, 45.0),1),
        "Umidade do ar": round(random.uniform(20, 98),0),
        "TDS": round(random.uniform(200.0, 1000.0),1),
        "Bomba": random.choice(["Ligada", "Desligada"]),
        "LED": random.choice(["Ligada", "Desligada"]),
    }

    return json.dumps(data)

# Conexao e publica de dados

client = mqtt.Client("ESP Simulada ghuehe")
client.on_connect = se_conectou
client.on_messege = nova_mensagem_foi_recebida

client.connect(broker, porta, 60)


# Envio de dados

try:
    while True:
        dados_dos_sensores = gera_dados_sensores()
        print(f"Enviando dados: {dados_dos_sensores}")
        client.publish(topico, dados_dos_sensores)

        # pausa 5 segundos para enviar dnv
        time.sleep(5)
except KeyboardInterrupt:
    print("Conexão encerrada por vc")
finally:
    client.disconnect()
    print("Desconectado do broker")
