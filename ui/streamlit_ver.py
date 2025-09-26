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


if "category" not in st.session_state:
     st.session_state["category"] = ["Food", "Travel", "Shopping", "Other"]
     # We'll use st.session_state (a streamlit feature) to store the list of categories. This way, if we add a new category, it stays in the dropdown until we close the app.
     # and we're setting default value of category when there is no category added.

st.title("Expense Tracker")
# Main Header of the page

st.sidebar.header("Navigation")
# st.sidebar is a shortcut to put widgets in the sidebar.
# widgets | small tools or anything button. Like: st.sidebar.button, st.sidebar.selectbox.

page = st.sidebar.radio("Go to", ["Add Expenses", "View Expenses"])
# page | where data would be save
# radio() | radio button

# Add expense Page
if page == "Add Expenses":
     st.subheader("Add a new expense.")
     category_choice = st.selectbox(
          "Category", st.session_state["category"], key="add_category"
          )
     if category_choice == "Other":
          custom_category = st.text_input("Enter custom catgory", key="custom_category")
     else:
          if "custom_category" in st.session_state:
               st.session_state["custom_category"] = ""
     with st.form("Add Expenses_form"):
          amount = st.number_input("Amount", min_value=0.0, step=0.1, key="amt")
    # st.number_input() | Create widget where users can enter a numeric value.
    # min_value=0.0 | The smallest allowed value is 0.0 (Prevents(Not allowed) negative value)
    # If user write negative value streamlit automatically set entered value to 0.0
    # step=0.1 | When the user click the ▲▼ buttons, the number increases/decreases by 0.1.
    # Key give special identify to widget. If two widgets don't have unique keys, their value can clash when re-rendering.
    # We can also track value after reruns with the helps of keys.
    # Example: user enter amount "42.5", we can read it with st.session_state["amt"].

          date_input = st.date_input("Date", key="date_input")
    # Default is today if we don't pass a value.
    # Create a calendar widget where we selects a date and will storei in database.
    
          description = st.text_area("Description", key="description")
    # Can write note/description

          submitted = st.form_submit_button("Save expense")
    # A form prevents reruns until you actually click Save Expense.
    # Streamlit keeps widget values in memory. If two widgets don't have unique keys, their values can clash when re-rendering.
    # Adding keys ensure each widget's state is tracked correctly (so category/ text input don't overwrite each other).
    # All values in the form become avaiable on the form submit.
    # Why use st.form_submit_button Without a form every widget change may rerun the app immediately (causing mid-edit UI jumps). The form batches changes and only acts when the user click submit.
    # submitted is False on normal reruns, it becomes True only once (the run immediately after the click).
    # Use it to control saving logic.
          if submitted:
               if category_choice == "Other":
                    custom_val = st.session_state.get("custom_category", "").strip()
                    if not custom_category.strip():
                         st.error("⚠️ Please enter a custom category or choose another category.")
                    else:
                         final_category = custom_category.strip().title()
                         # final_category = custom_category.strip() | Ensure the expense goes under the custom input instead of "Other".
                         # .strip() removes spaces.
                         # If user leave custom category blank, it stop and show and error(so category can't be empty).

                         if final_category not in st.session_state["category"]:
                              try:
                                   other_idx = st.session_state["category"].index("Other")
                                   st.session_state["category"].insert(other_idx, final_category)
                              except ValueError:
                                   st.session_state["category"].append(final_category)
                         # list.index("name") returns the index position where "name" occurs.
                         # Example: category.index(other)
                         # Prevent adding duplicate categories.
                         # This add custom_category to the list.
                         # .insert(-1, category) | putting custome_category before the last item, so "Other" always stays at the end.

                         # Clear the text field after a successful save. otherwise the old custom category text stays there forever.
                         # list.index("Other") raises ValueError if "Other" is not found (edge case.) The except handles that situation.
                         # If Other is missing, we simply append the new category to the end of the list (again checking duplicates before adding).

          


                         
                         st.session_state["expenses"].append({
                              "Amount":float(st.session_state.get("amt", 0.0)),
                              "Category": final_category,
                              "Date": st.session_state.get("date_input"),
                              "Descripition": st.session_state.get("description", "")
                         })
                         st.success("Expense Saved.")
               else:
                    final_category = category_choice
                    st.session_state["expenses"].append({
                         "Amount": float(amount),
                         "Category": final_category,
                         "Date": date_input,
                         "Description": description
                    })
                    st.success("✅ Expense saved.")


# View Expenses Page
elif page == "View Expenses":
     st.subheader("All Expenses")
             
     df = pd.DataFrame(st.session_state["expenses"])

     if not df.empty:
          filter_opts = ["All"] + st.session_state["category"]
          prev = st.session_state.get("view_category_filter", "All")
          index = filter_opts.index(prev) if prev in filter_opts else 0
          selected_cat = st.selectbox("Filter by category", filter_opts, index=index, key="view_category_filter")
          # builds the dropdown options from the same st.session_state["category"] list you update when user adds custom categories.
          # "All" is prepended so users can see everything.
          # Show filter dropdown on the view page. Because it reads st.session_state["category"].
          # Any new category inserted will appear here on the next rerun.

          if selected_cat != "All":
                  df = df[df["Category"] == selected_cat]
          # Filter the DataFrame so only rows with the chosen category are shown. If "All" is selected, we skip filtering.
                  
          st.dataframe(df)
          # Show filtered dataframe

          total = df["Amount"].sum()
          # Id df(DataFrame of displayed expenses) is not empty, compute the sum of the "Amount" column.
          # If it is empty, return 0.0 to avoid error calling .sum() on missing column or empty df.
          
          st.markdown(f"**Total:** ₹{total:.2f}")
          # f"**Total:** ₹{total:.2f}" formats the number with two decimal places and bold label (**Total**).

          csv = df.to_csv(index=False).encode("utf-8")
          # to convert df to CSV text using df.to_csv(index=False), which excludes the DataFrame index column from the CSV.
          # .encode("utf-8") converts the CSV string into bytes —— required by st.download_button which accepts bytes/IO for downlaods.
          # utf-8 encoding ensures non-ASCII characters (like ₹) are preserved.
          # utf-8 (Unicode Transformation Format - 8 bit) | The most common character encding on the internet, used to represent every character in the Unicode Standard using 1 to 4 bytes.
          # ASCII (American Standard Code for Information Interchange) | It is a character encoding standard used to represent text in conputer and other electronic devices. 7 bits ti represent 128 characters, including uppercase and lowercase letters, punctuation marks, numbers, and control characters.
          st.download_button("Download CSV", csv, file_name="expenses.csv", mime="text/csv")
          # mime |
     else:
          st.info("No expenses added yet.")
        # st.info() shows an informational blue box.
        # append({}) | is a list method that add whatever we oout inside of parentheses add as a  list.
          st.dataframe(df)