from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def conectar():
    try:
        connection = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="1234",
            database="bd_educare"
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Rota para a página inicial com a lista de pacientes
@app.route('/')
def index():
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM pacientes")
            pacientes = cursor.fetchall()
            return render_template('index.html', pacientes=pacientes)
        finally:
            cursor.close()
            connection.close()

# Rota para adicionar um novo paciente
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        periodo = request.form['periodo']
        curso = request.form['curso']
        dataDaUltimaConsulta = request.form['dataDaUltimaConsulta']
        email = request.form['email']
        telefone = request.form['telefone']
        observacoes = request.form['observacoes']
        links = request.form['links']
        
        connection = conectar()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO pacientes (nome, periodo, curso, dataDaUltimaConsulta, email, telefone, observacoes, links)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (nome, periodo, curso, dataDaUltimaConsulta, email, telefone, observacoes, links)
                )
                connection.commit()
                flash("Paciente adicionado com sucesso!")
                return redirect(url_for('index'))
            finally:
                cursor.close()
                connection.close()
    return render_template('adicionar.html')

# Rota para excluir um paciente
@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM pacientes WHERE id = %s", (id,))
            connection.commit()
            flash("Paciente removido com sucesso!")
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('index'))

# Rota para editar um paciente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    connection = conectar()
    if request.method == 'POST':
        # Atualizar paciente no banco de dados
        nome = request.form['nome']
        periodo = request.form['periodo']
        curso = request.form['curso']
        dataDaUltimaConsulta = request.form['dataDaUltimaConsulta']
        email = request.form['email']
        telefone = request.form['telefone']
        observacoes = request.form['observacoes']
        links = request.form['links']
        
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE pacientes
                    SET nome = %s, periodo = %s, curso = %s, dataDaUltimaConsulta = %s,
                        email = %s, telefone = %s, observacoes = %s, links = %s
                    WHERE id = %s
                """, (nome, periodo, curso, dataDaUltimaConsulta, email, telefone, observacoes, links, id))
                connection.commit()
                flash("Paciente atualizado com sucesso!")
                return redirect(url_for('index'))
            finally:
                cursor.close()
                connection.close()
    else:
        # Buscar paciente do banco de dados
        if connection:
            try:
                cursor = connection.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT * FROM pacientes WHERE id = %s", (id,))
                paciente = cursor.fetchone()
                return render_template('editar.html', paciente=paciente)
            finally:
                cursor.close()
                connection.close()

if __name__ == '__main__':
    app.run(debug=True)
