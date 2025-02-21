from flask import Flask
from routes import tarefa_bp
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)

    # Aplicando configurações
    app.config.from_object(Config)

    # Inicializando banco de dados
    db.init_app(app)

    #Registrando Blueprint das rotas de tarefa
    app.register_blueprint(tarefa_bp)

    return app

# Ao executar o aplicativo, o banco de dados é criado, se já não existir
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=app.config["DEBUG"])