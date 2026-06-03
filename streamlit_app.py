import streamlit as st
import random, string, hashlib

st.set_page_config(page_title="AEGIS AI - The IT Expert", page_icon="⚡")
st.title("AEGIS AI")
st.caption("The IT Expert - Your Personal Guide to Technology")

st.markdown("""
**Despre AEGIS**
AEGIS a fost creat de un tânăr programator român, Andrei Vieru, cu pasiunea de a construi un scut digital pentru lumea modernă.
Este un expert AI dedicat exclusiv domeniilor IT și Inteligență Artificială.

**📞 Contact:** Pentru colaborări, scrie-ne pe WhatsApp (doar mesaje): **0722 911 793**
""")

# ---------- BAZA DE CUNOȘTINȚE (EXPERTUL TECH) ----------
if "knowledge" not in st.session_state:
    st.session_state.knowledge = {
        "api": "Un API (Application Programming Interface) este un set de reguli care permite două aplicații software să comunice între ele.",
        "python": "Python este un limbaj de programare versatil și puternic, folosit în dezvoltarea web, știința datelor, inteligența artificială și automatizări.",
        "variabilă": "O variabilă este ca o cutie în care poți păstra o valoare. În Python, o creezi simplu: `x = 5`.",
        "listă": "O listă este o colecție ordonată de elemente, care poate fi modificată. Se scrie între paranteze pătrate: `[1, 2, 3]`.",
        "dicționar": "Un dicționar este o colecție de perechi cheie-valoare. Se scrie între acolade: `{'nume': 'Andrei', 'vârstă': 15}`.",
        "funcție": "O funcție este un bloc de cod reutilizabil care face o anumită sarcină. Se definește cu `def`: `def salut(): print('Salut!')`.",
        "buclă": "O buclă (loop) este o instrucțiune care repetă o bucată de cod. `for` și `while` sunt cele mai comune în Python.",
        "clasă": "O clasă (class) este un șablon pentru crearea de obiecte. Este fundamentul Programării Orientate pe Obiecte (OOP).",
        "ai": "Inteligența Artificială (AI) este simularea proceselor de inteligență umană de către mașini, în special sisteme informatice.",
        "samsung": "Samsung este o companie globală, lider în tehnologie, care produce telefoane Galaxy, laptopuri Galaxy Book, ceasuri și alte dispozitive inteligente.",
        "criptomonedă": "O monedă digitală descentralizată. Exemple: Bitcoin (BTC), Ethereum (ETH).",
        "mit": "MIT (Massachusetts Institute of Technology) este una dintre cele mai prestigioase universități din lume, lider în cercetare și inovație tehnologică.",
        "white hat": "White Hat Hacking este practica etică și legală de a testa securitatea sistemelor pentru a le proteja împotriva atacatorilor reali.",
    }

# ---------- GESTIUNEA SESIUNII ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_db" not in st.session_state:
    st.session_state.user_db = {}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

def hash_data(data): return hashlib.sha256(data.encode()).hexdigest()

# ---------- AUTENTIFICARE ----------
if not st.session_state.logged_in:
    st.subheader("Autentificare sau Înregistrare")
    auth_choice = st.radio("Alege o opțiune:", ["Autentificare", "Creează Cont Nou"])
    
    if auth_choice == "Autentificare":
        user = st.text_input("👤 Utilizator")
        pin = st.text_input("🔑 Parolă", type="password")
        if st.button("Autentificare"):
            if user in st.session_state.user_db and st.session_state.user_db[user] == hash_data(pin):
                st.session_state.logged_in = True
                st.session_state.user = user
                # Restaurează istoricul chat-ului
                if user in st.session_state.chat_history:
                    st.session_state.messages = st.session_state.chat_history[user]
                else:
                    st.session_state.messages = []
                st.success(f"Bun venit, {user}!")
                st.rerun()
            else:
                st.error("Autentificare eșuată.")
    else:
        new_user = st.text_input("👤 Alege un nume de utilizator")
        new_pin = st.text_input("🔑 Alege o parolă", type="password")
        if st.button("Creează Cont"):
            if new_user in st.session_state.user_db: st.error("Acest nume de utilizator există deja.")
            elif len(new_pin) < 4: st.error("Parola trebuie să aibă minim 4 caractere.")
            else:
                st.session_state.user_db[new_user] = hash_data(new_pin)
                st.success("Cont creat! Acum te poți autentifica.")
                st.info("Selectează 'Autentificare' și folosește datele tale.")

# ---------- INTERFAȚA PRINCIPALĂ ----------
else:
    # Salutul personalizat
    st.success(f"Salut, {st.session_state.user}! Cu ce te pot ajuta?")
    
    # Butonul de Chat Nou
    if st.button("➕ Chat Nou"):
        st.session_state.messages = []
        st.rerun()
    
    # Afișăm istoricul conversației
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
    
    # Câmpul de chat
    if prompt := st.chat_input("Scrie un mesaj..."):
        # Adaugă mesajul utilizatorului
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Răspunde
        with st.chat_message("assistant"):
            with st.spinner("AEGIS se gândește..."):
                # Caută în baza de cunoștințe
                found = False
                for key in st.session_state.knowledge:
                    if key in prompt.lower():
                        response = st.session_state.knowledge[key]
                        found = True
                        break
                
                # Dacă nu găsește, răspunde politicos
                if not found:
                    response = "Nu am această informație încă. Poți căuta pe Google sau Wikipedia pentru mai multe detalii."
                
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Salvează istoricul pentru utilizatorul curent
        st.session_state.chat_history[st.session_state.user] = st.session_state.messages
