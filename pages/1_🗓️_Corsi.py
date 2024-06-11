import streamlit as st
from utils.utils import *
import pandas as pd


def get_tipi_corso():
    result = execute_query(
        st.session_state["connection"],
        "SELECT DISTINCT Tipo FROM corsi;",
    )
    tipi = []
    for row in result.mappings():
        tipi.append(row["Tipo"])
    return tipi


def crea_pagina():
    col1, col2 = st.columns(2)

    query_num_corsi = execute_query(
        st.session_state["connection"],
        "SELECT COUNT(*) AS 'Corsi Totali', COUNT(DISTINCT Tipo) AS 'Tipo Corsi' FROM corsi;",
    )
    num_corsi_dict = [
        dict(zip(query_num_corsi.keys(), result)) for result in query_num_corsi
    ]

    col1.metric("Numero di corsi", f"{(num_corsi_dict[0]['Corsi Totali'])}")
    col2.metric("Tipi di corsi", f"{(num_corsi_dict[0]['Tipo Corsi'])}")

    st.subheader("Filtra i corsi")
    col21, col22 = st.columns([3, 1])

    filtri_corso = col22.multiselect(
        "Filtra il tipo",
        get_list(["Tipo"], "corsi"),
        format_func=lambda x: x,
        key="selezione_corsi",
    )

    range = col22.select_slider(
        "Seleziona un range di livello",
        [1, 2, 3, 4],
        value=(1, 4),
        key="range_livello_corsi",
    )

    def reset():
        st.session_state.selezione_corsi = []
        st.session_state.range_livello_corsi = (1, 4)

    col22.button("Reset", on_click=reset)

    if filtri_corso:
        if len(filtri_corso) == 1:
            query = f"SELECT * FROM corsi WHERE Livello BETWEEN {range[0]} AND {range[1]} AND Tipo = '{filtri_corso[0]}';"
        else:
            query = f"SELECT * FROM corsi WHERE Livello BETWEEN {range[0]} AND {range[1]} AND Tipo IN {tuple(filtri_corso)};"
    else:
        query = f"SELECT * FROM corsi WHERE Livello BETWEEN {range[0]} AND {range[1]};"
    corsi_filtrati = execute_query(st.session_state["connection"], query)

    df_corsi = pd.DataFrame(corsi_filtrati)
    col21.dataframe(df_corsi, use_container_width=True)

    expander = st.expander("Visualizza i programmi delle lezioni")

    if df_corsi.empty:
        expander.warning(
            "Nessun corso selezionato. Per favore, seleziona almeno un corso."
        )
    else:
        for index, row in df_corsi.iterrows():
            query = f"""
            SELECT PROGRAMMA.Giorno, PROGRAMMA.OraInizio, PROGRAMMA.Durata, PROGRAMMA.Sala, ISTRUTTORE.Nome, ISTRUTTORE.Cognome 
            FROM PROGRAMMA 
            INNER JOIN ISTRUTTORE ON PROGRAMMA.CodFisc = ISTRUTTORE.CodFisc 
            WHERE PROGRAMMA.CodC = '{row['CodC']}';
            """
            risultati = execute_query(st.session_state["connection"], query)

            if risultati:
                df_risultati = pd.DataFrame(
                    risultati,
                    columns=[
                        "Giorno",
                        "OraInizio",
                        "Durata",
                        "Sala",
                        "Nome",
                        "Cognome",
                    ],
                )
                risultati_dict = df_risultati.to_dict()

                expander.subheader(f":green[{row['Nome']}]")

                expander.write(f"**Tipo**: {row['Tipo']}")
                expander.write(f"**Livello**: {row['Livello']}")
                expander.write(
                    f"**Numero di lezioni**: {len(risultati_dict['Giorno'])}"
                )

                tot_lezioni = len(risultati_dict["Giorno"])

                nomi_lezioni = []
                i = 0
                while i < tot_lezioni:
                    nomi_lezioni.append(f"Lezione {i+1}")
                    i += 1
                if tot_lezioni == 0:
                    expander.warning("Nessuna lezione disponibile")
                else:
                    tabs = expander.tabs(nomi_lezioni)

                    for i, tab in enumerate(tabs):
                        tab.write(f"**Giorno**: {risultati_dict['Giorno'][i]}")
                        tab.write(
                            f"**Ora di inizio**: {risultati_dict['OraInizio'][i]}"
                        )
                        tab.write(f"**Durata**: {risultati_dict['Durata'][i]}")
                        tab.write(f"**Sala**: {risultati_dict['Sala'][i]}")
                        tab.write(
                            f"**Istruttore**: {risultati_dict['Nome'][i]} {risultati_dict['Cognome'][i]}"
                        )

                expander.divider()


if __name__ == "__main__":
    st.title(":blue[Corsi disponibili]")

    st.logo("images\BunzLogo4.png", link="https://github.com/66Bunz/BD-Streamlit")

    if check_connection():
        crea_pagina()
    else:
        st.error("Impossibile mostrare i corsi disponibili. Connessione al DB non effettuata. Si prega di connettere il DB dalla sidebar.", icon="🚨")
