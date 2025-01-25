from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

# Configurar o SQLite (você pode usar outro banco no futuro)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evitar warnings

# Inicializar o banco de dados
db = SQLAlchemy(app)

# Tabela de tarefas
class Tarefa(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    titulo    = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data      = db.Column(db.Date, nullable=False)
    concluida = db.Column(db.Boolean, default=False)

@app.route("/")
def tarefas():
    return render_template("index.html",tarefas=Tarefa.query.all())

@app.route("/criarTarefa",methods=["GET","POST"])
def criarTarefa():

    if request.method == "POST":

        t       = request.form.get("titulo")
        desc    = request.form.get("descricao")
        dt      = request.form.get("data").split("-")
        dt      = date(int(dt[0]),int(dt[1]),int(dt[2]))

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
        dt      = request.form.get("data").split("-")
        dt      = date(int(dt[0]),int(dt[1]),int(dt[2]))

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
    return redirect("/")

# Ao executar o aplicativo, o banco de dados é criado, se já não existir
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)