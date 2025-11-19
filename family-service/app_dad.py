import pika
import time
import logging
import random
import os

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [DAD] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')

def connect():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            return connection
        except pika.exceptions.AMQPConnectionError:
            logging.warning("Esperando conexión con RabbitMQ...")
            time.sleep(5)

def callback(ch, method, properties, body):
    msg = body.decode()
    logging.info(f"Escuchó que Ana está considerando: {msg}")
    
    approval = random.choice(["approved", "rejected"])
    response = f"VOTO:DAD:{approval}:{msg}"
    
    channel.basic_publish(
        exchange='romantic-approval',
        routing_key='',
        body=response.encode()
    )

    logging.info(f"🧔 Papá ha votado: {approval}")

connection = connect()
channel = connection.channel()

channel.exchange_declare(exchange='girl-thinking', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='girl-thinking', queue=queue_name)

channel.exchange_declare(exchange='romantic-approval', exchange_type='fanout')

logging.info("Esperando pensamientos de Ana para opinar como papá... 💭🧔")
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()