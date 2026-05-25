import streamlit as st
import random, string, hashlib

st.set_page_config(page_title="AEGIS AI", page_icon="🛡️")
st.title("🏛️ AEGIS AI - The Unbreakable Sentinel")

st.markdown("""
**Termeni și Condiții:** Acest AI este oferit ca atare, în scop educațional.
**Politica de Confidențialitate:** Nu stocăm parolele dvs. în text simplu.
""")

# ---------- INIȚIALIZARE BAZE DE DATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_db" not in st.session_state:
    st.session_state.user_db = {}

# --- BIBLIOTECA SUPREMĂ A CUNOȘTINȚELOR ---
if "knowledge" not in st.session_state:
    st.session_state.knowledge = {
        "api": "Un API (Application Programming Interface) este un set de reguli care permite două aplicații software să comunice între ele. Ex: API-ul vremii îți dă temperatura.",
        "hash": "Un hash este o amprentă digitală unică, rezultatul unei funcții matematice care transformă datele într-un șir de caractere.",
        "parolă": "O parolă este o cheie secretă, formată dintr-un șir de caractere, folosită pentru autentificare și protecția conturilor.",
        "securitate cibernetică": "Practica de a proteja sistemele, rețelele și programele de atacuri digitale.",
        "aegis": "AEGIS este un AI creat de Andrei Vieru, un scut digital suprem pentru securitate cibernetică.",
        "python": "Un limbaj de programare versatil. Resurse oficiale: [python.org](https://www.python.org)",
        "variabilă": "O cutie care ține o valoare. `x = 5`.",
        "listă": "O colecție ordonată. `[1, 2, 3]`.",
        "românia": "O țară în Europa de Est. Capitala: București. Turism: [romaniatourism.com](https://www.romaniatourism.com)",
        "piramidă": "Construcție monumentală. Cele mai faimoase: Piramidele din Giza, Egipt.",
    }

# --- BIBLIOTECA DE LINKURI PERFECTE ---
if "perfect_links" not in st.session_state:
    st.session_state.perfect_links = {
        "python": ["[Python.org](https://www.python.org)", "[W3Schools Python](https://www.w3schools.com/python/)"],
        "curs python": ["[Coursera Python Courses](https://www.coursera.org/courses?query=python)", "[freeCodeCamp Python](https://www.freecodecamp.org/learn/scientific-computing-with-python/)"],
        "securitate": ["[OWASP Top Ten](https://owasp.org/www-project-top-ten/)", "[SANS Institute](https://www.sans.org/)"],
        "știri": ["[BBC News](https://www.bbc.com/news)", "[Reuters](https://www.reuters.com/)"],
    }

# ---------- FILTRU DE SIGURANȚĂ ----------
BLOCKED_TERMS = ["prostituție", "droguri", "violență", "armă", "spargere", "țigan", "mafiot", "handicapat", "cum să fur", "cum să omor"]

def hash_data(data): return hashlib.sha256(data.encode()).hexdigest()

def generate_password(length=12, seeds=""):
    if length < 8: length = 12
    p = [random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase),
         random.choice(string.digits), random.choice(string.punctuation)]
    for w in seeds.split(): p.extend(list(w))
    p += random.choices(string.ascii_letters + string.digits + string.punctuation, k=max(0, length - len(p)))
    random.shuffle(p); return ''.join(p[:length])

def assess_password(password):
    s = sum([len(set(password))>7, any(c.islower() for c in password), any(c.isupper() for c in password),
             any(c.isdigit() for c in password), any(c in string.punctuation for c in password), len(password)>11])
    return ["Foarte slabă", "Slabă", "Medie", "Bună", "Puternică", "Legendară"][min(s,5)]

def is_safe_question(question):
    for term in BLOCKED_TERMS:
        if term in question.lower(): return False
    return True

# ---------- MOTORUL DE CĂUTARE INTELIGENT ----------
def find_answer(question):
    q = question.lower()
    
    # 1. Caută în linkuri perfecte
    for key in st.session_state.perfect_links:
        if key in q:
            links = st.session_state.perfect_links[key]
            response = "🔗 **Cele mai bune surse pentru tine:**\n\n"
            for link in links:
                response += f"- {link}\n"
            return response

    # 2. Caută în cunoștințe generale
    for key in st.session_state.knowledge:
        if key in q:
            return f"🤖 **{key.capitalize()}:** {st.session_state.knowledge[key]}"

    # 3. Dacă nu găsește nimic
    return None

# ---------- AUTENTIFICARE SAU ÎNREGISTRARE ----------
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
                st.success(f"🛡️ AEGIS deblocat. Bun venit, {user}.")
                st.rerun()
            else:
                st.error("⛔ Autentificare eșuată.")
    else:
        new_user = st.text_input("👤 Alege un nume de utilizator")
        new_pin = st.text_input("🔑 Alege o parolă", type="password")
        if st.button("Creează Cont"):
            if new_user in st.session_state.user_db:
                st.error("Acest nume de utilizator există deja.")
            elif len(new_pin) < 4:
                st.error("Parola trebuie să aibă minim 4 caractere.")
            else:
                st.session_state.user_db[new_user] = hash_data(new_pin)
                st.success("Cont creat cu succes! Acum te poți autentifica.")
                st.info("Selectează 'Autentificare' și folosește datele tale.")

# ---------- MENIUL PRINCIPAL ----------
else:
    st.success(f"⚔️ {st.session_state.user} > Comandă activă")
    cmd = st.selectbox("Alege o comandă:", ["help", "generate", "assess", "profile", "ask_ai", "exit"])
    
    if cmd == "help": st.info("[generate] [assess] [profile] [ask_ai] [exit]")
    elif cmd == "generate":
        seeds = st.text_input("🌱 Semințe (opțional)")
        if st.button("Generează Parola"):
            st.code(generate_password(12, seeds))
    elif cmd == "assess":
        pwd = st.text_input("🔍 Parola de evaluat")
        if st.button("Evaluează"):
            st.write(f"🛡️ Putere: {assess_password(pwd)}")
    elif cmd == "profile":
        u = st.text_input("👤 Nume utilizator"); t = st.text_input("🏷️ Tag (opțional)")
        seed = st.text_input("🌱 Cuvânt inspirație (opțional)")
        if st.button("Creează Profil"):
            p = generate_password(12, seed); uname = f"{u}{'_'+t if t else ''}"
            st.success(f"✅ Profil creat!"); st.code(f"👤 {uname}\n⚡ Parolă: {p}\n🛡️ Putere: {assess_password(p)}")
    elif cmd == "ask_ai":
        q = st.text_input("❓ Întreabă AEGIS")
        if st.button("Întreabă"):
            if is_safe_question(q):
                answer = find_answer(q)
                if answer:
                    st.write(answer)
                else:
                    st.write("🤖 Nu am aceste cunoștințe încă. Încearcă să cauți pe Google sau Wikipedia.")
            else:
                st.warning("AEGIS este un AI pentru securitate și educație. Nu pot răspunde la această întrebare.")
    elif cmd == "exit":
        st.session_state.logged_in = False
        st.write("🏁 AEGIS se închide."); st.rerun()
