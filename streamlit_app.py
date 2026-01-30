import streamlit as st
import pyrebase
import bcrypt
import uuid
from datetime import datetime

# Firebase Configuration (Replace with your actual config from Firebase Console)
firebase_config = {
    "apiKey": "AIzaSyYourApiKeyFromConsole",
    "authDomain": "ticketbookingap-default-rtdb.firebaseapp.com",
    "databaseURL": "https://ticketbookingap-default-rtdb.firebaseio.com/",
    "projectId": "ticketbookingap-default-rtdb",
    "storageBucket": "ticketbookingap-default-rtdb.appspot.com",
    "messagingSenderId": "123456789012",
    "appId": "1:123456789012:web:abcdef123456"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Helper Functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_uid():
    return str(uuid.uuid4())

def is_valid_email(email):
    return "@" in email and "." in email

# Session State for User
if 'user_uid' not in st.session_state:
    st.session_state.user_uid = None

# Sidebar: Show UID if logged in
if st.session_state.user_uid:
    st.sidebar.success(f"Logged in as: {st.session_state.user_uid}")
    if st.sidebar.button("Logout"):
        st.session_state.user_uid = None
        st.rerun()
else:
    st.sidebar.info("Please login or register.")

# Main App Logic
st.title("Ticket Booking App")

# Page Selection
page = st.selectbox("Navigate", ["Login", "Register", "Dashboard"]) if not st.session_state.user_uid else "Dashboard"

if page == "Register":
    st.header("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        if not is_valid_email(email):
            st.error("Invalid email format.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            # Check if user exists
            users = db.child("users").get().val() or {}
            if any(user.get("email") == email for user in users.values()):
                st.error("Email already registered.")
            else:
                uid = generate_uid()
                hashed_pw = hash_password(password)
                db.child("users").child(uid).set({
                    "email": email,
                    "password": hashed_pw,
                    "uid": uid
                })
                st.session_state.user_uid = uid
                st.success("Registered successfully! UID shown in sidebar.")
                st.rerun()

elif page == "Login":
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        users = db.child("users").get().val() or {}
        user_found = None
        for uid, user in users.items():
            if user.get("email") == email and check_password(password, user.get("password", "")):
                user_found = uid
                break
        if user_found:
            st.session_state.user_uid = user_found
            st.success("Logged in! UID shown in sidebar.")
            st.rerun()
        else:
            st.error("Invalid credentials.")

elif page == "Dashboard" and st.session_state.user_uid:
    st.header("Dashboard")
    
    # Order Placement
    st.subheader("Place an Order")
    event = st.text_input("Event Name")
    tickets = st.number_input("Number of Tickets", min_value=1, step=1)
    
    if st.button("Place Order"):
        if event.strip():
            order_id = generate_uid()
            order_data = {
                "order_id": order_id,
                "user_uid": st.session_state.user_uid,
                "event": event,
                "tickets": tickets,
                "timestamp": datetime.now().isoformat()
            }
            db.child("orders").child(order_id).set(order_data)
            st.success("Order placed! It will appear in orders.html (hosted separately).")
        else:
            st.error("Please enter an event name.")
    
    # View Orders (Optional: For the app itself)
    st.subheader("Your Orders")
    orders = db.child("orders").get().val() or {}
    user_orders = {k: v for k, v in orders.items() if v.get("user_uid") == st.session_state.user_uid}
    if user_orders:
        for order in user_orders.values():
            st.write(f"Event: {order['event']}, Tickets: {order['tickets']}, Time: {order['timestamp']}")
    else:
        st.info("No orders yet.")