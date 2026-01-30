import streamlit as st
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Food App", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
[data-testid="stToolbar"] {display:none;}

body{
    background:linear-gradient(180deg,#0d0d0d,#151515);
    color:white;
}

.food-row{
    display:flex;
    gap:16px;
    overflow-x:auto;
    padding:10px;
}
.food-row::-webkit-scrollbar{height:6px;}
.food-row::-webkit-scrollbar-thumb{
    background:#ff4d4d;border-radius:10px;
}

.food-card{
    min-width:220px;
    background:#1f1f1f;
    border-radius:22px;
    padding:18px;
    box-shadow:0 10px 30px rgba(0,0,0,.6);
    transition:.3s;
}
.food-card:hover{transform:scale(1.05);}

.sidebar{
    position:fixed;
    top:0;left:0;
    width:44%;
    height:100%;
    background:#181818;
    padding:20px;
    z-index:999;
    animation:slide .3s ease;
}

@keyframes slide{
    from{transform:translateX(-100%);}
    to{transform:translateX(0);}
}

button{
    border-radius:12px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "users" not in st.session_state:
    st.session_state.users = {}   # email: password

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "sidebar" not in st.session_state:
    st.session_state.sidebar = False

# ---------------- FUNCTIONS ----------------
def is_valid_gmail(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email)

def register_user(email, password):
    if email in st.session_state.users:
        return False
    st.session_state.users[email] = password
    return True

def login_user(email, password):
    return st.session_state.users.get(email) == password

# ---------------- AUTH UI ----------------
if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.experimental_rerun()
            else:
                st.error("Invalid login")

    with tab2:
        email = st.text_input("Email", key="r_email")
        password = st.text_input("Password", type="password", key="r_pass")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):
            if not is_valid_gmail(email):
                st.error("Only @gmail.com allowed")
            elif password != confirm:
                st.error("Passwords do not match")
            elif not register_user(email, password):
                st.error("Email already registered")
            else:
                st.success("Registration Successful 🎉 Now Login")

# ---------------- DASHBOARD ----------------
else:
    name = st.session_state.current_user.split("@")[0]

    col1, col2 = st.columns([1,9])
    with col1:
        if st.button("☰"):
            st.session_state.sidebar = True

    st.markdown(f"## Welcome, {name} 👋")

    # Sidebar
    if st.session_state.sidebar:
        st.markdown('<div class="sidebar">', unsafe_allow_html=True)
        st.markdown(f"### 👤 {name}")
        st.markdown("---")
        st.button("📦 Orders")
        st.button("💬 Support")

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.sidebar = False
            st.experimental_rerun()

        if st.button("❌ Close"):
            st.session_state.sidebar = False
            st.experimental_rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # Food Data
    foods = [
        ("Burger",149,"Juicy & tasty"),
        ("Pizza",199,"Cheese loaded"),
        ("Pasta",139,"Italian classic"),
        ("Fries",79,"Crispy"),
        ("Sandwich",99,"Fresh bread"),
        ("Noodles",129,"Spicy"),
        ("Biryani",249,"Hyderabadi"),
        ("Rolls",119,"Stuffed"),
        ("Momos",89,"Steam hot"),
        ("Ice Cream",69,"Sweet treat"),
    ]

    st.markdown('<div class="food-row">', unsafe_allow_html=True)
    for f in foods:
        st.markdown(f"""
        <div class="food-card">
            <h3>{f[0]}</h3>
            <h4 style="color:#4CAF50">₹{f[1]}</h4>
            <p>{f[2]}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)