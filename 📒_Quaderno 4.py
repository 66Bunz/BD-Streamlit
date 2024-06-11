import streamlit as st
import numpy as np
import pandas as pd
from utils.utils import *
import pymysql, cryptography


def crea_pagina():
    st.title("📒 - Quaderno 4")
    st.header("Sviluppo di un'applicazione web con Streamlit e MySQL")

    st.divider()

    st.subheader("Obiettivo")
    st.markdown(
        "Creare un’applicazione web in Python (Streamlit) in grado di interagire con un database MySQL in modo da eseguire interrogazioni in base alle interazioni dell’utente."
    )

    st.subheader("Descrizione del Database")
    st.markdown(
        "La base di dati si chiama PALESTRA e riguarda le attività di una palestra. Essa è caratterizzata dal seguente schema logico (le chiavi primarie sono sottolineate):"
    )
    st.code(
        """ISTRUTTORE (CodFisc, Nome, Cognome, DataNascita, Email, Telefono*)\n
CORSI (CodC, Nome, Tipo, Livello)\n
PROGRAMMA (CodFisc, Giorno, OraInizio, Durata, CodC, Sala)""",
        language="sql",
    )

    st.divider()

    st.subheader("Studente")
    st.markdown(
        """
    **MATRICOLA**: S313817\n
    **NOME**: Alessandro\n
    **COGNOME**: Burzio\n
    """
    )

    st.divider()

    st.subheader("Numero lezioni")
    lezioni = pd.DataFrame(
        {"Numero Lezioni": [1, 1, 1, 3, 3, 4, 4]},
        index=[8.30, 10, 11.30, 13, 14.30, 16, 17.30],
    )
    st.bar_chart(lezioni, y="Numero Lezioni")

    st.divider()

    giorni = pd.DataFrame(
        {"Numero Lezioni": [3, 2, 2, 2, 2]},
        index=[0, 1, 2, 3, 4],
    )

    st.area_chart(giorni)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Quaderno 4",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/66Bunz/BD-Streamlit/issues",
            "Report a bug": "https://github.com/66Bunz/BD-Streamlit/issues",
            "About": "# Quaderno 4 *Basi di dati* - Alessandro Burzio - S313817",
        },
    )

    st.logo("images\BunzLogo4.png", link="https://github.com/66Bunz/BD-Streamlit")

    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    check_connection()

    crea_pagina()
