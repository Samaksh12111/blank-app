import streamlit as st
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Food App",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION STATE ----------------
if "users" not in st.session_state:
    st.session_state.users = {}   # {email: password}

if "logged" not in st.session_state:
    st.session_state.logged = False

if "user" not in st.session_state:
    st.session_state.user = ""

# ---------------- HELPERS ----------------
def gmail_valid(email):
    return re.fullmatch(r"[a-zA-Z0-9._%+-]+@gmail\.com", email)

def logout():
    st.session_state.logged = False
    st.session_state.user = ""
    st.rerun()   # ✅ FIXED

# ---------------- STYLES ----------------
st.markdown("""
<style>
body { background:#fafafa; }
.card {
    background:white;
    padding:20px;
    border-radius:16px;
    box-shadow:0 4px 15px rgba(0,0,0,0.1);
    width:220px;
}
.price { color:#27ae60; font-size:18px; }
</style>
""", unsafe_allow_html=True)

# ---------------- AUTH UI ----------------
if not st.session_state.logged:

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    # -------- LOGIN --------
    with tab1:
        st.subheader("Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", key="login_btn"):
            if email in st.session_state.users and st.session_state.users[email] == password:
                st.session_state.logged = True
                st.session_state.user = email
                st.rerun()   # ✅ FIXED
            else:
                st.error("Invalid email or password")

    # -------- REGISTER --------
    with tab2:
        st.subheader("Register")

        email = st.text_input("Email", key="reg_email")
        p1 = st.text_input("Password", type="password", key="reg_pass")
        p2 = st.text_input("Confirm Password", type="password", key="reg_cpass")

        if st.button("Create Account", key="reg_btn"):
            if not gmail_valid(email):
                st.error("Only @gmail.com allowed")
            elif p1 != p2:
                st.error("Passwords do not match")
            elif email in st.session_state.users:
                st.error("Email already registered")
            else:
                st.session_state.users[email] = p1
                st.success("Registration successful 🎉 Please login")

# ---------------- MAIN APP ----------------
else:
    username = st.session_state.user.split("@")[0]

    # -------- SIDEBAR --------
    with st.sidebar:
        st.markdown(f"### 👤 {username}")
        st.markdown("---")
        st.button("📦 Orders")
        st.button("🛟 Support")
        if st.button("🚪 Logout"):
            logout()

    # -------- HEADER --------
    st.markdown(f"## 🍔 Welcome {username}")

    # -------- FOOD ITEMS --------
    foods = [
        ("Burger", 129, "Juicy & tasty"),
        ("Pizza", 199, "Cheesy delight"),
        ("Pasta", 149, "Italian style"),
        ("Fries", 79, "Crispy"),
        ("Sandwich", 99, "Fresh"),
        ("Momos", 89, "Spicy"),
        ("Taco", 159, "Mexican"),
        ("Noodles", 139, "Street style")
    ]

    st.markdown("### 🍽 Popular Dishes")

    cols = st.columns(len(foods))
    for i, food in enumerate(foods):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <h4>{food[0]}</h4>
                <div class="price">₹{food[1]}</div>
                <p>{food[2]}</p>
            </div>
            """, unsafe_allow_html=True)