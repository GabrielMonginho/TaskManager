from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Em app encontra-se o nosso servidor web de Flask #iniciar servidor numa variavel
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./database/tarefas.db" #conect servidor+base de dados
db = SQLAlchemy(app) #conect SQAlchemy+Servidor , numa variável
#sqlite3> sqlite3 database/tarefas.db  => código no terminal para aceder a shell sqlite
#.databases  => código no terminal para criar a base de dados

@app.route('/')
def home():
    todas_as_tarefas=Tarefa.query.all() #Consultamos e armazenamos todas as tarefas da base de dados
#Agora na variável todas_as_tarefas estão armazenadas todas as tarefas. Vamos entregar esta variável ao template index.html

    return render_template("index.html",lista_de_tarefas=todas_as_tarefas) #Vincular o index.html a app.py #conect servidor+HTML

class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True) #Identificador único de cada tarefa (não pode haver duas tarefas com o mesmo id, por isso é primary key)

    conteúdo = db.Column(db.String(200)) # Conteúdo da tarefa, um texto de máximo 200 caracteres

    feita = db.Column(db.Boolean) # Booleano que indica se uma tarefa foi feita ou não

with app.app_context():
    db.create_all() # Criação das tabelas
    db.session.commit() # Execução das tarefas pendentes da base de dados

@app.route('/criar-tarefa', methods=['POST'])
def criar():
# tarefa é um objeto da classe Tarefa (uma instância da classe)
    tarefa = Tarefa(conteúdo=request.form['conteúdo_tarefa'], feita=False) # id não é necessário atribuí-lo manualmente, porque a primary key gera-se automaticamente

    db.session.add(tarefa) # Adicionar o objeto da Tarefa à base de dados
    db.session.commit() # Executar a operação pendente da base de dados
    return redirect(url_for('home')) # Mensagem de log para ver através do navegador

@app.route('/eliminar-tarefa/<id>')
def eliminar(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).delete() # Pesquisa-se dentro da base de dados, aquele registro cujo id coincida com o proporcionado pelo parâmetro da rota. Quando se encontrar elimina-se

    db.session.commit() # Executar a operação pendente da base de dados
    return redirect(url_for('home')) # Redireciona-nos à função home() e se tudo correu bem, ao atualizar, a tarefa eliminada não vai aparecer na listagem

@app.route('/tarefa-feita/<id>')
def feita(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).first() # Obtém-se a tarefa que se procura

    tarefa.feita = not(tarefa.feita) # Guardar na variável booleana da tarefa, o seu contrário

    db.session.commit() # Executar a operação pendente da base de dados
    return redirect(url_for('home')) # Redireciona-nos para a função home()

if __name__ == '__main__':
    app.run(debug=False)  # O debug=True faz com que cada vez que reiniciemos o servidor ou modifiquemos o código, o servidor de Flask reinicia-se sozinho

