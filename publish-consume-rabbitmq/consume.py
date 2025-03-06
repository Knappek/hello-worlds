import pika
import time
import os

# RabbitMQ connection URI
AMQP_URI = os.getenv("RABBITMQ_URI", "amqp://e5a1134a-9db0-4884-9a7a-e75df6521ef7:70F97fhSllXjLZnZ_DZm3T3X@tcp.172.30.7.140.nip.io:17000/af2ba650-4f96-4ade-99c4-0a25c0680ce9")

# Establish connection and channel
params = pika.URLParameters(AMQP_URI)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declare queue
queue_name = 'test_queue'
channel.queue_declare(queue=queue_name, durable=True)

def callback(ch, method, properties, body):
    print(f"[x] Received {body.decode()}")
    time.sleep(1)  # Simulate processing time
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Consume messages
channel.basic_consume(queue=queue_name, on_message_callback=callback)
print('[*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
