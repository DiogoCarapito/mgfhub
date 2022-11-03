import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import csv
import sys

maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

## Html do indicador para teste de confrontação
'''https://sdm.min-saude.pt/BI.aspx?id=001&CLUSTERS=S'''

html_inicio = 'https://sdm.min-saude.pt/BI.aspx?id='
html_fim = '&CLUSTERS=S'

## Teste se já existeo csv
html_bruto = []
inicio = 0
dados = {}

try:
    '''file = open("scrapped_indicadores.csv", "r+")
    dados = list(csv.reader(file, delimiter=","))
    inicio = len(dados)+1'''
    with open("data/scrapped_indicadores.csv", 'r') as data:
        dados = csv.DictReader(data)
        '''for line in csv.DictReader(data):
            dados.append(line)
            inicio +=1
        '''s
    file.close()

except:
    dados = []
    inicio = 1

print(dados)
## Lista de codigos de indicadores que faltam
fim = inicio + 2 - 1
#fim = 448
lista_codigo_html = np.arange(inicio,fim +1).tolist()

lista = []
lista_corpo = []

## Loop para fazer scraping
for html_code in lista_codigo_html:
    html = html_inicio + str(html_code) + html_fim
    rqst = requests.get(html)
    soup = BeautifulSoup(rqst.content, 'html.parser')
    main_html = soup.find(id='MainContent_lbl_BI')

    items_header = []
    items_body = []

    for line in main_html.strings:
        ## Teste para excluir paginas que dão erro
        if line[0:4] == '': break
        ## Break para parar para onde já não interessa
        if line == 'BI': break
        item = repr(line).strip("' '")

        if len(items_header) < 9:
            items_header.append(item)
            print(len(items_header) - 1, item)
        else:
            items_body.append(item)
            print(len(items_body) - 1, item)
    print('\n')

    lista.append(items_header)
    lista_corpo.append(items_body)

## For Loop para iterar sobre o cada linha e atribuir a um dicionário para criação da tabela
for numero_indicador, cabecalho in enumerate(lista):

    if len(cabecalho)<5 : continue
    print(cabecalho[0])

    area_subarea_dimensao_test = lista_corpo[numero_indicador][3 + lista_corpo[numero_indicador].index('Área | Subárea | Dimensão')]
    if len(area_subarea_dimensao_test)>5:
        area_subarea_dimensao = area_subarea_dimensao_test.split(' | ')
    else:
        area_subarea_dimensao = ['','','']

    dict_indicador = {
        'id': cabecalho[0],
        'codigo': cabecalho[4],
        'codigo_siars': cabecalho[5],
        'nome_abreviado': cabecalho[6],
        'designacao': cabecalho[8],
        'objetivo': lista_corpo[numero_indicador][1],


        'formula': lista_corpo[numero_indicador][4+lista_corpo[numero_indicador].index('Fórmula')],
        'unidade_de_medida': lista_corpo[numero_indicador][4+lista_corpo[numero_indicador].index('Unidade de medida')],
        'output': lista_corpo[numero_indicador][4 + lista_corpo[numero_indicador].index('Output')],
        'estado_do_indicador': lista_corpo[numero_indicador][4 + lista_corpo[numero_indicador].index('Estado do indicador')],

        'area': area_subarea_dimensao[0],
        'subarea': area_subarea_dimensao[1],
        'dimensao': area_subarea_dimensao[2],


        'tipo_de_indicador': lista_corpo[numero_indicador][4 + lista_corpo[numero_indicador].index('Tipo de Indicador')],
        'area_clinica': lista_corpo[numero_indicador][4 + lista_corpo[numero_indicador].index('Área clínica')],
        'inclusao_de_utentes_no_indicador': lista_corpo[numero_indicador][4 + lista_corpo[numero_indicador].index('Inclusão de utentes no indicador')],
        'prazo_para_registos': lista_corpo[numero_indicador][4 + lista_corpo[numero_indicador].index('Prazo para Registos')],
        'link': html_inicio + cabecalho[0] + html_fim

    }
    print(dict_indicador)
    dados.append(dict_indicador)

## Gravação em .csv
df = pd.DataFrame(dados)
df.to_csv('data/scrapped_indicadores.csv')

'''file = open("scrapped_indicadores.csv", "a+")
for line in  
file.close()
'''
