import pika
import time
import logging
import threading
import os

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [GIRL] %(message)s',
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


def on_proposal(ch, method, properties, body):
    msg = body.decode()
    logging.info(f"💖 Escuchó propuesta: {msg}")

    channel.exchange_declare(exchange='girl-thinking', exchange_type='fanout')
    channel.basic_publish(
        exchange='girl-thinking',
        routing_key='',
        body=msg.encode()
    )
    logging.info(f"🔔 Ana está pensando... Notificando a la familia con: {msg}")
    
def on_final_decision(ch, method, properties, body):
    msg = body.decode()
    if "APPROVED" in msg.upper():
        logging.info(f"💍 Ana: ¡Sí acepto! La Saga ha finalizado con éxito. ({msg})")
    elif "REJECTED" in msg.upper():
        logging.info(f"💔 Ana: Corazón roto... La Saga finalizó con rechazo. ({msg})")
    else:
        logging.info(f"Resultado desconocido: {msg}")


def start_decision_consumer():
    conn = connect()
    ch = conn.channel()
    
    exchange_name = 'romantic-decision'
    ch.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    result = ch.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    ch.queue_bind(exchange=exchange_name, queue=queue_name)
    
    logging.info(f"[DECISION-THREAD] Escuchando final en '{exchange_name}'")
    ch.basic_consume(queue=queue_name, on_message_callback=on_final_decision, auto_ack=True)
    ch.start_consuming()


connection = connect()
channel = connection.channel()

threading.Thread(target=start_decision_consumer, daemon=True).start()

channel.exchange_declare(exchange='romantic-proposal', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='romantic-proposal', queue=queue_name)

logging.info("Esperando propuestas de amor... 💘")
channel.basic_consume(queue=queue_name, on_message_callback=on_proposal, auto_ack=True)
channel.start_consuming()