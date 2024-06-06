import streamlit as st
from utils.utils import *
import pandas as pd
from datetime import date, time


def inserisci(prod_dict):
    if check_dati(prod_dict):
        attributi = ", ".join(prod_dict.keys())
        valori = tuple(prod_dict.values())
        query = f"INSERT INTO programma ({attributi}) VALUES {valori};"

        try:
            execute_query(st.session_state["connection"], query)
            st.session_state["connection"].commit()
        except Exception as e:
            st.error(e)
            return False
        return True
    else:
        return False


def check_dati(prod_dict):
    for chiave, valore in prod_dict.items():
        if valore == "":
            return False
        if chiave == "Durata":
            if valore < 0 or valore > 60:
                return False
        elif chiave == "Giorno":
            if valore in ["Sabato", "Domenica"]:
                return False
        return True


def check_disponibilita(prod_dict):
    query = f"SELECT CodFisc, Giorno, OraInizio FROM programma WHERE CodFisc='{prod_dict['CodFisc']}' AND Giorno='{prod_dict['Giorno']}'"

    risultato = execute_query(st.session_state["connection"], query).mappings().first()
    if risultato is None:
        return True

    return False


def crea_pagina():
    with st.form("Nuova lezione", clear_on_submit=True):
        st.header(":blue[Aggiungi le informazioni della lezione]")

        opzioni_istruttori = get_list(["Nome", "Cognome", "CodFisc"], "istruttore")
        opzioni_corsi = get_list(["Nome", "CodC"], "corsi")

        istruttore = st.selectbox(
            "Istruttore",
            opzioni_istruttori,
            index=None,
            placeholder="Seleziona un istruttore...",
            format_func=lambda x: f"{x[0]} {x[1]} - {x[2]}",
        )

        corso = st.selectbox(
            "Corso",
            opzioni_corsi,
            index=None,
            placeholder="Seleziona un corso...",
            format_func=lambda x: f"{x[0]} - {x[1]}",
        )

        giorno = st.selectbox(
            "Giorno", ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"]
        )

        ora = st.time_input("Ora", time(8, 0))
        durata = st.select_slider("Durata (minuti)", range(1, 61))
        sala = st.text_input("Sala", placeholder="Inserisci la sala")

        submitted = st.form_submit_button("Submit", type="primary")

    if submitted:
        codice_fiscale = istruttore[2]

        insert_dict = {
            "CodFisc": codice_fiscale,
            "Giorno": giorno,
            "OraInizio": str(ora),
            "Durata": int(durata),
            "CodC": corso[1],
            "Sala": sala,
        }

        if check_dati(insert_dict) and check_disponibilita(insert_dict):
            if inserisci(insert_dict):
                st.success("Hai inserito una nuova lezione: ", icon="✅")
                st.write(insert_dict)
            else:
                st.error("Impossibile aggiungere la lezione.", icon="⚠️")


if __name__ == "__main__":
    st.title("Nuova lezione")

    if check_connection():
        crea_pagina()
    else:
        st.error("Connessione al DB non effettuata")
