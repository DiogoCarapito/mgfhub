import tabula
import pandas as pd
import re
#from pdfminer.high_level import extract_text

text=extract_text('extra/apmcg_ICPC-v-1.7.pdf')
print(text)

#table = tabula.read_pdf('extra/apmcg_ICPC-v-1.7.pdf',pages=51)
#print(table)

#df = pd.DataFrame(table)
#print(df.dropna())