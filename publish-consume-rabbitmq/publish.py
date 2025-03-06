import pika
import os
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Read RabbitMQ connection URI from environment variable
AMQP_URI = os.getenv("RABBITMQ_URI", "amqp://e5a1134a-9db0-4884-9a7a-e75df6521ef7:70F97fhSllXjLZnZ_DZm3T3X@tcp.172.30.7.140.nip.io:17000/af2ba650-4f96-4ade-99c4-0a25c0680ce9")

# Publisher function
def publish_message(message):
    params = pika.URLParameters(AMQP_URI)
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
