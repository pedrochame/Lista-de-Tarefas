from flask import Flask
from routes import tarefa_bp
from config import Config
from extensions import db

app = Flask(__name__)

# Aplicando configurações
app.config.from_object(Config)

# Inicializando banco de dados
db.init_app(app)

#Registrando Blueprint das rotas de tarefa
app.register_blueprint(tarefa_bp)

# Ao executar o aplicativo, o banco de dados é criado, se já não existir
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=app.config["DEBUG"])