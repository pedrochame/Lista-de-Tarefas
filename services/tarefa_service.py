from models import Tarefa
from extensions import db

#Função que valida se os dados recebidos em uma requisição estão com as chaves necessárias e seus respectivos valores preenchidos
def validaDadosRecebidos(dic):

    camposTarefa = {"titulo","descricao","data"}

    if camposTarefa != dic.keys():
        return False
    
    if all(valor not in ["",None] for valor in dic.values()):
        return True
    
    return False

# Função que retorna todos os registros no banco de dados e o status a ser respondido pela rota
def lista_tarefas():
    
    lista = []
    
    for tarefa in Tarefa.query.all():
        lista.append(tarefa.toDict())

    return lista , 200

# Função que retorna um registro do banco de dados pelo ID e o status a ser respondido pela rota
def buscaTarefaPorId(id):
    
    # Com o método get_or_404(), se a tarefa não existir, uma resposta com status 404 é lançada automaticamente
    return Tarefa.query.get_or_404(id).toDict() , 200

# Função que cria um registro no banco de dados, retornando-o junto do status a ser respondido pela rota
def criaTarefa(dados):

    if validaDadosRecebidos(dados) == False:
        return {"erro" : "Todas as informações da tarefa são obrigatórias."} , 400

    titulo    = dados["titulo"]
    descricao = dados["descricao"]
    data      = dados["data"]

    try:
        tarefa = Tarefa(titulo,descricao,data)
    except ValueError as e:
        return { "erro" : str(e) } , 400

    db.session.add(tarefa)
    db.session.commit()
    
    return tarefa.toDict() , 201

# Função que edita um registro no banco de dados, retornando-o junto do status a ser respondido pela rota
def editaTarefa(id, dados):

    if validaDadosRecebidos(dados) == False:
        return {"erro" : "Todas as informações da tarefa são obrigatórias."} , 400
    
    titulo    = dados["titulo"]
    descricao = dados["descricao"]
    data      = dados["data"]

    tarefa = Tarefa.query.get_or_404(id)

    try:
        tarefa.update(titulo,descricao,data)
    except ValueError as e:
        return {"erro" : str(e)} , 400

    db.session.commit()

    return tarefa.toDict() , 200

# Função que deleta um registro do banco de dados, retornando uma mensagem e o status a ser respondido pela rota
def apagaTarefa(id):
    
    tarefa = Tarefa.query.get_or_404(id)
    
    db.session.delete(tarefa)
    db.session.commit()

    return {"mensagem":"Tarefa deletada."} , 200

# Função que altera o campo CONCLUIDA de um registro no banco de dados, retornando-o junto do status a ser respondido pela rota
def concluiTarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    tarefa.update_status()
    db.session.commit()

    return tarefa.toDict() , 200