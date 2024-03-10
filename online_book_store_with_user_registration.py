import streamlit as st

# Initialize users dictionary with some default users
users = {
    "john_doe": "password123",
    "jane_smith": "abc@123"
}

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

    # Save the updated user dictionary to session state
    st.session_state.users = users

    return True

def login_page(login_state):
    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")

    st.header("Register")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Register"):
        if register(new_username, new_password):
            st.success("Registered successfully!")
        else:
            st.error("Username already exists.")

if __name__ == "__main__":
    main()
