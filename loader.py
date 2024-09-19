
import pika
import json
import pandas as pd
from sqlalchemy import create_engine

def load_data_to_db(data):
    # Conectar ao banco de dados (substitua com suas credenciais)
    engine = create_engine('sqlite:///vendas.db')
    
    # Converte os dados para DataFrame
    df = pd.DataFrame(data)
    
    # Insere os dados no banco de dados
    df.to_sql('vendas', engine, if_exists='append', index=False)
    print(" [x] Dados carregados no banco de dados")

def callback(ch, method, properties, body):
    data = json.loads(body)
    load_data_to_db(data)
    
    # Confirma que a mensagem foi processada
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_loader():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Cria a fila transformed_data se não existir
    channel.queue_declare(queue='transformed_data')

    # Consome mensagens da fila transformed_data
    channel.basic_consume(queue='transformed_data', on_message_callback=callback, auto_ack=False)
    
    print(" [*] Aguardando mensagens de transformed_data")
    channel.start_consuming()

if __name__ == '__main__':
    start_loader()
