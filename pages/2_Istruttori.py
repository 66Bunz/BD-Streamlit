import streamlit as st
from utils.utils import *
import pandas as pd
from datetime import date


def crea_pagina():
    col1, col2 = st.columns([1, 2])

    filtro_congome = col1.text_input("Cerca per Cognome", key="filtro_congome")
    range_data = col1.date_input(
        "Seleziona un range di date di nascita",
        (date(1970, 1, 1), date.today()),
        key="range_data",
    )

    col11, col12 = col1.columns(2)

    if col11.button("Cerca"):
        query = f"""
        SELECT CodFisc, Nome, Cognome, DataNascita, Email, Telefono
        FROM ISTRUTTORE
        WHERE Cognome LIKE '{filtro_congome}%' AND DataNascita BETWEEN '{range_data[0]}' AND '{range_data[1]}';
        """

        query_istruttori = execute_query(st.session_state["connection"], query)

        df_istruttori = pd.DataFrame(query_istruttori)
        if not df_istruttori.empty:

            for index, istruttore in df_istruttori.iterrows():
                col21, col22 = col2.columns([3, 1])
                col21.markdown(f"### Istruttore {index + 1}")
                col21.markdown(f"**Codice Fiscale**: {istruttore['CodFisc']}")
                col21.markdown(f"**Nome**: {istruttore['Nome']}")
                col21.markdown(f"**Cognome**: {istruttore['Cognome']}")
                col21.markdown(f"**Data di Nascita**: {istruttore['DataNascita']}")
                col21.markdown(f"**Email**: {istruttore['Email']}")
                if istruttore["Telefono"] is None:
                    col21.markdown(f"**Telefono**: :red[Non disponibile]")
                else:
                    col21.markdown(
                        f"**Telefono**: [{istruttore['Telefono']}](tel:{istruttore['Telefono']})"
                    )
                col22.image("images/user.png", use_column_width=False)
                col22.write("image: Flaticon.com")
                col2.divider()

        else:
            col2.warning(
                "Nessun istruttore trovato per i criteri di ricerca specificati."
            )

    def reset():
        st.session_state.filtro_congome = ""
        st.session_state.range_data = (date(1970, 1, 1), date.today())

    col12.button("Reset", on_click=reset)


if __name__ == "__main__":
    st.title("Istruttori disponibili")

    if check_connection():
        crea_pagina()
    else:
        st.error("Connessione al DB non effettuata")
