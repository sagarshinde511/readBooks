import mysql.connector
import pandas as pd
import streamlit as st

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="82.180.143.66",
        user="u263681140_students",
        passwd="testStudents@123",
        database="u263681140_students"
    )

# Query to fetch joined data
def fetch_data():
    query = """
        SELECT 
            BookHistory.date AS BorrowDate,
            BookHistory.RFidNo,
            BookHistory.BookId,
            BookHistory.ReturnDate,
            BookInfo.BookName,
            BookInfo.Author,
            BookStudents.Name AS StudentName,
            BookStudents.Branch,
            BookStudents.Year
        FROM 
            BookHistory
        JOIN 
            BookInfo 
        ON 
            BookHistory.BookId = BookInfo.id
        JOIN 
            BookStudents 
        ON 
            BookHistory.RFidNo = BookStudents.RFidNo
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(results)

# Streamlit app
def main():
    st.title("Library Management System")
    st.subheader("View Book Borrowing Details")
    
    try:
        data = fetch_data()
        if not data.empty:
            st.dataframe(data)
        else:
            st.write("No data found in the database.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
