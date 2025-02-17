from extensions.database import db
from utils.formatters import converteData

# Tabela de tarefas
class Tarefa(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    titulo    = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data      = db.Column(db.String(10), nullable=False)
    concluida = db.Column(db.Boolean, default=False)

    def toDict(self):
        return {
            "id":self.id,"titulo":self.titulo,
            "descricao":self.descricao,
            "data":converteData(self.data),
            "concluida":self.concluida
        }