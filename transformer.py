
import pika
import json
import pandas as pd

def transform_data(data):
    # Exemplo de transformação (limpeza e normalização)
    df = pd.DataFrame(data)
    
    # Exemplo: converter valores para numérico
    df['vendas'] = pd.to_numeric(df['vendas'], errors='coerce')
    
    # Retorna dados transformados como dicionário
    return df.to_dict(orient='records')

def callback(ch, method, properties, body):
    data = json.loads(body)
    transformed_data = transform_data(data)
    
    # Enviar os dados transformados para a próxima fila
    send_to_next_queue(transformed_data)

    # Confirma que a mensagem foi processada
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(" [x] Dados transformados e enviados para transformed_data")

def send_to_next_queue(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Cria a fila transformed_data se não existir
    channel.queue_declare(queue='transformed_data')

    # Publica os dados transformados na fila
    channel.basic_publish(exchange='',
                          routing_key='transformed_data',
                          body=json.dumps(data))
    connection.close()

def start_transformer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Cria a fila raw_data se não existir
    channel.queue_declare(queue='raw_data')

    # Consome mensagens da fila raw_data
    channel.basic_consume(queue='raw_data', on_message_callback=callback, auto_ack=False)
    
    print(" [*] Aguardando mensagens de raw_data")
    channel.start_consuming()

if __name__ == '__main__':
    start_transformer()
