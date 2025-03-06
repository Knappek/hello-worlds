# Publish & Consume from RabbitMQ

A simple web app to publish messages to RabbitMQ and a simple consumer to read the published messages.

## Prerequisites

- a RabbitMQ server and its external `uri` endpoint

## Run it

Start the publisher web app:

```shell
export RABBITMQ_URI=amqp://<username>:<password>@<host>:<port>/<vhost> # amqps:// if SSL is enabled
# option if SSL is enabled and you need to provide a ca certificate
export RABBITMQ_CA_CERT_PATH=/path/to/ca.crt
python3 publish.py
```

In another shell start the consumer:

```shell
export RABBITMQ_URI=amqp://<username>:<password>@<host>:<port>/<vhost> # amqps:// if SSL is enabled
# option if SSL is enabled and you need to provide a ca certificate
export RABBITMQ_CA_CERT_PATH=/path/to/ca.crt
python3 consume.py
```

Then publish some messages:

```shell
curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:5000/send  -d '{"message": "Hello RabbitMQ"}'
```
