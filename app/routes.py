from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/sobre")
def sobre():
    return render_template('sobre.html')

@app.route("/graficos")
def graficos():
    return render_template('graficos.html')