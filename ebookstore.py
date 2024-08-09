import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('ebookstore.db')
cursor = conn.cursor()

# Create the 'books' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        quantity INTEGER
    )
''')

# Insert default values into the 'books' table
cursor.execute("INSERT INTO books (id, title, author, quantity) VALUES (?, ?, ?, ?)", 
               (3001, "A Tale of Two Cities", "Charles Dickens", 30))
cursor.execute("INSERT INTO books (id, title, author, quantity) VALUES (?, ?, ?, ?)", 
               (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40))
cursor.execute("INSERT INTO books (id, title, author, quantity) VALUES (?, ?, ?, ?)", 
               (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25))
cursor.execute("INSERT INTO books (id, title, author, quantity) VALUES (?, ?, ?, ?)", 
               (3004, "The Lord of the Rings", "J.R.R Tolkien", 37))
cursor.execute("INSERT INTO books (id, title, author, quantity) VALUES (?, ?, ?, ?)", 
               (3005, "Alice in Wonderland", "Lewis Carroll", 12))

conn.commit()

# Function to enter a new book into the database
def enter_book():
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    quantity = int(input("Enter book quantity: "))
    
    cursor.execute("INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)", (title, author, quantity))
    conn.commit()
    print("Book added successfully!")

# Function to update book information
def update_book():
    book_id = int(input("Enter the book ID to update: "))
    new_quantity = int(input("Enter the new quantity: "))
    
    cursor.execute("UPDATE books SET quantity = ? WHERE id = ?", (new_quantity, book_id))
    conn.commit()
    print("Book information updated!")

# Function to delete a book from the database
def delete_book():
    book_id = int(input("Enter the book ID to delete: "))
    
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    print("Book deleted from the database!")

# Function to search for a specific book
def search_book():
    search_title = input("Enter book title to search: ")
    
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + search_title + '%',))
    books = cursor.fetchall()
    
    if not books:
        print("No matching books found.")
    else:
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}")

# Main program loop
while True:
    print("\nMenu:")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search book")
    print("0. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        enter_book()
    elif choice == '2':
        update_book()
    elif choice == '3':
        delete_book()
    elif choice == '4':
        search_book()
    elif choice == '0':
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
conn.close()
