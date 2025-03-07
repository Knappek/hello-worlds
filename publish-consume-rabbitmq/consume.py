import pika
import time
import os
import ssl

# Read RabbitMQ connection URI from environment variable
AMQP_URI = os.getenv("RABBITMQ_URI")
if not AMQP_URI:
    raise ValueError("RABBITMQ_URI environment variable is not set")

params = pika.URLParameters(AMQP_URI)
ssl_options = None
if AMQP_URI.startswith("amqps"):
    ca_cert_path = os.getenv("RABBITMQ_CA_CERT_PATH")
    ssl_context = ssl.create_default_context(cafile=ca_cert_path) if ca_cert_path else ssl.create_default_context()
    ssl_options = pika.SSLOptions(ssl_context)
    params.ssl_options = ssl_options
    print(f"[i] using SSL")

# Establish connection and channel
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
