from flask import Flask, render_template, request, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL


def create_app():
    from app import routes
    routes.init_app(app)

    return app


app = Flask(__name__)
Bootstrap(app)



# conexão com o banco de dados
app.config['MYSQL_Host'] = 'localhost' # 127.0.0.1
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'contatos'

mysql = MySQL(app)


@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/quem-somos")
def quem_somos():
    return render_template("quem-somos.html")

'''
@app.route("/contatos")
def contatos():
    return render_template("contatos.html")

'''


@app.route('/contato', methods=['GET', 'POST'])
def contatos():
    if request.method == "POST":
        email = request.form['email']
        nome = request.form['nome']
        assunto = request.form['assunto']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contatos(email, nome, assunto) VALUES (%s, %s, %s)", (email, nome, assunto))
       
        mysql.connection.commit()
        
        cur.close()

        return 'sucesso'
    return render_template('contato.html')


# rota usuários para listar todos os usuário no banco de dados.
@app.route('/users')
def users():
    cur = mysql.connection.cursor()

    users = cur.execute("SELECT * FROM contatos")

    if users > 0:
        userDetails = cur.fetchall()

        return render_template("users.html", userDetails=userDetails)


   
