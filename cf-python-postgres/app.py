from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
import cfenv

# Load environment variables from Cloud Foundry
postgres_service_name = os.getenv("POSTGRES_SERVICE")

if not postgres_service_name:
    print("you must set the env variable POSTGRES_SERVICE to match your postgres service name")
    exit(1)

app_env = cfenv.AppEnv()
pg_service = app_env.get_service(name=postgres_service_name)

if not pg_service:
    print("PostgreSQL service not found!")
    exit(1)

# Database configuration
db_url = pg_service.credentials["uri"]

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(name=data["name"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id, "name": new_user.name})

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{ "id": user.id, "name": user.name } for user in users])

@app.route("/info", methods=["GET"])
def get_info():
    with db.engine.connect() as connection:
        result = connection.execute(text("SHOW shared_buffers;"))
        shared_buffers = result.fetchone()[0]
    
    info = {
        "app_name": "Python app that consumes Postgres service",
        "database_url": db_url,
        "shared_buffers": shared_buffers
    }
    return jsonify(info)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
