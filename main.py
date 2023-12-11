import streamlit as st
books = [
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A novel about the decadence and excess of the Jazz Age.",
        "link": "https://www.gutenberg.org/ebooks/64317"
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "description": "A novel about racial injustice in the American South.",
        "link": "https://www.gutenberg.org/ebooks/710"
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "description": "A novel about the societal pressures faced by women in Regency England.",
        "link": "https://www.gutenberg.org/ebooks/1342"
    }
]

users = {}  
def main():
    st.title("Online Book Store")

    login_state = get_login_state()

    if not login_state["logged_in"]:
        login_page(login_state)
        st.stop()

    operation = st.sidebar.selectbox("Operation", ["View Books", "Order Books", "Manage Books"])

    if operation == "View Books":
        view_books()
    elif operation == "Order Books":
        order_books()
    elif operation == "Manage Books":
        manage_books()

def get_login_state():
    login_state = {"logged_in": False, "username": None}

    if "login_state" in st.session_state:
        login_state = st.session_state.login_state

    return login_state

def set_login_state(logged_in, username):
    st.session_state.login_state = {"logged_in": logged_in, "username": username}

def login(username, password):
    if username in users and users[username] == password:
        set_login_state(True, username)
        return True
    return False

def logout():
    set_login_state(False, None)

def register(username, password):
    if username in users:
        return False

    users[username] = password
    set_login_state(True, username)
    return True

def login_page(login_state):
    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.success("Logged in successfully.")
        else:
            st.error("Invalid username or password.")

    st.markdown("---")

    st.header("Register")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Register"):
        if register(new_username, new_password):
            st.success("Registered and logged in successfully.")
        else:
            st.error("Username already taken.")

def view_books():
    st.header("Available Books")

    if len(books) == 0:
        st.write("No books available.")
    else:
        for book in books:
            st.write(f"- [{book['title']}]({book['link']}) by {book['author']}")
            st.write(book['description'])
            st.write("---")

def order_books():
    st.header("Order Books")

    book_options = [book["title"] for book in books]
    selected_book = st.selectbox("Select a book to order", book_options)

    name = st.text_input("Name")
    address = st.text_input("Address")
    city = st.text_input("City")
    state = st.text_input("State")
    zip_code = st.text_input("Zip Code")

    if st.button("Place Order"):
        selected_book_index = book_options.index(selected_book)
        selected_book = books[selected_book_index]

        order = {
            "book": selected_book["title"],
            "author": selected_book["author"],
            "name": name,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code
        }

        username = get_login_state()["username"]
        if username not in users:
            users[username] = {"orders": []}
        users[username]["orders"].append(order)

        st.success("Order placed successfully!")

def manage_books():
    st.header("Manage Books")

    action = st.selectbox("Select an action", ["Add Book", "Edit Book", "Delete Book"])

    if action == "Add Book":
        add_book()
    elif action == "Edit Book":
        edit_book()
    elif action == "Delete Book":
        delete_book()

def add_book():
    st.subheader("Add Book")

    title = st.text_input("Title")
    author = st.text_input("Author")
    description = st.text_area("Description")
    link = st.text_input("Link")

    if st.button("Add"):
        book = {
            "title": title,
            "author": author,
            "description": description,
            "link": link
        }
        books.append(book)
        st.success(f"Added '{title}' by {author} to the bookstore.")

def edit_book():
    st.subheader("Edit Book")

    book_options = [book["title"] for book in books]
    selected_book = st.selectbox("Select a book to edit", book_options)

    selected_book_index = book_options.index(selected_book)
    selected_book_data = books[selected_book_index]
    
    new_title = st.text_input("Title", value=selected_book_data["title"])
    new_author = st.text_input("Author", value=selected_book_data["author"])
    new_description = st.text_area("Description", value=selected_book_data["description"])
    new_link = st.text_input("Link", value=selected_book_data["link"])

    if st.button("Save Changes"):
        books[selected_book_index]["title"] = new_title
        books[selected_book_index]["author"] = new_author
        books[selected_book_index]["description"] = new_description
        books[selected_book_index]["link"] = new_link

        st.success(f"'{selected_book}' updated successfully.")

def delete_book():
    st.subheader("Delete Book")

    book_options = [book["title"] for book in books]
    selected_book = st.selectbox("Select a book to delete", book_options)

    if st.button("Delete"):
        selected_book_index = book_options.index(selected_book)
        del books[selected_book_index]

        st.success(f"'{selected_book}' deleted successfully.")

if __name__ == "__main__":
  main()
