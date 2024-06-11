import streamlit as st
from utils.utils import *
import pandas as pd
from datetime import date


def check_dati(prod_dict):
    for item in prod_dict.items():
        if item[0] != "Telefono":
            if item[1] == "":
                return False
    return True


def inserisci(prod_dict):
    if check_dati(prod_dict):
        attributi = ", ".join(prod_dict.keys())
        valori = tuple(prod_dict.values())

        query = f"""
        INSERT INTO ISTRUTTORE (CodFisc, Nome, Cognome, DataNascita, Email, Telefono) 
        VALUES (
            '{prod_dict['CodFisc']}', 
            '{prod_dict['Nome']}', 
            '{prod_dict['Cognome']}', 
            '{prod_dict['DataNascita']}', 
            '{prod_dict['Email']}', 
            {'NULL' if prod_dict['Telefono'] is None else f"{prod_dict['Telefono']}"}
        )
        """

        try:
            execute_query(st.session_state["connection"], query)
            st.session_state["connection"].commit()
        except Exception as e:
            st.error(e)
            return False
        return True
    else:
        return False


def crea_pagina():
    with st.form("Nuovo Istruttore", clear_on_submit=True):
        st.header(":blue[Aggiungi le informazioni dell'istruttore]")

        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome", placeholder="Inserisci il nome dell'istruttore")
        cognome = col2.text_input(
            "Cognome", placeholder="Inserisci il cognome dell'istruttore"
        )
        codice_fiscale = st.text_input(
            "Codice fiscale", placeholder="Inserisci il codice fiscale dell'istruttore"
        )

        data_nascita = str(st.date_input("Data di nascita"))
        data_nascita

        col1, col2 = st.columns(2)
        email = col1.text_input(
            "Email", placeholder="Inserisci l'email dell'istruttore"
        )
        telefono = col2.text_input(
            "Telefono", placeholder="Inserisci il telefono dell'istruttore"
        )

        if telefono == "":
            telefono = None

        insert_dict = {
            "CodFisc": codice_fiscale,
            "Nome": nome,
            "Cognome": cognome,
            "DataNascita": data_nascita,
            "Email": email,
            "Telefono": telefono,
        }

        submitted = st.form_submit_button("Submit", type="primary")

    if submitted:
        if inserisci(insert_dict):
            st.success("Hai inserito un nuovo istruttore: ", icon="✅")
            st.write(insert_dict)
        else:
            st.error("Impossibile aggiungere l'istruttore.", icon="⚠️")


if __name__ == "__main__":
    st.title(":blue[Nuovo istruttore]")

    st.logo("images\BunzLogo4.png", link="https://github.com/66Bunz/BD-Streamlit")

    if check_connection():
        crea_pagina()
    else:
        st.error("Impossibile aggiungere un nuovo istruttore. Connessione al DB non effettuata. Si prega di connettere il DB dalla sidebar.", icon="🚨")
