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

# Query to fetch all data
def fetch_all_data():
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

# Query to search for a book by BookId
def search_book_by_id(book_id):
    query = """
        SELECT 
            id AS BookId,
            BookName,
            Author
        FROM 
            BookInfo
        WHERE 
            id = %s
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (book_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# Streamlit app
def main():
    st.title("Library Management System")
    st.subheader("View and Search Book Details")

    # Section 1: Display all data
    st.header("All Borrowing Details")
    try:
        data = fetch_all_data()
        if not data.empty:
            st.dataframe(data)
        else:
            st.write("No data found in the database.")
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")

    # Section 2: Search book by BookId
    st.header("Search for a Book by BookId")
    book_id = st.text_input("Enter BookId to search:")
    if st.button("Search"):
        try:
            result = search_book_by_id(book_id)
            if result:
                st.write("Book Details Found:")
                st.json(result)
            else:
                st.write(f"No book found with BookId: {book_id}")
        except Exception as e:
            st.error(f"An error occurred while searching: {e}")

if __name__ == "__main__":
    main()
