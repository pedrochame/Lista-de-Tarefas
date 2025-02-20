from flask import Blueprint, request, jsonify
from services import lista_tarefas, buscaTarefaPorId, criaTarefa, editaTarefa, apagaTarefa, concluiTarefa

tarefa_bp = Blueprint("tarefa_bp",__name__)

# Rota para retornar todas as tarefas
@tarefa_bp.route("/tarefas")
def get_tarefas():
    resposta , status = lista_tarefas()
    return jsonify(resposta) , status

# Rota para retorna uma tarefa pelo ID
@tarefa_bp.route("/tarefas/<int:id>")
def get_tarefa(id):
    resposta , status = buscaTarefaPorId(id)
    return jsonify(resposta) , status

# Rota para criar uma tarefa
@tarefa_bp.route("/tarefas",methods=["POST"])
def create_tarefa():
    resposta , status = criaTarefa(request.get_json())     
    return jsonify(resposta) , status

# Rota para alterar uma tarefa
@tarefa_bp.route("/tarefas/<int:id>",methods=["PUT"])
def update_tarefa(id):
    resposta , status = editaTarefa(id , request.get_json())     
    return jsonify(resposta) , status

# Rota para deletar uma tarefa
@tarefa_bp.route("/tarefas/<int:id>",methods=["DELETE"])
def delete_tarefa(id):
    resposta , status = apagaTarefa(id)
    return jsonify(resposta) , status

# Rota para concluir uma tarefa
@tarefa_bp.route("/tarefas/<int:id>/concluir",methods=["PATCH"])
def concluir_tarefa(id):
    resposta , status = concluiTarefa(id)
    return jsonify(resposta), status