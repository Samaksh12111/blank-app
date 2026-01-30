import streamlit as st
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="FoodieHub", layout="wide", initial_sidebar_state="collapsed")

# ---------------- HIDE STREAMLIT UI ----------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
body {
    background-color: #0e1117;
    color: white;
    font-family: 'Arial', sans-serif;
}
.sidebar-drawer {
    position: fixed;
    top: 0;
    left: -44%;
    width: 44%;
    height: 100%;
    background: #1f1f1f;
    z-index: 1000;
    transition: left 0.3s;
    padding: 20px;
}
.sidebar-drawer.open {
    left: 0;
}
.drawer-item {
    margin: 20px 0;
    font-size: 18px;
    cursor: pointer;
}
.hamburger {
    font-size: 24px;
    cursor: pointer;
}
.food-container {
    display: flex;
    overflow-x: auto;
    gap: 16px;
    padding: 16px 0;
}
.food-card {
    min-width: 200px;
    background: #ffffff;
    color: #000;
    border-radius: 18px;
    padding: 10px;
    flex-shrink: 0;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}
.food-card img {
    width: 100%;
    border-radius: 14px;
}
.food-card h3 {
    margin: 8px 0 4px 0;
}
.food-card .price {
    color: #27ae60;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "users" not in st.session_state:
    st.session_state.users = {}
if "logged" not in st.session_state:
    st.session_state.logged = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "drawer_open" not in st.session_state:
    st.session_state.drawer_open = False

# ---------------- HELPERS ----------------
def gmail_valid(email):
    return re.fullmatch(r"[a-zA-Z0-9._%+-]+@gmail\.com", email)

def logout():
    st.session_state.logged = False
    st.session_state.user = ""
    st.session_state.drawer_open = False
    st.experimental_rerun()

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
                st.experimental_rerun()
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

    # Hamburger icon for drawer
    st.markdown(f"""
    <div>
        <span class="hamburger" onclick="toggleDrawer()">☰</span>
        <h2>🍔 Welcome {username}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Drawer HTML
    st.markdown(f"""
    <div id="drawer" class="sidebar-drawer">
        <div class="drawer-item">{username}</div>
        <div class="drawer-item">Orders</div>
        <div class="drawer-item">Support</div>
        <div class="drawer-item" onclick="logoutClicked()">Logout</div>
    </div>
    <script>
    const drawer = document.getElementById('drawer');
    function toggleDrawer() {{
        drawer.classList.toggle('open');
    }}
    function logoutClicked() {{
        fetch('/?logout=1').then(()=>{{location.reload();}});
    }}
    </script>
    """, unsafe_allow_html=True)

    # Check for logout via JS
    if st.experimental_get_query_params().get("logout"):
        logout()

    # Dishes horizontal scroll
    foods = [
        ("Burger", 129, "Juicy & tasty",
         "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=400&q=80"),
        ("Pizza", 199, "Cheesy delight",
         "https://images.unsplash.com/photo-1548365328-9f547fb0951c?auto=format&fit=crop&w=400&q=80"),
        ("Pasta", 149, "Italian style",
         "https://images.unsplash.com/photo-1525755662778-989d0524087e?auto=format&fit=crop&w=400&q=80"),
        ("Momos", 89, "Spicy momos",
         "https://images.unsplash.com/photo-1604909053196-2c7c5b5a8c89?auto=format&fit=crop&w=400&q=80"),
        ("French Fries", 79, "Crispy & hot",
         "https://images.unsplash.com/photo-1617196037110-8c6b7f14cfb1?auto=format&fit=crop&w=400&q=80"),
    ]

    st.markdown("### 🍽 Popular Dishes")
    dish_html = '<div class="food-container">'
    for f in foods:
        dish_html += f"""
        <div class="food-card">
            <img src="{f[3]}">
            <h3>{f[0]}</h3>
            <div class="price">₹{f[1]}</div>
            <p>{f[2]}</p>
        </div>
        """
    dish_html += '</div>'
    st.markdown(dish_html, unsafe_allow_html=True)