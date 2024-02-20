import streamlit as st


def tutorial_bicsp():
    tutorial = [
        {
            "texto": "#### 1. Abrir o [BI CSP - Contratualização](https://bicsp.min-saude.pt/pt/contratualizacao/idg/Paginas/default.aspx)",
            "imagem": "assets/tutorial/tutorial_bicsp_1.png",
        },
        {
            "texto": "#### 2. Ir ao separador **UF - IDG - Indicadores**",
            "imagem": "assets/tutorial/tutorial_bicsp_2.png",
        },
        {
            "texto": "#### 3. Selecionar o 'Ano/Mês' e a 'Unidade'",
            "imagem": "assets/tutorial/tutorial_bicsp_3.png",
        },
        {
            "texto": "#### 3. Selecionar o **More optionss** nos ... do canto superior direito da tabela",
            "imagem": "assets/tutorial/tutorial_bicsp_4.png",
        },
        {
            "texto": "#### 4. Selecionar o botão **Export data**",
            "imagem": "assets/tutorial/tutorial_bicsp_5.png",
        },
        {
            "texto": "#### 5. Selecionar a 2ª ou 3ª opção, ** Sumarized Data** ou **Underlying data** e selecionar o botão **Export**",
            "imagem": "assets/tutorial/tutorial_bicsp_6.png",
        },
        {
            "texto": "#### 6. Depois de gravar o ficheiro, arrastar (da pasta de transferencias) para o local de upload do mgfhub",
            "imagem": "assets/tutorial/tutorial_bicsp_7.png",
        },
    ]

    with st.expander(
        "Como extrair o ficheiro excel necessário do BI-CSP?", expanded=False
    ):
        for each in tutorial:
            st.write(each["texto"])
            if each["imagem"]:
                st.image(each["imagem"], use_column_width=True)


def tutorial_mimuf():
    with st.expander(
        "Como extrair o ficheiro excel necessário do MIM@UF?", expanded=False
    ):
        st.write("#### 1. Abrir o MIM@UF")

        st.write("#### 2. Navegar para a pasta **Indicadores**")

        st.write(
            "#### 3. Selecionar o relatório P02_01_R03_ Indicadores por lista de utentes de médico**"
        )

        st.write("...")
