import streamlit as st
import pyperclip

from transformers import AutoTokenizer, BertForSequenceClassification

import icd10

from utils.style import page_config, main_title


page_config()

main_title("text-to-ICPC2 (mas para já, teste com ICD-10)")


def process_request_icd10(text):
    encoded_input = tokenizer(text, return_tensors="pt")
    output = model(**encoded_input)

    results = output.logits.detach().cpu().numpy()[0].argsort()[::-1][:5]
    final_results = [config.id2label[ids] for ids in results]

    return final_results


def process_request_icpc2(text):
    result = {
        "input": text,
        "icpc2": "T90",
        "description": "Diabetes não insulino-dependente",
        "rating": 0.9,
    }

    result2 = {
        "input": text,
        "icpc2": "T89",
        "description": "Diabetes insulino-dependente",
        "rating": 0.8,
    }

    st.session_state["response_icpc2"].append(result)
    st.session_state["response_icpc2"].append(result2)


def resposta(result):
    icpc2 = result["icpc2"]
    description = result["description"]
    # rating = result["rating"]

    col_icpc_1, col_icpc_2, col_icpc_4, col_icpc_5, col_icpc_6 = st.columns(
        [1, 6, 3, 3, 1]
    )

    with col_icpc_1:
        st.markdown(
            f'<p style="text-align: center; font-size: 18px;">{icpc2}</p>',
            unsafe_allow_html=True,
        )

    with col_icpc_2:
        st.markdown(
            f'<p style="text-align: left; font-size: 18px;">{description}</p>',
            unsafe_allow_html=True,
        )

    # with col_icpc_3:
    #     st.markdown(
    #         f'<p style="text-align: center; font-size: 18px;">{rating}</p>',
    #         unsafe_allow_html=True,
    #     )

    with col_icpc_4:
        if st.button(
            "Copiar código",
            type="primary",
            key=f"copy_{icpc2}",
        ):
            pyperclip.copy(icpc2)

    with col_icpc_5:
        if st.button(
            "Copiar descrição",
            type="primary",
            key=f"copy_{description}",
        ):
            pyperclip.copy(description)

    with col_icpc_6:
        st.button(":thumbsdown:", key=f"thumbsdown_{icpc2}")


if "input_icd10" not in st.session_state:
    st.session_state["input_icd10"] = ""

if "output_icd10" not in st.session_state:
    st.session_state["output_icd10"] = []

if "response_icpc2" not in st.session_state:
    st.session_state["response_icpc2"] = []

if "input_icpc2" not in st.session_state:
    st.session_state["input_icpc2"] = ""

tab_icd10, tab_icpc2 = st.tabs(["ICD-10", "ICPC2"])

with tab_icd10:
    st.write(
        "O objetivo é converter um diagnóstico em texto clínico converter o código ICD-10 correspondente utilizado um modelo já pré-treinado como prova de conceito. A utilização pode ser usada como feedback para treinar o modelo e melhorar a performance."
    )
    st.divider()

    tokenizer = AutoTokenizer.from_pretrained("AkshatSurolia/ICD-10-Code-Prediction")
    model = BertForSequenceClassification.from_pretrained(
        "AkshatSurolia/ICD-10-Code-Prediction"
    )
    config = model.config

    col_text_input_1, col_text_input_2 = st.columns([3, 1])

    with col_text_input_1:
        st.session_state["input_icd10"] = st.text_input(
            "Colocar o texto aqui:",
            label_visibility="collapsed",
            # on_change=process_request(st.session_state["input"]),
            value="diabetes mellitus",
            key="inputicd10",
        )

    with col_text_input_2:
        if st.button("Submeter", key="submeter_icd10"):
            # st.session_state["response"] = []
            # process_request(st.session_state["input"])
            st.session_state["output_icd10"] = process_request_icd10(
                st.session_state["input_icd10"]
            )

    if st.session_state["input_icd10"]:
        st.write("")
        for each in st.session_state["output_icd10"]:
            col_1, col_2, col_3, col_4, col_5 = st.columns([1, 4, 2, 2, 1])
            code = icd10.find(each).description

            with col_1:
                st.write(each)
            with col_2:
                st.write(code)

            with col_3:
                if st.button("Copiar código", type="primary", key=f"code_{each}"):
                    pyperclip.copy(each)

            with col_4:
                if st.button(
                    "Copiar descrição", type="primary", key=f"description_{each}"
                ):
                    pyperclip.copy(code)
            # st.markdown(f"https://www.icd10data.com/search?s={each}")

            with col_5:
                st.button(":thumbsdown:", key=f"thumbsdown_{each}")

    st.divider()
    st.markdown(
        "Modelo utilizado: **AkshatSurolia/ICD-10-Code-Prediction** disponível em [Hugging Face](https://huggingface.co/AkshatSurolia/ICD-10-Code-Prediction)"
    )
    st.markdown(
        "Código fonte disponível em [https://github.com/DiogoCarapito/text-to-icpc2](https://github.com/DiogoCarapito/text-to-icpc2)"
    )

with tab_icpc2:
    # descricao("Insira o texto e obtenha o código ICPC2 correspondente")

    st.write("Ainda não funciona, só vai dar diabetes :smile:")

    col_text_input_1, col_text_input_2 = st.columns([3, 1])

    with col_text_input_1:
        st.session_state["input_icpc2"] = st.text_input(
            "Colocar o texto aqui:",
            label_visibility="collapsed",
            # on_change=process_request(st.session_state["input"]),
            key="inputicpc2",
        )

    with col_text_input_2:
        if st.button("Submeter", key="submeter_icpc2"):
            st.session_state["response_icpc2"] = []
            process_request_icpc2(st.session_state["input_icpc2"])

    if st.session_state["input_icpc2"]:
        st.write("")
        for each in st.session_state["response_icpc2"]:
            resposta(each)


def main():
    return None
