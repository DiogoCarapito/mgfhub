import streamlit as st


@st.cache_data()
def tutorial_loop(tutorial):
    # loop through the content and create a card for each row
    for i, each in enumerate(tutorial):
        # for each in tutorial:
        st.write(each["texto"])
        if each["imagem"]:
            st.image(each["imagem"], use_column_width=True)
        # show a divider between each step, except for the last one
        if i != len(tutorial) - 1:
            st.write("")


@st.cache_data()
def tutorial_expander(tutorial):
    with st.expander("Tutorial", expanded=False):
        col_tutorial_1, col_tutorial_2, col_tutorial_3 = st.columns([1, 6, 1])
        with col_tutorial_1:
            st.empty()

        with col_tutorial_2:
            tutorial_loop(tutorial)

        with col_tutorial_3:
            st.empty()


@st.cache_data()
def tutorial_bicsp():
    tutorial = [
        {
            "texto": "##### 1. Abrir o [BI CSP - Contratualização](https://bicsp.min-saude.pt/pt/contratualizacao/idg/Paginas/default.aspx)",
            "imagem": "content/tutorial_bicsp/tutorial_bicsp_1.png",
        },
        {
            "texto": "##### 2. Ir ao separador **UF - IDG - Indicadores**",
            "imagem": "content/tutorial_bicsp/tutorial_bicsp_2.png",
        },
        {
            "texto": "##### 3. Selecionar o 'Ano/Mês' e a 'Unidade'",
            "imagem": "content/tutorial_bicsp/tutorial_bicsp_3.png",
        },
        {
            "texto": "##### 4. Selecionar o **More optionss** nos ... do canto superior direito da tabela",
            "imagem": "content/tutorial_bicsp/tutorial_bicsp_4.png",
        },
        {
            "texto": "##### 5. Selecionar o botão **Export data**",
            "imagem": "content/tutorial_bicsp/tutorial_bicsp_5.png",
        },
        {
            "texto": "##### 6. Selecionar a 2ª ou 3ª opção, **Sumarized Data** ou **Underlying data** e selecionar o botão **Export**",
            "imagem": "content/tutorial_bicsp/tutorial_bicsp_6.png",
        },
        {
            "texto": "##### 7. Depois de gravar o ficheiro, arrastar (da pasta de transferencias) para o local de upload do mgfhub",
            "imagem": "content/tutorial_bicsp/tutorial_bicsp_7.png",
        },
    ]
    st.subheader("Como extrair o ficheiro excel necessário do BI-CSP?")
    tutorial_expander(tutorial)


@st.cache_data()
def tutorial_mimuf():
    tutorial = [
        {
            "texto": "##### 1. Abrir o MIM@UF e fazer login",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_1.png",
        },
        {
            "texto": "##### 2. Navegar para a pasta Indicadores",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_2.png",
        },
        {
            "texto": "##### 3. Pasta P02.01. Indicadores USF/UCSP'",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_3.png",
        },
        {
            "texto": "##### 4. Selecionar o relatório P02_01_R03. Indicadores por lista de utentes de médico",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_4.png",
        },
        # {
        #     "texto": "##### 5. ...",
        #     "imagem": "content/tutorial_mimuf/tutorial_mimuf_5.png",
        # },
        {
            "texto": "##### 5. Selecionar o Mês de Analise e o Ano de Contratualização e depois Executar Relatório",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_6.png",
        },
        {
            "texto": "##### 6. Executar Relatório",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_7.png",
        },
        {
            "texto": "##### 7. Vão ser necessários vários passos intermédios antes de exportar a tabela",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_8.png",
        },
        {
            "texto": "##### 8. Mudar para indicador Flutuante",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_9.png",
        },
        {
            "texto": "##### 9. Transformar o filtro Médico Familia para uma coluna na tabela, passando com rato entre as duas colunas e clicar na lupa",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_10.png",
        },
        {
            "texto": "##### 10. Escrever Méd e selecionar Médico Familia",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_11.png",
        },
        {
            "texto": "##### 11. Corrigir as linas unificadas na Planilha e depois butão com colinas a amarelo",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_12.png",
        },
        {
            "texto": "##### 12. Voltar ao Home e clicar no botão Exportar",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_13.png",
        },
        {
            "texto": '##### 13. Selecionar Excel com texto simples; Tirar ☑️ do "Exportar título do relatório"; Tirar ☑️ do "Exportar Informações de Pagina Por"; Tirar ☑️ do "Exportar detalhes do filtro"; Clicar em Exportar',
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_14.png",
        },
        {
            "texto": "##### 14. Abrir o Excel",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_15.png",
        },
        {
            "texto": "##### 16. Exportar como Livro",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_16.png",
        },
        {
            "texto": "##### 17. Fazer o upload do ficheiro para o mgfhub",
            "imagem": "content/tutorial_mimuf/tutorial_mimuf_17.png",
        },
    ]
    st.subheader("Como extrair o ficheiro excel necessário do MIM@UF?")
    tutorial_expander(tutorial)
