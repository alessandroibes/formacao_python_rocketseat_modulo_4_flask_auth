from flask import Flask, jsonify, request
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user
)

from database import db
from models.user import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
# view Login


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return jsonify({ "message": "Autenticação realizada com sucesso" })
    
    return jsonify({ "message": "Credenciais inválidas" }), 400


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({ "message": "Lougout realizado com sucesso!" })


@app.route("/user", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()        
        return jsonify({ "message": "Usuário cadastrado com sucesso" })

    return jsonify({ "message": "Dados inválidos" }), 400


@app.route("/user/<int:id_user>", methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return { "username": user.username }
    
    return jsonify({ "message": "Usuário não encontrado" }), 404


@app.route("/user/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    new_password = data.get("password")
    if user and new_password:
        user.password = new_password
        db.session.commit()

        return jsonify({ "message": f"Usuário {id_user} atualizado com sucesso" })
    
    return jsonify({ "message": "Usuário não encontrado" }), 404


@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)