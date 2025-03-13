import pika
import os
import ssl
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

AMQP_URI = os.getenv("RABBITMQ_URI")
if not AMQP_URI:
    raise ValueError("RABBITMQ_URI environment variable is not set")

params = pika.URLParameters(AMQP_URI)
ssl_options = None
if AMQP_URI.startswith("amqps"):
    ca_cert_path = os.getenv("RABBITMQ_CA_CERT_PATH")
    ssl_context = ssl.create_default_context(cafile=ca_cert_path) if ca_cert_path else ssl.create_default_context()
    ssl_options = pika.SSLOptions(ssl_context)

    # # skip verification
    # ssl_context = ssl.create_default_context()
    # ssl_context.check_hostname = False
    # ssl_context.verify_mode = ssl.CERT_NONE
    # ssl_options = pika.SSLOptions(ssl_context)
    print(f"[i] using SSL")
    
if ssl_options:
    params.ssl_options = ssl_options

def publish_message(message):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    queue_name = 'test_queue'
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2  # Make message persistent
                          ))
    connection.close()
    print(f"[x] Sent '{message}'")

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    message = data.get("message", "Default message")
    publish_message(message)
    return jsonify({"status": "Message sent", "message": message})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
