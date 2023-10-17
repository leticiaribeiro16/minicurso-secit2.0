from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'minicurso-teste.mysql.database.azure.com',
    'user': 'leticia',
    'password': '26demaio.',
    'database': 'minicurso'
}

# Conexão com o banco de dados
db = mysql.connector.connect(**db_config)
cursor = db.cursor(dictionary=True)

# Rotas
@app.route('/')
def index():
    cursor.execute('SELECT * FROM tarefas')
    data = cursor.fetchall()
    return render_template('index.html', data=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        # Por padrão, definimos 'feita' como False (não concluída) ao adicionar
        cursor.execute('INSERT INTO tarefas (nome, descricao, feita) VALUES (%s, %s, %s)', (nome, descricao, False))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cursor.execute('SELECT * FROM tarefas WHERE id = %s', (id,))
    data = cursor.fetchone()
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        # Aqui não atualizamos o campo 'feita' porque o usuário não está editando o status
        cursor.execute('UPDATE tarefas SET nome = %s, descricao = %s WHERE id = %s', (nome, descricao, id))
        db.commit()
        return redirect(url_for('index'))
    
    return render_template('edit.html', data=data)

@app.route('/delete/<int:id>')
def delete(id):
    # Adicione o código para excluir dados no banco de dados
    cursor.execute('DELETE FROM tarefas WHERE id = %s', (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
