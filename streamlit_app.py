import streamlit as st
import requests
from bs4 import BeautifulSoup
from plyer import tts
import webbrowser


# ---------- AI SPEAK ----------
def speak(text):
    try:
        tts.speak(text)
    except:
        pass


# ---------- SEARCH FUNCTION ----------
def web_search(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    result = soup.find("a", class_="result__a")
    snippet = soup.find("a", class_="result__snippet")

    if result and snippet:
        return f"{result.text}\n\n{snippet.text}"
    else:
        return "मुझे सही जानकारी नहीं मिली।"


# ---------- STREAMLIT UI ----------
st.set_page_config(
    page_title="Hindi AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Hindi AI Assistant")
st.caption("Streamlit based Smart AI")

# Auto welcome
if "welcome_done" not in st.session_state:
    speak("नमस्ते, मैं आपका ए आई असिस्टेंट हूँ। आप मुझसे कुछ भी पूछ सकते हैं।")
    st.session_state.welcome_done = True


# ---------- Buttons ----------
col1, col2 = st.columns(2)

with col1:
    if st.button("📺 YouTube खोलो"):
        speak("यूट्यूब खोल रहा हूँ")
        webbrowser.open("https://youtube.com")

with col2:
    if st.button("🌐 Google खोलो"):
        speak("गूगल खोल रहा हूँ")
        webbrowser.open("https://google.com")


st.divider()

# ---------- Question Input ----------
question = st.text_input("🤔 कुछ भी पूछो (Search AI):")

if st.button("🔍 Search"):
    if question.strip() == "":
        st.warning("कृपया कोई सवाल लिखिए")
    else:
        speak("मैं इंटरनेट से जानकारी ढूंढ रहा हूँ")
        with st.spinner("Search कर रहा हूँ..."):
            answer = web_search(question)

        st.success("📌 Answer:")
        st.write(answer)
        speak("यह रहा आपका जवाब")