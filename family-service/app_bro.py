import pika
import time
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [BIG-BROTHER] %(message)s',
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
    logging.info(f"Escuchando los pensamientos de Ana: {msg}")
    logging.info("Baa... otro tonto persiguiendo a mi hermana 😒 (Solo logueando desaprobación)\n")

connection = connect()
channel = connection.channel()

channel.exchange_declare(exchange='girl-thinking', exchange_type='fanout')
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='girl-thinking', queue=queue_name)

logging.info("Big Brother está espiando los pensamientos de Ana...")
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()