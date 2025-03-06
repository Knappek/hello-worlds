import pika
import time
import os

AMQP_URI = os.getenv("RABBITMQ_URI")
if not AMQP_URI:
    raise ValueError("RABBITMQ_URI environment variable is not set")

params = pika.URLParameters(AMQP_URI)
connection = pika.BlockingConnection(params)
channel = connection.channel()

queue_name = 'test_queue'
channel.queue_declare(queue=queue_name, durable=True)

def callback(ch, method, properties, body):
    print(f"[x] Received {body.decode()}")
    time.sleep(1)  # Simulate processing time
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue=queue_name, on_message_callback=callback)
print('[*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
