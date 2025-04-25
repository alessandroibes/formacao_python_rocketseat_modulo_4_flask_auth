from flask import Flask, jsonify, request
from flask_login import LoginManager

from database import db
from models.user import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

# view Login

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return jsonify({ "message": "Autenticação realizada com sucesso" })
    
    return jsonify({ "message": "Credenciais inválidas" }), 400


@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)