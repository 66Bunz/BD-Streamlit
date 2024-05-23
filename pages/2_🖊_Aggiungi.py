import streamlit as st
from utils.utils import *


def get_list(attributo):
    query = f"SELECT DISTINCT {attributo} FROM products"
    result = execute_query(st.session_state["connection"], query)
    result_list = []
    for row in result.mappings():
        result_list.append(row[attributo])
    return result_list


def get_info():
    return get_list("productLine"), get_list("productScale"), get_list("productVendor")


def check_info(prod_dict):
    for value in prod_dict.values():
        if value == "":
            return False
    return True


def insert(prod_dict):
    if check_info(prod_dict):
        attributi = ", ".join(prod_dict.keys())
        valori = tuple(prod_dict.values())
        query = f"INSERT INTO products ({attributi}) VALUES {valori};"
        # try-except per verificare che l'operazione MySQL abbia avuto successo, generare un errore altrimenti
        try:
            execute_query(st.session_state["connection"], query)
            st.session_state["connection"].commit()
        except Exception as e:
            st.error(e)
            return False
        return True
    else:
        return False


def create_form():
    with st.form("Nuovo Prodotto"):
        st.header(":blue[Inserisci un nuovo prodotto]")

        categorie, scale, venditori = get_info()
        code = st.text_input("Codice prodotto", placeholder="S**_****")
        nome = st.text_input(
            "Nome prodotto", placeholder="Inserisci il nome del prodotto"
        )
        categoria = st.selectbox("Categoria", categorie)
        scala = st.selectbox("Scala prodotto", scale)
        venditore = st.selectbox("Venditore", venditori)
        descrizione = st.text_area(
            "Descrizione", placeholder="Inserisci la descrizione del prodotto"
        )
        qta = st.slider("Quantità", 0, 10000)
        prezzo = st.number_input("Prezzo", 1.00)
        msrp = st.number_input("MSRP")

        # dizionario finale con tutti i parametri
        insert_dict = {
            "productCode": code,
            "productName": nome,
            "productLine": categoria,
            "productScale": scala,
            "productVendor": venditore,
            "productDescription": descrizione,
            "quantityInStock": qta,
            "buyPrice": prezzo,
            "MSRP": msrp,
        }

        # tasto submit fondamentale nel form
        submitted = st.form_submit_button("Submit", type="primary")

    if submitted:
        if insert(insert_dict):
            st.success("Hai inserito questo prodotto: ", icon="✅")
            st.write(insert_dict)
        else:
            st.error("Impossibile aggiungere il prodotto.", icon="⚠️")


def main():
    st.title("🖊 Aggiungi")
    if check_connection():
        create_form()


if __name__ == "__main__":
    main()
