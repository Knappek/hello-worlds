#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def get_client_ip():
    # Get the X-Forwarded-For header, or fallback to remote address
    forwarded_for = request.headers.get('X-Forwarded-For', request.remote_addr)
    return f'Client IP: {forwarded_for}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

