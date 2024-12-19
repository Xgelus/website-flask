from app import app
from flask import render_template, request
import pandas as pd
import matplotlib as plt 

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/sobre")
def sobre():
    return render_template('sobre.html')

num_profissionais_saude_al = pd.read_excel('app\static\\num_profissionais.xlsx')

@app.route("/profissionais-al", methods=["GET", "POST"])
def profissionais():
    resultado = None
    municipios = num_profissionais_saude_al['Município'].unique()  # Lista de municípios
    anos = [col.split()[-1] for col in num_profissionais_saude_al.columns if "Anestesista" in col]  # Lista de anos
    
    if request.method == "POST":
        municipio = request.form.get("municipio")
        ano = request.form.get("ano")   
        
        # Filtrar os dados
        dados_municipio = num_profissionais_saude_al[num_profissionais_saude_al["Município"] == municipio]
        colunas_filtradas = [col for col in dados_municipio.columns if ano in col]
        
        # Selecionar as colunas de profissionais e quantidades
        dados_filtrados = dados_municipio[['Município'] + colunas_filtradas]
        
        # Organizar os dados em um formato de tabela com Profissionais de Saúde e Quantidades
        tabela = []
        for col in colunas_filtradas:
            profissional = col.replace(f" {ano}", "")  # Extrai o nome do profissional da coluna
            quantidade = dados_filtrados[col].sum()  # Soma das quantidades para o ano e município
            tabela.append([profissional, quantidade])
        
        # Convertendo para tabela html-css
        resultado = pd.DataFrame(tabela, columns=["Profissional de Saúde", "Quantidade"]).to_html(
            classes='table-auto border-collapse border border-gray-300', index=False, escape=False
        )
    
    return render_template("profissionais.html", municipios=municipios, anos=anos, resultado=resultado)


if __name__ == '__main__':
    app.run(debug=True)