from flask import Flask, render_template, request, redirect, url_for, session, flash
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
    
# Rota para cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']  # Considere usar hash para a senha
        
        connection = conectar()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
                connection.commit()
                flash('Cadastro realizado com sucesso!')
                return redirect(url_for('login'))
            finally:
                cursor.close()
                connection.close()
    return render_template('cadastro.html')



@app.route('/pagina_protegida')
def pagina_protegida():
    if 'usuario' in session:
        return 'Conteúdo protegido!'
    return redirect(url_for('login'))


# Logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Remove a sessão do usuário
    flash('Você saiu com sucesso!')
    return redirect(url_for('login'))  # Redireciona de volta para a tela de login


# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Lógica de autenticação simples (exemplo com dados fixos)
        if email == 'admin@admin.com' and senha == '1234':
            session['usuario'] = email  # Cria a sessão
            return redirect(url_for('index'))  # Redireciona para a página inicial após o login
        else:
            flash('Login ou senha incorretos!')  # Mensagem de erro
            return redirect(url_for('login'))  # Volta para a tela de login

    return render_template('login.html')


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
        laudos = request.form['laudos']

        
        connection = conectar()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO pacientes (nome, periodo, curso, dataDaUltimaConsulta, email, telefone, observacoes, links)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (nome, periodo, curso, dataDaUltimaConsulta, email, telefone, observacoes, laudos)
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
        laudos = request.form['laudos']

        
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO pacientes (nome, periodo, curso, dataDaUltimaConsulta, email, telefone, observacoes, laudos)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (nome, periodo, curso, dataDaUltimaConsulta, email, telefone, observacoes, laudos)
                )              
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

@app.route('/laudos/<int:id>')
def ver_laudos(id):
    connection = conectar()
    if connection:
        try:
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT laudos FROM pacientes WHERE id = %s", (id,))
            paciente = cursor.fetchone()
            if paciente and paciente['laudos']:
                return render_template('laudos.html', laudo_texto=paciente['laudos'])
            else:
                return render_template('laudos.html', laudo_texto="Nenhum laudo disponível.")
        finally:
            cursor.close()
            connection.close()


@app.route('/relatorio')
def relatorio():
    try:
        connection = conectar()
        if connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # Exemplo: Agrupando pacientes por curso
                cursor.execute("""
                    SELECT 
                        curso,
                        COUNT(*) AS total_pacientes,
                        MAX(dataDaUltimaConsulta) AS ultima_consulta
                    FROM pacientes
                    GROUP BY curso
                """)
                dados_relatorio = cursor.fetchall()
            return render_template('relatorio.html', relatorio=dados_relatorio)
    except pymysql.MySQLError as e:
        return f"Erro ao gerar relatório: {e}"
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
