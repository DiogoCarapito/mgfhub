python

# seleção do documento e paginas com as tabelas
# 2022
# documento = 'data/ACSS-Operacionalizacao_CSP_2022_Final.pdf'
# pages = [76,77,78,79,80]

documento = "data/Operacionalizacao_CSP_2023_VF.pdf"
pages_com_impacto = [60, 61, 62]
pages_sem_impacto = [63, 64]
# Seleção das paginas onde estão as tabelas


tabela_com_impacto = tabula.read_pdf(documento, pages=pages_com_impacto)
# tabela_sem_impacto = tabula.read_pdf(documento, pages=pages_sem_impacto)

df_com_impacto = pd.concat(
    [
        tabela_com_impacto[pages_com_impacto.index(page)].dropna()
        for page in pages_com_impacto
    ],
    ignore_index=True,
)
# df_sem_impacto = pd.concat([tabela_sem_impacto[pages_sem_impacto.index(page)].dropna() for page in pages_sem_impacto],ignore_index=True)

"""
for col in df.columns:
    print(col)
"""
# print(df.columns[2])
# regex = '\d+\.*\d'

print(df_com_impacto)

"""#
df = df.assign(id=[int(row['ID Indicador']) for index,row in df.iterrows()])
df = df.drop(columns=['ID Indicador'])
df.rename(columns={'Nome Indicador':'nome_indicador','Int var.':'intervalo_aceitavel','Int. Esperado':'intervalo_esperado'}, inplace=True)

# Regular expressions para extrir os intervalos minimo e máximo
regex_min = '\[(\d*\.*\d)'
regex_max = '(\d*\.*\d)\]'
"""

"""# Criação de novas colunas com os valores extraidos de min e max dos intervalos aceitáveis e esperados
df = df.assign(min_aceitavel=[re.findall(regex_min,row['intervalo_aceitavel'])[0] for index, row in df.iterrows()])
df = df.assign(min_esperado=[re.findall(regex_min,row['intervalo_esperado'])[0] for index, row in df.iterrows()])
df = df.assign(max_esperado=[re.findall(regex_max,row['intervalo_esperado'])[0] for index, row in df.iterrows()])
df = df.assign(max_aceitavel=[re.findall(regex_max,row['intervalo_aceitavel'])[0] for index, row in df.iterrows()])
"""
# df = df[['id','nome_indicador','min_aceitavel','min_esperado','max_esperado','max_aceitavel','intervalo_aceitavel','intervalo_esperado']]


"""df.to_csv('../data/usf_ucsp_indicadores_2023_com_impactoIDG.csv',index=False)
df.to_csv('../data/usf_ucsp_indicadores_2023_sem_impactoIDG.csv',index=False)"""
