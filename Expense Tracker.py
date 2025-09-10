"""
Expense Tracker
---------------
A simple CLI-based expense tracker using Python + MySQL.

Features:
1. Add new expense
2. View expenses (all, by date, by category)
3. Update an expense
6. Delete expenses (by category, ID, or date range)
7. Show total spent
8. Exit
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load database credentials from .env file
load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "3306"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "expense_tracker")
)

print("✅ Database connected")
mycursor = mydb.cursor()

while True:
    print("\n-- Expense Tracker ---")
    print("1. Add new expense")
    print("2. View")
    print("3. Update an expense")
    print("4. Total spent")
    print("5. Delete")
    print("6. Exit")

    choice = input("Enter your choice: ")

    # 1. Add expense
    if choice == "1":
        Date = input("Enter date (YYYY-MM-DD): ")
        Amount = float(input("Enter amount: "))
        Category = input("Enter category: ")
        Description = input("Enter description: ")

        sql = "INSERT INTO expenses(Date, Amount, Category, Description) VALUES (%s,%s,%s,%s)"
        values = (Date, Amount, Category, Description)

        mycursor.execute(sql, values)
        mydb.commit()

        print("✅ New expense added!")
        continue

    # 2. View expenses
    elif choice == "2":
        print("A. View All")
        print("B. View by date")
        print("C. View by category")
        view_choice = input("Enter your choice: ")

        if view_choice.upper() == "A":
            mycursor.execute("SELECT * FROM expenses")
            result = mycursor.fetchall()
            if result:
                for row in result:
                    print(row)
            else:
                print("⚠️ No records found")
            continue

        elif view_choice.upper() == "B":
            view_by_start_date = input("Enter start date (YYYY-MM-DD): ")
            view_by_end_date = input("Enter end date (YYYY-MM-DD): ")
            mycursor.execute(
                "SELECT * FROM expenses WHERE date BETWEEN %s AND %s",
                (view_by_start_date, view_by_end_date)
            )
            result_by_date = mycursor.fetchall()
            if result_by_date:
                for row in result_by_date:
                    print(row)
            else:
                print("⚠️ No records found in given range")
            continue

        elif view_choice.upper() == "C":
            view_by_category = input("Enter category: ")
            mycursor.execute("SELECT * FROM expenses WHERE category = %s", (view_by_category,))
            result_category = mycursor.fetchall()
            if result_category:
                for row in result_category:
                    print(row)
            else:
                print("⚠️ No expenses found")
            continue

    # 3. Update expense
    elif choice == "3":
        new_amt = float(input("Enter new amount: "))
        id_to_update = int(input("Enter ID to update: "))

        mycursor.execute("SELECT * FROM expenses WHERE id = %s", (id_to_update,))
        record = mycursor.fetchone()

        if record:
            mycursor.execute(
                "UPDATE expenses SET amount = %s WHERE id = %s",
                (new_amt, id_to_update)
            )
            mydb.commit()
            print(mycursor.rowcount, "record(s) updated")
        else:
            print("⚠️ No record found with that ID!")
        continue

    #     # 7. Total spent
    # elif choice == "4":
    #     mycursor.execute("SELECT SUM(amount) FROM expenses")
    #     total = mycursor.fetchone()[0]

    #     if total is None:
    #         total = 0.0
    #     else:
    #         total = float(total)
    #     print("💰 Total spent:", total)
    #     continue



    elif choice == "4":
        print("A. Total spent")
        print("B. Total spent by Category")
        print("C. Total spent by Date")

        Total_choice = input("Enter your choice: ")

    # Total spent
    # 
        if Total_choice.upper() == "A":
            mycursor.execute("select sum(amount) as total from expenses")
            total_result = mycursor.fetchall()

            if mycursor.rowcount == 0:
                print("No data found in database")

            else:
                print(f"Your total spend id {total_result}")

    # Total spent by category
        elif Total_choice.upper() == "B":
            Total_spent_category = input("Enter category: ")

            mycursor.execute("select sum(amount) as total from expenses where category = %s",(Total_spent_category,))
            category_sum = mycursor.fetchone()
            if mycursor.rowcount == 0:
                print(f"No data found in {Total_spent_category}")

            else:
                print(f"Total spend of {Total_spent_category} is {category_sum}")


    # Total spent by Date
        elif Total_choice.upper() == "C":
            Total_start_date = input("Enter starting date range (YYYY-MM-DD): ")
            Total_end_date = input("Enter ending date range (YYYY-MM-DD): ")

            mycursor.execute("select sum(amount) as total from expenses where date between %s and %s", (Total_start_date, Total_end_date))
            date_sum = mycursor.fetchone()

            if mycursor.rowcount == "0":
                print(f"No expense found in {Total_start_date} to {Total_end_date}")

            else:
                print(f"Total expense in {Total_start_date} to {Total_end_date} is {date_sum}")


    # 6. Delete expense
    elif choice == "5":
        print("A. Delete by Category")
        print("B. Delete by ID")
        print("C. Delete by Date")
        delete_choice = input("Enter your choice: ")

        if delete_choice.upper() == "A":
            category_choice = input("Enter category: ")
            mycursor.execute("SELECT id, date, amount, category FROM expenses WHERE category = %s",
                             (category_choice,))
            rows = mycursor.fetchall()

            if not rows:
                print(f"⚠️ No expenses found in category {category_choice}.")
            else:
                print(f"\nExpenses in category '{category_choice}':")
                for row in rows:
                    print(f"ID: {row[0]}, Date: {row[1]}, Amount: {row[2]}, Category: {row[3]}")

                id_to_delete_by_category = int(input("Enter ID to delete: "))
                mycursor.execute("DELETE FROM expenses WHERE id = %s", (id_to_delete_by_category,))
                mydb.commit()
                print(f"🗑️ Deleted record {id_to_delete_by_category}")
            continue

        elif delete_choice.upper() == "B":
            id_to_delete = int(input("Enter ID to delete: "))
            mycursor.execute("DELETE FROM expenses WHERE id = %s", (id_to_delete,))
            mydb.commit()
            print("🗑️ Expense deleted (if existed).")
            continue

        elif delete_choice.upper() == "C":
            delete_start_date = input("Enter start date (YYYY-MM-DD): ")
            delete_end_date = input("Enter end date (YYYY-MM-DD): ")
            mycursor.execute(
                "SELECT id,date,amount,category FROM expenses WHERE date BETWEEN %s AND %s",
                (delete_start_date, delete_end_date)
            )
            result_date = mycursor.fetchall()

            if not result_date:
                print("⚠️ No expenses found in given range")
            else:
                print(f"\nExpenses in range from {delete_start_date} to {delete_end_date}:")
                for row in result_date:
                    print(f"ID: {row[0]}, Date: {row[1]}, Amount: {row[2]}, Category: {row[3]}")

                id_input = input("Enter ID to delete: ")
                ids_to_delete = [int(i.strip()) for i in id_input.split(",") if i.strip().isdigit()]
                
                if not ids_to_delete:
                    print("⚠️ No valid ID(s) entered.")
                else:
                    print(f"You are about to delete the following ID(s): {','.join(map(str, ids_to_delete))}")
                    confirmation = input("Are you sure? Type YES to confirm, or NO to cancle: ").strip().upper()

                    if confirmation.upper() == "YES":
                        placeholders = ",".join(["%s"] * len(ids_to_delete))
                        mycursor.execute(f"delete from expenses where id in ({placeholders})", ids_to_delete)
                        mydb.commit()
                        print(f"🗑️ Deleted {mycursor.rowcount} record(s).")
                    
                    elif confirmation.upper() == "NO":
                        print("❎ Deletion cancelled.")

                    else:
                        print("❌ Invalid confirmation input. No records were deleted.")
                continue


        elif delete_choice.upper() == "D":
            confirmation_all = input("Type YES to confirm, or NO to cancle: ").strip().upper()
            if not confirmation_all:
                print("No data deleted.")

            elif confirmation_all == "YES":
                mycursor.execute("delete from expenses")
                mydb.commit()
                print("Data deleted successfully.")

        else:
            print("❌ Invalid choice. Please try again.")
            continue

    # 8. Exit
    elif choice == "6":
        print("👋 Exiting... Bye!")
        break

    else:
        print("❌ Invalid choice. Try again")
        continue