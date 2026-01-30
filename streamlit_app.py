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
    background:linear-gradient(180deg,#0b0b0b,#151515);
    color:white;
}

/* Burger Button */
.burger-btn button{
    font-size:22px;
    padding:6px 14px;
    border-radius:12px;
}

/* Sidebar overlay */
.overlay{
    position:fixed;
    inset:0;
    background:rgba(0,0,0,0.6);
    z-index:998;
}

/* Sidebar */
.sidebar{
    position:fixed;
    top:0;
    left:0;
    width:44%;
    height:100%;
    background:#1b1b1b;
    padding:24px;
    z-index:999;
    animation:slide .25s ease;
}

@keyframes slide{
    from{transform:translateX(-100%);}
    to{transform:translateX(0);}
}

/* Food cards horizontal */
.food-row{
    display:flex;
    gap:18px;
    overflow-x:auto;
    padding:20px 6px;
}
.food-row::-webkit-scrollbar{height:6px;}
.food-row::-webkit-scrollbar-thumb{
    background:#ff6b6b;border-radius:10px;
}

.food-card{
    min-width:230px;
    background:#222;
    border-radius:22px;
    padding:18px;
    box-shadow:0 12px 30px rgba(0,0,0,.6);
    transition:.3s;
}
.food-card:hover{transform:scale(1.06);}

.price{color:#4CAF50;font-weight:700;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged" not in st.session_state:
    st.session_state.logged = False

if "user" not in st.session_state:
    st.session_state.user = ""

if "sidebar" not in st.session_state:
    st.session_state.sidebar = False

# ---------------- FUNCTIONS ----------------
def gmail_valid(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email)

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state.logged:

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if st.session_state.users.get(email) == password:
                st.session_state.logged = True
                st.session_state.user = email
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        email = st.text_input("Email", key="r1")
        p1 = st.text_input("Password", type="password")
        p2 = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):
            if not gmail_valid(email):
                st.error("Only @gmail.com allowed")
            elif p1 != p2:
                st.error("Passwords not matching")
            elif email in st.session_state.users:
                st.error("Email already registered")
            else:
                st.session_state.users[email] = p1
                st.success("Registration successful 🎉")

# ---------------- DASHBOARD ----------------
else:
    username = st.session_state.user.split("@")[0]

    col1, col2 = st.columns([1,9])
    with col1:
        st.markdown('<div class="burger-btn">', unsafe_allow_html=True)
        if st.button("☰"):
            st.session_state.sidebar = True
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"## Welcome, **{username}** 👋")

    # Overlay click = close sidebar
    if st.session_state.sidebar:
        st.markdown(
            "<div class='overlay'></div>",
            unsafe_allow_html=True
        )

        st.markdown("<div class='sidebar'>", unsafe_allow_html=True)
        st.markdown(f"### 👤 {username}")
        st.markdown("---")
        st.button("📦 Orders")
        st.button("💬 Support")

        if st.button("🚪 Logout"):
            st.session_state.logged = False
            st.session_state.sidebar = False
            st.experimental_rerun()

        if st.button("❌ Close"):
            st.session_state.sidebar = False
            st.experimental_rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # FOOD DATA (10+ items)
    foods = [
        ("Burger",149,"Juicy & tasty"),
        ("Pizza",199,"Extra cheese"),
        ("Pasta",139,"Italian style"),
        ("Fries",79,"Crispy hot"),
        ("Sandwich",99,"Fresh"),
        ("Biryani",249,"Hyderabadi"),
        ("Momos",89,"Steam hot"),
        ("Noodles",129,"Spicy"),
        ("Rolls",119,"Stuffed"),
        ("Ice Cream",69,"Sweet"),
    ]

    st.markdown('<div class="food-row">', unsafe_allow_html=True)
    for f in foods:
        st.markdown(f"""
        <div class="food-card">
            <h3>{f[0]}</h3>
            <div class="price">₹{f[1]}</div>
            <p>{f[2]}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)