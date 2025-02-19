from extensions import db
from datetime import datetime

# Tabela de tarefas
class Tarefa(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    titulo    = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data      = db.Column(db.Date, nullable=False)
    concluida = db.Column(db.Boolean, default=False)

    def __init__(self, titulo, descricao, data):

        # Se o título tiver mais de 100 caracteres, uma exceção é lançada
        if len(str(titulo))>100:
            raise Exception
        
        self.titulo = str(titulo)
        self.descricao = str(descricao)


        # Se a data não estiver no formato que o método de conversão para tipo Date espera, uma exceção é lançada
        try:
            self.data = datetime.strptime(data,"%Y-%m-%d").date()
        except:
            raise Exception

        self.concluida = False
    
    def update(self, titulo, descricao, data):
        # Se o título tiver mais de 100 caracteres, uma exceção é lançada
        if len(str(titulo))>100:
            raise Exception
        
        self.titulo = str(titulo)
        self.descricao = str(descricao)


        # Se a data não estiver no formato que o método de conversão para tipo Date espera, uma exceção é lançada
        try:
            self.data = datetime.strptime(data,"%Y-%m-%d").date()
        except:
            raise Exception

    def update_status(self):
        self.concluida = True


    def toDict(self):
        return {
            "id":self.id,
            "titulo":self.titulo,
            "descricao":self.descricao,
            "data": self.data.strftime('%d/%m/%Y'),
            "concluida":self.concluida
        }