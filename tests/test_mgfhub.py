# import streamlit as st
from streamlit.testing.v1 import AppTest

pages = [
    "mgfhub.py",
    "pages/2_Indicadores.py",
    "pages/3_IDE.py",
    "pages/5_FAQs.py",
    "pages/6_Sobre.py",
]

for each_page in pages:
    test = AppTest(each_page, default_timeout=30)
    test.run()
    assert not test.exception
