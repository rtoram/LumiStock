from flask import Flask, render_template, request, send_file
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS produtos 
                 (id INTEGER PRIMARY KEY, modelo TEXT, genero TEXT, cor TEXT, tamanho TEXT, quantidade INTEGER, valor_unitario REAL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        modelo = request.form['modelo']
        genero = request.form['genero']
        cor = request.form['cor']
        tamanho = request.form['tamanho']
        quantidade = int(request.form['quantidade'])
        valor_unitario = float(request.form['valor_unitario'])

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO produtos (modelo, genero, cor, tamanho, quantidade, valor_unitario) VALUES (?, ?, ?, ?, ?, ?)",
                  (modelo, genero, cor, tamanho, quantidade, valor_unitario))
        conn.commit()
        conn.close()
        return "Produto cadastrado com sucesso!"
    return render_template('cadastro.html')

@app.route('/orcamento')
def orcamento():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM produtos")
    produtos = c.fetchall()
    conn.close()

    pdf_file = "orcamento_lumistock.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    c.drawString(100, 800, "Orçamento - LumiStock")
    y = 780
    for produto in produtos:
        texto = f"{produto[1]} - {produto[2]} - {produto[3]} - {produto[4]} - Qtde: {produto[5]} - R$ {produto[6]}"
        c.drawString(100, y, texto)
        y -= 20
    c.save()

    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
