from streamlit.testing.v1 import AppTest
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can access the variables using os.getenv

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

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
