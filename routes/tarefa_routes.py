from models import Tarefa
from flask import Blueprint,render_template, request, redirect, jsonify
from extensions import db

tarefa_bp = Blueprint("tarefa_bp",__name__)

# Rota que pega todas as tarefas no banco de dados, e retorna um json as contendo
@tarefa_bp.route("/tarefas")
def get_tarefas():

    listaTarefas = []
    tarefas = Tarefa.query.all()
    
    for tarefa in tarefas:
        listaTarefas.append(tarefa.toDict())

    return jsonify(listaTarefas),200

# Rota que pega uma tarefa pelo id no banco de dados, e retorna ela em formato json
@tarefa_bp.route("/tarefas/<int:id>")
def get_tarefa(id):

    # Com o método get_or_404(), se a tarefa não existir, uma resposta com status 404 é lançada automaticamente
    tarefa = Tarefa.query.get_or_404(id).toDict()
    
    return jsonify(tarefa),200

# Rota que cria uma nova tarefa e retorna a mesma em formato json
@tarefa_bp.route("/tarefas",methods=["POST"])
def create_tarefa():

    dados = request.get_json()

    if validaDadosRecebidos(dados) == False:
        return jsonify({"erro" : "Todas as informações da tarefa são obrigatórias."}), 400

    titulo    = dados["titulo"]
    descricao = dados["descricao"]
    data      = dados["data"]

    try:
        tarefa = Tarefa(titulo,descricao,data)
    except ValueError as e:
        return jsonify({ "erro" : str(e) }),400

    db.session.add(tarefa)
    db.session.commit()
        
    return jsonify(tarefa.toDict()), 201

# Rota que altera uma tarefa e retorna a mesma em formato json
@tarefa_bp.route("/tarefas/<int:id>",methods=["PUT"])
def update_tarefa(id):

    dados = request.get_json()

    if validaDadosRecebidos(dados) == False:
        return jsonify({"erro" : "Todas as informações da tarefa são obrigatórias."}), 400
    
    titulo    = dados["titulo"]
    descricao = dados["descricao"]
    data      = dados["data"]

    tarefa = Tarefa.query.get_or_404(id)

    try:
        tarefa.update(titulo,descricao,data)
    except ValueError as e:
        return jsonify({"erro" : str(e)}), 400

    db.session.commit()
        
    return jsonify(tarefa.toDict()), 200

# Rota que deleta uma tarefa e retorna uma mensagem de confirmação
@tarefa_bp.route("/tarefas/<int:id>",methods=["DELETE"])
def delete_tarefa(id):
    
    tarefa = Tarefa.query.get_or_404(id)
    
    db.session.delete(tarefa)
    db.session.commit()

    return jsonify({"mensagem":"Tarefa deletada."}), 200

# Rota que conclui uma tarefa e retorna a mesma em formato json
@tarefa_bp.route("/tarefas/<int:id>/concluir",methods=["PATCH"])
def concluir_tarefa(id):
    
    tarefa = Tarefa.query.get_or_404(id)
    tarefa.update_status()
    db.session.commit()

    return jsonify(tarefa.toDict()), 200

def validaDadosRecebidos(dic):
    camposTarefa = ["titulo","descricao","data"]
    for chave in camposTarefa:
        if dic[chave] in ["",None]:
            return False
    return True