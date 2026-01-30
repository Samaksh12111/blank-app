import streamlit as st
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FoodieHub",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- HIDE STREAMLIT UI ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

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
    st.rerun()

# ---------------- STYLES ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}

.food-card {
    background: #ffffff;
    color: #000;
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

.food-img {
    width: 100%;
    border-radius: 14px;
}

.price {
    color: #27ae60;
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- AUTH ----------------
if not st.session_state.logged:

    st.title("🍔 FoodieHub")

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if email in st.session_state.users and st.session_state.users[email] == password:
                st.session_state.logged = True
                st.session_state.user = email
                st.rerun()
            else:
                st.error("Invalid email or password")

    with tab2:
        email = st.text_input("Email", key="reg_email")
        p1 = st.text_input("Password", type="password", key="reg_pass")
        p2 = st.text_input("Confirm Password", type="password", key="reg_cpass")

        if st.button("Create Account"):
            if not gmail_valid(email):
                st.error("Only @gmail.com allowed")
            elif p1 != p2:
                st.error("Passwords do not match")
            elif email in st.session_state.users:
                st.error("Already registered")
            else:
                st.session_state.users[email] = p1
                st.success("Account created 🎉 Login now")

# ---------------- MAIN APP ----------------
else:
    username = st.session_state.user.split("@")[0]

    st.markdown(f"## 🍔 Welcome **{username}**")
    st.markdown("### 🍽 Popular Dishes")

    foods = [
        ("Burger", 129, "Juicy & tasty",
         "https://images.unsplash.com/photo-1550547660-d9450f859349"),
        ("Pizza", 199, "Cheesy delight",
         "https://images.unsplash.com/photo-1548365328-9f547fb0951c"),
        ("Pasta", 149, "Italian style",
         "https://images.unsplash.com/photo-1525755662778-989d0524087e"),
        ("Momos", 89, "Spicy momos",
         "https://images.unsplash.com/photo-1604909053196-2c7c5b5a8c89"),
    ]

    for food in foods:
        st.markdown(f"""
        <div class="food-card">
            <img src="{food[3]}" class="food-img">
            <h3>{food[0]}</h3>
            <div class="price">₹{food[1]}</div>
            <p>{food[2]}</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        logout()