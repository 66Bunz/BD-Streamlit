import streamlit as st
from utils.utils import *
import pandas as pd


def create_tab_prodotti(tab_prodotti):
    col1, col2, col3 = tab_prodotti.columns(3)
    payment_info = execute_query(
        st.session_state["connection"],
        "SELECT SUM(amount) AS 'Total Amount', MAX(amount) AS 'Max Payment', AVG(amount) AS 'Average Payment' FROM payments;",
    )

    payment_info_dict = [
        dict(zip(payment_info.keys(), result)) for result in payment_info
    ]

    col1.metric(
        "Importo Totale", f"$ {compact_format(payment_info_dict[0]['Total Amount'])}"
    )
    col2.metric(
        "Pagamento Massimo", f"$ {compact_format(payment_info_dict[0]['Max Payment'])}"
    )
    col3.metric(
        "Pagamento Medio",
        f"$ {compact_format(payment_info_dict[0]['Average Payment'])}",
    )

    with tab_prodotti.expander("Panoramica prodotti"):
        prod_col1, prod_col2, prod_col3 = st.columns([3, 3, 6])

        sort_param = prod_col1.radio(
            "Ordina per:", ["Codice", "Nome", "Quantità", "Prezzo"]
        )

        sort_param_dict = {
            "Codice": "code",
            "Nome": "name",
            "Quantità": "quantity",
            "Prezzo": "price",
        }

        sort_choice = prod_col2.selectbox("Ordine:", ["Crescente", "Decrescente"])

        sort_choice_dict = {"Crescente": "ASC", "Decrescente": "DESC"}

        if prod_col1.button("Mostra", type="primary"):
            query_base = "SELECT productCode AS 'code', productName AS 'name', quantityInStock AS quantity, buyPrice AS price, MSRP FROM products"
            query_sort = f"ORDER BY {sort_param_dict[sort_param]} {sort_choice_dict[sort_choice]};"

            prodotti = execute_query(
                st.session_state["connection"], query_base + " " + query_sort
            )

            df_prodotti = pd.DataFrame(prodotti)
            st.dataframe(df_prodotti, use_container_width=True)

    with tab_prodotti.expander("Pagamenti"):
        query = "SELECT MIN(paymentDate), MAX(paymentDate) FROM payments"

        date = execute_query(st.session_state["connection"], query)

        min_max = [dict(zip(date.keys(), result)) for result in date]

        min_value = min_max[0]["MIN(paymentDate)"]
        max_value = min_max[0]["MAX(paymentDate)"]

        date_range = st.date_input(
            "Seleziona il range di date:",
            value=(min_value, max_value),
            min_value=min_value,
            max_value=max_value,
        )
        query = f"SELECT paymentDate, SUM(amount) as 'Total Amount' FROM payments WHERE paymentDate >'{date_range[0]}' AND paymentDate <'{date_range[1]}' GROUP BY paymentDate"

        paymentsDate = execute_query(st.session_state["connection"], query)
        df_paymentDate = pd.DataFrame(paymentsDate)

        # verificare che ci siano dati nel periodo selezionato
        if df_paymentDate.empty:
            st.warning("Nessun dato trovato.", icon="⚠️")
        else:
            # trasformare in float e date type
            df_paymentDate["Total Amount"] = df_paymentDate["Total Amount"].astype(
                float
            )
            df_paymentDate["paymentDate"] = pd.to_datetime(
                df_paymentDate["paymentDate"]
            )

            st.write("Periodo", date_range[0], "-", date_range[1])
            st.line_chart(df_paymentDate, x="paymentDate", y="Total Amount")


def create_tab_staff(tab_staff):
    col1, col2 = tab_staff.columns(2)

    president_query = (
        "SELECT lastName,firstName FROM employees WHERE jobTitle='President'"
    )
    president = (
        execute_query(st.session_state["connection"], president_query)
        .mappings()
        .first()
    )
    vp_sales_query = (
        "SELECT lastName,firstName FROM employees WHERE jobTitle='VP Sales'"
    )
    vp_sales = (
        execute_query(st.session_state["connection"], vp_sales_query).mappings().first()
    )

    col1.markdown(
        f"#### :blue[PRESIDENT:] {president['firstName']} {president['lastName']}"
    )
    col2.markdown(
        f"#### :orange[VP SALES:] {vp_sales['firstName']} {vp_sales['lastName']}"
    )

    staff_query = "SELECT jobTitle,COUNT(*) as numDipendenti FROM employees GROUP BY jobTitle ORDER BY numDipendenti DESC;"

    staff = execute_query(st.session_state["connection"], staff_query)
    df_staff = pd.DataFrame(staff)
    tab_staff.markdown("### Componenti Staff")

    tab_staff.bar_chart(
        df_staff, x="jobTitle", y="numDipendenti", use_container_width=True
    )


def create_tab_clienti(tab_clienti):
    col1, col2 = tab_clienti.columns(2)
    
    query = "SELECT COUNT(*) as 'numeroClienti',country FROM customers GROUP by country order by `numeroClienti` DESC;"
    result = execute_query(st.session_state["connection"], query)
    df = pd.DataFrame(result)
    
    col1.subheader("Distribuzione clienti nel mondo")
    col1.dataframe(df, use_container_width=True, height=350)

    query = "SELECT customername, state, creditLimit FROM customers WHERE country = 'USA' AND creditLimit > 100000 ORDER BY creditLimit DESC;"
    result = execute_query(st.session_state["connection"], query)
    df = pd.DataFrame(result)

    col2.subheader("Clienti con maggior *credit limit* negli USA")
    col2.dataframe(df, use_container_width=True, height=350)


def main():
    st.title("📈 Analisi")

    tab_prodotti, tab_staff, tab_clienti = st.tabs(["Prodotti", "Staff", "Clienti"])

    if check_connection():
        create_tab_prodotti(tab_prodotti)
        create_tab_staff(tab_staff)
        create_tab_clienti(tab_clienti)


if __name__ == "__main__":
    main()
