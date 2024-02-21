import streamlit as st


def tutorial_bicsp():
    tutorial = [
        {
            "texto": "##### 1. Abrir o [BI CSP - Contratualização](https://bicsp.min-saude.pt/pt/contratualizacao/idg/Paginas/default.aspx)",
            "imagem": "content/tutorial/tutorial_bicsp_1.png",
        },
        {
            "texto": "##### 2. Ir ao separador **UF - IDG - Indicadores**",
            "imagem": "content/tutorial/tutorial_bicsp_2.png",
        },
        {
            "texto": "##### 3. Selecionar o 'Ano/Mês' e a 'Unidade'",
            "imagem": "content/tutorial/tutorial_bicsp_3.png",
        },
        {
            "texto": "##### 4. Selecionar o **More optionss** nos ... do canto superior direito da tabela",
            "imagem": "content/tutorial/tutorial_bicsp_4.png",
        },
        {
            "texto": "##### 5. Selecionar o botão **Export data**",
            "imagem": "content/tutorial/tutorial_bicsp_5.png",
        },
        {
            "texto": "##### 6. Selecionar a 2ª ou 3ª opção, **Sumarized Data** ou **Underlying data** e selecionar o botão **Export**",
            "imagem": "content/tutorial/tutorial_bicsp_6.png",
        },
        {
            "texto": "##### 7. Depois de gravar o ficheiro, arrastar (da pasta de transferencias) para o local de upload do mgfhub",
            "imagem": "content/tutorial/tutorial_bicsp_7.png",
        },
    ]

    with st.expander(
        "Como extrair o ficheiro excel necessário do BI-CSP?", expanded=False
    ):
        col_tutorial_1, col_tutorial_2, col_tutorial_3 = st.columns([1, 4, 1])
        with col_tutorial_1:
            st.empty()

        with col_tutorial_2:
            for each in tutorial:
                st.write(each["texto"])
                if each["imagem"]:
                    st.image(each["imagem"], use_column_width=True)
                st.divider()

        with col_tutorial_3:
            st.empty()


def tutorial_mimuf():
    tutorial = [
        {
            "texto": "##### 1. Abrir o MIM@UF e fazer login",
            "imagem": "content/tutorial/tutorial_bicsp_7.png",
        },
        {
            "texto": "##### 2. Navegar para a pasta Indicadores",
            "imagem": "content/tutorial/tutorial_bicsp_7.png",
        },
        {
            "texto": "##### 3. Selecionar o relatório P02_01_R03_ Indicadores por lista de utentes de médico**'",
            "imagem": "content/tutorial/tutorial_bicsp_7.png",
        },
        {
            "texto": "##### 4. Executar a query pelo mês de analise e ano de contratualização",
            "imagem": "content/tutorial/tutorial_bicsp_7.png",
        },
        {
            "texto": "##### 5. ...",
            "imagem": "content/tutorial/tutorial_bicsp_7.png",
        },
        {
            "texto": "##### 6. ...",
            "imagem": "content/tutorial/tutorial_bicsp_7.png",
        },
        {
            "texto": "##### 7. Depois de gravar o ficheiro, arrastar (da pasta de transferencias) para o local de upload do mgfhub",
            "imagem": "content/tutorial/tutorial_bicsp_7.png",
        },
    ]

    with st.expander(
        "Como extrair o ficheiro excel necessário do MIM@UF?", expanded=False
    ):
        col_tutorial_1, col_tutorial_2, col_tutorial_3 = st.columns([1, 4, 1])
        with col_tutorial_1:
            st.empty()

        with col_tutorial_2:
            for each in tutorial:
                st.write(each["texto"])
                if each["imagem"]:
                    st.image(each["imagem"], use_column_width=True)
                st.divider()

        with col_tutorial_3:
            st.empty()
