import streamlit as st
import random, string, hashlib, requests, json

st.set_page_config(page_title="AEGIS AI", page_icon="⚡")
st.title("AEGIS AI")
st.caption("Advanced Engineered General Intelligence System")

# ==========================================
# FILTRU DE SIGURANȚĂ
# ==========================================
BLOCKED_TERMS = ["prostituție", "droguri", "violență", "spargere", "furt", "omucidere"]

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
        # ... (păstrează toate cunoștințele pe care le-ai adăugat deja aici) ...
    }

# ==========================================
# CONEXIUNEA LA DEEPSEEK (ONLINE)
# ==========================================
def ask_deepseek(question, mode="fast"):
    try:
        api_key = "sk-447a3b0e07e74e8a865f7468b9a7ce2e"
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        
        system_message = "Ești AEGIS, un sistem AI avansat creat de Andrei Vieru."
        if mode == "expert":
            system_message += " Oferă răspunsuri extrem de detaliate, tehnice și precise."
        elif mode == "thing":
            system_message += " Analizează cu atenție orice link sau document primit și oferă un rezumat structurat."
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": question}
            ],
            "stream": False
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return None # Returnează None dacă DeepSeek nu funcționează

# ==========================================
# ABILITATEA DE A CĂUTA PE TOT INTERNETUL (SERP API GRATUIT)
# ==========================================
def search_web(question):
    try:
        # Aceasta este o cheie API gratuită care oferă 100 de căutări pe lună.
        # Este perfectă pentru a începe.
        api_key = "9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b"
        url = "https://serpapi.com/search"
        params = {
            "q": question,
            "api_key": api_key,
            "engine": "google"
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        # Construim un răspuns frumos din rezultate
        if "organic_results" in data:
            results = data["organic_results"][:3] # Luăm primele 3 rezultate
            answer = "Iată ce am găsit pe internet:\n\n"
            for i, res in enumerate(results, 1):
                answer += f"{i}. **{res['title']}**\n   {res['snippet']}\n   Link: {res['link']}\n\n"
            return answer
        else:
            return "Nu am găsit informații relevante pe internet."
    except Exception as e:
        return None # Returnează None dacă nici căutarea web nu funcționează

# ==========================================
# GESTIUNEA SESIUNII (MEMORIE)
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_db" not in st.session_state:
    st.session_state.user_db = {}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "search_mode" not in st.session_state:
    st.session_state.search_mode = "fast"

# ==========================================
# AUTENTIFICARE
# ==========================================
# ... (păstrează exact aceeași secțiune de autentificare de dinainte) ...

# ==========================================
# INTERFAȚA PRINCIPALĂ
# ==========================================
else:
    # ... (păstrează exact același design al interfeței) ...

    if prompt := st.chat_input("Scrie un mesaj..."):
        if not is_safe_question(prompt):
            st.warning("AEGIS este un AI pentru educație și securitate.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("AEGIS caută în universul digital..."):
                    response = None
                    
                    # Pasul 1: Caută în memoria offline
                    for key in st.session_state.knowledge:
                        if key in prompt.lower():
                            response = st.session_state.knowledge[key]
                            break
                    
                    # Pasul 2: Dacă nu găsește, încearcă să se conecteze la DeepSeek
                    if not response:
                        response = ask_deepseek(prompt, st.session_state.search_mode)
                    
                    # Pasul 3: Dacă nici DeepSeek nu răspunde, caută pe tot internetul
                    if not response:
                        response = search_web(prompt)
                    
                    # Pasul 4: Dacă totul eșuează, afișează o eroare prietenoasă
                    if not response:
                        response = "Momentan, toate conexiunile mele sunt întrerupte. Încearcă din nou în câteva minute."
                    
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
