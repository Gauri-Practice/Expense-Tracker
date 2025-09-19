import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Tracker", layout="wide")
# page_title | text shown on the browser tab
# layout="wide" | Setting page size

if "expenses" not in st.session_state:
     st.session_state["expenses"] = []
    #  st_session_state | A special dictinary in Streamlit to store variables during the app session. Data here doesn't reset when you change pages.
    # if "expenses" not in st.session_state | checks if the key "expenses" already exists in the session state. If not, we create it.
    # st.session_state["expenses"] = [] | Initializes an empty list where we'll store expense dictionaries.

st.title("Expense Tracker")
# Main Header of the page

# st.write("This is a demo Streamlit app with dummy data.")
# # st.write | can show text, variables, tables, charts, etc.

# data = {f"""
#     Date = ["2025-09-01","2025-09-05","2025-09-10"],
#     "Category" = ["Food","Transport","Shopping"],
#     "Amount" = [120,50,553],
#     "Description" = ["I bought ice-creams","I went to my friend's house","I bought dress for my sister."]
#     """}

# df = pd.DataFrame(data)
# # df = short form of data frame.
# # DataFrame are like tables in Excel - Can display tables aor charts directly.

# if st.button("Show Expenses Table"):
#     st.table(df)
# # st.button | Create button named "Show expenses table"
# # st.table(df) | for small, simple tables we can use st.table() ➜ For bigger or interactive tables we'll use st.dataframe()

st.sidebar.header("Navigation")

# st.sidebar is a shortcut to put widgets in the sidebar.
# widgets | small tools or anything button. Like: st.sidebar.button, st.sidebar.selectbox.
page = st.sidebar.radio("Go to", ["Add Expenses", "View Expenses"])
# page | where data would be save
# radio() | radio button

# Add expense Page
if page == "Add Expenses":
    st.subheader("Add a new expense.")
    amount = st.number_input("Amount", min_value=0.0, step=0.1)
    # st.number_input() | Create widget where users can enter a numeric value.
    # min_value=0.0 | The smallest allowed value is 0.0 (Prevents(Not allowed) negative value)
    # If user write negative value streamlit automatically set entered value to 0.0
    # step=0.1 | When the user click the ▲▼ buttons, the number increases/decreases by 0.1.

    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Other"])
    date = st.date_input("Date")
    # Default is today if we don't pass a value.
    # Create a calendar widget where we selects a date and will storei in database.
    
    description = st.text_area("Description")
    # Can write note/description

    if st.button("Save Expenses"):
        # bool | a condition (True only when clicked during that run).
        st.session_state["expenses"].append({
             "Amount": amount,
             "Category": category,
             "Date": date,
             "Description": description
        })
        st.success(f"Expense of ₹{amount} added under {category}.")
        # 

# View Expenses Page
elif page == "View Expenses":
        st.subheader("All Expenses")
        if st.session_state["expenses"]:
             import pandas as pd
             df = pd.DataFrame(st.session_state["expenses"])
             st.dataframe(df)
        else:
             st.info("No expenses added yet.")
        # st.info() shows an informational blue box.
        # append({}) | is a list method that add whatever we oout inside of parentheses add as a  list.

