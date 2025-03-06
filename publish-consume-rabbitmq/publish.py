import pika
import os
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

AMQP_URI = os.getenv("RABBITMQ_URI")
if not AMQP_URI:
    raise ValueError("RABBITMQ_URI environment variable is not set")

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
