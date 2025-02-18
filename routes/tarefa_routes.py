from models import Tarefa
from flask import Blueprint,render_template, request, redirect, jsonify
from utils import converteData
from extensions import db

tarefa_bp = Blueprint("tarefa_bp",__name__)

@tarefa_bp.route("/")
def tarefas():

    filtro = request.args.get("filtro")
    if filtro==None or (int(filtro) not in [-1,0,1]):
        filtro="-1"
        
    return render_template("index.html",filtro=filtro)

# Rota para busca de tarefas
@tarefa_bp.route("/busca")
def busca():

    filtro = request.args.get("filtro")

    if int(filtro) not in [-1,0,1]:
        return redirect("/")
    
    lista = []

    if filtro:
        if filtro == "-1":
            tarefas = Tarefa.query.order_by(Tarefa.data)
        else:
            tarefas = Tarefa.query.filter_by(concluida = filtro).order_by(Tarefa.data)

        for tarefa in tarefas:
            lista.append(tarefa.toDict())
    
    else:
        return redirect("/")
    
    return jsonify(lista)

@tarefa_bp.route("/criarTarefa",methods=["GET","POST"])
def criarTarefa():

    if request.method == "POST":

        t       = request.form.get("titulo")
        desc    = request.form.get("descricao")
        dt      = request.form.get("data")

        tarefa = Tarefa(t,desc,dt)
        db.session.add(tarefa)
        db.session.commit()
        
        return redirect("/")
    
    else:

        return render_template("criarTarefa.html")
    
@tarefa_bp.route("/alterarTarefa",methods=["GET","POST"])
def alterarTarefa():

    if request.method == "POST":

        id      = int(request.form.get("id"))
        t       = request.form.get("titulo")
        desc    = request.form.get("descricao")
        dt      = request.form.get("data")

        tarefa = Tarefa.query.get(id)

        if tarefa == None:
            return redirect("/")

        tarefa.update(t,desc,dt)
        
        db.session.commit()
        
        return redirect("/")
    
    else:
        id = int(request.args.get("id"))
        tarefa = Tarefa.query.get(id)
        if tarefa == None:
            return redirect("/")
        
        #tarefa.data = converteData(tarefa.data)
        return render_template("alterarTarefa.html",tarefa = tarefa)
    
@tarefa_bp.route("/excluirTarefa",methods=["GET","POST"])
def excluirTarefa():
    id = int(request.args.get("id"))
    tarefa = Tarefa.query.get(id)
    if tarefa == None:
        return redirect("/")
    db.session.delete(tarefa)
    db.session.commit()
    return redirect("/?filtro="+request.args.get("filtro"))

@tarefa_bp.route("/concluirTarefa",methods=["GET","POST"])
def concluirTarefa():
    id = int(request.args.get("id"))
    tarefa = Tarefa.query.get(id)
    if tarefa == None:
        return redirect("/")
    tarefa.concluida = True
    db.session.commit()
    return redirect("/?filtro="+request.args.get("filtro"))