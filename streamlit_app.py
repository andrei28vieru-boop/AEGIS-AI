import streamlit as st
import random, string, hashlib

st.set_page_config(page_title="AEGIS AI", page_icon="⚡")
st.title("AEGIS AI")
st.caption("Advanced Engineered General Intelligence System")

# ---------- FILTRU DE SIGURANȚĂ ----------
BLOCKED_TERMS = ["prostituție", "droguri", "violență", "spargere", "furt"]

def hash_data(data): return hashlib.sha256(data.encode()).hexdigest()

def is_safe_question(question):
    for term in BLOCKED_TERMS:
        if term in question.lower(): return False
    return True

# ==========================================
# BIBLIOTECA SUPREMĂ DE CUNOȘTINȚE (OFFLINE)
# ==========================================
if "knowledge" not in st.session_state:
    st.session_state.knowledge = {
        # --- Cunoștințe Generale ---
        "api": "Un API (Application Programming Interface) este un set de reguli care permite două aplicații software să comunice între ele.",
        "hash": "Un hash este o amprentă digitală unică, rezultatul unei funcții matematice care transformă datele într-un șir de caractere.",
        "python": "Python este un limbaj de programare versatil, folosit în dezvoltarea web, știința datelor și inteligența artificială.",
        "aegis": "AEGIS este un AI creat de Andrei Vieru, un sistem avansat de inteligență artificială.",
        "românia": "România este o țară situată în Europa de Est. Capitala este București.",
        "univers": "Universul este tot ceea ce există: spațiu, timp, materie și energie. Se estimează că are o vechime de 13,8 miliarde de ani.",
        "soare": "Soarele este steaua din centrul sistemului nostru solar. Este o minge uriașă de plasmă fierbinte.",
        "planetă": "O planetă este un corp ceresc care orbitează o stea. În sistemul nostru solar sunt 8 planete.",
        "galaxie": "O galaxie este un sistem uriaș de stele, planete, gaze și praf cosmic. Galaxia noastră se numește Calea Lactee.",
        "medicina": "Medicina este știința și practica de a diagnostica, trata și preveni bolile.",
        "istorie": "Istoria este studiul trecutului, bazat pe documente, artefacte și alte surse.",
        "filosofie": "Filosofia este studiul problemelor fundamentale legate de existență, cunoaștere, valori, rațiune, minte și limbaj.",
        "sport": "Sportul este o activitate fizică competitivă sau recreativă.",
        "muzica": "Muzica este arta de a combina sunete într-o manieră plăcută sau expresivă.",
        "geografie": "Geografia este știința care studiază suprafața Pământului, clima, populația și resursele naturale.",
        "stiinta": "Știința este cunoașterea sistematică a lumii fizice sau materiale, obținută prin observație și experimentare.",
        "tehnologie": "Tehnologia este aplicarea cunoștințelor științifice pentru scopuri practice.",
        "internet": "Internetul este o rețea globală de calculatoare interconectate, care permite comunicarea și accesul la informații.",
        "economie": "Economia este știința care studiază producția, distribuția și consumul de bunuri și servicii.",
        "politica": "Politica este procesul de luare a deciziilor pentru un grup sau o societate.",
        "psihologie": "Psihologia este știința care studiază comportamentul uman și procesele mentale.",
        "sociologie": "Sociologia este studiul societății umane, al relațiilor sociale și al instituțiilor.",
        "limba": "Limba este un sistem de comunicare bazat pe cuvinte și reguli gramaticale.",
        "arta": "Arta este o gamă variată de activități umane care implică creația de obiecte vizuale, auditive sau interpretative.",
    }

# ==========================================
# MOTORUL DE RĂSPUNS INTELIGENT
# ==========================================
def get_smart_response(question):
    q = question.lower()
    # Caută în cunoștințele existente
    for key in st.session_state.knowledge:
        if key in q:
            return st.session_state.knowledge[key]
    # Dacă nu găsește, oferă un răspuns util
    return f"Nu am informații specifice despre '{question}' în baza mea de date. Însă poți căuta pe Google sau Wikipedia pentru mai multe detalii."

# ==========================================
# GESTIUNEA SESIUNII
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_db" not in st.session_state:
    st.session_state.user_db = {}
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# AUTENTIFICARE
# ==========================================
if not st.session_state.logged_in:
    st.subheader("Autentificare")
    auth_choice = st.radio("Opțiuni:", ["Autentificare", "Creează Cont Nou"])
    
    if auth_choice == "Autentificare":
        user = st.text_input("👤 Utilizator")
        pin = st.text_input("🔑 Parolă", type="password")
        if st.button("Autentificare"):
            if user in st.session_state.user_db and st.session_state.user_db[user] == hash_data(pin):
                st.session_state.logged_in = True
                st.session_state.user = user
                st.success(f"Bun venit, {user}.")
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

# ==========================================
# INTERFAȚA PRINCIPALĂ
# ==========================================
else:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.caption(f"Conectat: {st.session_state.user}")
    with col2:
        if st.button("➕ Nou"):
            st.session_state.messages = []
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input("Scrie un mesaj..."):
        if not is_safe_question(prompt):
            st.warning("AEGIS este un AI pentru educație și securitate.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                response = get_smart_response(prompt)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
