from app import app
from flask import render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import base64
import json
import folium

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
            
        resultado = tabela
    return render_template("profissionais.html", municipios=municipios, anos=anos, resultado=resultado)

@app.route('/saiba-mais')
def saiba_mais():
    return render_template('saiba-mais.html')

@app.route('/mortalidade-infantil')
def mortalidade_infantil():
        # Ler os dados do CSV
    df = pd.read_csv("app\static\mortalidade-infantil-alagoas.csv")
    anos = df.columns[1:]  # Colunas com os anos
    valores = df.iloc[0, 1:]  # Valores da Taxa de Mortalidade Infantil

    # Criar o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(anos, valores, marker='o', color='blue', label='Taxa de Mortalidade Infantil')
    plt.title('Taxa de Mortalidade Infantil (2006-2022)', fontsize=14)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Taxa (%)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(alpha=0.5)
    plt.legend()

    # Salvar o gráfico em um buffer para exibição
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    # Converter o gráfico para Base64
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
    return render_template('mortalidade-infantil.html', plot_url=plot_url)

@app.route('/bases-samu')
def bases_samu():
    with open('app\static\\bases-samu.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
      
        # Criar um mapa centralizado
    m = folium.Map(location=[-9.5, -36.5], zoom_start=8)
    
    # Adicionar os pontos ao mapa
    for feature in json_data['features']:
        coords = feature['geometry']['coordinates']
        props = feature['properties']
        popup_info = f"{props['Nome']}<br>{props['Endereço']}<br>{props['Município']}"
        folium.Marker(
            location=[coords[1], coords[0]],
            popup=popup_info,
        ).add_to(m)
        
    # Caminho para salvar o mapa como um arquivo HTML temporário
    map_path = os.path.join(os.path.dirname(__file__), 'static', 'mapa.html')

    # Salvar o mapa como um arquivo HTML
    m.save(map_path)
    return render_template('bases-samu.html', map_path=map_path)

@app.route('/leitos-de-internacao')
def leitos_de_internacao():
    return render_template('leitos-de-internação.html')

@app.route('/postos-de-saude')
def postos_de_saude():
    return render_template('postos-de-saude.html')