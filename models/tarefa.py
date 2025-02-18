from extensions import db
from datetime import datetime
from utils import converteData

# Tabela de tarefas
class Tarefa(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    titulo    = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data      = db.Column(db.Date, nullable=False)
    concluida = db.Column(db.Boolean, default=False)

    def __init__(self, titulo, descricao, data, concluida=False):
        self.titulo = str(titulo)
        self.descricao = str(descricao)
        self.data = datetime.strptime(data,"%Y-%m-%d").date()
        self.concluida = bool(concluida)
    
    def update(self, titulo, descricao, data):
        self.titulo = str(titulo)
        self.descricao = str(descricao)
        self.data = datetime.strptime(data,"%Y-%m-%d").date()


    def toDict(self):
        return {
            "id":self.id,"titulo":self.titulo,
            "descricao":self.descricao,
            "data": self.data.strftime('%d/%m/%Y'),
            "concluida":self.concluida
        }