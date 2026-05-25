import streamlit as st
import random, string, hashlib

st.set_page_config(page_title="AEGIS AI", page_icon="🛡️")
st.title("🏛️ AEGIS AI - The Unbreakable Sentinel")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "knowledge" not in st.session_state:
    st.session_state.knowledge = {"api": "Interfață pentru comunicare între aplicații.",
                                  "hash": "Amprentă digitală unică, transformare unidirecțională.",
                                  "parolă": "Cheie secretă pentru autentificare."}

USER_DB = {"Andrei": hashlib.sha256("python".encode()).hexdigest()}


def hash_data(data): return hashlib.sha256(data.encode()).hexdigest()


def generate_password(length=12, seeds=""):
    if length < 8: length = 12
    p = [random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase),
         random.choice(string.digits), random.choice(string.punctuation)]
    for w in seeds.split(): p.extend(list(w))
    p += random.choices(string.ascii_letters + string.digits + string.punctuation, k=max(0, length - len(p)))
    random.shuffle(p);
    return ''.join(p[:length])


def assess_password(password):
    s = sum([len(set(password)) > 7, any(c.islower() for c in password), any(c.isupper() for c in password),
             any(c.isdigit() for c in password), any(c in string.punctuation for c in password), len(password) > 11])
    return ["Foarte slabă", "Slabă", "Medie", "Bună", "Puternică", "Legendară"][min(s, 5)]


if not st.session_state.logged_in:
    st.subheader("Autentificare")
    user = st.text_input("👤 Utilizator")
    pin = st.text_input("🔑 Parolă", type="password")
    if st.button("Autentificare"):
        if user in USER_DB and USER_DB[user] == hash_data(pin):
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success(f"🛡️ AEGIS deblocat. Bun venit, {user}.")
            st.rerun()
        else:
            st.error("⛔ Autentificare eșuată.")
else:
    st.success(f"⚔️ {st.session_state.user} > Comandă activă")
    cmd = st.selectbox("Alege o comandă:", ["help", "generate", "assess", "profile", "ask", "learn", "exit"])

    if cmd == "help":
        st.info("[generate] [assess] [profile] [ask] [learn] [exit]")
    elif cmd == "generate":
        seeds = st.text_input("🌱 Semințe (opțional)")
        if st.button("Generează Parola"):
            st.code(generate_password(12, seeds))
    elif cmd == "assess":
        pwd = st.text_input("🔍 Parola de evaluat")
        if st.button("Evaluează"):
            st.write(f"🛡️ Putere: {assess_password(pwd)}")
    elif cmd == "profile":
        u = st.text_input("👤 Nume utilizator")
        t = st.text_input("🏷️ Tag (opțional)")
        seed = st.text_input("🌱 Cuvânt inspirație (opțional)")
        if st.button("Creează Profil"):
            p = generate_password(12, seed)
            uname = f"{u}{'_' + t if t else ''}"
            st.success(f"✅ Profil creat!")
            st.code(f"👤 {uname}\n⚡ Parolă: {p}\n🛡️ Putere: {assess_password(p)}")
    elif cmd == "ask":
        q = st.text_input("❓ Întrebare")
        if st.button("Întreabă AEGIS"):
            found = False
            for key in st.session_state.knowledge:
                if key in q.lower():
                    st.write(f"🤖 {key.capitalize()}: {st.session_state.knowledge[key]}")
                    found = True;
                    break
            if not found: st.write("🤖 Nu am cunoștințe despre asta.")
    elif cmd == "learn":
        term = st.text_input("📚 Termen")
        defi = st.text_input("📝 Definiție")
        if st.button("Învață AEGIS"):
            st.session_state.knowledge[term.lower()] = defi
            st.success("✅ Informație asimilată.")
    elif cmd == "exit":
        st.session_state.logged_in = False
        st.write("🏁 AEGIS se închide.")
        st.rerun()
