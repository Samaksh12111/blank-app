import streamlit as st
import requests
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Food App", layout="wide")

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
body {background:#ffffff;}

.food-row {
    display:flex;
    gap:20px;
    overflow-x:auto;
    padding-bottom:10px;
}
.food-card {
    min-width:220px;
    padding:20px;
    border-radius:20px;
    background:#f8f8f8;
    box-shadow:0 10px 25px rgba(0,0,0,0.1);
    transition:0.3s;
}
.food-card:hover {
    transform:scale(1.05);
}
.sidebar-overlay {
    position:fixed;
    top:0;left:0;
    width:100%;height:100%;
    background:rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

FIREBASE_URL = "https://foodiehubproject-default-rtdb.firebaseio.com/users.json"

# ---------------- FUNCTIONS ----------------
def is_valid_gmail(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email)

def get_users():
    r = requests.get(FIREBASE_URL)
    return r.json() if r.json() else {}

def email_exists(email):
    users = get_users()
    for u in users.values():
        if u.get("email") == email:
            return True
    return False

def register_user(email, password):
    data = {"email": email, "password": password}
    requests.post(FIREBASE_URL, json=data)

def login_user(email, password):
    users = get_users()
    for u in users.values():
        if u.get("email") == email and u.get("password") == password:
            return True
    return False

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "sidebar" not in st.session_state:
    st.session_state.sidebar = False

# ---------------- AUTH ----------------
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab2:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):
            if not is_valid_gmail(email):
                st.error("❌ Only @gmail.com allowed")
            elif password != confirm:
                st.error("❌ Password mismatch")
            elif email_exists(email):
                st.error("❌ Email already registered")
            else:
                register_user(email, password)
                st.success("🎉 Registration Successful! Now Login")

    with tab1:
        email = st.text_input("Email", key="l")
        password = st.text_input("Password", type="password", key="p")

        if st.button("Login"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials")

# ---------------- DASHBOARD ----------------
else:
    name = st.session_state.user_email.split("@")[0]

    col1, col2 = st.columns([1,9])
    with col1:
        if st.button("☰"):
            st.session_state.sidebar = True

    st.title(f"Welcome, {name} 👋")

    foods = [
        ("Burger",149,"Juicy & tasty"),
        ("Pizza",199,"Extra cheese"),
        ("Pasta",159,"Italian classic"),
        ("Fries",79,"Crispy hot"),
        ("Sandwich",99,"Fresh"),
        ("Momos",129,"Steam delight"),
        ("Noodles",139,"Spicy"),
        ("Tacos",179,"Mexican"),
        ("Wrap",149,"Healthy"),
        ("Ice Cream",89,"Sweet")
    ]

    st.markdown('<div class="food-row">', unsafe_allow_html=True)
    for f in foods:
        st.markdown(f"""
        <div class="food-card">
        <h3>{f[0]}</h3>
        <h4>₹{f[1]}</h4>
        <p>{f[2]}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- SIDEBAR ----------
    if st.session_state.sidebar:
        st.markdown('<div class="sidebar-overlay"></div>', unsafe_allow_html=True)
        with st.sidebar:
            st.markdown(f"### 👤 {name}")
            st.button("📦 Orders")
            st.button("💬 Support")
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.sidebar = False
                st.experimental_rerun()