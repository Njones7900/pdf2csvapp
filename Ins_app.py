import streamlit as st  # data app development
import subprocess  # process in the os
from subprocess import STDOUT, check_call  # os process manipulation
import os  # os process manipulation
import base64  # byte object into a pdf file
import uuid
import pandas as pd
import tabula
import tabulate
from sqlalchemy import Float


@st.cache
def gh():
    proc = subprocess.Popen('apt-get install -y ghostscript', shell=True, stdin=None, stdout=open(os.devnull, "wb"),
                            stderr=STDOUT)
    proc.wait()


gh()

st.title("PDF Table Extractor")
st.subheader("For Insurance Docs")

st.image("https://raw.githubusercontent.com/camelot-dev/camelot/master/docs/_static/camelot.png", width=200)

# file uploader on streamlit

input_pdf = st.file_uploader(label="upload your pdf here", type='pdf')

if input_pdf is not None:
    # byte object into a PDF file
    with open("input.pdf", "wb") as f:
        base64_pdf = base64.b64encode(input_pdf.read()).decode('utf-8')
        f.write(base64.b64decode(base64_pdf))
    f.close()

    # Read the pdf with Tabula and convert to csv
    tabula.convert_into(input_pdf, "tabula.csv", output_format="csv", pages="all", area=(122.018, 72.293, 721.013,
                                                                                         538.943))
    #  Convert csv to df
    df = pd.read_csv("tabula.csv")

    st.markdown("### Output Table of entire PDF")

    # display the output after parsing
    st.write(df)

    # Changed Unnamed: 5 to data type float
    df['Unnamed: 5'] = pd.to_numeric(df['Unnamed: 5'], errors='coerce')

    # Pivoted into df
    tmp_df = df[['Unnamed: 1', 'Unnamed: 5']]
    pivot_table = tmp_df.pivot_table(
        index=['Unnamed: 1'],
        values=['Unnamed: 5'],
        aggfunc={'Unnamed: 5': ['sum']}
    )

    st.markdown("### Output Pivot Table")

    # Display Pivot Table Output
    st.write(pivot_table)

    # Download as a csv file
    st.download_button("Download as CSV",
                       pivot_table.to_csv(),
                       file_name='insurance_totals.csv',
                       mime='text/csv')
