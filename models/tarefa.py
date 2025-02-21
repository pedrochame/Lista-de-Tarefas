from extensions import db
from datetime import datetime

# Tabela de tarefas
class Tarefa(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    titulo    = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data      = db.Column(db.Date, nullable=False)
    concluida = db.Column(db.Boolean, default=False)

    def __init__(self, titulo, descricao, data):

        # O campo TÍTULO no banco de dados possui tamanho 100, então somente os 100 primeiros caracteres são incluídos
        self.titulo = str(titulo)[0:100]
        
        self.descricao = str(descricao)


        # Se a data não estiver no formato que o método de conversão para tipo Date espera, uma exceção é lançada
        try:
            self.data = datetime.strptime(data,"%Y-%m-%d").date()
        except ValueError:
            raise ValueError("A data "+data+" deve estar no formato YYYY-MM-DD")

        self.concluida = False
    
    def update(self, titulo, descricao, data):

        # O campo TÍTULO no banco de dados possui tamanho 100, então somente os 100 primeiros caracteres são incluídos
        self.titulo = str(titulo)[0:100]

        self.descricao = str(descricao)


        # Se a data não estiver no formato que o método de conversão para tipo Date espera, uma exceção é lançada
        try:
            self.data = datetime.strptime(data,"%Y-%m-%d").date()
        except ValueError:
            raise ValueError("A data "+data+" deve estar no formato YYYY-MM-DD")

    def update_status(self):
        self.concluida = not self.concluida


    def toDict(self):
        return {
            "id":self.id,
            "titulo":self.titulo,
            "descricao":self.descricao,
            "data": self.data.strftime('%d/%m/%Y'),
            "concluida":self.concluida
        }