import streamlit as st
import pandas as pd

from utils.style import (
    main_title,
    intro,
    card_container,
    page_config,
    # bem_vindos_2,
    novidades,
    bottom_suport_email,
)

# from utils.grpd import consent_popup


def main():
    page_config()

    # main title
    main_title("mgfhub")

    # style columns
    col1, col2, col3 = st.columns([1, 6, 1])

    # empty column to style the page
    with col1:
        st.empty()

    # main content
    with col2:
        # welcome message
        # bem_vindos_2("Bem vind@ à nova versão 2.1 🎉")

        # intro from content/intro.md
        intro("content/intro.md")

        st.success(
            """
#### Funcionalidade de Visão por Indicador e Profissional reposta:

Já não se faz o passo da lupa para transformar o filtro Médico Familia em coluna (esta funcionalidade aparentemente foi removida do MIM@UF).
Para ultrapassar esta limitação agora é necessário:
- Fazer uma extração por cada médico do mesmo relatório (P02_01_R03. Indicadores por lista de utentes de médico).
- Antes de exportar, garantir que estão selecionados ☑️ em "Exportar título do relatório", ☑️ "Exportar Informações de Pagina Por" e ☑️ "Exportar detalhes do filtro" (anteriormente era pedido para retirar, mas na realidade têm informação útil que permite a identificação automática do médico, particularmente útil na nova solução).

- No fim, fazer o upload dos ficheiros todos para o mgfhub no mesmo local, que faz a junção automática dos dados.

Há um novo tutorial com a explicação detalhada dos novos passos na secção de [FAQs](https://mgfhub.com/FAQs).

Os ficheiros antigos do MIM@UF continuam a funcionar, não é necessário voltar a extrair os que já funcionavam antes da alteração para fazer visões temporais.

Agradeço o feedback e reportar qualquer erro que encontrem para [mgfhub.suporte@gmail.com](mailto:mgfhub.suporte@gmail.com)
"""
        )

        # novidades from content/novidades.csv
        # it picks the most recent one
        novidades("content/changelog.csv")

        # st.warning(
        #     "Ainda não é possível fazer upload de ficheiros do BI-CSP e MIM@UF referentes ao ano de 2025. Será corrigido até ao fim de Março."
        # )

        # card containers with links to other pages

        # open content/cartoes_home.csv and read the content with pandas
        cartoes_home = pd.read_csv("content/cartoes_home.csv")

        # loop through the content and create a card for each row
        for each in cartoes_home.values:
            card_container(
                title=each[0],
                text=each[1],
                image=None,
                # link=each[3],
                # icon=each[4],
                em_construcao=each[5],
            )

    # empty column to style the page
    with col3:
        st.empty()

    # if "consent" not in st.session_state:
    #     consent_popup()

    st.write("")
    bottom_suport_email()


if __name__ == "__main__":
    main()
