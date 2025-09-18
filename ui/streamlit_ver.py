import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Tracker", layout="wide")
# page_title | text shown on the browser tab
# layout="wide" | Setting page size

st.title("Expense Tracker")
# Main Header of the page

st.write("This is a demo Streamlit app with dummy data.")
# st.write | can show text, variables, tables, charts, etc.

data = {f"""
    Date = ["2025-09-01","2025-09-05","2025-09-10"],
    "Category" = ["Food","Transport","Shopping"],
    "Amount" = [120,50,553],
    "Description" = ["I bought ice-creams","I went to my friend's house","I bought dress for my sister."]
    """}

df = pd.DataFrame(data)
# df = short form of data frame.
# DataFrame are like tables in Excel - Can display tables aor charts directly.

if st.button("Show Expenses Table"):
    st.table(df)
# st.button | Create button named "Show expenses table"
# st.table(df) | for small, simple tables we can use st.table() ➜ For bigger or interactive tables we'll use st.dataframe()
