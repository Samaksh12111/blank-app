import streamlit as st
import requests
import uuid

# ---------------- CONFIG ----------------
FIREBASE_URL = "https://ticketbookingap-default-rtdb.firebaseio.com"

st.set_page_config(page_title="Food App", layout="wide")

# Hide Streamlit UI
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.card {
    background:#111;
    padding:20px;
    border-radius:16px;
    box-shadow:0 8px 20px rgba(0,0,0,0.4);
    margin-bottom:20px;
}
.food-name {font-size:22px;font-weight:bold;color:#fff;}
.price {color:#00ff7f;font-size:18px;}
.desc {color:#ccc;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- FUNCTIONS ----------------
def register_user(email, password):
    uid = str(uuid.uuid4())
    data = {
        "email": email,
        "password": password
    }
    requests.put(f"{FIREBASE_URL}/users/{uid}.json", json=data)

def login_user(email, password):
    res = requests.get(f"{FIREBASE_URL}/users.json").json()

    if not res:
        return False

    for uid, user in res.items():
        if not isinstance(user, dict):
            continue

        db_email = user.get("email")
        db_pass = user.get("password")

        if db_email == email and db_pass == password:
            return True

    return False

# ---------------- AUTH UI ----------------
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if email and password:
                if login_user(email, password):
                    st.session_state.logged_in = True
                    st.success("Login Successful ✅")
                    st.rerun()
                else:
                    st.error("Invalid Email or Password ❌")
            else:
                st.warning("All fields required")

    with tab2:
        st.subheader("Register")
        remail = st.text_input("Email ", key="r1")
        rpass = st.text_input("Password ", type="password", key="r2")
        cpass = st.text_input("Confirm Password", type="password", key="r3")

        if st.button("Create Account"):
            if not remail or not rpass or not cpass:
                st.warning("All fields required")
            elif rpass != cpass:
                st.error("Passwords do not match ❌")
            else:
                register_user(remail, rpass)
                st.success("Registration Successful 🎉 Now Login")

# ---------------- FOOD HOME ----------------
else:
    st.title("🍔 Food App")
    st.write("Swiggy / Zomato style food cards 😋")

    foods = [
        {"name": "Cheese Burger", "price": "₹99", "desc": "Juicy & cheesy"},
        {"name": "Pizza", "price": "₹199", "desc": "Extra cheese loaded"},
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
                <div class="desc">{food['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()