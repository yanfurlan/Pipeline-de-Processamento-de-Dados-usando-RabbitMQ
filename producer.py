
import pika
import json
import requests

def extract_data():
    # Exemplo de chamada a uma API de dados de vendas (substitua com sua fonte)
    response = requests.get('https://api.exemplo.com/vendas')
    return response.json()

def send_to_queue(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Cria a fila se não existir
    channel.queue_declare(queue='raw_data')

    # Publica os dados brutos na fila
    channel.basic_publish(exchange='',
                          routing_key='raw_data',
                          body=json.dumps(data))
    print(" [x] Dados enviados para raw_data")
    connection.close()

if __name__ == '__main__':
    data = extract_data()
    send_to_queue(data)
