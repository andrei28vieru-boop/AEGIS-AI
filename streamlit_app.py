import streamlit as st
import random, string, hashlib

st.set_page_config(page_title="AEGIS AI", page_icon="🛡️")
st.title("🏛️ AEGIS AI - The Unbreakable Sentinel")

st.markdown("""
**Termeni și Condiții:** Acest AI este oferit ca atare, în scop educațional.
**Politica de Confidențialitate:** Nu stocăm parolele dvs. în text simplu.
""")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_db" not in st.session_state:
    st.session_state.user_db = {}
if "knowledge" not in st.session_state:
    st.session_state.knowledge = {
        "api": "Un API (Application Programming Interface) este un set de reguli care permite două aplicații software să comunice între ele.",
        "hash": "Un hash este o amprentă digitală unică, rezultatul unei funcții matematice care transformă datele într-un șir de caractere. Este folosit pentru a verifica integritatea datelor.",
        "parolă": "O parolă este o cheie secretă, formată dintr-un șir de caractere, folosită pentru autentificare și pentru a proteja accesul la un cont sau dispozitiv.",
        "ai": "Inteligența Artificială (AI) este simularea proceselor de inteligență umană de către mașini, în special sisteme informatice. Include învățarea, raționamentul și auto-corecția.",
        "securitate cibernetică": "Securitatea cibernetică este practica de a proteja sistemele, rețelele și programele de atacuri digitale. Aceste atacuri au ca scop accesarea, modificarea sau distrugerea informațiilor.",
        "python": "Python este un limbaj de programare puternic și versatil, ușor de învățat, folosit în dezvoltarea web, știința datelor, inteligența artificială și automatizări.",
        "aegis": "AEGIS este un AI creat de Andrei Vieru, un scut digital pentru securitate cibernetică. Este un Sentinel de Neînvins."
    }

BLOCKED_TERMS = ["prostituție", "droguri", "violență", "armă", "spargere"]

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
                found = False
                for key in st.session_state.knowledge:
                    if key in q.lower():
                        st.write(f"🤖 {key.capitalize()}: {st.session_state.knowledge[key]}")
                        found = True; break
                if not found:
                    st.write("🤖 Nu am aceste cunoștințe. Poți întreba despre API, Hash, Parolă, AI, Securitate Cibernetică sau Python.")
            else:
                st.warning("AEGIS este un AI pentru securitate și educație. Nu pot răspunde la această întrebare.")
    elif cmd == "exit":
        st.session_state.logged_in = False
        st.write("🏁 AEGIS se închide."); st.rerun()
