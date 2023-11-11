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
        maxInt = int(maxInt / 10)

## Html do indicador para teste de confrontação
"""https://sdm.min-saude.pt/BI.aspx?id=001&CLUSTERS=S"""

html_inicio = "https://sdm.min-saude.pt/BI.aspx?id="
html_fim = "&CLUSTERS=S"

## Teste se já existeo csv
html_bruto = []
dados = []

categorias = [
    "id",
    "codigo",
    "codigo_siars",
    "nome_abreviado",
    "designacao",
    "objetivo",
    "formula",
    "unidade_de_medida",
    "output",
    "estado_do_indicador",
    "area",
    "subarea",
    "dimensao",
    "tipo_de_indicador",
    "area_clinica",
    "inclusao_de_utentes_no_indicador",
    "prazo_para_registos",
    "link",
]

try:
    file = open("../data/scrapped_indicadores.csv", "r")
    dados = list(csv.reader(file, delimiter=","))
    ## Qual o id do último indicador para começar no seguinte
    inicio = int(dados[-1][0]) + 1
    file.close()

except:
    dados = []
    dados.append(categorias)
    inicio = 1

## Lista de codigos de indicadores que faltam
fim = inicio + 100 - 1
# fim = 448
lista_codigo_html = np.arange(inicio, fim + 1).tolist()

lista = []
lista_corpo = []

## Loop para fazer scraping
for html_code in lista_codigo_html:
    html = html_inicio + str(html_code) + html_fim
    rqst = requests.get(html)
    soup = BeautifulSoup(rqst.content, "html.parser")
    main_html = soup.find(id="MainContent_lbl_BI")

    items_header = []
    items_body = []

    for line in main_html.strings:
        ## Teste para excluir paginas que dão erro
        if line[0:4] == "":
            break
        ## Break para parar para onde já não interessa
        if line == "BI":
            break
        item = repr(line).strip("' '")

        if len(items_header) < 9:
            items_header.append(item)
            # print(len(items_header) - 1, item)
        else:
            items_body.append(item)
            # print(len(items_body) - 1, item)
    # print('\n')
    print(items_header[0])
    lista.append(items_header)
    lista_corpo.append(items_body)

print("---")
## For Loop para iterar sobre o cada linha e atribuir a um dicionário para criação da tabela
for numero_indicador, cabecalho in enumerate(lista):
    if len(cabecalho) < 5:
        continue
    if cabecalho[0][:4] == "Erro":
        continue
    print(cabecalho[0])

    area_subarea_dimensao_test = lista_corpo[numero_indicador][
        3 + lista_corpo[numero_indicador].index("Área | Subárea | Dimensão")
    ]
    if len(area_subarea_dimensao_test) > 5:
        area_subarea_dimensao = area_subarea_dimensao_test.split(" | ")
    else:
        area_subarea_dimensao = ["", "", ""]

    list_indicador = [
        int(cabecalho[0]),  #'id',
        cabecalho[4],  #'codigo',
        cabecalho[5],  #'codigo_siars',
        cabecalho[6],  #'nome_abreviado',
        cabecalho[8],  #'designacao',
        lista_corpo[numero_indicador][1],  #'objetivo',
        lista_corpo[numero_indicador][
            4 + lista_corpo[numero_indicador].index("Fórmula")
        ],  #'formula',
        lista_corpo[numero_indicador][
            4 + lista_corpo[numero_indicador].index("Unidade de medida")
        ],  #'unidade_de_medida',
        lista_corpo[numero_indicador][
            4 + lista_corpo[numero_indicador].index("Output")
        ],  #'output',
        lista_corpo[numero_indicador][
            4 + lista_corpo[numero_indicador].index("Estado do indicador")
        ],  #'estado_do_indicador',
        area_subarea_dimensao[0],  #'area',
        area_subarea_dimensao[1],  #'subarea',
        area_subarea_dimensao[2],  #'dimensao',
        lista_corpo[numero_indicador][
            4 + lista_corpo[numero_indicador].index("Tipo de Indicador")
        ],  #'tipo_de_indicador',
        lista_corpo[numero_indicador][
            4 + lista_corpo[numero_indicador].index("Área clínica")
        ],  #'area_clinica',
        lista_corpo[numero_indicador][
            4 + lista_corpo[numero_indicador].index("Inclusão de utentes no indicador")
        ],  #'inclusao_de_utentes_no_indicador',
        lista_corpo[numero_indicador][
            4 + lista_corpo[numero_indicador].index("Prazo para Registos")
        ],  #'prazo_para_registos',
        html_inicio + cabecalho[0] + html_fim,  #'link'
    ]

    # print(list_indicador)
    dados.append(list_indicador)

## Gravação em .csv
df = pd.DataFrame(dados, columns=dados[0])
df.to_csv("../data/scrapped_indicadores.csv", index=False, header=False)
