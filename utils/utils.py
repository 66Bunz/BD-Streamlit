import streamlit as st
from sqlalchemy import create_engine, text
import time


def get_list(attributi, tabella):
    attributi_str = ", ".join(attributi)
    query = f"SELECT DISTINCT {attributi_str} FROM {tabella}"
    query_result = execute_query(st.session_state["connection"], query)

    if len(attributi) == 1:
        return [row[attributi[0]] for row in query_result.mappings()]
    result_list = []
    for row in query_result.mappings():
        result_list.append(tuple(row[attributo] for attributo in attributi))

    return result_list


def connect_db(dialect, username, password, host, dbname):
    try:
        engine = create_engine(f"{dialect}://{username}:{password}@{host}/{dbname}")
        conn = engine.connect()
        return conn
    except:
        return False


def execute_query(conn, query):
    return conn.execute(text(query))


def compact_format(num):
    num = float(num)
    if abs(num) >= 1e9:
        return "{:.2f}B".format(num / 1e9)
    elif abs(num) >= 1e6:
        return "{:.2f}M".format(num / 1e6)
    elif abs(num) >= 1e3:
        return "{:.2f}K".format(num / 1e3)
    else:
        return "{:.0f}".format(num)


def check_connection():
    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    with st.sidebar:
        if st.button("Connettiti al Database"):
            with st.spinner("Connettendo il DB..."):
                myconnection = connect_db(
                    dialect="mysql+pymysql",
                    username="root",
                    password="",
                    host="localhost",
                    dbname="palestra",
                )
                if myconnection is not False:
                    st.session_state["connection"] = myconnection

                    st.toast("Connessione al DB riuscita", icon="✅")

                else:
                    st.session_state["connection"] = False
                    st.error("Errore nella connessione al DB")

                    st.toast("Errore nella connessione al DB", icon="❌")

    if st.session_state["connection"]:
        st.sidebar.success("Connesso al DB")
        return True
