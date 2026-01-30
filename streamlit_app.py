import streamlit as st
import requests
import uuid

FIREBASE_URL = "https://ticketbookingap-default-rtdb.firebaseio.com"

st.set_page_config(page_title="Food App", layout="wide")

# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- FUNCTIONS ----------
def register_user(email, password):
    uid = str(uuid.uuid4())
    data = {
        "email": email,
        "password": password
    }
    requests.put(f"{FIREBASE_URL}/users/{uid}.json", json=data)
    return True

def login_user(email, password):
    users = requests.get(f"{FIREBASE_URL}/users.json").json()
    if users:
        for uid, user in users.items():
            if user["email"] == email and user["password"] == password:
                return True
    return False

# ---------- UI ----------
st.markdown("""
<style>
.card {
    background:#ffffff;
    padding:20px;
    border-radius:15px;
    box-shadow:0 8px 20px rgba(0,0,0,0.1);
    margin-bottom:20px;
}
.food-name {font-size:22px;font-weight:bold;}
.price {color:green;font-size:18px;}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN / REGISTER ----------
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("🔑 Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.success("Login Successful ✅")
                st.rerun()
            else:
                st.error("Invalid Email or Password ❌")

    with tab2:
        st.subheader("📝 Register")
        remail = st.text_input("Email ", key="r1")
        rpass = st.text_input("Password ", type="password", key="r2")
        cpass = st.text_input("Confirm Password", type="password", key="r3")

        if st.button("Register"):
            if rpass != cpass:
                st.error("Password not matched ❌")
            else:
                register_user(remail, rpass)
                st.success("Registration Successful 🎉 Please Login")

# ---------- FOOD HOME ----------
else:
    st.title("🍔 Food App")
    st.write("Order your favorite food 😋")

    foods = [
        {"name": "Cheese Burger", "price": "₹99", "desc": "Juicy & tasty"},
        {"name": "Pizza", "price": "₹199", "desc": "Cheesy delight"},
        {"name": "Pasta", "price": "₹149", "desc": "Italian classic"},
        {"name": "French Fries", "price": "₹79", "desc": "Crispy & hot"},
    ]

    cols = st.columns(2)
    for i, food in enumerate(foods):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="card">
                <div class="food-name">{food['name']}</div>
                <div class="price">{food['price']}</div>
                <p>{food['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()