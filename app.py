from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

# Configurar o SQLite (você pode usar outro banco no futuro)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evitar warnings

# Inicializar o banco de dados
db = SQLAlchemy(app)

# Função para alterar data de aaaa-mm-dd para dd/mm/aaaa e vice-versa
def converteData(dt):
    if dt[2] == "-":
        return dt.split("-")[2]+"-"+dt.split("-")[1]+"-"+dt.split("-")[0]
    return dt.split("/")[2]+"/"+dt.split("/")[1]+"/"+dt.split("/")[0]

# Tabela de tarefas
class Tarefa(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    titulo    = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data      = db.Column(db.String(10), nullable=False)
    concluida = db.Column(db.Boolean, default=False)

    def toDict(self):
        return {"id":self.id,"titulo":self.titulo,"descricao":self.descricao,"data":converteData(self.data),"concluida":self.concluida}

@app.route("/")
def tarefas():

    filtro = request.args.get("filtro")
    if filtro==None or (int(filtro) not in [-1,0,1]):
        filtro="-1"
        
    return render_template("index.html",filtro=filtro)

# Rota para busca de tarefas
@app.route("/busca")
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

@app.route("/criarTarefa",methods=["GET","POST"])
def criarTarefa():

    if request.method == "POST":

        t       = request.form.get("titulo")
        desc    = request.form.get("descricao")
        dt      = converteData(request.form.get("data"))

        tarefa = Tarefa(titulo=t,descricao=desc,data=dt)
        db.session.add(tarefa)
        db.session.commit()
        
        return redirect("/")
    
    else:

        return render_template("criarTarefa.html")
    
@app.route("/alterarTarefa",methods=["GET","POST"])
def alterarTarefa():

    if request.method == "POST":

        id      = int(request.form.get("id"))
        t       = request.form.get("titulo")
        desc    = request.form.get("descricao")
        dt      = converteData(request.form.get("data"))

        tarefa = Tarefa.query.get(id)

        if tarefa == None:
            return redirect("/")

        tarefa.titulo, tarefa.descricao, tarefa.data = t, desc, dt
        db.session.commit()
        
        return redirect("/")
    
    else:
        id = int(request.args.get("id"))
        tarefa = Tarefa.query.get(id)
        if tarefa == None:
            return redirect("/")
        
        tarefa.data = converteData(tarefa.data)
        return render_template("alterarTarefa.html",tarefa = tarefa)
    
@app.route("/excluirTarefa",methods=["GET","POST"])
def excluirTarefa():
    id = int(request.args.get("id"))
    tarefa = Tarefa.query.get(id)
    if tarefa == None:
        return redirect("/")
    db.session.delete(tarefa)
    db.session.commit()
    return redirect("/")

@app.route("/concluirTarefa",methods=["GET","POST"])
def concluirTarefa():
    id = int(request.args.get("id"))
    tarefa = Tarefa.query.get(id)
    if tarefa == None:
        return redirect("/")
    tarefa.concluida = True
    db.session.commit()
    return redirect("/?filtro="+request.args.get("filtro"))

# Ao executar o aplicativo, o banco de dados é criado, se já não existir
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)