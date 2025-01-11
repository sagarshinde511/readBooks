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

# Query to fetch joined data by BookId
def fetch_book_details(book_id):
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
        WHERE 
            BookHistory.BookId = %s
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (book_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(results)

# Streamlit app
def main():
    st.title("Library Management System")
    st.subheader("Search Book by BookId")
    
    # Input for BookId
    book_id = st.text_input("Enter BookId to search:")
    
    if st.button("Search"):
        if book_id.strip():
            try:
                data = fetch_book_details(book_id)
                if not data.empty:
                    st.dataframe(data)
                else:
                    st.write("No data found for the given BookId.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid BookId.")

if __name__ == "__main__":
    main()
