import streamlit as st
import hashlib
import bcrypt
import json
import time
from pathlib import Path
from deep_translator import GoogleTranslator


# -----------------------------
# CONSTANTE PERSISTENTE
# -----------------------------
USERS_DB_PATH = Path("users_db.json")
FORTRESS_STATE_PATH = Path("aegis_fortress.json")

# -----------------------------
# FUNCȚII USER DATABASE
# -----------------------------
def load_user_db():
    try:
        if USERS_DB_PATH.exists():
            with open(USERS_DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        return {}
    return {}

def save_user_db(db):
    tmp = USERS_DB_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    tmp.replace(USERS_DB_PATH)

def hash_pwd(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_pwd(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except:
        return False



st.set_page_config(page_title="AEGIS AI - The Ultimate IT Mentor", page_icon="💎")
st.title("💎 AEGIS AI")
st.caption("The Ultimate IT Mentor — Learn. Build. Conquer.")

# ---------- SECȚIUNEA DE LIMBI ----------
if "lang" not in st.session_state:
    st.session_state.lang = "Romanian"

lang_map = {
    "Romanian": "ro", "English": "en", "Spanish": "es", "Chinese (Simplified)": "zh-CN", "Hindi": "hi", "Arabic": "ar",
    "French": "fr", "German": "de", "Portuguese": "pt", "Russian": "ru", "Japanese": "ja", "Korean": "ko",
    "Turkish": "tr", "Italian": "it", "Polish": "pl", "Dutch": "nl", "Greek": "el", "Swedish": "sv",
    "Thai": "th", "Vietnamese": "vi"
}

def translate_text(text, target_lang):
    if target_lang == "ro": return text
    try: return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e: return f"Translation error: {str(e)}"

if not st.session_state.get("logged_in", False):
    selected_lang = st.selectbox("🌐 Choose your language / Alege limba", list(lang_map.keys()))
    st.session_state.lang = selected_lang

about_text_ro = """
**💎 Despre AEGIS**
AEGIS a fost creat de un tânăr programator român, Andrei Vieru, cu pasiunea de a construi un scut digital pentru lumea modernă.
Este un mentor IT interactiv — te învață, te testează, te ghidează.
**📞 Contact:** Pentru colaborări, scrie-ne pe WhatsApp (doar mesaje): **0722 911 793**
"""
st.markdown(translate_text(about_text_ro, lang_map[st.session_state.lang]))

# ---- BAZA DE CUNOȘTINȚE HYBRID ----
if "knowledge" not in st.session_state:
    st.session_state.knowledge = {
        "api": {
            "beginner": "Un API e ca un chelner într-un restaurant. Tu comanzi mâncarea, el merge la bucătărie și îți aduce farfuria. API-ul duce cererea ta la un server și îți aduce răspunsul înapoi.",
            "professional": "Un API (Application Programming Interface) este un set de reguli și protocoale care permite două aplicații software să comunice. API-urile REST folosesc HTTP și JSON pentru a transfera date între client și server.",
            "expert": "La nivel arhitectural, un API trebuie proiectat cu versionare, rate limiting, autentificare OAuth 2.0, și documentație OpenAPI. Performanța depinde de caching strategies, paginare și optimizarea query-urilor.",
            "code": "# Exemplu Python: Apelarea unui API\nimport requests\nresponse = requests.get('https://api.example.com/data')\ndata = response.json()\nprint(data)",
            "real_world": "Când folosești aplicația Meteo, ea folosește un API să ceară date de la serverul de vreme. Când postezi pe Instagram, aplicația folosește API-ul Instagram să trimită poza ta.",
            "quiz": {"question": "Ce protocol folosesc majoritatea API-urilor moderne?", "options": ["HTTP", "FTP", "SMTP", "SSH"], "answer": "HTTP"},
            "related": ["api rest", "json", "oauth", "http"]
        },

        "python": {
            "beginner": "Python e ca un limbaj pe care îl vorbești cu computerul. E simplu, ca engleza. Scrii ce vrei să facă, iar el execută. E perfect pentru începători!",
            "professional": "Python e un limbaj de programare high-level, interpretat, cu tipare dinamică. Este folosit în web development, data science, AI/ML și automatizări.",
            "expert": "Python 3.x oferă async/await, GIL pentru thread safety, și un ecosistem vast prin PyPI. Arhitectura permite OOP și programare funcțională.",
            "code": "print('Salut, lume!')\nprint('Bun venit, {nume}!'.format(nume='Andrei'))",
            "real_world": "Python e folosit de NASA, Google, Netflix și Spotify.",
            "quiz": {"question": "Ce cuvânt cheie definește o funcție în Python?", "options": ["func", "def", "function", "define"], "answer": "def"},
            "related": ["variabilă", "funcție", "clasă", "pip", "django"]
        },

        "ai": {
            "beginner": "Inteligența Artificială e ca un copil care învață. Îi arăți multe poze cu pisici, și el învață să recunoască o pisică.",
            "professional": "AI include subdomenii precum Machine Learning, Deep Learning, NLP și Computer Vision.",
            "expert": "Implementările moderne folosesc transformere, diffusion models și reinforcement learning. Optimizarea necesită GPU-uri și tehnici de fine-tuning.",
            "code": "# Exemplu simplu de AI\nfrom sklearn.linear_model import LinearRegression\nmodel = LinearRegression()",
            "real_world": "AI este folosit în Tesla Autopilot, ChatGPT, Google Photos și sisteme medicale.",
            "quiz": {"question": "Ce tip de AI folosește rețele neuronale profunde?", "options": ["Machine Learning", "Deep Learning", "NLP", "Vision"], "answer": "Deep Learning"},
            "related": ["ml", "deep learning", "transformers", "neural networks"]
        }
    }
        
       
aegis_level = {

    "api": {
        "beginner": "Un API e ca un chelner într-un restaurant. Tu comanzi mâncarea, el merge la bucătărie și îți aduce farfuria. API-ul duce cererea ta la un server și aduce răspunsul înapoi.",
        "professional": "Un API (Application Programming Interface) este un set de reguli și protocoale care permite două aplicații software să comunice. API-urile REST folosesc HTTP și JSON pentru a transfera date între client și server.",
        "expert": "La nivel arhitectural, un API trebuie proiectat cu versionare, rate limiting, autentificare OAuth 2.0, și documentație OpenAPI. Performanța depinde de caching strategies, paginare și optimizarea query-urilor.",
        "code": "# Exemplu Python: Apelarea unui API\nimport requests\nresponse = requests.get('https://api.example.com/data')\ndata = response.json()\nprint(data)",
        "real_world": "Când folosești aplicația Meteo, ea folosește un API să ceară date de la serverul de vreme. Când postezi pe Instagram, aplicația folosește API-ul Instagram să trimită poza ta.",
        "quiz": {"question": "Ce protocol folosesc majoritatea API-urilor moderne?",
                 "options": ["HTTP", "FTP", "SMTP", "SSH"], "answer": "HTTP"},
        "related": ["api rest", "json", "oauth", "http"]
    },

    "python": {
        "beginner": "Python e ca un limbaj pe care îl vorbești cu computerul. E simplu, ca engleza. Scrii ce vrei să facă, iar el execută. E perfect pentru începători!",
        "professional": "Python este un limbaj de programare high-level, interpretat, cu tipare dinamică. Este folosit în web development, data science, AI/ML și automatizări.",
        "expert": "Python 3.x oferă async/await, GIL pentru thread safety, și un ecosistem vast prin PyPI. Arhitectura permite OOP și programare funcțională.",
        "code": "print('Salut, lume!')\n\ndef salut(nume):\n    return f'Bun venit, {nume}!'\n\nprint(salut('Andrei'))",
        "real_world": "Python e folosit de NASA, Google, Netflix și Spotify.",
        "quiz": {"question": "Ce keyword definește o funcție în Python?",
                 "options": ["func", "def", "function", "define"], "answer": "def"},
        "related": ["variabilă", "funcție", "clasă", "pip", "django"]
    },

    "ai": {
        "beginner": "Inteligența Artificială e ca un copil care învață. Îi arăți multe poze cu pisici, și el învață să recunoască o pisică. AI face același lucru — învață din date.",
        "professional": "AI este simularea proceselor de inteligență umană. Subdomenii: Machine Learning, Deep Learning, NLP, Computer Vision.",
        "expert": "Implementările moderne folosesc Transformer, difuzie și reinforcement learning. Optimizarea necesită GPU-uri și tehnici de fine-tuning.",
        "code": "# Exemplu ML cu Scikit-learn\nfrom sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier()\nmodel.fit(X_train, y_train)\nprint(model.score(X_test, y_test))",
        "real_world": "AI e peste tot: Face ID, Google Maps, Netflix, Alexa, Siri.",
        "quiz": {"question": "Care este un subset al AI?",
                 "options": ["Machine Learning", "Word", "Chrome", "Photoshop"], "answer": "Machine Learning"},
        "related": ["machine learning", "deep learning", "neural network", "nlp"]
    },

    "samsung": {
        "beginner": "Samsung e ca un magazin imens de tehnologie. Fac telefoane Galaxy, laptopuri Galaxy Book, ceasuri Galaxy Watch, și multe altele!",
        "professional": "Samsung Electronics este lider global în tehnologie: procesoare, ecrane AMOLED, memorii și dispozitive Galaxy.",
        "expert": "Samsung domină semiconductori (DRAM, NAND), display-uri și inovația pliabilă. Ecosistemul Galaxy integrează telefoane, tablete, laptopuri, watch-uri și IoT.",
        "code": "# Conectare SmartThings API\nimport requests\nheaders = {'Authorization': 'Bearer TOKEN'}\nr = requests.get('https://api.smartthings.com/v1/devices', headers=headers)",
        "real_world": "Samsung face de la telefoane la frigidere inteligente. Galaxy Book5 Pro 360 e laptopul tău viitor!",
        "quiz": {"question": "Cum se numește asistentul AI Samsung?", "options": ["Siri", "Alexa", "Bixby", "Cortana"],
                 "answer": "Bixby"},
        "related": ["samsung galaxy book5 pro 360", "galaxy ai", "one ui 7"]
    },

    "cpu": {
        "beginner": "CPU-ul e creierul computerului. Tot ce faci — click, tastare, deschidere aplicație — trece prin CPU.",
        "professional": "CPU execută instrucțiuni prin ciclul fetch-decode-execute. Performanța: frecvență, core-uri, cache, arhitectură.",
        "expert": "Procesoarele moderne (Intel Core Ultra, Apple M4) folosesc 3nm, NPU pentru AI, DDR5 și PCIe 5.0.",
        "code": "import platform, os\nprint(platform.processor())\nprint(os.cpu_count())",
        "real_world": "CPU-ul e în laptop, telefon, PlayStation, mașini Tesla. Fiecare click e procesat de CPU.",
        "quiz": {"question": "Ce înseamnă CPU?",
                 "options": ["Central Processing Unit", "Computer Personal Unit", "Central Power Utility",
                             "Core Processing Utility"], "answer": "Central Processing Unit"},
        "related": ["gpu", "ram", "ssd", "intel", "amd"]
    },

    "samsung galaxy book5 pro 360": {
        "beginner": "E laptopul visurilor tale, Andrei! Subțire, se pliază, ecran superb, baterie toată ziua. Perfect pentru AEGIS!",
        "professional": "Laptop convertibil premium: AMOLED 2X 16\", Intel Core Ultra 7 Series 2, 16GB DDR5, 1TB SSD, S Pen, Wi-Fi 7, 25 ore baterie.",
        "expert": "Arhitectura Lunar Lake cu NPU 48 TOPS, display 500 nits HDR 120Hz, vapor chamber cooling, 1.66 kg.",
        "code": "book5 = {'display': '16 AMOLED 2X', 'cpu': 'Ultra 7 256V', 'ram': '16GB', 'ssd': '1TB', 'price': '13298 RON'}\nfor k,v in book5.items(): print(f'{k}: {v}')",
        "real_world": "Tu îl vei folosi pentru AEGIS — pe plajă în Spania, la Tucano în Sinaia, sau acasă noaptea.",
        "quiz": {"question": "Ce procesor are Book5 Pro 360?",
                 "options": ["Ultra 7 256V", "M4", "Snapdragon", "Ryzen 9"], "answer": "Ultra 7 256V"},
        "related": ["samsung", "laptop", "intel", "windows 11"]
    },

    "cloud": {
        "beginner": "Cloud-ul e ca un hard disk uriaș pe internet. În loc să ții fișierele doar pe laptop, le pui 'în nor' și poți să le accesezi de oriunde, de pe orice dispozitiv.",
        "professional": "Cloud computing-ul livrează servicii de calcul (servere, stocare, baze de date, rețele) prin internet. Modele: IaaS (infrastructură), PaaS (platformă), SaaS (software). Lideri: AWS, Azure, Google Cloud.",
        "expert": "Arhitecturile cloud-native folosesc microservicii, containere (Docker, Kubernetes), serverless (AWS Lambda) și CI/CD. Optimizarea costurilor implică auto-scaling, reserved instances și FinOps.",
        "code": "# Upload fișier pe AWS S3\nimport boto3\ns3 = boto3.client('s3')\ns3.upload_file('fisier.txt', 'bucket', 'fisier.txt')\nprint('Upload complet!')",
        "real_world": "Google Drive, iCloud, Netflix, Instagram — toate folosesc cloud. Pozele tale de pe telefon sunt în cloud. AEGIS rulează pe Streamlit Cloud chiar acum!",
        "quiz": {"question": "Ce înseamnă SaaS?",
                 "options": ["Software as a Service", "Storage as a System", "Server and Application Setup",
                             "System as a Software"], "answer": "Software as a Service"},
        "related": ["aws", "azure", "google cloud", "saas", "docker", "serverless"]
    },

    "blockchain": {
        "beginner": "Blockchain-ul e ca un caiet de notițe pe care toată lumea poate scrie, dar nimeni nu poate șterge. Fiecare pagină e un 'bloc' legat de cel anterior — de aici 'lanț de blocuri'.",
        "professional": "Blockchain este un registru distribuit și descentralizat care înregistrează tranzacții immutable. Folosește consens (PoW, PoS), criptografie și smart contracts. Aplicații: criptomonede, DeFi, NFT-uri, supply chain.",
        "expert": "Implementările enterprise (Hyperledger, Corda) oferă blockchain privat. Scalabilitatea se rezolvă prin Layer 2 (Lightning Network, Polygon), sharding și rollups.",
        "code": "# Hash blockchain în Python\nimport hashlib, json\ndef create_block(data, prev):\n    block = {'data': data, 'prev': prev}\n    block['hash'] = hashlib.sha256(json.dumps(block).encode()).hexdigest()\n    return block",
        "real_world": "Bitcoin e cel mai faimos blockchain. Ethereum permite smart contracts. NFT-urile se vând pe blockchain.",
        "quiz": {"question": "Cine a creat Bitcoin?",
                 "options": ["Elon Musk", "Satoshi Nakamoto", "Bill Gates", "Vitalik Buterin"],
                 "answer": "Satoshi Nakamoto"},
        "related": ["bitcoin", "ethereum", "nft", "defi", "web3", "smart contract"]
    },

    "cybersecurity": {
        "beginner": "Securitatea cibernetică e ca o alarmă pentru casa ta digitală. Te protejează de hoți (hackeri), încuie ușile (parole) și te avertizează când cineva încearcă să intre.",
        "professional": "Cybersecurity protejează sisteme, rețele și date împotriva atacurilor digitale. Domenii: network security, application security, cryptography, incident response. Amenințări: malware, phishing, ransomware, DDoS, zero-day.",
        "expert": "Strategiile defense-in-depth implementează multiple layere: firewall (L3/L4), WAF (L7), IDS/IPS, SIEM, EDR/XDR. Zero Trust Architecture elimină perimetrul tradițional.",
        "code": "# Hash securizat parolă\nimport hashlib, os\ndef hash_pwd(p):\n    salt = os.urandom(32)\n    return salt + hashlib.pbkdf2_hmac('sha256', p.encode(), salt, 100000)",
        "real_world": "Când intri pe internet banking, conexiunea e criptată. WhatsApp folosește criptare end-to-end. Antivirusul blochează viruși.",
        "quiz": {"question": "Ce atac criptează fișierele și cere răscumpărare?",
                 "options": ["Phishing", "Ransomware", "DDoS", "SQL Injection"], "answer": "Ransomware"},
        "related": ["firewall", "vpn", "encryption", "malware", "phishing"]
    },

    "docker": {
        "beginner": "Docker e ca o cutie magică în care pui codul tău cu tot ce are nevoie ca să ruleze. Poți să muți cutia pe orice computer și va funcționa la fel. Gata cu 'pe laptopul meu merge'!",
        "professional": "Docker este o platformă de containerizare care pachetează aplicațiile cu toate dependențele într-un container izolat. Containerele sunt lightweight față de VM-uri și rulează pe Docker Engine.",
        "expert": "Arhitectura Docker: Dockerfile → Image → Container. Orchestration cu Kubernetes, Docker Compose pentru multi-container, registry cu Docker Hub. Best practices: multi-stage builds, layer caching, non-root users.",
        "code": "# Dockerfile exemplu\nFROM python:3.11\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ['streamlit', 'run', 'app.py']",
        "real_world": "AEGIS ar putea rula într-un container Docker! Așa l-ai putea deploya oriunde — pe orice server, în orice țară. Netflix, Spotify, Uber — toate folosesc containere.",
        "quiz": {"question": "Ce fișier definește un container Docker?",
                 "options": ["Dockerfile", "docker.txt", "container.yml", "docker.cfg"], "answer": "Dockerfile"},
        "related": ["kubernetes", "docker compose", "container", "devops", "serverless"]
    },

    "machine learning": {
        "beginner": "Machine Learning e ca un copil care învață din exemple. Îi arăți 1000 de poze cu pisici, și el învață singur cum arată o pisică. Nu-i spui tu regulile — le descoperă singur!",
        "professional": "ML este un subset al AI unde algoritmii învață din date fără a fi programați explicit. Tipuri: supervised (date etichetate), unsupervised (pattern-uri ascunse), reinforcement (recompense).",
        "expert": "Algoritmi: Random Forest, XGBoost, SVM, Neural Networks. Optimizare: gradient descent, backpropagation. Evaluare: cross-validation, confusion matrix, ROC-AUC. Feature engineering și hyperparameter tuning.",
        "code": "# ML cu Scikit-learn\nfrom sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier()\nmodel.fit(X_train, y_train)\nprint(f'Acuratețe: {model.score(X_test, y_test):.2%}')",
        "real_world": "Când Netflix îți recomandă un film, când Google Maps prezice traficul, când banca detectează o tranzacție frauduloasă — Machine Learning e în spate.",
        "quiz": {"question": "Ce tip de ML folosește date etichetate?",
                 "options": ["Supervised", "Unsupervised", "Reinforcement", "Manual"], "answer": "Supervised"},
        "related": ["deep learning", "neural network", "ai", "data science", "tensorflow"]
    },

    "firewall": {
        "beginner": "Un firewall e ca un bodyguard la intrarea într-un club. El verifică pe toți cei care vor să intre. Dacă ești pe listă, intri. Dacă nu, rămâi afară. Firewall-ul face același lucru cu datele.",
        "professional": "Un firewall monitorizează și filtrează traficul de rețea pe baza unor reguli de securitate predefinite. Poate fi hardware sau software și operează la nivel de rețea (Layer 3/4) sau aplicație (Layer 7).",
        "expert": "Next-Generation Firewall (NGFW) integrează IPS, DPI, SSL inspection și application awareness. Arhitecturi: perimeter firewall, distributed firewall, cloud firewall (AWS Security Groups, Azure NSG).",
        "code": "# Reguli firewall simplificate\nfirewall_rules = {\n    'allow': ['80', '443', '22'],\n    'deny': ['23', '21', '3389']\n}\ndef check_port(port):\n    return 'ALLOW' if port in firewall_rules['allow'] else 'DENY'",
        "real_world": "Routerul tău de acasă are un firewall încorporat. Windows are Windows Defender Firewall. Fiecare site web e protejat de un WAF (Web Application Firewall).",
        "quiz": {"question": "Ce face un firewall?",
                 "options": ["Filtrează traficul", "Scrie cod", "Editează poze", "Trimite email-uri"],
                 "answer": "Filtrează traficul"},
        "related": ["vpn", "ids", "ips", "encryption", "cybersecurity"]
    },

    "neural network": {
        "beginner": "O rețea neuronală e ca un creier artificial făcut din mulți 'neuroni' mici conectați între ei. Fiecare neuron primește informație, o procesează și o trimite mai departe. Împreună, rezolvă probleme complexe.",
        "professional": "O rețea neuronală artificială este inspirată de creierul uman, formată din straturi de neuroni interconectați. Fiecare conexiune are o pondere (weight) care se ajustează prin backpropagation.",
        "expert": "Arhitecturi: CNN (imagini), RNN/LSTM (secvențe), Transformer (NLP). Antrenare: forward pass, loss calculation, backward pass (gradient descent). Optimizare: Adam, SGD, learning rate scheduling.",
        "code": "# Rețea neuronală simplă cu Keras\nfrom tensorflow.keras.models import Sequential\nfrom tensorflow.keras.layers import Dense\nmodel = Sequential([\n    Dense(64, activation='relu'),\n    Dense(32, activation='relu'),\n    Dense(1, activation='sigmoid')\n])\nmodel.compile(optimizer='adam', loss='binary_crossentropy')",
        "real_world": "Când deblochezi telefonul cu fața, o rețea neuronală recunoaște fața ta. Când Google Translate traduce un text, o rețea neuronală face traducerea.",
        "quiz": {"question": "Ce algoritm ajustează ponderile într-o rețea neuronală?",
                 "options": ["Backpropagation", "Quick Sort", "Binary Search", "Dijkstra"],
                 "answer": "Backpropagation"},
        "related": ["deep learning", "machine learning", "cnn", "rnn", "transformer"]
    },

    "encryption": {
        "beginner": "Criptarea e ca un limbaj secret. Scrii un mesaj, îl transformi în ceva de necitit (criptezi), și doar persoana care are 'cheia' poate să-l citească (decripteze).",
        "professional": "Criptarea transformă datele într-un format codificat folosind algoritmi matematici. Tipuri: simetrică (AES — aceeași cheie) și asimetrică (RSA — cheie publică + privată).",
        "expert": "Standarde: AES-256 (guvernamental), RSA-4096, ECC. TLS 1.3 pentru web. Criptarea end-to-end (Signal Protocol). Hashing: SHA-256, bcrypt. Quantum-resistant cryptography în dezvoltare.",
        "code": "# Criptare simetrică cu Python\nfrom cryptography.fernet import Fernet\nkey = Fernet.generate_key()\ncipher = Fernet(key)\nencrypted = cipher.encrypt(b'Mesaj secret')\ndecrypted = cipher.decrypt(encrypted)",
        "real_world": "WhatsApp folosește criptare end-to-end. HTTPS (lacătul verde din browser) e criptare. Când plătești cu cardul online, datele sunt criptate.",
        "quiz": {"question": "Ce tip de criptare folosește două chei diferite?",
                 "options": ["Asimetrică", "Simetrică", "Hashing", "Compresie"], "answer": "Asimetrică"},
        "related": ["decryption", "aes", "rsa", "ssl", "tls", "https"]
    },

    "kubernetes": {
        "beginner": "Kubernetes e ca un dirijor de orchestră. Ai multe containere (muzicieni) și Kubernetes se asigură că toate cântă la timp, că niciunul nu lipsește și că totul sună perfect.",
        "professional": "Kubernetes (K8s) este o platformă open-source pentru automatizarea deployment-ului, scalării și managementului containerelor. Componente: Pods, Nodes, Services, Deployments, ConfigMaps.",
        "expert": "Arhitectură: Control Plane (API Server, etcd, Scheduler) + Worker Nodes (kubelet, kube-proxy). Networking: CNI (Calico, Cilium). Service Mesh: Istio. GitOps: ArgoCD, Flux.",
        "code": "# Deployment Kubernetes (YAML)\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: aegis-app\nspec:\n  replicas: 3\n  selector:\n    matchLabels:\n      app: aegis\n  template:\n    spec:\n      containers:\n      - name: aegis\n        image: aegis:latest\n        ports:\n        - containerPort: 8501",
        "real_world": "Google, Netflix, Spotify — toate rulează pe Kubernetes. Când Netflix are milioane de utilizatori simultan, Kubernetes scalează automat serverele.",
        "quiz": {"question": "Ce e un Pod în Kubernetes?",
                 "options": ["Cel mai mic obiect deployabil", "Un tip de bază de date", "Un limbaj de programare",
                             "Un protocol de rețea"], "answer": "Cel mai mic obiect deployabil"},
        "related": ["docker", "docker compose", "helm", "istio", "devops", "microservices"]
    },

    "iot": {
        "beginner": "IoT (Internet of Things) e când obiectele din casa ta devin 'smart' și se conectează la internet. Frigiderul îți spune că ai rămas fără lapte, ceasul îți monitorizează somnul, becurile se aprind singure.",
        "professional": "IoT conectează dispozitive fizice (senzori, actuatori) la internet pentru colectare de date și control. Protocoale: MQTT, CoAP, Zigbee. Platforme: AWS IoT, Azure IoT Hub.",
        "expert": "Arhitecturi: Edge Computing (procesare locală), Fog Computing, Cloud IoT. Securitate: PKI pentru device-uri, OTA updates. Provocări: scalabilitate miliarde de device-uri, latență, interoperabilitate.",
        "code": "# Simulare senzor IoT\nimport random, time\nwhile True:\n    temp = random.uniform(20.0, 30.0)\n    print(f'Temperatură: {temp:.1f}°C')\n    time.sleep(5)",
        "real_world": "Galaxy Watch-ul tău e un dispozitiv IoT! La fel și Alexa, becurile Philips Hue, termostatele Nest, și mașinile Tesla conectate la internet.",
        "quiz": {"question": "Ce înseamnă IoT?",
                 "options": ["Internet of Things", "Internet of Technology", "Input Output Transfer",
                             "Internal Operating Tool"], "answer": "Internet of Things"},
        "related": ["arduino", "raspberry pi", "sensor", "cloud", "5g"]
    },

    "5g": {
        "beginner": "5G e a cincea generație de internet mobil. E ca și cum ai trece de la o șosea cu 2 benzi la o autostradă cu 100 de benzi. Totul e mai rapid, mai instant.",
        "professional": "5G este standardul de rețea mobilă cu viteze de până la 20 Gbps, latență sub 1ms și capacitate pentru 1 milion de device-uri pe km². Benzi: low-band, mid-band, mmWave.",
        "expert": "Arhitectură 5G: Network Slicing (rețele virtuale dedicate), MEC (Multi-access Edge Computing), beamforming. 3GPP Release 17/18. Aplicații critice: V2X (vehicule autonome), remote surgery, Industry 4.0.",
        "code": "# Verifică viteza internetului (conceptual)\nimport speedtest\nst = speedtest.Speedtest()\nprint(f'Download: {st.download()/1e6:.1f} Mbps')\nprint(f'Upload: {st.upload()/1e6:.1f} Mbps')\nprint(f'Ping: {st.results.ping} ms')",
        "real_world": "Telefonul tău Galaxy A56 suportă 5G! Când vezi '5G' în bara de sus, ești conectat la cea mai rapidă rețea mobilă din lume.",
        "quiz": {"question": "Ce viteză maximă teoretică are 5G?",
                 "options": ["20 Gbps", "100 Mbps", "1 Gbps", "500 Mbps"], "answer": "20 Gbps"},
        "related": ["iot", "wifi 7", "bandwidth", "latency", "network"]
    },

    "wifi 7": {
        "beginner": "Wi-Fi 7 e cea mai nouă și mai rapidă tehnologie de internet wireless. E ca Wi-Fi-ul pe care îl știi, dar pe steroizi. Perfect pentru gaming, streaming 8K și realitate virtuală.",
        "professional": "Wi-Fi 7 (802.11be) oferă viteze de până la 46 Gbps, canale de 320 MHz, 4096-QAM, Multi-Link Operation (MLO) și latență ultra-scăzută.",
        "expert": "MLO permite conectarea simultană pe mai multe benzi (2.4, 5, 6 GHz). 16x16 MU-MIMO, OFDMA îmbunătățit. Compatibilitate cu Wi-Fi 6/6E. Aplicații enterprise: AR/VR fără fir, Industry 4.0.",
        "code": "# Verifică rețelele Wi-Fi disponibile (Windows)\n# import subprocess\n# result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], capture_output=True, text=True)\n# print(result.stdout)",
        "real_world": "Samsung Galaxy Book5 Pro 360 are Wi-Fi 7! Când îl vei avea, vei putea descărca un film 4K în câteva secunde.",
        "quiz": {"question": "Ce viteză maximă teoretică are Wi-Fi 7?",
                 "options": ["46 Gbps", "10 Gbps", "1 Gbps", "100 Gbps"], "answer": "46 Gbps"},
        "related": ["5g", "bandwidth", "latency", "router", "network"]
    },

    "ssd": {
        "beginner": "SSD-ul e ca o bibliotecă ultra-rapidă pentru fișierele tale. Spre deosebire de HDD (care are piese care se învârt), SSD-ul nu are piese mișcătoare și e de 10 ori mai rapid.",
        "professional": "SSD (Solid State Drive) folosește memorie NAND flash pentru stocare persistentă. Interfețe: SATA III (până la 550 MB/s), NVMe PCIe 4.0/5.0 (până la 14 GB/s).",
        "expert": "Tehnologii: 3D NAND (straturi multiple), SLC/MLC/TLC/QLC caching, DRAM cache vs DRAM-less. NVMe 2.0, ZNS (Zoned Namespaces) pentru centre de date. Endurance: TBW (Total Bytes Written).",
        "code": "# Verifică viteza discului (conceptual)\nimport time, os\nsize = 1024*1024*100  # 100MB\nstart = time.time()\nwith open('test.bin', 'wb') as f:\n    f.write(os.urandom(size))\nend = time.time()\nprint(f'Viteză scriere: {size/(end-start)/1e6:.0f} MB/s')",
        "real_world": "Laptopul tău viitor (Book5 Pro 360) are SSD NVMe de 1TB. Se deschide în 5 secunde. Jocurile se încarcă instant. Aplicațiile pornesc fără delay.",
        "quiz": {"question": "Ce interfață e mai rapidă pentru SSD?",
                 "options": ["NVMe PCIe", "SATA III", "USB 3.0", "FireWire"], "answer": "NVMe PCIe"},
        "related": ["hdd", "ram", "nvme", "storage", "motherboard"]
    },

    "html": {
        "beginner": "HTML e ca scheletul unei case. Fiecare pagină web e construită pe un schelet HTML — el ține totul în picioare: texte, poze, butoane.",
        "professional": "HTML (HyperText Markup Language) este limbajul standard pentru structurarea paginilor web, folosind elemente și tag-uri pentru a defini conținutul.",
        "expert": "HTML5 aduce semantic elements (article, section, nav), suport multimedia nativ (video, audio), canvas pentru grafică și API-uri moderne (localStorage, Web Workers).",
        "code": "<!DOCTYPE html>\n<html>\n<head><title>Pagina mea</title></head>\n<body>\n  <h1>Salut, Andrei!</h1>\n  <p>Acesta e AEGIS.</p>\n</body>\n</html>",
        "real_world": "Fiecare site pe care-l vizitezi — Google, YouTube, Instagram — e construit pe HTML. E prima limbă pe care o învață orice web developer.",
        "quiz": {"question": "Ce înseamnă HTML?",
                 "options": ["HyperText Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language",
                             "Home Tool Markup Language"], "answer": "HyperText Markup Language"},
        "related": ["css", "javascript", "dom", "frontend", "web development"]
    },

    "css": {
        "beginner": "Dacă HTML e scheletul casei, CSS e vopseaua, mobila și decorațiunile. CSS face site-urile să arate FRUMOS — culori, fonturi, layout-uri.",
        "professional": "CSS (Cascading Style Sheets) controlează prezentarea vizuală a paginilor web: layout, culori, fonturi, animații și responsive design.",
        "expert": "CSS modern include Flexbox și Grid pentru layout, custom properties (variabile), animații keyframe, media queries pentru responsive design și preprocesoare ca Sass.",
        "code": "/* CSS simplu */\nbody {\n  background-color: #0a0a0a;\n  color: white;\n  font-family: Arial, sans-serif;\n}\n\nh1 {\n  color: #00ffcc;\n  text-align: center;\n}",
        "real_world": "Când vezi un site frumos — cu culori, animații, butoane stilizate — totul e făcut cu CSS. Fără CSS, internetul ar fi alb-negru și urât.",
        "quiz": {"question": "Ce face CSS într-o pagină web?",
                 "options": ["Stilizează conținutul", "Rulează pe server", "Gestionează baza de date",
                             "Face calcule matematice"], "answer": "Stilizează conținutul"},
        "related": ["html", "javascript", "frontend", "responsive design", "bootstrap"]
    },

    "javascript": {
        "beginner": "JavaScript e magicianul paginii web. Face butoanele să reacționeze, animațiile să se miște și totul să fie INTERACTIV. E ca un creier pentru site-uri.",
        "professional": "JavaScript este un limbaj de scripting pentru web, permițând conținut dinamic, manipulare DOM și comunicare asincronă cu serverele.",
        "expert": "JS modern (ES2024+) suportă async/await, modules, arrow functions, destructuring, spread operators. Rulează pe server prin Node.js, Deno, Bun. Framework-uri: React, Vue, Angular.",
        "code": "// JavaScript simplu\ndocument.querySelector('button').addEventListener('click', () => {\n  alert('Salut, Andrei! AEGIS e cel mai tare!');\n});",
        "real_world": "Google Maps, YouTube, Facebook, Instagram — toate folosesc JavaScript. Orice site pe care dai click și se întâmplă ceva — acolo e JavaScript.",
        "quiz": {"question": "Unde rulează JavaScript?",
                 "options": ["În browser și pe server (Node.js)", "Doar pe server", "Doar în browser", "Pe Marte"],
                 "answer": "În browser și pe server (Node.js)"},
        "related": ["html", "css", "react", "node.js", "typescript"]
    },

    "sql": {
        "beginner": "SQL e ca un bibliotecar care găsește orice carte într-o bibliotecă imensă. Îi spui ce cauți, și el știe exact unde e. SQL face același lucru cu datele.",
        "professional": "SQL (Structured Query Language) gestionează și interoghează baze de date relaționale. Operații: SELECT, INSERT, UPDATE, DELETE, JOIN-uri între tabele.",
        "expert": "Optimizare SQL: indexing (B-tree, hash), query execution plans, normalization vs denormalization, stored procedures, triggers, window functions, CTE-uri.",
        "code": "-- SQL simplu\nSELECT nume, varsta\nFROM utilizatori\nWHERE oras = 'Ploiesti'\nORDER BY nume ASC;",
        "real_world": "Când faci login pe un site, SQL caută numele tău în baza de date. Când verifici soldul la bancă, SQL îți aduce tranzacțiile. E peste tot.",
        "quiz": {"question": "Ce comandă SQL extrage date?", "options": ["SELECT", "GET", "FETCH", "EXTRACT"],
                 "answer": "SELECT"},
        "related": ["database", "mysql", "postgresql", "nosql", "orm"]
    },

    "react": {
        "beginner": "React e ca un set de piese LEGO pentru site-uri. Construiești bucăți mici (componente) și le îmbini într-o pagină web interactivă și rapidă.",
        "professional": "React este o bibliotecă JavaScript pentru construirea interfețelor utilizator, bazată pe componente reutilizabile și Virtual DOM pentru performanță.",
        "expert": "React avansat: hooks (useState, useEffect, useContext), state management (Redux, Zustand), server components, Next.js pentru SSR, React Native pentru mobile.",
        "code": "// Componentă React simplă\nfunction Salut({nume}) {\n  return <h1>Salut, {nume}! Bine ai venit la AEGIS!</h1>;\n}\n\nexport default function App() {\n  return <Salut nume='Andrei' />;\n}",
        "real_world": "Facebook, Instagram, Netflix, Airbnb — toate folosesc React. E una dintre cele mai populare tehnologii web din lume.",
        "quiz": {"question": "Cine a creat React?", "options": ["Facebook (Meta)", "Google", "Microsoft", "Amazon"],
                 "answer": "Facebook (Meta)"},
        "related": ["javascript", "angular", "vue", "frontend", "next.js"]
    },

    "linux": {
        "beginner": "Linux e ca un motor invizibil care rulează lumea. Nu-l vezi, dar e în telefoane, servere, supercomputere și chiar în mașina Tesla. E gratuit și foarte puternic.",
        "professional": "Linux este un kernel open-source pentru sisteme de operare. Distribuții populare: Ubuntu, Fedora, Debian, Arch. Domină serverele, cloud-ul și dispozitivele embedded.",
        "expert": "Linux kernel: process scheduling (CFS), memory management, VFS, namespaces/cgroups pentru containere. Administrare: systemd, iptables/nftables, LVM, kernel tuning.",
        "code": "# Comenzi Linux esențiale\nls -la           # Listare fișiere\ncd /var/log      # Navigare\nsudo systemctl restart nginx   # Restart serviciu\ngrep 'error' app.log           # Căutare în fișiere\nchmod +x script.sh             # Permisiuni executare",
        "real_world": "Android rulează pe kernel Linux. Google, Facebook, NASA — toate folosesc Linux pe servere. 100% din supercomputerele lumii rulează Linux.",
        "quiz": {"question": "Cine a creat Linux?",
                 "options": ["Linus Torvalds", "Bill Gates", "Steve Jobs", "Elon Musk"], "answer": "Linus Torvalds"},
        "related": ["ubuntu", "bash", "terminal", "kernel", "debian"]
    },

    "vpn": {
        "beginner": "Un VPN e ca un tunel secret între tine și internet. Nimeni nu poate vedea ce faci — nici hackerii, nici furnizorul de internet. E ca o pelerină de invizibilitate digitală.",
        "professional": "VPN (Virtual Private Network) criptează traficul de internet și îl direcționează printr-un server securizat, ascunzând adresa IP și protejând confidențialitatea.",
        "expert": "Protocoale VPN: WireGuard (modern, rapid), OpenVPN (flexibil), IKEv2/IPSec (mobil). Arhitecturi: site-to-site, remote access, split tunneling, kill switch.",
        "code": "# Configurare WireGuard (exemplu)\n[Interface]\nPrivateKey = <cheia-ta-privata>\nAddress = 10.0.0.2/24\nDNS = 1.1.1.1\n\n[Peer]\nPublicKey = <cheia-serverului>\nEndpoint = vpn.example.com:51820\nAllowedIPs = 0.0.0.0/0",
        "real_world": "Când te conectezi la Wi-Fi-ul unui hotel sau cafenea, un VPN te protejează de hackeri. Jurnaliștii și activiștii folosesc VPN-uri pentru siguranță.",
        "quiz": {"question": "Ce face un VPN?",
                 "options": ["Criptează conexiunea și ascunde IP-ul", "Accelerează internetul", "Repară viruși",
                             "Editează poze"], "answer": "Criptează conexiunea și ascunde IP-ul"},
        "related": ["encryption", "cybersecurity", "firewall", "privacy", "proxy"]
    },

    "android": {
        "beginner": "Android e ca un sistem de operare care face telefonul tău să fie SMART. E creat de Google și e folosit de miliarde de telefoane, tablete și ceasuri din toată lumea.",
        "professional": "Android este un sistem de operare open-source bazat pe kernel Linux, dezvoltat de Google. Domină piața mobilă cu peste 70% cotă globală.",
        "expert": "Arhitectura Android: kernel Linux, HAL, Android Runtime (ART), framework Java/Kotlin. Componente: Activities, Services, Broadcast Receivers, Content Providers. Jetpack Compose pentru UI modern.",
        "code": "// Kotlin — Activitate Android simplă\nclass MainActivity : ComponentActivity() {\n  override fun onCreate(savedInstanceState: Bundle?) {\n    super.onCreate(savedInstanceState)\n    setContent {\n      Text('Salut, Andrei! AEGIS rulează pe Android!')\n    }\n  }\n}",
        "real_world": "Telefonul tău Galaxy A56 rulează Android! Samsung, Xiaomi, OnePlus — toate folosesc Android. E cel mai folosit sistem de operare din lume.",
        "quiz": {"question": "Cine deține Android?", "options": ["Google", "Samsung", "Microsoft", "Apple"],
                 "answer": "Google"},
        "related": ["ios", "kotlin", "flutter", "google play", "linux"]
    },

    "windows": {
        "beginner": "Windows e ca un birou digital pe care îl folosești zilnic. E sistemul de operare care pornește când deschizi laptopul — cu pictograme, ferestre și bara de start.",
        "professional": "Microsoft Windows este cel mai popular sistem de operare pentru PC-uri. Windows 11 oferă Copilot AI, suport pentru aplicații Android și securitate avansată.",
        "expert": "Windows 11 arhitectură: kernel NT, Hyper-V virtualization, WSL2 pentru Linux, DirectStorage pentru gaming, TPM 2.0 pentru securitate. PowerShell pentru administrare avansată.",
        "code": "# PowerShell — Comenzi utile\nGet-Process | Sort-Object CPU -Descending\nGet-Service | Where-Object Status -eq 'Running'\nwinget install Python.Python.3.12",
        "real_world": "Majoritatea laptopurilor din lume rulează Windows. Samsung Galaxy Book5 Pro 360 al tău va rula Windows 11 cu Copilot AI integrat.",
        "quiz": {"question": "Ce companie creează Windows?", "options": ["Microsoft", "Apple", "Google", "IBM"],
                 "answer": "Microsoft"},
        "related": ["linux", "macos", "powershell", "kernel", "uefi"]
    },

    "github": {
        "beginner": "GitHub e ca o bibliotecă uriașă unde programatorii își pun codul. E și o rețea socială pentru developeri — poți colabora, învăța și arăta ce ai construit.",
        "professional": "GitHub este cea mai mare platformă de găzduire a codului sursă, folosind Git pentru versionare. Oferă CI/CD prin GitHub Actions, code review și project management.",
        "expert": "GitHub avansat: Actions workflows, Codespaces, Dependabot, code scanning cu CodeQL, branch protection rules, GitHub Pages, API REST și GraphQL.",
        "code": "# Comenzi Git + GitHub\ngit clone https://github.com/andrei28vieru-boop/AEGIS-AI.git\ngit add .\ngit commit -m 'Added new AEGIS LEVEL terms'\ngit push origin main",
        "real_world": "AEGIS e pe GitHub chiar acum! Toate companiile mari — Google, Microsoft, Facebook — au codul pe GitHub. E portofoliul tău de developer.",
        "quiz": {"question": "Ce sistem de versionare folosește GitHub?", "options": ["Git", "SVN", "Mercurial", "CVS"],
                 "answer": "Git"},
        "related": ["git", "github actions", "devops", "ci/cd", "repository"]
    },

    "json": {
        "beginner": "JSON e ca un translator universal pentru computere. Orice limbaj de programare înțelege JSON — e modul în care aplicațiile vorbesc între ele pe internet.",
        "professional": "JSON (JavaScript Object Notation) este un format lightweight de schimb de date, ușor de citit pentru oameni și simplu de procesat pentru mașini. Folosește perechi cheie-valoare și array-uri.",
        "expert": "JSON suportă tipuri: string, number, boolean, null, object, array. Validare prin JSON Schema. Alternativă la XML, mai compact. JSON Lines pentru streaming. JSONB în PostgreSQL pentru interogări rapide.",
        "code": "{\n  \"nume\": \"Andrei\",\n  \"varsta\": 15,\n  \"proiect\": \"AEGIS\",\n  \"termeni\": 725,\n  \"obiectiv\": \"Billionaire\"\n}",
        "real_world": "Când verifici vremea pe telefon, aplicația primește datele în JSON. API-urile Google, Facebook, Instagram — toate returnează JSON. E limba universală a internetului.",
        "quiz": {"question": "Ce înseamnă JSON?",
                 "options": ["JavaScript Object Notation", "Java System Online Network", "Just Simple Object Name",
                             "JSON Standard Object Notation"], "answer": "JavaScript Object Notation"},
        "related": ["api", "xml", "api rest", "database", "mongodb"]
    },

    "bitcoin": {
        "beginner": "Bitcoin e ca aurul digital. Nu există fizic — e doar pe internet. Nimeni nu-l controlează: nici bănci, nici guverne. Oamenii îl trimit direct unul altuia, ca pe un email cu bani.",
        "professional": "Bitcoin (BTC) este prima criptomonedă descentralizată, creată în 2009 de Satoshi Nakamoto. Rulează pe tehnologia blockchain și folosește Proof of Work pentru securitate.",
        "expert": "Bitcoin: supply limitat la 21 milioane, mining cu SHA-256, halving la fiecare 210,000 blocuri, Lightning Network pentru Layer 2 scaling. UTXO model, non-Turing complete scripting.",
        "code": "# Verifică prețul Bitcoin în timp real\nimport requests\nresponse = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')\ndata = response.json()\nprint(f\"BTC: ${data['bpi']['USD']['rate']}\")",
        "real_world": "El Salvador a adoptat Bitcoin ca monedă națională. Companii ca Tesla și MicroStrategy dețin Bitcoin. Poți cumpăra Bitcoin pe Binance sau Coinbase.",
        "quiz": {"question": "Care e supply-ul maxim de Bitcoin?",
                 "options": ["21 milioane", "100 milioane", "Nelimitat", "1 miliard"], "answer": "21 milioane"},
        "related": ["blockchain", "ethereum", "criptomonedă", "mining", "wallet"]
    },

    "gpu": {
        "beginner": "GPU-ul e ca un artist care pictează tot ce vezi pe ecran — jocuri, filmulețe, poze. Face asta de sute de ori pe secundă, mult mai rapid decât CPU-ul la grafică.",
        "professional": "GPU (Graphics Processing Unit) este un procesor specializat pentru calcule paralele masive, esențial pentru randare 3D, gaming, AI și mining crypto.",
        "expert": "GPU-urile moderne (NVIDIA CUDA, AMD ROCm) au mii de core-uri pentru parallel computing. Tensor Cores pentru AI, RT Cores pentru ray tracing. VRAM (GDDR6X, HBM3) oferă bandwidth masiv.",
        "code": "# Verifică GPU-ul disponibil pentru AI\nimport torch\nprint(f\"CUDA disponibil: {torch.cuda.is_available()}\")\nprint(f\"GPU: {torch.cuda.get_device_name(0)}\")\nprint(f\"Memorie: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB\")",
        "real_world": "NVIDIA face GPU-uri care antrenează AI-ul din spatele ChatGPT. GPU-ul tău integrat Intel Arc din viitorul Book5 Pro 360 poate rula jocuri și accelerare AI.",
        "quiz": {"question": "Ce companie domină piața de GPU-uri pentru AI?",
                 "options": ["NVIDIA", "Intel", "AMD", "Apple"], "answer": "NVIDIA"},
        "related": ["cpu", "ram", "nvidia", "deep learning", "ssd"]
    },

    "ram": {
        "beginner": "RAM-ul e ca un birou imens. Cu cât ai mai mult birou, cu atât poți lucra la mai multe lucruri simultan fără să se aglomereze. Când închizi calculatorul, biroul se golește.",
        "professional": "RAM (Random Access Memory) este memoria volatilă care stochează date temporar pentru procesor. DDR5 oferă viteze de până la 6400 MT/s cu consum redus.",
        "expert": "RAM arhitectură: canale (single/dual/quad), timing-uri CAS, XMP/EXPO pentru overclocking. ECC RAM pentru servere corectează erori. LPDDR5X în laptopuri oferă până la 8533 MT/s.",
        "code": "# Verifică RAM disponibilă în Python\nimport psutil\nram = psutil.virtual_memory()\nprint(f\"Total: {ram.total / 1e9:.1f} GB\")\nprint(f\"Disponibil: {ram.available / 1e9:.1f} GB\")\nprint(f\"Utilizat: {ram.percent}%\")",
        "real_world": "Samsung Galaxy Book5 Pro 360 are 16GB DDR5 RAM — poți rula AEGIS, browser cu 50 de tab-uri, PyCharm și Netflix simultan fără lag.",
        "quiz": {"question": "Ce tip de RAM e în Book5 Pro 360?", "options": ["DDR5", "DDR4", "DDR3", "LPDDR4X"],
                 "answer": "DDR5"},
        "related": ["cpu", "ssd", "gpu", "motherboard", "ddr5"]
    },

    "nvidia": {
        "beginner": "NVIDIA e ca un magician al graficii. Fac plăci video care transformă codul în lumi 3D incredibile și antrenează inteligența artificială. Sunt creierul din spatele ChatGPT și al jocurilor video.",
        "professional": "NVIDIA este liderul mondial în GPU-uri și AI computing. Seria GeForce pentru gaming, RTX cu ray tracing, și CUDA pentru calcul paralel în deep learning.",
        "expert": "NVIDIA arhitecturi: Hopper (H100 — datacenter AI), Ada Lovelace (RTX 40 — consumer), Blackwell (2024 — next-gen). CUDA API permite GPU computing. TensorRT pentru inferență optimizată.",
        "code": "# Verifică GPU NVIDIA cu CUDA\nimport torch\nif torch.cuda.is_available():\n    print(f\"GPU: {torch.cuda.get_device_name(0)}\")\n    print(f\"CUDA Cores: {torch.cuda.get_device_properties(0).multi_processor_count}\")\nelse:\n    print(\"Niciun GPU NVIDIA detectat\")",
        "real_world": "NVIDIA valorează peste 2 trilioane de dolari în 2024. GPU-urile lor antrenează ChatGPT, conduc mașini autonome și randează filmele Marvel.",
        "quiz": {"question": "Cum se numește platforma NVIDIA pentru AI?",
                 "options": ["CUDA", "TensorFlow", "PyTorch", "OpenCL"], "answer": "CUDA"},
        "related": ["gpu", "ai", "deep learning", "intel", "amd"]
    },

    "intel": {
        "beginner": "Intel e ca un bucătar-șef care gătește procesoarele din majoritatea laptopurilor. E compania care a inventat microprocesorul și încă e una dintre cele mai mari din lume.",
        "professional": "Intel Corporation este cel mai mare producător de procesoare x86 pentru PC-uri și servere. Produce procesoare Core Ultra, Xeon și plăci grafice Arc.",
        "expert": "Intel arhitecturi: Lunar Lake (Core Ultra 200V — 3nm, AI NPU), Arrow Lake (desktop), Granite Rapids (Xeon server). Foundry services (Intel 18A). Gaudi acceleratoare AI.",
        "code": "# Verifică CPU-ul Intel\nimport platform\ncpu = platform.processor()\nprint(f\"CPU: {cpu}\")\nprint(f\"Arhitectură: {platform.architecture()[0]}\")",
        "real_world": "Samsung Galaxy Book5 Pro 360 rulează pe Intel Core Ultra 7 256V. Intel procesoare sunt în miliarde de dispozitive — de la laptopuri la servere NASA.",
        "quiz": {"question": "Ce serie de procesoare Intel e în Book5 Pro 360?",
                 "options": ["Core Ultra 7", "Core i9", "Pentium", "Atom"], "answer": "Core Ultra 7"},
        "related": ["cpu", "amd", "nvidia", "gpu", "motherboard"]
    },

    "amd": {
        "beginner": "AMD e ca un underdog care a devenit campion. Era mereu pe locul 2 după Intel, dar acum face unele dintre cele mai rapide procesoare din lume. Și plăci video, și cipuri pentru console.",
        "professional": "AMD (Advanced Micro Devices) produce procesoare Ryzen (desktop/laptop), plăci grafice Radeon și cipuri pentru console (PlayStation 5, Xbox Series X).",
        "expert": "AMD arhitecturi: Zen 5 (Ryzen 9000), RDNA 3 (Radeon RX 7000), CDNA (instinct AI accelerators). Chiplet design pentru yield și costuri reduse. 3D V-Cache pentru gaming.",
        "code": "# Verifică CPU AMD Ryzen\nimport platform\ncpu = platform.processor()\nprint(f\"CPU: {cpu}\")",
        "real_world": "PlayStation 5 și Xbox Series X rulează pe cipuri AMD. Toate consolele next-gen sunt AMD. Ryzen domină piața de desktop pentru gameri și creatori.",
        "quiz": {"question": "Care e concurentul principal al AMD?", "options": ["Intel", "NVIDIA", "Apple", "Samsung"],
                 "answer": "Intel"},
        "related": ["cpu", "intel", "nvidia", "gpu", "motherboard"]
    },

    "apple": {
        "beginner": "Apple e ca un designer de lux al tehnologiei. Fac iPhone, MacBook, iPad — toate scumpe, dar elegante și ușor de folosit. E ca Mercedes-ul din lumea tech.",
        "professional": "Apple Inc. este cea mai valoroasă companie din lume, cunoscută pentru iPhone, Mac, iPad și ecosistemul integrat de hardware și software.",
        "expert": "Apple Silicon: cipuri M-series (M4 — 3nm, Neural Engine). Arhitectură unificată memory. Ecosistem: iOS, macOS, watchOS, visionOS. App Store cu peste 2 milioane de aplicații.",
        "code": "// Swift — Limbajul Apple pentru iOS/macOS\nimport SwiftUI\nstruct ContentView: View {\n    var body: some View {\n        Text(\"Salut, Andrei!\")\n            .font(.largeTitle)\n            .foregroundColor(.blue)\n    }\n}",
        "real_world": "iPhone-ul e cel mai vândut smartphone. Apple Watch domină piața de smartwatch-uri. Apple Vision Pro a lansat era spatial computing.",
        "quiz": {"question": "Cum se numesc procesoarele Apple pentru Mac?",
                 "options": ["M-series (M1, M2, M3, M4)", "A-series", "S-series", "X-series"],
                 "answer": "M-series (M1, M2, M3, M4)"},
        "related": ["ios", "macos", "iphone 16 pro max", "samsung", "macbook pro 16"]
    },

    "tesla": {
        "beginner": "Tesla e ca un iPhone pe roți. Mașinile lor sunt electrice, rapide și pline de tehnologie. Se conduc singure pe autostradă și primesc update-uri ca un telefon.",
        "professional": "Tesla Inc. este lider în vehicule electrice și energie curată, fondată de Elon Musk. Produce Model S, 3, X, Y și Cybertruck cu tehnologie de conducere autonomă.",
        "expert": "Tesla Full Self-Driving (FSD) folosește computer vision și rețele neuronale antrenate pe miliarde de km. Dojo supercomputer pentru training AI. 4680 battery cells pentru eficiență.",
        "code": "# Simulare autonomie Tesla\nbattery_kwh = 75  # Model 3 Long Range\nefficiency_wh_km = 150  # Wh per km\nautonomie_km = (battery_kwh * 1000) / efficiency_wh_km\nprint(f\"Autonomie estimată: {autonomie_km:.0f} km\")",
        "real_world": "Tesla Model Y a fost cea mai vândută mașină din lume în 2023. Tesla produce și baterii Powerwall pentru case și panouri solare.",
        "quiz": {"question": "Cine e CEO-ul Tesla?",
                 "options": ["Elon Musk", "Jeff Bezos", "Tim Cook", "Satya Nadella"], "answer": "Elon Musk"},
        "related": ["elon musk", "ev", "ai", "nvidia", "green tech"]
    },

    "spotify": {
        "beginner": "Spotify e ca un DJ personal care știe exact ce muzică îți place. Cauți orice melodie, asculți podcasturi, și descoperi artiști noi. E ca un radio infinit în buzunar.",
        "professional": "Spotify este cea mai mare platformă de streaming audio din lume cu peste 500 milioane de utilizatori. Oferă muzică, podcasturi și recomandări bazate pe AI.",
        "expert": "Spotify arhitectură: microservicii, Kafka pentru streaming de date, Cassandra pentru scalability, ML pentru Discover Weekly și algoritmi de recomandare. Codec Ogg Vorbis/AAC.",
        "code": "# Caută un artist pe Spotify API\nimport requests\nheaders = {'Authorization': 'Bearer YOUR_TOKEN'}\nresponse = requests.get(\n    'https://api.spotify.com/v1/search',\n    headers=headers,\n    params={'q': 'Depeche Mode', 'type': 'artist'}\n)\ndata = response.json()\nfor artist in data['artists']['items']:\n    print(f\"{artist['name']} — Popularitate: {artist['popularity']}\")",
        "real_world": "Spotify a schimbat industria muzicală. Artiștii sunt plătiți per stream. Playlist-uri ca Discover Weekly folosesc AI să-ți găsească muzică nouă în fiecare săptămână.",
        "quiz": {"question": "Câți utilizatori are Spotify?",
                 "options": ["Peste 500 milioane", "100 milioane", "1 miliard", "50 milioane"],
                 "answer": "Peste 500 milioane"},
        "related": ["streaming", "ai", "machine learning", "podcast", "apple"]
    },

    "database": {
        "beginner": "O bază de date e ca o bibliotecă digitală imensă. În loc de cărți, ține informații organizate — nume, numere, poze. Când cauți ceva, găsești instant.",
        "professional": "O bază de date este o colecție structurată de date stocate electronic. Tipuri: relaționale (SQL) cu tabele și relații, și non-relaționale (NoSQL) cu documente, grafuri sau cheie-valoare.",
        "expert": "Arhitecturi de baze de date: master-slave replication, sharding pentru scalare orizontală, ACID vs BASE, indexing (B-tree, hash, GiST), query optimization cu EXPLAIN, connection pooling.",
        "code": "-- Creează o bază de date și o tabelă\nCREATE DATABASE aegis_db;\nUSE aegis_db;\nCREATE TABLE users (\n    id INT PRIMARY KEY AUTO_INCREMENT,\n    name VARCHAR(100),\n    level VARCHAR(20)\n);\nINSERT INTO users (name, level) VALUES ('Andrei', 'Expert');",
        "real_world": "Când îți verifici soldul la bancă, datele tale sunt într-o bază de date. Facebook stochează miliarde de poze în baze de date. AEGIS însuși ar putea folosi o bază de date pentru termeni.",
        "quiz": {"question": "Care sunt cele două tipuri principale de baze de date?",
                 "options": ["SQL și NoSQL", "HTML și CSS", "JSON și XML", "RAM și ROM"], "answer": "SQL și NoSQL"},
        "related": ["sql", "mysql", "postgresql", "mongodb", "nosql"]
    },

    "mysql": {
        "beginner": "MySQL e ca un bibliotecar foarte rapid care organizează datele în tabele. E folosit de Facebook, YouTube și milioane de site-uri. E gratuit și foarte popular.",
        "professional": "MySQL este un sistem de management al bazelor de date relaționale (RDBMS) open-source. Folosește SQL pentru interogări și este parte a stivei LAMP (Linux, Apache, MySQL, PHP).",
        "expert": "MySQL: engine-uri InnoDB (ACID, foreign keys) și MyISAM (rapid, fără FK). Replication (master-slave, group replication). Indexing: B-tree, full-text. Partitioning, stored procedures, triggers, views.",
        "code": "-- MySQL: Creează utilizator și acordă permisiuni\nCREATE USER 'andrei'@'localhost' IDENTIFIED BY 'parola_sigura';\nGRANT ALL PRIVILEGES ON aegis_db.* TO 'andrei'@'localhost';\nFLUSH PRIVILEGES;",
        "real_world": "WordPress rulează pe MySQL. Facebook a pornit cu MySQL. Platforme ca Uber și Airbnb îl folosesc pentru date critice. E peste tot pe web.",
        "quiz": {"question": "MySQL este un sistem de baze de date de tip...?",
                 "options": ["Relațional (SQL)", "Document (NoSQL)", "Graph", "Key-Value"],
                 "answer": "Relațional (SQL)"},
        "related": ["sql", "database", "postgresql", "mongodb", "orm"]
    },

    "mongodb": {
        "beginner": "MongoDB e ca un caiet de notițe flexibil. În loc de tabele rigide, poți scrie orice fel de notiță, în orice format, și o găsești rapid. E baza de date preferată pentru aplicații moderne.",
        "professional": "MongoDB este o bază de date NoSQL orientată pe documente, stocând datele în format BSON (similar JSON). Ideală pentru date nestructurate și scalare orizontală.",
        "expert": "MongoDB: sharding pentru scalare, replica sets pentru high availability, aggregation pipeline pentru analytics. Indexing: compound, text, geospatial, TTL. Schema validation opțională.",
        "code": "// MongoDB: Inserare și căutare documente\ndb.users.insertOne({\n  name: 'Andrei',\n  level: 'Expert',\n  projects: ['AEGIS', 'Coffee Business']\n});\ndb.users.find({ level: 'Expert' });",
        "real_world": "Forbes, eBay, și Adobe folosesc MongoDB. E alegerea preferată pentru startup-uri care au nevoie de flexibilitate și scalare rapidă.",
        "quiz": {"question": "Ce format folosește MongoDB pentru stocare?",
                 "options": ["BSON (Binary JSON)", "CSV", "XML", "YAML"], "answer": "BSON (Binary JSON)"},
        "related": ["nosql", "database", "mysql", "json", "postgresql"]
    },

    "node.js": {
        "beginner": "Node.js e ca un motor care face JavaScript să ruleze pe server, nu doar în browser. Cu Node.js poți construi un site întreg — frontend și backend — folosind aceeași limbă.",
        "professional": "Node.js este un runtime JavaScript construit pe motorul V8 de la Chrome. Permite dezvoltarea de aplicații server-side cu JavaScript, folosind un model asincron non-blocant.",
        "expert": "Node.js: event loop pentru I/O non-blocant, libuv pentru operații asincrone, cluster module pentru multi-threading, streams pentru date mari. npm — cel mai mare ecosistem de pachete.",
        "code": "// Server Node.js simplu\nconst http = require('http');\nconst server = http.createServer((req, res) => {\n  res.writeHead(200, {'Content-Type': 'text/plain'});\n  res.end('Salut, Andrei! AEGIS rulează pe Node.js!');\n});\nserver.listen(3000, () => console.log('Server pornit pe portul 3000'));",
        "real_world": "Netflix, LinkedIn, și Uber folosesc Node.js. E backend-ul din spatele a milioane de aplicații web moderne.",
        "quiz": {"question": "Pe ce motor JavaScript rulează Node.js?",
                 "options": ["V8 (Chrome)", "SpiderMonkey (Firefox)", "JavaScriptCore (Safari)", "Chakra (Edge)"],
                 "answer": "V8 (Chrome)"},
        "related": ["javascript", "npm", "express", "backend", "react"]
    },

    "typescript": {
        "beginner": "TypeScript e ca JavaScript, dar cu super-puteri. Adaugă 'tipuri' — etichete care spun exact ce fel de date folosești. E ca și cum ai avea un corector care te avertizează înainte să greșești.",
        "professional": "TypeScript este un superset tipat al JavaScript, dezvoltat de Microsoft. Adaugă tipuri statice, interfețe, generice și compilare în JavaScript standard.",
        "expert": "TypeScript: type system avansat (union, intersection, conditional types), decorators, declaration files (.d.ts), strict mode, tsconfig pentru configurare. Integrare perfectă cu VS Code.",
        "code": "// TypeScript: Funcție cu tipuri\nfunction salut(nume: string, varsta: number): string {\n  return `Salut, ${nume}! Ai ${varsta} ani.`;\n}\nconsole.log(salut('Andrei', 15));",
        "real_world": "Angular, Deno, și VS Code sunt scrise în TypeScript. Majoritatea companiilor mari migrează de la JavaScript la TypeScript pentru proiecte complexe.",
        "quiz": {"question": "Cine a creat TypeScript?", "options": ["Microsoft", "Google", "Facebook", "Apple"],
                 "answer": "Microsoft"},
        "related": ["javascript", "react", "angular", "node.js", "frontend"]
    },

    "next.js": {
        "beginner": "Next.js e ca un atelier magic pentru site-uri React. Face site-urile să se încarce instant și să fie găsite ușor de Google. E folosit de cele mai mari companii din lume.",
        "professional": "Next.js este un framework React pentru producție, oferind Server-Side Rendering (SSR), Static Site Generation (SSG) și routing bazat pe fișiere.",
        "expert": "Next.js 14+: App Router cu React Server Components, streaming cu Suspense, server actions pentru mutații, ISR (Incremental Static Regeneration), middleware pe edge. Optimizat pentru Vercel.",
        "code": "// Next.js: Pagină simplă\nexport default function Home() {\n  return (\n    <div>\n      <h1>Salut, Andrei!</h1>\n      <p>AEGIS construit cu Next.js</p>\n    </div>\n  );\n}",
        "real_world": "TikTok, Twitch, Hulu și Nike folosesc Next.js. E framework-ul React #1 pentru site-uri moderne, rapide și SEO-friendly.",
        "quiz": {"question": "Ce companie a creat Next.js?", "options": ["Vercel", "Google", "Meta", "Netflix"],
                 "answer": "Vercel"},
        "related": ["react", "javascript", "typescript", "frontend", "ssr"]
    },

    "express": {
        "beginner": "Express e ca un schelet gata-făcut pentru servere web. În loc să construiești totul de la zero, Express îți dă piesele de bază și tu le aranjezi cum vrei. Simplu și rapid.",
        "professional": "Express.js este un framework minimalist pentru Node.js, oferind routing, middleware și suport pentru API-uri REST. Este cel mai popular framework Node.js.",
        "expert": "Express: middleware chain (req, res, next), error handling, route parameters, query strings. Combinat cu body-parser, cors, helmet pentru securitate. Alternativă modernă: Fastify.",
        "code": "// Express server simplu\nconst express = require('express');\nconst app = express();\napp.get('/', (req, res) => {\n  res.json({ message: 'Salut, Andrei!', project: 'AEGIS' });\n});\napp.listen(3000, () => console.log('Server Express pornit!'));",
        "real_world": "PayPal, Uber, și Twitter au folosit Express la început. Milioane de API-uri rulează pe Express. E fundamentul backend-ului JavaScript modern.",
        "quiz": {"question": "Express este un framework pentru...?", "options": ["Node.js", "Python", "Ruby", "PHP"],
                 "answer": "Node.js"},
        "related": ["node.js", "javascript", "api rest", "backend", "fastapi"]
    },

    "npm": {
        "beginner": "npm e ca un magazin imens cu piese gratuite pentru proiectele tale de cod. Ai nevoie de ceva — cauți pe npm, instalezi și folosești. E cel mai mare magazin de cod din lume.",
        "professional": "npm (Node Package Manager) este managerul de pachete implicit pentru Node.js, oferind acces la peste 2 milioane de pachete pentru dezvoltare JavaScript.",
        "expert": "npm: package.json pentru dependențe, semantic versioning (semver), lock files (package-lock.json), scripts personalizate, npm audit pentru securitate, npx pentru executare one-time.",
        "code": "# Comenzi npm esențiale\nnpm init -y                    # Inițializează proiect\nnpm install express            # Instalează pachet\nnpm install -g create-react-app  # Instalare globală\nnpm run start                 # Rulează script\nnpm audit fix                 # Repară vulnerabilități",
        "real_world": "npm e folosit de peste 17 milioane de developeri. Orice proiect JavaScript modern începe cu npm install. Ecosistemul npm e cel mai mare din lume.",
        "quiz": {"question": "Ce fișier conține dependențele unui proiect Node.js?",
                 "options": ["package.json", "app.js", "config.yml", "docker-compose.yml"], "answer": "package.json"},
        "related": ["node.js", "javascript", "pip", "pypi", "express"]
    },

    "rest api": {
        "beginner": "Un REST API e ca un meniu într-un restaurant. Tu alegi din meniu (faci o cerere), chelnerul o duce la bucătărie (server), și primești mâncarea (răspunsul). Simplu și standardizat.",
        "professional": "REST (Representational State Transfer) este un stil arhitectural pentru API-uri web, folosind metode HTTP (GET, POST, PUT, DELETE) și resurse identificate prin URL-uri.",
        "expert": "REST principles: statelessness, cacheability, uniform interface, resource-based URLs. HATEOAS pentru descoperire. Versionare (v1/, header). Paginare, filtrare, rate limiting. OpenAPI/Swagger pentru documentație.",
        "code": "# API REST cu Flask (Python)\nfrom flask import Flask, jsonify\napp = Flask(__name__)\n@app.route('/api/hello')\ndef hello():\n    return jsonify({'message': 'Salut, Andrei!', 'status': 'success'})\nif __name__ == '__main__':\n    app.run(port=5000)",
        "real_world": "API-urile Google Maps, Twitter, și GitHub sunt REST. Când o aplicație mobilă comunică cu un server, aproape sigur folosește un REST API.",
        "quiz": {"question": "Ce metodă HTTP folosești pentru a OBȚINE date?",
                 "options": ["GET", "POST", "PUT", "DELETE"], "answer": "GET"},
        "related": ["api", "json", "http", "oauth", "express"]
    },

    "http": {
        "beginner": "HTTP e ca un poștaș al internetului. Când scrii un site în browser, HTTP duce cererea ta la server și aduce pagina înapoi. E fundamentul pe care rulează tot web-ul.",
        "professional": "HTTP (HyperText Transfer Protocol) este protocolul de comunicare la baza World Wide Web. Metode: GET, POST, PUT, DELETE. Status codes: 200 (OK), 404 (Not Found), 500 (Server Error).",
        "expert": "HTTP/2: multiplexing, header compression (HPACK), server push. HTTP/3: bazat pe QUIC (UDP), latență redusă. HTTPS = HTTP + TLS. Caching headers (ETag, Cache-Control), CORS, cookies.",
        "code": "# Cerere HTTP simplă cu Python\nimport requests\nresponse = requests.get('https://api.github.com')\nprint(f\"Status: {response.status_code}\")\nprint(f\"Headers: {dict(response.headers)}\")\nprint(f\"Body: {response.json()}\")",
        "real_world": "Fiecare pagină web pe care o vizitezi folosește HTTP sau HTTPS. Status 200 = totul e bine. Status 404 = pagina nu există. Status 500 = eroare pe server.",
        "quiz": {"question": "Ce înseamnă status code 404?",
                 "options": ["Not Found (Pagină negăsită)", "OK (Totul bine)", "Server Error", "Redirect"],
                 "answer": "Not Found (Pagină negăsită)"},
        "related": ["https", "api", "dns", "tcp", "rest api"]
    },

    "dns": {
        "beginner": "DNS e ca o agendă telefonică a internetului. În loc să ții minte numere (adrese IP), scrii numele site-ului (google.com) și DNS-ul îl traduce automat în adresa corectă.",
        "professional": "DNS (Domain Name System) este sistemul care traduce numele de domenii în adrese IP. Funcționează ca o bază de date distribuită global, cu servere recursive și authoritative.",
        "expert": "DNS: record types (A, AAAA, CNAME, MX, TXT, NS, SOA), DNSSEC pentru autentificare, TTL pentru caching, Anycast pentru reziliență. DNS over HTTPS (DoH) și DNS over TLS (DoT) pentru confidențialitate.",
        "code": "# Verifică înregistrări DNS cu Python\nimport socket\ndomain = 'google.com'\nip = socket.gethostbyname(domain)\nprint(f\"{domain} → {ip}\")",
        "real_world": "De fiecare dată când scrii un site în browser, DNS-ul lucrează în fundal. Fără DNS, ar trebui să ții minte numere IP pentru fiecare site.",
        "quiz": {"question": "Ce face DNS-ul?",
                 "options": ["Traduce nume de domenii în IP-uri", "Criptează date", "Stochează fișiere",
                             "Rulează aplicații"], "answer": "Traduce nume de domenii în IP-uri"},
        "related": ["ip", "http", "https", "domain", "network"]
    },

    "https": {
        "beginner": "HTTPS e ca un plic securizat pentru datele tale pe internet. Când vezi lacătul verde în browser, înseamnă că nimeni nu poate citi ce trimiți — parolele și cardul tău sunt în siguranță.",
        "professional": "HTTPS (HyperText Transfer Protocol Secure) combină HTTP cu TLS/SSL pentru criptare end-to-end, autentificare a serverului și integritatea datelor transmise.",
        "expert": "TLS 1.3: handshake redus la 1-RTT, forward secrecy obligatorie, ciphersuite-uri moderne (AES-GCM, ChaCha20-Poly1305). Certificate X.509, PKI, Certificate Transparency. HSTS pentru forțare HTTPS.",
        "code": "# Verifică certificatul SSL al unui site\nimport ssl\nimport socket\nctx = ssl.create_default_context()\nwith ctx.wrap_socket(socket.socket(), server_hostname='google.com') as s:\n    s.connect(('google.com', 443))\n    cert = s.getpeercert()\n    print(f\"Emis de: {cert['issuer']}\")\n    print(f\"Expiră: {cert['notAfter']}\")",
        "real_world": "Când faci cumpărături online sau intri pe internet banking, HTTPS îți protejează datele. Site-urile fără HTTPS sunt marcate ca 'Not Secure'.",
        "quiz": {"question": "Ce indică lacătul verde în browser?",
                 "options": ["Conexiune securizată HTTPS", "Site-ul e rapid", "Site-ul are viruși",
                             "E nevoie de parolă"], "answer": "Conexiune securizată HTTPS"},
        "related": ["http", "ssl", "tls", "encryption", "certificate"]
    },

    "tcp": {
        "beginner": "TCP e ca un poștaș foarte atent. Nu doar că duce pachetele la destinație, dar verifică să ajungă TOATE și în ordinea corectă. Dacă unul se pierde, îl retrimite.",
        "professional": "TCP (Transmission Control Protocol) oferă comunicare fiabilă, orientată pe conexiune. Garantează livrarea pachetelor în ordine, fără erori, prin three-way handshake și acknowledgment.",
        "expert": "TCP: congestion control (Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery), flow control cu sliding window, segmentare și reassembly. TCP vs UDP: fiabilitate vs viteză.",
        "code": "# Client TCP simplu în Python\nimport socket\nclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\nclient.connect(('example.com', 80))\nclient.send(b'GET / HTTP/1.1\\r\\nHost: example.com\\r\\n\\r\\n')\nresponse = client.recv(4096)\nprint(response.decode())\nclient.close()",
        "real_world": "Când descarci un fișier, trimiți un email, sau încarci o pagină web, TCP se asigură că fiecare bucățică de date ajunge corect și completă.",
        "quiz": {"question": "TCP garantează...?",
                 "options": ["Livrare fiabilă în ordine", "Cea mai rapidă viteză", "Anonimitate", "Criptare automată"],
                 "answer": "Livrare fiabilă în ordine"},
        "related": ["ip", "http", "dns", "udp", "network"]
    },

    "ip address": {
        "beginner": "O adresă IP e ca adresa casei tale, dar pe internet. Când trimiți un pachet de date, adresa IP spune exact unde trebuie să ajungă — ca un GPS pentru informație.",
        "professional": "IP (Internet Protocol) adrese identifică unic fiecare dispozitiv pe o rețea. IPv4: 32 biți (4 miliarde adrese). IPv6: 128 biți (adrese practic nelimitate).",
        "expert": "IPv6: adrese hexazecimale pe 8 grupuri, elimină nevoia de NAT, suportă autoconfigurare (SLAAC), IPsec nativ. Subnetting, CIDR notation, private vs public IP ranges (RFC 1918).",
        "code": "# Verifică adresa IP publică și locală\nimport requests\nimport socket\npublic_ip = requests.get('https://api.ipify.org').text\nprint(f\"IP Public: {public_ip}\")\nlocal_ip = socket.gethostbyname(socket.gethostname())\nprint(f\"IP Local: {local_ip}\")",
        "real_world": "Fiecare dispozitiv conectat la internet are o adresă IP — laptopul tău, telefonul, serverele AEGIS. Poliția folosește IP-uri pentru a găsi infractori online.",
        "quiz": {"question": "Câte adrese are IPv6?",
                 "options": ["Practic nelimitate (2^128)", "4 miliarde", "1 milion", "65,000"],
                 "answer": "Practic nelimitate (2^128)"},
        "related": ["dns", "tcp", "http", "router", "network"]
    },

    "router": {
        "beginner": "Router-ul e ca un polițist de trafic pentru internetul din casa ta. Dirijează datele între dispozitivele tale și internet, asigurându-se că fiecare pachet ajunge unde trebuie.",
        "professional": "Un router direcționează pachetele de date între rețele, folosind tabele de rutare și protocoale ca OSPF, BGP. Router-ul de acasă combină funcții de routing, switch și access point Wi-Fi.",
        "expert": "Routing: static vs dynamic (RIP, OSPF, BGP), NAT/PAT pentru partajare IP public, port forwarding, QoS pentru prioritizare trafic, firewall integrat. MESH networking pentru acoperire extinsă.",
        "code": "# Verifică ruta către o destinație (traceroute)\nimport subprocess\nresult = subprocess.run(['tracert', 'google.com'], capture_output=True, text=True)\nprint(result.stdout)",
        "real_world": "Router-ul tău de acasă conectează laptopul, telefonul și televizorul la internet simultan. Router-ele enterprise dirijează traficul pentru companii întregi.",
        "quiz": {"question": "Ce face un router?",
                 "options": ["Direcționează traficul între rețele", "Stochează fișiere", "Rulează aplicații",
                             "Editează documente"], "answer": "Direcționează traficul între rețele"},
        "related": ["ip", "dns", "tcp", "wifi 7", "network"]
    },

    "ethernet": {
        "beginner": "Ethernet e ca o șosea pentru date în interiorul casei tale. Conectează laptopul, PC-ul și router-ul prin cabluri, oferind internet stabil și rapid.",
        "professional": "Ethernet (IEEE 802.3) este tehnologia standard pentru rețele locale (LAN) prin cablu. Viteze: de la 10 Mbps (Ethernet) până la 400 Gbps (400 Gigabit Ethernet).",
        "expert": "Ethernet standards: 10GBASE-T (cupru), 100GBASE-LR4 (fibră), PoE pentru alimentare prin cablu. Frame structure: preamble, MAC dest/src, EtherType, payload, FCS. Switching vs routing la Layer 2.",
        "code": "# Verifică adresa MAC a interfeței de rețea\nimport uuid\nmac = uuid.getnode()\nmac_address = ':'.join(f'{(mac >> 8*i) & 0xff:02x}' for i in range(5, -1, -1))\nprint(f\"Adresa MAC: {mac_address}\")",
        "real_world": "Când conectezi laptopul la router prin cablu, folosești Ethernet. E mai rapid și mai stabil decât Wi-Fi-ul. Toate centrele de date folosesc Ethernet pentru servere.",
        "quiz": {"question": "Ethernet este o tehnologie pentru...?",
                 "options": ["Rețele locale prin cablu", "Internet wireless", "Stocare de date", "Procesare AI"],
                 "answer": "Rețele locale prin cablu"},
        "related": ["router", "ip", "wifi 7", "lan", "network"]
    },

    "lan": {
        "beginner": "LAN-ul e ca o petrecere privată pentru dispozitivele din casa ta. Laptopul, telefonul și imprimanta vorbesc între ele prin LAN, fără să iasă pe internetul mare.",
        "professional": "LAN (Local Area Network) conectează dispozitive într-o zonă restrânsă (casă, birou). Folosește Ethernet și Wi-Fi, cu switch-uri și access point-uri pentru conectivitate.",
        "expert": "LAN topologii: star, mesh, bus. VLAN-uri pentru segmentare logică. Subnetting pentru organizare IP. Protocoale: ARP pentru rezolvare MAC, STP pentru prevenire bucle. 802.1X pentru autentificare de port.",
        "code": "# Scanează dispozitivele din LAN\nimport os\nnetwork = '192.168.1.'\nfor i in range(1, 255):\n    ip = network + str(i)\n    response = os.system(f'ping -n 1 -w 100 {ip}')\n    if response == 0:\n        print(f\"Dispozitiv găsit: {ip}\")",
        "real_world": "LAN-ul tău de acasă conectează toate dispozitivele la același router. Când trimiți un fișier de pe laptop pe telefon prin Wi-Fi, folosești LAN-ul.",
        "quiz": {"question": "Ce înseamnă LAN?",
                 "options": ["Local Area Network", "Large Access Node", "Limited Area Net",
                             "Long-range Antenna Network"], "answer": "Local Area Network"},
        "related": ["wan", "ethernet", "wifi 7", "router", "network"]
    },

    "wan": {
        "beginner": "WAN-ul e ca o autostradă care leagă orașe întregi. În timp ce LAN-ul e casa ta, WAN-ul e internetul întreg — conectează milioane de LAN-uri din toată lumea.",
        "professional": "WAN (Wide Area Network) acoperă arii geografice extinse, conectând LAN-uri prin routere și link-uri de telecomunicații. Internetul este cel mai mare WAN.",
        "expert": "WAN technologies: MPLS, SD-WAN, VPN site-to-site, leased lines, satelit. Protocoale: BGP pentru rutare inter-domenii, MPLS pentru traffic engineering. SD-WAN optimizează traficul pe multiple link-uri.",
        "code": "# Verifică latența către un server extern\nimport subprocess\nresult = subprocess.run(['ping', '-n', '4', 'google.com'], capture_output=True, text=True)\nprint(result.stdout)",
        "real_world": "Când accesezi un site din America sau Asia, datele călătoresc prin WAN. Companiile cu birouri în mai multe țări folosesc WAN pentru a conecta echipele.",
        "quiz": {"question": "Internetul este un exemplu de...?", "options": ["WAN", "LAN", "PAN", "MAN"],
                 "answer": "WAN"},
        "related": ["lan", "router", "ip", "dns", "network"]
    },

    "subnet mask": {
        "beginner": "Subnet mask e ca un separator care îți spune care parte din adresa IP e numele străzii și care e numărul casei. Ajută router-ul să știe unde să trimită datele.",
        "professional": "Subnet mask separă adresa IP în porțiunea de rețea și porțiunea de host. Notație: zecimală punctată (255.255.255.0) sau CIDR (/24).",
        "expert": "Subnetting: împărțirea unui spațiu IP în subrețele mai mici. VLSM (Variable Length Subnet Masking) pentru utilizare eficientă. Calcul: network address, broadcast address, usable hosts. Supernetting pentru agregare de rute.",
        "code": "# Calculează adresa de rețea dintr-un IP și subnet mask\nimport ipaddress\nip = ipaddress.IPv4Address('192.168.1.100')\nsubnet = ipaddress.IPv4Network('192.168.1.0/24', strict=False)\nprint(f\"Adresa IP: {ip}\")\nprint(f\"Rețea: {subnet.network_address}\")\nprint(f\"Broadcast: {subnet.broadcast_address}\")\nprint(f\"Host-uri utilizabile: {subnet.num_addresses - 2}\")",
        "real_world": "Administratorii de rețea folosesc subnet mask-uri pentru a organiza rețelele pe departamente. Acasă, router-ul tău folosește de obicei 255.255.255.0.",
        "quiz": {"question": "Ce înseamnă /24 în notație CIDR?",
                 "options": ["255.255.255.0", "255.0.0.0", "255.255.0.0", "255.255.255.255"],
                 "answer": "255.255.255.0"},
        "related": ["ip address", "router", "lan", "dns", "network"]
    },

    "mac address": {
        "beginner": "Adresa MAC e ca o amprentă digitală unică pentru fiecare dispozitiv. Niciun telefon, laptop sau imprimantă nu are aceeași adresă MAC — e înscrisă în hardware din fabrică.",
        "professional": "MAC (Media Access Control) address este un identificator unic de 48 de biți asignat interfeței de rețea. Format: șase perechi hexazecimale (00:1A:2B:3C:4D:5E).",
        "expert": "MAC: OUI (Organizationally Unique Identifier) — primii 24 biți identifică producătorul. MAC filtering pentru securitate, MAC spoofing pentru bypass. ARP (Address Resolution Protocol) leagă IP-ul de MAC.",
        "code": "# Obține adresa MAC a mașinii curente\nimport uuid\nmac = uuid.getnode()\nmac_address = ':'.join(f'{(mac >> 8*i) & 0xff:02x}' for i in range(5, -1, -1))\nprint(f\"Adresa MAC: {mac_address}\")",
        "real_world": "Când te conectezi la un Wi-Fi, router-ul îți înregistrează adresa MAC. Unele rețele folosesc MAC filtering pentru a permite doar dispozitivelor autorizate.",
        "quiz": {"question": "Adresa MAC are...?",
                 "options": ["48 biți (6 perechi hexa)", "32 biți (4 perechi)", "64 biți (8 perechi)",
                             "16 biți (2 perechi)"], "answer": "48 biți (6 perechi hexa)"},
        "related": ["ip address", "ethernet", "router", "lan", "network"]
    },

    "ssl": {
        "beginner": "SSL e ca un bodyguard care-ți păzește conversațiile pe internet. Când vezi lacătul în browser, SSL-ul lucrează să țină hackerii departe de datele tale.",
        "professional": "SSL (Secure Sockets Layer) și succesorul său TLS criptează comunicarea între browser și server. TLS 1.3 este standardul actual, oferind securitate pentru HTTPS.",
        "expert": "TLS 1.3: elimină algoritmi slabi (RC4, MD5), suportă doar forward secrecy, handshake redus la 1-RTT. Certificate X.509, PKI, chain of trust, certificate pinning, OCSP stapling.",
        "code": "# Verifică versiunea TLS a unui server\nimport ssl\nimport socket\nctx = ssl.create_default_context()\nwith ctx.wrap_socket(socket.socket(), server_hostname='google.com') as s:\n    s.connect(('google.com', 443))\n    print(f\"Versiune TLS: {s.version()}\")",
        "real_world": "Când faci cumpărături online, SSL/TLS îți criptează datele cardului. Orice site cu 'https://' și lacătul verde folosește această tehnologie.",
        "quiz": {"question": "Care este succesorul modern al SSL?",
                 "options": ["TLS (Transport Layer Security)", "SSH", "FTP", "HTTP"],
                 "answer": "TLS (Transport Layer Security)"},
        "related": ["https", "encryption", "certificate", "tls", "cybersecurity"]
    },

    "tls": {
        "beginner": "TLS e versiunea modernă a SSL-ului. E ca un scut invizibil care-ți protejează parolele, mesajele și plățile online de ochii curioșilor.",
        "professional": "TLS (Transport Layer Security) asigură confidențialitatea, integritatea și autentificarea în comunicațiile web. TLS 1.3 oferă securitate îmbunătățită față de versiunile anterioare.",
        "expert": "TLS 1.3: elimină suportul pentru ciphersuite-uri nesigure, impune Perfect Forward Secrecy, reduce latența handshake-ului. 0-RTT pentru reconectări rapide. Certificate Transparency pentru detectarea certificatelor malițioase.",
        "code": "# Testează suportul TLS al unui server\nimport subprocess\nresult = subprocess.run(['openssl', 's_client', '-connect', 'google.com:443', '-tls1_3'], capture_output=True, text=True)\nif 'CONNECTED' in result.stdout:\n    print(\"Serverul suportă TLS 1.3!\")\nelse:\n    print(\"Serverul nu suportă TLS 1.3\")",
        "real_world": "Băncile, magazinele online și rețelele sociale folosesc TLS să-ți protejeze datele. Fără TLS, oricine ar putea să-ți fure parolele pe Wi-Fi-ul public.",
        "quiz": {"question": "Ce oferă Perfect Forward Secrecy în TLS?",
                 "options": ["Chei de sesiune unice, neafectate de compromiterea cheii private", "Criptare mai rapidă",
                             "Compatibilitate cu dispozitive vechi", "Conexiune fără parolă"],
                 "answer": "Chei de sesiune unice, neafectate de compromiterea cheii private"},
        "related": ["ssl", "https", "encryption", "certificate", "cybersecurity"]
    },

    "certificate": {
        "beginner": "Un certificat digital e ca un pașaport pentru site-uri web. Demonstrează că site-ul este cine pretinde că e, nu un fals. E eliberat de autorități de încredere.",
        "professional": "Certificatele SSL/TLS (X.509) autentifică identitatea unui website și permit criptarea conexiunilor. Sunt emise de Certificate Authorities (CA) precum Let's Encrypt, DigiCert, Sectigo.",
        "expert": "Certificate: Domain Validation (DV), Organization Validation (OV), Extended Validation (EV). Chain of trust: root CA → intermediate CA → leaf certificate. Wildcard (*.domain.com), SAN (multi-domain). ACME protocol pentru automatizare (Let's Encrypt).",
        "code": "# Generează certificat self-signed (test)\nimport subprocess\nsubprocess.run([\n    'openssl', 'req', '-x509', '-newkey', 'rsa:4096',\n    '-keyout', 'key.pem', '-out', 'cert.pem',\n    '-days', '365', '-nodes',\n    '-subj', '/CN=localhost'\n])\nprint(\"Certificat self-signed generat!\")",
        "real_world": "Let's Encrypt oferă certificate SSL GRATUITE pentru milioane de site-uri. Înainte, certificatele costau sute de dolari pe an. Acum orice site poate fi securizat gratuit.",
        "quiz": {"question": "Ce organizație oferă certificate SSL gratuite?",
                 "options": ["Let's Encrypt", "Microsoft", "Google", "Amazon"], "answer": "Let's Encrypt"},
        "related": ["ssl", "tls", "https", "certificate authority", "encryption"]
    },

    "ssh": {
        "beginner": "SSH e ca o cheie magică ce-ți deschide ușa către servere de la distanță. Poți controla un computer din altă parte a lumii, în siguranță, prin criptare.",
        "professional": "SSH (Secure Shell) oferă acces terminal criptat la servere remote. Înlocuiește Telnet și FTP nesecurizate. Folosește autentificare prin parolă sau chei publice/private.",
        "expert": "SSH: key-based auth (RSA 4096, Ed25519), agent forwarding, port forwarding (local/remote/dynamic), SSH tunneling, config file (~/.ssh/config), multiplexing pentru conexiuni rapide, SSHFP DNS records.",
        "code": "# Conectare SSH cu Python\nimport paramiko\nclient = paramiko.SSHClient()\nclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())\nclient.connect('example.com', username='user', key_filename='/path/to/key')\nstdin, stdout, stderr = client.exec_command('ls -la')\nprint(stdout.read().decode())\nclient.close()",
        "real_world": "Administratorii de servere folosesc SSH zilnic. GitHub folosește SSH pentru push securizat de cod. Fără SSH, internetul ar fi mult mai nesigur.",
        "quiz": {"question": "SSH înlocuiește ce protocol nesecurizat?", "options": ["Telnet", "HTTPS", "FTP", "SMTP"],
                 "answer": "Telnet"},
        "related": ["encryption", "linux", "terminal", "ssl", "cybersecurity"]
    },

    "flask": {
        "beginner": "Flask e ca un set de piese LEGO pentru site-uri web în Python. E atât de simplu încât poți face un site funcțional în doar 5 linii de cod.",
        "professional": "Flask este un micro-framework Python pentru aplicații web, oferind routing, template-uri Jinja2 și suport pentru extensii. Ideal pentru API-uri și aplicații mici până la medii.",
        "expert": "Flask: application factory pattern, blueprints pentru modularizare, context locals (request, session, g), before/after request hooks, error handlers. Extensii: Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-CORS.",
        "code": "from flask import Flask, jsonify\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return jsonify({'message': 'Salut, Andrei!', 'project': 'AEGIS'})\n\nif __name__ == '__main__':\n    app.run(debug=True, port=5000)",
        "real_world": "Pinterest, LinkedIn și Reddit au folosit Flask la început. E perfect pentru prototipuri rapide și API-uri. AEGIS ar putea avea un backend Flask!",
        "quiz": {"question": "Flask este un framework pentru...?", "options": ["Python", "JavaScript", "Ruby", "PHP"],
                 "answer": "Python"},
        "related": ["python", "django", "api rest", "json", "fastapi"]
    },

    "django": {
        "beginner": "Django e ca un supermarket complet pentru site-uri web. Vine cu TOT inclus — autentificare, bază de date, panou admin. E framework-ul Python preferat pentru proiecte mari.",
        "professional": "Django este un framework Python full-stack, urmând principiul 'batteries included'. Oferă ORM, admin panel, autentificare, formulare și securitate încorporată.",
        "expert": "Django: MTV architecture (Model-Template-View), QuerySet lazy evaluation, middleware stack, class-based views, Django REST Framework pentru API-uri. Migrații automate de schemă. Suport pentru PostgreSQL, MySQL, SQLite.",
        "code": "# Django: views.py\nfrom django.http import JsonResponse\n\ndef home(request):\n    return JsonResponse({\n        'message': 'Salut, Andrei!',\n        'project': 'AEGIS',\n        'framework': 'Django'\n    })",
        "real_world": "Instagram, Spotify, YouTube și NASA folosesc Django. E alegerea #1 pentru startup-uri care vor să construiască rapid aplicații web complexe și sigure.",
        "quiz": {"question": "Django urmează principiul...?",
                 "options": ["Batteries included (totul inclus)", "Micro-framework minimalist", "Doar frontend",
                             "Doar pentru mobile"], "answer": "Batteries included (totul inclus)"},
        "related": ["python", "flask", "sql", "orm", "fastapi"]
    },

    "fastapi": {
        "beginner": "FastAPI e ca Flask, dar pe steroizi. E cel mai rapid framework Python pentru API-uri și vine cu documentație automată. Scrii codul și primești un site de testare GRATIS.",
        "professional": "FastAPI este un framework Python modern pentru API-uri, folosind type hints și async/await. Oferă validare automată, documentație OpenAPI și performanță comparabilă cu Node.js.",
        "expert": "FastAPI: Pydantic pentru validare, Starlette pentru performanță asincronă, dependency injection, background tasks, WebSocket support. Generare automată de OpenAPI/Swagger docs. Testare cu TestClient.",
        "code": "from fastapi import FastAPI\napp = FastAPI(title='AEGIS API', version='1.0')\n\n@app.get('/')\nasync def home():\n    return {'message': 'Salut, Andrei!', 'project': 'AEGIS'}\n\n@app.get('/terms/{term_id}')\nasync def get_term(term_id: str):\n    return {'term': term_id, 'definition': 'Coming soon...'}",
        "real_world": "Netflix, Uber și Microsoft folosesc FastAPI pentru API-uri rapide. E framework-ul Python cu cea mai rapidă creștere. Perfect pentru un API AEGIS în viitor!",
        "quiz": {"question": "FastAPI generează automat...?",
                 "options": ["Documentație OpenAPI/Swagger", "Aplicații mobile", "Jocuri video", "Editoare de text"],
                 "answer": "Documentație OpenAPI/Swagger"},
        "related": ["python", "flask", "django", "api rest", "json"]
    },

    "pandas": {
        "beginner": "Pandas e ca un Excel ultra-inteligent pentru programatori. Analizezi date, faci grafice, filtrezi informații — totul în câteva linii de cod Python.",
        "professional": "Pandas este o bibliotecă Python pentru manipularea și analiza datelor, oferind structuri DataFrame și Series pentru date tabulare și time series.",
        "expert": "Pandas: vectorized operations, groupby aggregation, merge/join/concat, pivot tables, handling missing data, multi-index, datetime operations. Integrare cu NumPy, Matplotlib, Scikit-learn. Performanță prin Cython backend.",
        "code": "import pandas as pd\n\ndata = {\n    'nume': ['Andrei', 'Ana', 'Maria'],\n    'varsta': [15, 17, 14],\n    'proiect': ['AEGIS', 'Design', 'Web']\n}\ndf = pd.DataFrame(data)\nprint(df.describe())\nprint(f\"Vârsta medie: {df['varsta'].mean():.1f} ani\")",
        "real_world": "Toate companiile mari — Google, Facebook, Goldman Sachs — folosesc Pandas pentru analiză de date. E folosit în știință, finanțe, marketing și sport.",
        "quiz": {"question": "Care e structura principală de date în Pandas?",
                 "options": ["DataFrame", "Array", "List", "Dictionary"], "answer": "DataFrame"},
        "related": ["python", "numpy", "matplotlib", "data science", "machine learning"]
    },

    "numpy": {
        "beginner": "NumPy e ca un calculator științific ultra-rapid pentru Python. Face calcule matematice complexe în milisecunde — matrice, vectori, statistică.",
        "professional": "NumPy este fundamentul științei datelor în Python, oferind array-uri N-dimensionale și funcții matematice optimizate în C pentru performanță.",
        "expert": "NumPy: ndarray cu broadcasting, vectorization, slicing avansat, fancy indexing, universal functions (ufuncs), linear algebra (numpy.linalg), random sampling, FFT. Integrare cu C prin ctypes și Cython.",
        "code": "import numpy as np\n\narr = np.array([1, 2, 3, 4, 5])\nprint(f\"Medie: {np.mean(arr)}\")\nprint(f\"Deviație standard: {np.std(arr):.2f}\")\nprint(f\"Maxim: {np.max(arr)}, Minim: {np.min(arr)}\")\n\n# Operații pe matrice\nmatrix = np.array([[1, 2], [3, 4]])\nprint(f\"Determinant: {np.linalg.det(matrix):.0f}\")",
        "real_world": "NASA, CERN și toate companiile de AI folosesc NumPy. E biblioteca #1 pentru calcule științifice în Python. Toate framework-urile de ML (TensorFlow, PyTorch) se bazează pe concepte NumPy.",
        "quiz": {"question": "NumPy optimizează calculele prin...?",
                 "options": ["Vectorizare și cod C", "JavaScript în browser", "CSS și HTML", "Machine learning"],
                 "answer": "Vectorizare și cod C"},
        "related": ["python", "pandas", "matplotlib", "data science", "scikit-learn"]
    },

    "tensorflow": {
        "beginner": "TensorFlow e ca o fabrică de inteligență artificială creată de Google. Construiești modele AI care recunosc poze, traduc limbi și prezic viitorul — totul cu cod Python.",
        "professional": "TensorFlow este un framework open-source de la Google pentru machine learning și deep learning. Oferă Keras API pentru construirea rapidă de rețele neuronale.",
        "expert": "TensorFlow: static și dynamic graphs (Eager Execution), TensorBoard pentru vizualizare, TF Serving pentru deployment, TF Lite pentru mobile/IoT, distribuție pe GPU/TPU, mixed precision training.",
        "code": "import tensorflow as tf\nfrom tensorflow.keras.models import Sequential\nfrom tensorflow.keras.layers import Dense\n\nmodel = Sequential([\n    Dense(128, activation='relu', input_shape=(784,)),\n    Dense(64, activation='relu'),\n    Dense(10, activation='softmax')\n])\nmodel.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])\nprint(\"Model TensorFlow creat cu succes!\")",
        "real_world": "Google Translate, Google Photos și YouTube recomandări folosesc TensorFlow. E folosit de Airbnb, Uber, Twitter și mii de companii pentru AI.",
        "quiz": {"question": "Cine a creat TensorFlow?", "options": ["Google", "Facebook", "Microsoft", "Apple"],
                 "answer": "Google"},
        "related": ["pytorch", "keras", "deep learning", "machine learning", "ai"]
    },

    "pytorch": {
        "beginner": "PyTorch e ca un atelier de construit inteligență artificială creat de Facebook. E mai flexibil decât TensorFlow și preferat de cercetători pentru experimente rapide.",
        "professional": "PyTorch este un framework open-source de machine learning dezvoltat de Meta (Facebook). Oferă dynamic computation graphs și este lider în cercetarea AI.",
        "expert": "PyTorch: autograd pentru diferențiere automată, TorchScript pentru producție, distributed training (DDP, FSDP), mixed precision cu torch.cuda.amp, ONNX export. Domină conferințele AI (NeurIPS, ICML).",
        "code": "import torch\nimport torch.nn as nn\n\nmodel = nn.Sequential(\n    nn.Linear(784, 128),\n    nn.ReLU(),\n    nn.Linear(128, 10),\n    nn.Softmax(dim=1)\n)\nprint(f\"Model PyTorch creat cu {sum(p.numel() for p in model.parameters())} parametri\")",
        "real_world": "Tesla folosește PyTorch pentru mașinile autonome. OpenAI a folosit PyTorch pentru a antrena modelele GPT. E framework-ul #1 în cercetarea AI.",
        "quiz": {"question": "Cine a creat PyTorch?", "options": ["Meta (Facebook)", "Google", "Microsoft", "Amazon"],
                 "answer": "Meta (Facebook)"},
        "related": ["tensorflow", "deep learning", "machine learning", "ai", "python"]
    },

    "scikit-learn": {
        "beginner": "Scikit-learn e ca o cutie de instrumente gata-făcute pentru machine learning. Ai nevoie de un algoritm? E deja acolo. Importi, antrenezi, folosești — în 3 linii de cod.",
        "professional": "Scikit-learn este o bibliotecă Python pentru machine learning clasic, oferind algoritmi pentru clasificare, regresie, clustering și preprocessing.",
        "expert": "Scikit-learn: Pipeline API pentru workflows, cross-validation (KFold, Stratified), GridSearchCV/RandomizedSearchCV pentru hyperparameter tuning, feature engineering (OneHotEncoder, StandardScaler), metrics comprehensive.",
        "code": "from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\nmodel = RandomForestClassifier(n_estimators=100)\nmodel.fit(X_train, y_train)\nprint(f\"Acuratețe: {accuracy_score(y_test, model.predict(X_test)):.2%}\")",
        "real_world": "Spotify folosește Scikit-learn pentru recomandări muzicale. Băncile îl folosesc pentru detectarea fraudelor. E biblioteca #1 pentru ML clasic în Python.",
        "quiz": {"question": "Scikit-learn e folosit pentru...?",
                 "options": ["Machine Learning clasic", "Deep Learning", "Web Development", "Mobile Apps"],
                 "answer": "Machine Learning clasic"},
        "related": ["python", "pandas", "numpy", "machine learning", "tensorflow"]
    },

    "jupyter": {
        "beginner": "Jupyter e ca un caiet de laborator digital. Scrii cod, vezi rezultatele imediat, adaugi notițe și grafice — totul într-un singur loc. Perfect pentru experimente și învățare.",
        "professional": "Jupyter Notebook este o aplicație web interactivă pentru crearea și partajarea documentelor cu cod live, ecuații, vizualizări și text narativ.",
        "expert": "Jupyter: kernel-uri multiple (Python, R, Julia), magics (%timeit, %%bash), widget-uri interactive, JupyterLab ca IDE complet, nbconvert pentru export (PDF, HTML, slides). Voilà pentru dashboard-uri.",
        "code": "# Într-un notebook Jupyter:\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.linspace(0, 10, 100)\ny = np.sin(x)\nplt.plot(x, y)\nplt.title('Grafic creat în Jupyter')\nplt.show()",
        "real_world": "Data scientists la Google, Netflix și NASA folosesc Jupyter zilnic. E tool-ul standard pentru analiză de date, cercetare AI și tutoriale de programare.",
        "quiz": {"question": "Jupyter suportă doar Python?",
                 "options": ["Nu — suportă R, Julia și altele", "Da, doar Python", "Doar JavaScript", "Doar Java"],
                 "answer": "Nu — suportă R, Julia și altele"},
        "related": ["python", "pandas", "matplotlib", "data science", "anaconda"]
    },

    "matplotlib": {
        "beginner": "Matplotlib e ca un pictor pentru datele tale. Transformă numerele în grafice frumoase — linii, bare, puncte. E cel mai vechi și mai folosit tool de vizualizare din Python.",
        "professional": "Matplotlib este o bibliotecă Python pentru crearea de vizualizări statice, animate și interactive. Oferă control complet asupra fiecărui element al graficului.",
        "expert": "Matplotlib: Figure și Axes architecture, subplots, custom styling (rcParams), backends (Agg, TkAgg, interactive), animații (FuncAnimation), integrare cu Pandas și Seaborn.",
        "code": "import matplotlib.pyplot as plt\n\nluni = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai']\ntermeni_aegis = [51, 380, 785, 1010, 1430]\n\nplt.figure(figsize=(10, 6))\nplt.plot(luni, termeni_aegis, marker='o', color='#00ffcc', linewidth=2)\nplt.title('Creșterea AEGIS', fontsize=16)\nplt.xlabel('Luna')\nplt.ylabel('Număr de termeni')\nplt.grid(True, alpha=0.3)\nplt.show()",
        "real_world": "Toate publicațiile științifice folosesc Matplotlib pentru grafice. NASA îl folosește pentru vizualizarea datelor spațiale. E fundamentul vizualizării în Python.",
        "quiz": {"question": "Matplotlib este o bibliotecă pentru...?",
                 "options": ["Vizualizare de date", "Machine Learning", "Web Development", "Baze de date"],
                 "answer": "Vizualizare de date"},
        "related": ["python", "numpy", "pandas", "seaborn", "data science"]
    },

    "seaborn": {
        "beginner": "Seaborn e ca un designer de modă pentru grafice. Ia Matplotlib-ul de bază și îl face SUPERB — culori frumoase, stiluri elegante, totul automat.",
        "professional": "Seaborn este o bibliotecă Python de vizualizare statistică, construită peste Matplotlib. Oferă interfețe simplificate pentru grafice statistice complexe.",
        "expert": "Seaborn: heatmaps, pairplots, violin plots, swarm plots, facet grids pentru vizualizări multi-dimensionale. Integrare nativă cu Pandas DataFrames. Teme built-in (darkgrid, whitegrid, ticks).",
        "code": "import seaborn as sns\nimport pandas as pd\n\ndata = pd.DataFrame({\n    'nivel': ['Începător', 'Profesionist', 'Expert'] * 5,\n    'scor': [85, 72, 95, 78, 88, 92, 90, 85, 98, 82, 79, 91, 87, 93, 96]\n})\nsns.barplot(data=data, x='nivel', y='scor', palette='viridis')\nplt.title('Performanță AEGIS pe nivele')\nplt.show()",
        "real_world": "Cercetătorii în științe sociale și biologie folosesc Seaborn pentru analize statistice vizuale. E standardul pentru grafice științifice elegante.",
        "quiz": {"question": "Seaborn e construit peste...?",
                 "options": ["Matplotlib", "NumPy", "Pandas", "Scikit-learn"], "answer": "Matplotlib"},
        "related": ["matplotlib", "pandas", "python", "data science", "numpy"]
    },

    "opencv": {
        "beginner": "OpenCV e ca un ochi magic pentru computer. Îl învață să vadă și să înțeleagă poze și video — recunoaște fețe, obiecte, mișcare.",
        "professional": "OpenCV (Open Source Computer Vision Library) este o bibliotecă open-source pentru computer vision și procesare de imagini, cu peste 2500 de algoritmi optimizați.",
        "expert": "OpenCV: image processing (filtre, morphing, thresholding), feature detection (SIFT, ORB, FAST), object detection (Haar cascades, DNN module), camera calibration, video analysis, integrare CUDA pentru GPU.",
        "code": "import cv2\nimport numpy as np\n\n# Citește o imagine și aplică detecție de margini\nimg = cv2.imread('poza.jpg')\nedges = cv2.Canny(img, 100, 200)\ncv2.imshow('Margini detectate', edges)\ncv2.waitKey(0)\ncv2.destroyAllWindows()",
        "real_world": "Tesla folosește OpenCV pentru mașini autonome. Instagram și Snapchat pentru filtre faciale. Sistemele de securitate pentru recunoaștere facială.",
        "quiz": {"question": "OpenCV e specializat în...?",
                 "options": ["Computer Vision", "Web Development", "Baze de date", "Blockchain"],
                 "answer": "Computer Vision"},
        "related": ["python", "deep learning", "ai", "computer vision", "tensorflow"]
    },

    "git": {
        "beginner": "Git e ca un jurnal magic pentru codul tău. Salvează fiecare schimbare și poți să te întorci oricând la o versiune anterioară. E ca un 'undo' infinit și puternic.",
        "professional": "Git este un sistem de versionare distribuit care urmărește modificările în codul sursă. Concepte fundamentale: commit, branch, merge, rebase, remote.",
        "expert": "Git avansat: interactive rebase, cherry-pick, bisect pentru debugging, hooks (pre-commit, post-receive), submodules, worktrees, reflog pentru recuperare. GitFlow și trunk-based development workflows.",
        "code": "# Git workflow zilnic\ngit status                    # Vezi ce ai modificat\ngit add .                     # Adaugă toate schimbările\ngit commit -m \"+420 termeni\"  # Salvează local\ngit push origin main          # Trimite pe GitHub\ngit log --oneline -5          # Vezi ultimele 5 commit-uri",
        "real_world": "AEGIS e pe Git chiar acum. Linux kernel-ul (cel mai mare proiect open-source) folosește Git. Toate companiile tech — Google, Microsoft, Apple — folosesc Git.",
        "quiz": {"question": "Ce comandă Git trimite codul pe server?",
                 "options": ["git push", "git send", "git upload", "git deploy"], "answer": "git push"},
        "related": ["github", "github actions", "devops", "version control", "ci/cd"]
    },

    "github actions": {
        "beginner": "GitHub Actions e ca un robot-asistent care lucrează pentru tine. De fiecare dată când pui cod nou pe GitHub, robotul îl testează automat și îți spune dacă e totul bine.",
        "professional": "GitHub Actions este o platformă CI/CD integrată în GitHub pentru automatizarea workflow-urilor: testare, build, deployment direct din repository.",
        "expert": "GitHub Actions: YAML workflows, events triggers (push, pull_request, schedule), matrix builds pentru testare multiplatformă, secrets management, self-hosted runners, marketplace cu acțiuni comunitare.",
        "code": "# .github/workflows/test.yml\nname: Test AEGIS\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - uses: actions/setup-python@v4\n        with:\n          python-version: '3.11'\n      - run: pip install -r requirements.txt\n      - run: python -m pytest tests/",
        "real_world": "AEGIS poate folosi GitHub Actions pentru a testa automat codul la fiecare push. Facebook, Google și mii de proiecte open-source îl folosesc zilnic.",
        "quiz": {"question": "GitHub Actions este un tool de...?",
                 "options": ["CI/CD — Integrare și Deployment Continuu", "Design grafic", "Editare video",
                             "Baze de date"], "answer": "CI/CD — Integrare și Deployment Continuu"},
        "related": ["github", "git", "devops", "ci/cd", "docker"]
    },

    "ci/cd": {
        "beginner": "CI/CD e ca o bandă rulantă magică pentru cod. Scrii codul, iar banda îl testează automat și îl pune pe internet. Fără muncă manuală, fără stres, fără erori.",
        "professional": "CI/CD (Continuous Integration / Continuous Delivery) automatizează testarea și deployment-ul codului, permițând livrări rapide și sigure în producție.",
        "expert": "CI/CD pipeline: build → test → stage → deploy. Tools: GitHub Actions, Jenkins, GitLab CI, CircleCI. Strategii: blue-green deployment, canary releases, feature flags. Infrastructure as Code pentru medii consistente.",
        "code": "# Exemplu: Pipeline CI/CD simplu\n# 1. Developer push-uiește codul\n# 2. CI: Build + Test automat\n# 3. CD: Deploy pe staging\n# 4. Aprobare manuală (opțional)\n# 5. CD: Deploy pe producție\nprint(\"AEGIS deployed successfully!\")",
        "real_world": "Netflix deploy-ează de mii de ori pe zi folosind CI/CD. Amazon face deploy la fiecare secundă. CI/CD e standardul în industrie pentru livrare rapidă și sigură.",
        "quiz": {"question": "Ce înseamnă CD în CI/CD?",
                 "options": ["Continuous Delivery/Deployment", "Code Development", "Computer Design", "Cloud Database"],
                 "answer": "Continuous Delivery/Deployment"},
        "related": ["github actions", "devops", "git", "docker", "jenkins"]
    },

    "devops": {
        "beginner": "DevOps e ca o punte între programatori și administratorii de servere. În loc să se certe, lucrează împreună să livreze cod mai repede și mai sigur.",
        "professional": "DevOps este o cultură și set de practici care unifică development-ul (Dev) și operațiunile (Ops), automatizând întregul ciclu de viață al aplicațiilor.",
        "expert": "DevOps practices: CI/CD, Infrastructure as Code (Terraform, Ansible), monitoring (Prometheus, Grafana), logging (ELK stack), containerization (Docker, Kubernetes). CALMS framework: Culture, Automation, Lean, Measurement, Sharing.",
        "code": "# DevOps: Monitorizare simplă cu Prometheus\nfrom prometheus_client import start_http_server, Counter\n\nrequests_total = Counter('aegis_requests_total', 'Total requests to AEGIS')\nrequests_total.inc()\nstart_http_server(8000)\nprint(\"Metrics available at http://localhost:8000\")",
        "real_world": "Amazon, Netflix și Etsy au revoluționat DevOps. Companiile care adoptă DevOps deploy-ează de 200x mai frecvent și recuperează din incidente de 24x mai rapid.",
        "quiz": {"question": "DevOps unește...?",
                 "options": ["Development și Operations", "Design și Operations", "Development și Optimization",
                             "Database și Operations"], "answer": "Development și Operations"},
        "related": ["ci/cd", "docker", "kubernetes", "github actions", "terraform"]
    },


    "graphql": {
        "beginner": "GraphQL e ca un restaurant unde comanzi EXACT ce vrei, nici mai mult, nici mai puțin. În loc să primești un platou fix (ca la REST), tu scrii ce câmpuri vrei și le primești fix pe acelea.",
        "professional": "GraphQL este un limbaj de interogare pentru API-uri care permite clientului să solicite exact datele de care are nevoie. Folosește un singur endpoint și un sistem de tipuri puternic definit.",
        "expert": "GraphQL: schema definită cu tipuri, query-uri, mutații și subscription-uri. Resolvere, batching și caching cu DataLoader. Apollo Client/Server, Federation pentru microservicii. Persisted queries, security (depth limiting, rate limiting).",
        "code": "# Query GraphQL\nquery {\n  user(id: \"1\") {\n    name\n    email\n    posts {\n      title\n    }\n  }\n}",
        "real_world": "GitHub, Facebook, Shopify și multe altele folosesc GraphQL. În loc să faci 5 cereri REST, faci una singură și primești exact ce ai nevoie.",
        "quiz": {"question": "GraphQL este alternativă la...?", "options": ["REST API", "SOAP", "gRPC", "WebSockets"],
                 "answer": "REST API"},
        "related": ["api rest", "apollo", "federation", "graphql client", "schema"]
    },

    "redis": {
        "beginner": "Redis e ca o memorie ultra-rapidă care ține minte date între sesiuni. Dacă un site e încet, Redis accelerează lucrurile stocând rezultatele în cache.",
        "professional": "Redis este un magazin de structuri de date în-memory, folosit ca cache, message broker și bază de date NoSQL. Suportă string-uri, hash-uri, liste, set-uri, hyperloglogs, stream-uri.",
        "expert": "Redis: persistare RDB/AOF, replicare master-slave, cluster, sentinel pentru HA. Operații atomice, Lua scripting, pub/sub. RedisJSON, RedisSearch, RedisTimeSeries ca module. Pipeline și tranzacții.",
        "code": "# Redis cu Python (redis-py)\nimport redis\nr = redis.Redis(host='localhost', port=6379, db=0)\nr.set('user:1', 'Andrei')\nprint(r.get('user:1'))",
        "real_world": "Twitter, GitHub, Stack Overflow folosesc Redis pentru cache. De asemenea, stochează sesiuni de utilizator, cozi de mesaje, și contoare în timp real.",
        "quiz": {"question": "Redis stochează date în...?",
                 "options": ["memorie (RAM)", "disc dur", "bandă magnetică", "nor"], "answer": "memorie (RAM)"},
        "related": ["cache", "database", "message queue", "pub/sub", "memcached"]
    },

    "kafka": {
        "beginner": "Kafka e ca o bandă rulantă de mesaje între aplicații. O aplicație pune mesaje la un capăt, alta le ia de la celălalt. Poate gestiona milioane de mesaje pe secundă.",
        "professional": "Apache Kafka este o platformă distribuită de streaming de evenimente. Folosește topic-uri, producători, consumatori, brokeri. Oferă durabilitate, scalabilitate și ordonare.",
        "expert": "Kafka: partiționare, replicare, offset management, exactly-once semantics, Kafka Streams, ksqlDB, Connect pentru integrare. ZooKeeper sau KRaft pentru consens. Raft în noile versiuni.",
        "code": "# Producător Kafka simplu (Python)\nfrom kafka import KafkaProducer\nproducer = KafkaProducer(bootstrap_servers='localhost:9092')\nproducer.send('topic-test', b'Mesaj de la AEGIS')\nproducer.flush()",
        "real_world": "LinkedIn, Netflix, Uber folosesc Kafka pentru procesare în timp real. De exemplu, când livrezi mâncare, Kafka transmite comanda între sisteme.",
        "quiz": {"question": "Kafka este specializat în...?",
                 "options": ["streaming de evenimente", "stocare de fișiere", "baze de date SQL", "machine learning"],
                 "answer": "streaming de evenimente"},
        "related": ["message queue", "streaming", "zookeeper", "event sourcing", "pub/sub"]
    },

    "elasticsearch": {
        "beginner": "Elasticsearch e ca Google pentru datele tale. Cauți ceva în aplicație și găsești instant, chiar și în milioane de documente. E perfect pentru căutare și analiză rapidă.",
        "professional": "Elasticsearch este un motor de căutare și analiză distribuit, bazat pe Lucene. Suportă text complet, agregări, geo-search, și este parte din stack-ul ELK.",
        "expert": "Elasticsearch: cluster, noduri, shard-uri, replica-uri. Query DSL, bool queries, aggregations buckets/metrics, mapping, analizoare (stemming, tokenizare). Ingest pipelines, rollups, ILM. Securitate și audit.",
        "code": "# Căutare în Elasticsearch (Python)\nfrom elasticsearch import Elasticsearch\nes = Elasticsearch(['http://localhost:9200'])\nres = es.search(index='articole', body={'query': {'match': {'titlu': 'AEGIS'}}})\nprint(res['hits']['hits'])",
        "real_world": "Wikipedia, GitHub, eBay folosesc Elasticsearch pentru căutare. Este și baza pentru logging centralizat (ELK: Elasticsearch, Logstash, Kibana).",
        "quiz": {"question": "Elasticsearch este bazat pe...?", "options": ["Lucene", "MySQL", "MongoDB", "Redis"],
                 "answer": "Lucene"},
        "related": ["kibana", "logstash", "elk", "search", "lucene"]
    },

    "prometheus": {
        "beginner": "Prometheus e ca un monitor care urmărește sănătatea aplicațiilor. Colectează metrici (câte cereri, cât timp, erori) și te alertează când ceva nu merge bine.",
        "professional": "Prometheus este un sistem open-source de monitorizare și alertare, cu model pull-based, metrici multi-dimensionale, și limbaj de interogare PromQL.",
        "expert": "Prometheus: exposition metrics (client libraries), exporters, service discovery, TSDB, recording rules, Alertmanager. Integrare cu Grafana. Federation. Pushgateway pentru job-uri scurte.",
        "code": "# Exporter simplu Python\nfrom prometheus_client import start_http_server, Counter\nc = Counter('requests_total', 'Total requests')\nc.inc()\nstart_http_server(8000)",
        "real_world": "Kubernetes folosește Prometheus implicit pentru monitorizare. Multe companii monitorizează microserviciile cu Prometheus + Grafana.",
        "quiz": {"question": "Prometheus folosește modelul...?",
                 "options": ["pull (trage metrici)", "push (împinge metrici)", "batch", "real-time push"],
                 "answer": "pull (trage metrici)"},
        "related": ["grafana", "alertmanager", "metrics", "monitoring", "kubernetes"]
    },

    "grafana": {
        "beginner": "Grafana e ca un tablou de bord superb pentru datele tale. Ia metrici din Prometheus, Elasticsearch și le arată în grafice colorate, ușor de citit.",
        "professional": "Grafana este o platformă open-source pentru vizualizare și analiză de metrici. Suportă multiple surse de date (Prometheus, Loki, Elasticsearch, InfluxDB, MySQL).",
        "expert": "Grafana: dashboard-uri, panel-uri, variabile, alertare, anotări, plugin-uri, provisionare (as code). Integrare cu Loki pentru loguri, Tempo pentru trace-uri. SSO și permisiuni RBAC.",
        "code": "# Configurare sursă de date în Grafana (JSON)\n{\n  \"name\": \"Prometheus\",\n  \"type\": \"prometheus\",\n  \"url\": \"http://prometheus:9090\",\n  \"access\": \"proxy\"\n}",
        "real_world": "Grafana este folosit de companii ca PayPal, Bloomberg, eBay pentru a monitoriza sănătatea sistemelor și a afișa KPI-uri executive.",
        "quiz": {"question": "Grafana este folosit pentru...?",
                 "options": ["vizualizare metrici", "bază de date", "server web", "compilator"],
                 "answer": "vizualizare metrici"},
        "related": ["prometheus", "loki", "dashboard", "monitoring", "timeseries"]
    },

    "terraform": {
        "beginner": "Terraform e ca un arhitect care desenează toată infrastructura IT ca pe un plan. Cu câteva linii de cod, creezi servere, baze de date, rețele — totul la comandă.",
        "professional": "Terraform este un tool Infrastructure as Code (IaC) de la HashiCorp, care folosește limbaj declarativ HCL pentru a provisiona resurse în cloud și on-premise.",
        "expert": "Terraform: state management (local/remote), modules, providers (AWS, Azure, GCP), workspaces, import. Terragrunt pentru orchestrare. Plan/apply/destroy. Sentinel pentru policy as code.",
        "code": "# Exemplu Terraform (AWS instance)\nresource \"aws_instance\" \"aegis\" {\n  ami           = \"ami-0c55b159cbfafe1f0\"\n  instance_type = \"t2.micro\"\n  tags = { Name = \"AEGIS-Server\" }\n}",
        "real_world": "Netflix, Airbnb, Uber își gestionează infrastructura cu Terraform. În loc să configurezi manual servere, scrii cod și Terraform le creează pe toate.",
        "quiz": {"question": "Terraform este un tool de...?",
                 "options": ["Infrastructure as Code", "CI/CD", "Containerizare", "Machine Learning"],
                 "answer": "Infrastructure as Code"},
        "related": ["aws", "hcl", "state", "pulumi", "openstack"]
    },

    "ansible": {
        "beginner": "Ansible e ca un robot care configurează automat servere. Vrei să instalezi același soft pe 100 de servere? Ansible face asta în câteva minute.",
        "professional": "Ansible este un automation engine agentless, folosind SSH pentru a rula playbook-uri scrise în YAML. Folosit pentru configurare, deploy, orchestră.",
        "expert": "Ansible: inventory, modules, playbooks, roles, ansible-vault pentru secrete, facts, handlers, tags. Tower/AWX pentru UI și orchestră avansată. Plugins de conexiune și inventar.",
        "code": "# Playbook Ansible pentru instalare nginx\n- hosts: webservers\n  tasks:\n    - name: Install nginx\n      apt:\n        name: nginx\n        state: present",
        "real_world": "Red Hat, NASA, Evernote folosesc Ansible. Este simplu și nu necesită agenți pe servere, doar SSH.",
        "quiz": {"question": "Ansible este un tool de...?",
                 "options": ["automatizare configurare", "bază de date", "server web", "design grafic"],
                 "answer": "automatizare configurare"},
        "related": ["devops", "automation", "ssh", "yaml", "terraform"]
    },

    "rust": {
        "beginner": "Rust e un limbaj de programare care e și rapid ca C++, și sigur ca Python. Nu se blochează, nu are erori de memorie, și e iubit de programatori.",
        "professional": "Rust este un limbaj de programare sistem care garantează siguranța memoriei fără garbage collector. Folosește ownership, borrowing, lifetimes. Performanță similară C++.",
        "expert": "Rust: cargo (build system), crates, pattern matching, trait-uri, async/await, FFI cu C, WebAssembly. Zero-cost abstractions, fearless concurrency. Folosit în sisteme critice.",
        "code": "fn main() {\n    let name = \"Andrei\";\n    println!(\"Salut, {}!\", name);\n}",
        "real_world": "Firefox, Dropbox, Cloudflare folosesc Rust. De asemenea, Deno (runtime JS) e scris în Rust. Este cel mai iubit limbaj în sondaje de 8 ani consecutiv.",
        "quiz": {"question": "Rust garantează...?",
                 "options": ["siguranța memoriei", "viteză mică", "garbage collector", "interpretare"],
                 "answer": "siguranța memoriei"},
        "related": ["cargo", "systems programming", "memory safety", "c++", "webassembly"]
    },

    "webassembly": {
        "beginner": "WebAssembly (WASM) e ca un super-putere pentru browser. Cod scris în C++, Rust, Go rulează aproape la fel de repede ca nativ în pagină web.",
        "professional": "WebAssembly este un format de instrucțiuni binare portabil, care rulează în browser la viteză aproape nativă. Permite utilizarea de cod scris în limbaje low-level în web.",
        "expert": "WASM: stack-based VM, liniară memorie, modul, import/export funcții. Compilare din C/C++ (Emscripten), Rust (wasm-pack), Go, AssemblyScript. WASI (System Interface) pentru outside browser.",
        "code": "// Exemplu WASM în Rust (export)\n#[no_mangle]\npub extern \"C\" fn add(a: i32, b: i32) -> i32 {\n    a + b\n}",
        "real_world": "Google Earth, Figma, Photoshop Web rulează WebAssembly pentru performanță mare în browser. De asemenea, jocuri și aplicații video.",
        "quiz": {"question": "WebAssembly rulează în...?",
                 "options": ["browser", "server", "bază de date", "sistem de operare"], "answer": "browser"},
        "related": ["rust", "c++", "javascript", "wasm", "web performance"]
    },

    "grpc": {
        "beginner": "gRPC e ca un curier ultra-rapid între microservicii. Folosește Protocol Buffers (un format comprimat) și HTTP/2 pentru viteză și streaming.",
        "professional": "gRPC este un framework RPC open-source de la Google, bazat pe HTTP/2 și Protocol Buffers. Suportă streaming bidirecțional, autentificare, și generare de cod pentru mai multe limbaje.",
        "expert": "gRPC: service definition .proto, server streaming, client streaming, bidirectional streaming. Interceptors, deadline, load balancing. Integrare cu Envoy, Kubernetes. gRPC-Web pentru browser.",
        "code": "# .proto definitie\nservice AegisService {\n  rpc GetTerm (TermRequest) returns (TermResponse);\n}",
        "real_world": "Netflix, Dropbox, CoreOS folosesc gRPC pentru comunicații între microservicii. Este mai rapid decât REST JSON.",
        "quiz": {"question": "Ce format de serializare folosește gRPC?",
                 "options": ["Protocol Buffers", "JSON", "XML", "YAML"], "answer": "Protocol Buffers"},
        "related": ["protobuf", "http2", "rpc", "microservices", "grpc gateway"]
    },

    "protobuf": {
        "beginner": "Protocol Buffers (protobuf) e ca o valiză super-eficientă pentru date. Împachetează informația mai mic și mai rapid decât JSON. E folosit de Google.",
        "professional": "Protocol Buffers este un limbaj neutru, extensibil pentru serializarea datelor structurate. Produce mesaje binare mici și rapide, cu scheme .proto și generare de cod.",
        "expert": "Protobuf: tipuri scalare, enum, mesaje nested, oneof, map. Compatibilitate înainte/înapoi cu câmpuri opționale. Well-known types (Timestamp, Any). gRPC folosește protobuf ca IDL.",
        "code": "syntax = \"proto3\";\nmessage Person {\n  string name = 1;\n  int32 age = 2;\n}",
        "real_world": "Google folosește protobuf intern pentru aproape toate serviciile. De asemenea, multe companii îl adoptă pentru performanță și compatibilitate.",
        "quiz": {"question": "Protobuf produce date în format...?", "options": ["binar", "text", "JSON", "CSV"],
                 "answer": "binar"},
        "related": ["grpc", "serialization", "schema", "json", "messagepack"]
    },

    "hadoop": {
        "beginner": "Hadoop e ca un sistem de depozitare și procesare pentru cantități uriașe de date, răspândite pe mai multe calculatoare.",
        "professional": "Apache Hadoop este un framework open-source pentru stocarea și procesarea distribuită a big data, folosind HDFS și MapReduce.",
        "expert": "Hadoop: HDFS pentru stocare distribuită, YARN pentru gestionarea resurselor, MapReduce pentru procesare batch. Ecosistem: Hive, Pig, HBase, Spark.",
        "code": "# Exemplu simplu Hadoop MapReduce (Java)\npublic class WordCount {\n  public static void main(String[] args) throws Exception {\n    Job job = Job.getInstance();\n    job.setMapperClass(TokenizerMapper.class);\n    job.setReducerClass(IntSumReducer.class);\n    System.exit(job.waitForCompletion(true) ? 0 : 1);\n  }\n}",
        "real_world": "Companii precum Facebook, Twitter, eBay folosesc Hadoop pentru a procesa petabytes de date de utilizatori.",
        "quiz": {"question": "Ce înseamnă HDFS în Hadoop?",
                 "options": ["Hadoop Distributed File System", "High Density File System", "Hadoop Data File System",
                             "High Definition File System"], "answer": "Hadoop Distributed File System"},
        "related": ["spark", "hive", "big data", "mapreduce", "hdfs"]
    },
    "spark": {
        "beginner": "Spark e ca un motor ultra-rapid pentru prelucrarea datelor. Face calcule în memorie, de 100 de ori mai rapid decât Hadoop.",
        "professional": "Apache Spark este un motor unificat de procesare a datelor pentru big data, cu API-uri în Java, Scala, Python, R. Suportă SQL, streaming, ML, graph.",
        "expert": "Spark: RDD (Resilient Distributed Dataset), DataFrame, Dataset. Catalyst optimizer, Tungsten execution engine. Suportă procesare batch, streaming (Spark Streaming, Structured Streaming), MLlib, GraphX.",
        "code": "# Spark cu Python (PySpark)\nfrom pyspark.sql import SparkSession\nspark = SparkSession.builder.appName(\"AEGIS\").getOrCreate()\ndf = spark.read.csv(\"date.csv\", header=True)\ndf.show()",
        "real_world": "Netflix, Uber, Airbnb folosesc Spark pentru recomandări, analiză trafic, detectare fraudă.",
        "quiz": {"question": "Spark procesează date în...?",
                 "options": ["memorie (RAM)", "disc dur", "bază de date", "cloud"], "answer": "memorie (RAM)"},
        "related": ["hadoop", "big data", "pyspark", "scala", "dataframe"]
    },
    "hive": {
        "beginner": "Hive e ca un translator care îți permite să scrii comenzi SQL pentru datele din Hadoop, fără să știi programare complexă.",
        "professional": "Apache Hive este un data warehouse construit peste Hadoop, care oferă un limbaj asemănător SQL (HiveQL) pentru interogarea datelor stocate în HDFS.",
        "expert": "Hive: HiveQL compilat în MapReduce, Tez sau Spark. Metastore pentru metadate (bazat pe RDBMS). Suportă partiționare, bucket, UDF-uri.",
        "code": "-- HiveQL\nCREATE TABLE users (id INT, name STRING)\nROW FORMAT DELIMITED FIELDS TERMINATED BY ',';\nLOAD DATA INPATH '/data/users.csv' INTO TABLE users;\nSELECT COUNT(*) FROM users;",
        "real_world": "Amazon, Netflix, LinkedIn folosesc Hive pentru analize de date și rapoarte pe big data.",
        "quiz": {"question": "Ce limbaj folosește Hive pentru interogări?",
                 "options": ["HiveQL", "SQL", "MapReduce", "Java"], "answer": "HiveQL"},
        "related": ["hadoop", "spark", "hql", "big data", "data warehouse"]
    },
    "pig": {
        "beginner": "Pig e ca un script simplu pentru prelucrarea datelor mari. Scrii câteva comenzi, iar el le transformă în programe complexe.",
        "professional": "Apache Pig este o platformă de analiză a datelor mari care folosește un limbaj procedural numit Pig Latin, transformând scripturile în job-uri MapReduce, Tez sau Spark.",
        "expert": "Pig Latin: LOAD, FOREACH, FILTER, GROUP, JOIN, STORE. Permite UDF-uri în Java, Python, JavaScript. Suportă tipuri complexe (bag, tuple, map).",
        "code": "-- Pig Latin\nusers = LOAD '/data/users.csv' USING PigStorage(',') AS (id:int, name:chararray);\ngrouped = GROUP users BY id;",
        "real_world": "Yahoo, Twitter, LinkedIn au folosit Pig pentru a procesa fluxuri de date înaintea apariției Spark.",
        "quiz": {"question": "Care este limbajul lui Apache Pig?", "options": ["Pig Latin", "SQL", "Java", "Python"],
                 "answer": "Pig Latin"},
        "related": ["hadoop", "hive", "big data", "mapreduce", "pig latin"]
    },
    "hbase": {
        "beginner": "HBase e ca o bază de date distribuită care permite citiri și scrieri în timp real pe miliarde de rânduri, ca un Google Bigtable.",
        "professional": "Apache HBase este o bază de date NoSQL distribuită, column-oriented, construită peste HDFS, care oferă acces în timp real la date mari.",
        "expert": "HBase: model tabelar cu rânduri și coloane, chei de rând sortate. Suportă versionare, compresie, filtre. Folosește ZooKeeper pentru coordonare.",
        "code": "# HBase shell\ncreate 'users', 'personal', 'professional'\nput 'users', 'row1', 'personal:name', 'Andrei'\nget 'users', 'row1'",
        "real_world": "Facebook folosește HBase pentru sistemul de mesagerie, iar Twitter pentru analytics.",
        "quiz": {"question": "HBase este o bază de date de tip...?",
                 "options": ["column-oriented", "document", "key-value", "graph"], "answer": "column-oriented"},
        "related": ["hadoop", "hdfs", "big data", "nosql", "zookeeper"]
    },
    "zookeeper": {
        "beginner": "ZooKeeper e ca un organizator pentru sisteme distribuite. Ține evidența serverelor și ajută la coordonarea lor.",
        "professional": "Apache ZooKeeper este un serviciu centralizat pentru menținerea configurației, denumirii și sincronizării în sisteme distribuite.",
        "expert": "ZooKeeper: arhitectură master-slave, znode-uri (date), observatori, consens atomic. Folosit de Kafka, HBase, Hadoop, Solr.",
        "code": "# Conectare ZooKeeper cu Python (kazoo)\nfrom kazoo.client import KazooClient\nzk = KazooClient(hosts='127.0.0.1:2181')\nzk.start()\nzk.create('/aegis', b'some_data')",
        "real_world": "Apache Kafka, HBase și Solr folosesc ZooKeeper pentru a gestiona cluster-ele.",
        "quiz": {"question": "Ce rol are ZooKeeper în sisteme distribuite?",
                 "options": ["coordonare", "stocare date", "procesare batch", "streaming"], "answer": "coordonare"},
        "related": ["kafka", "hbase", "distributed systems", "consensus", "apache"]
    },
    "airflow": {
        "beginner": "Airflow e ca un ceas inteligent care programează și monitorizează fluxuri de lucru (workflow-uri) în lumea datelor.",
        "professional": "Apache Airflow este o platformă open-source pentru crearea, programarea și monitorizarea workflow-urilor (DAG-uri) scrise în Python.",
        "expert": "Airflow: DAG (Directed Acyclic Graph), operatori, senzori, hook-uri. UI pentru monitorizare, backfill, variabile, conexiuni. Executori: Sequential, Local, Celery, Kubernetes.",
        "code": "# DAG simplu Airflow\nfrom airflow import DAG\nfrom airflow.operators.bash import BashOperator\nfrom datetime import datetime\nwith DAG('aegis_dag', start_date=datetime(2025,1,1)) as dag:\n    t1 = BashOperator(task_id='print_date', bash_command='date')",
        "real_world": "Airbnb (creatorul), Spotify, Walmart folosesc Airflow pentru a programa pipeline-uri de date.",
        "quiz": {"question": "Ce reprezintă DAG în Airflow?",
                 "options": ["Directed Acyclic Graph", "Data Aggregation Graph", "Dynamic Algorithm Graph",
                             "Distributed Access Gateway"], "answer": "Directed Acyclic Graph"},
        "related": ["etl", "workflow", "python", "big data", "scheduler"]
    },
    "dbt": {
        "beginner": "dbt e ca un instrument care te ajută să transformi datele din baze de date folosind doar SQL, ca un fel de control al versiunilor pentru date.",
        "professional": "dbt (data build tool) este un instrument de transformare a datelor în depozitele de date, folosind SELECT-uri SQL și concepte de modularizare, testare și documentare.",
        "expert": "dbt: modele (SQL), materializări (table, view, incremental, ephemeral), teste (unique, not null, relationships), documentație, lineage, CLI și Cloud.",
        "code": "-- dbt model (models/users.sql)\nSELECT id, name, email FROM {{ ref('raw_users') }} WHERE status = 'active'",
        "real_world": "GitLab, Snowflake, JetBlue folosesc dbt pentru analize de date și documentare.",
        "quiz": {"question": "Ce limbaj se folosește în dbt pentru definirea modelelor?",
                 "options": ["SQL", "Python", "Java", "Scala"], "answer": "SQL"},
        "related": ["etl", "data warehouse", "snowflake", "bigquery", "analytics"]
    },
    "snowflake": {
        "beginner": "Snowflake e ca un depozit de date în nor, care separă stocarea de calcul, astfel încât să poți crește independent și să plătești doar pentru ce folosești.",
        "professional": "Snowflake este o platformă de date bazată pe cloud, cu arhitectură separată de stocare și calcul, suport pentru date semi-structurate și scalare aproape infinită.",
        "expert": "Snowflake: virtual warehouses, micro-partitioning, time travel, zero-copy cloning, suport pentru JSON, Avro, Parquet. Integrare cu dbt, Spark, Airflow.",
        "code": "-- SQL în Snowflake\nCREATE WAREHOUSE aegis_wh;\nCREATE DATABASE aegis_db;\nCREATE TABLE users (id INT, name STRING);\nSELECT * FROM users;",
        "real_world": "5000+ companii, inclusiv Adobe, DoorDash, Netflix, folosesc Snowflake ca data cloud.",
        "quiz": {"question": "Snowflake separă...?",
                 "options": ["stocarea de calcul", "datele de metadate", "cloud de on-premise", "SQL de NoSQL"],
                 "answer": "stocarea de calcul"},
        "related": ["cloud", "data warehouse", "bigquery", "redshift", "databricks"]
    },
    "bigquery": {
        "beginner": "BigQuery e ca un motor de căutare pentru date masive, în cloud-ul Google. Scrii SQL și el găsește răspunsuri rapid, chiar și în petabytes.",
        "professional": "Google BigQuery este un data warehouse serverless, scalabil, care permite interogarea rapidă a seturilor mari de date folosind SQL, cu securitate și integrare în ecosistemul Google Cloud.",
        "expert": "BigQuery: arhitectură coloane, clustering, partiționare, BI Engine, federated queries (Cloud Storage, Drive, Sheets), integrare cu Data Studio, Looker.",
        "code": "# Python client pentru BigQuery\nfrom google.cloud import bigquery\nclient = bigquery.Client()\nquery = \"SELECT name FROM `project.dataset.users` LIMIT 10\"\ndf = client.query(query).to_dataframe()",
        "real_world": "Twitter, Spotify, The New York Times folosesc BigQuery pentru analize de date în timp real.",
        "quiz": {"question": "BigQuery este produs de...?", "options": ["Google", "Amazon", "Microsoft", "Snowflake"],
                 "answer": "Google"},
        "related": ["gcp", "data warehouse", "big data", "sql", "analytics"]
    },
    "databricks": {
        "beginner": "Databricks e ca un mediu de lucru unificat pentru ingineri de date și oameni de știință, construit în jurul Apache Spark.",
        "professional": "Databricks este o platformă unificată de analiză a datelor bazată pe cloud, care combină data engineering, data science și machine learning, creată de fondatorii Apache Spark.",
        "expert": "Databricks: Delta Lake pentru stocare fiabilă, MLflow pentru ciclul ML, colaborare în notebook-uri, auto-scaling, cluster management, Unity Catalog.",
        "code": "# PySpark în Databricks Notebook\ndf = spark.read.csv(\"/mnt/data.csv\", header=True)\ndf.createOrReplaceTempView(\"users\")\nresult = spark.sql(\"SELECT name FROM users\")",
        "real_world": "Shell, HP, Comcast, Bank of America folosesc Databricks pentru transformarea datelor și AI.",
        "quiz": {"question": "Databricks a fost fondat de creatorii...?",
                 "options": ["Apache Spark", "Hadoop", "Kafka", "Airflow"], "answer": "Apache Spark"},
        "related": ["spark", "delta lake", "mlflow", "lakehouse", "big data"]
    },
    "delta lake": {
        "beginner": "Delta Lake e ca un strat de fiabilitate peste stocarea ta de date, asigurându-se că nu se corup și că poți face modificări în siguranță.",
        "professional": "Delta Lake este un strat de stocare open-source care aduce fiabilitatea ACID a bazelor de date la lacurile de date (data lakes), suportând citiri și scrieri concurente.",
        "expert": "Delta Lake: tranzacții ACID, time travel (versiuni), schema enforcement, schema evolution, merge (upsert/delete), streaming, integrare cu Spark.",
        "code": "# Delta Lake în PySpark\ndf.write.format(\"delta\").save(\"/mnt/delta/users\")\ndf2 = spark.read.format(\"delta\").load(\"/mnt/delta/users\")\ndf2.createOrReplaceTempView(\"users\")",
        "real_world": "Folosit intens de companii care construiesc data lakes fiabile, cum ar fi Apple, Samsung, Adobe.",
        "quiz": {"question": "Ce oferă Delta Lake lacurilor de date?",
                 "options": ["tranzacții ACID", "numai citire", "procesare în memorie", "indexare"],
                 "answer": "tranzacții ACID"},
        "related": ["spark", "databricks", "data lake", "iceberg", "hudi"]
    },
    "apache ice": {
        "beginner": "Apache Iceberg e ca un catalog inteligent pentru tabele mari, care face căutările și actualizările mult mai rapide și eficiente.",
        "professional": "Apache Iceberg este un format de tabel open-source pentru seturi de date uriașe, conceput pentru a îmbunătăți performanța și fiabilitatea în data lakes.",
        "expert": "Iceberg: partiționare ascunsă, evoluția schemei, time travel, compatibilitate cu multiple engine-uri (Spark, Flink, Trino).",
        "code": "-- Creare tabel Iceberg în Spark\nCREATE TABLE iceberg.default.users (id INT, name STRING) USING iceberg",
        "real_world": "Netflix, Apple, LinkedIn folosesc Iceberg pentru a gestiona petabytes de date în mod eficient.",
        "quiz": {"question": "Iceberg este un format de...?", "options": ["tabel", "fișier", "stream", "bază de date"],
                 "answer": "tabel"},
        "related": ["data lake", "spark", "flink", "trino", "lakehouse"]
    },
    "flink": {
        "beginner": "Flink e ca un procesor de date în flux continuu (streaming), care reacționează la evenimente în timp real.",
        "professional": "Apache Flink este un framework de procesare a fluxurilor de date (stream processing) cu latență scăzută, toleranță la erori și capabilități de procesare batch.",
        "expert": "Flink: DataStream API, Table API, CEP (complex event processing), exactly-once semantics, checkpoints și savepoints, integrare cu Kafka, RabbitMQ.",
        "code": "# Flink DataStream în Java\nDataStream<String> stream = env.addSource(new FlinkKafkaConsumer<>(\"topic\", new SimpleStringSchema(), props));\nstream.map(s -> s.toUpperCase()).print();",
        "real_world": "Alibaba, Uber, Zalando folosesc Flink pentru sisteme de recomandare, monitorizare, fraude.",
        "quiz": {"question": "Flink este specializat în...?",
                 "options": ["stream processing", "batch processing", "data warehouse", "machine learning"],
                 "answer": "stream processing"},
        "related": ["kafka", "streaming", "spark streaming", "event driven", "real time"]
    },
    "kinesis": {
        "beginner": "Kinesis e ca o conductă de date în cloud-ul Amazon, care transportă milioane de mesaje în timp real între aplicații.",
        "professional": "Amazon Kinesis este o platformă de streaming de date în timp real, care permite colectarea, procesarea și analiza fluxurilor de date la scară largă pe AWS.",
        "expert": "Kinesis: Kinesis Data Streams (shard-uri), Kinesis Data Firehose (încărcare în S3, Redshift, Elasticsearch), Kinesis Data Analytics (SQL, Flink).",
        "code": "# Python boto3 pentru Kinesis\nimport boto3\nkinesis = boto3.client('kinesis')\nresponse = kinesis.put_record(StreamName='test', Data=b'data', PartitionKey='1')",
        "real_world": "Netflix, Pinterest, Airbnb folosesc Kinesis pentru înregistrarea activităților utilizatorilor și monitorizare.",
        "quiz": {"question": "Kinesis este serviciu de streaming de la...?",
                 "options": ["Amazon AWS", "Google Cloud", "Microsoft Azure", "Apache"], "answer": "Amazon AWS"},
        "related": ["aws", "streaming", "kafka", "firehose", "real time"]
    },
    "pubsub": {
        "beginner": "Pub/Sub (Google) e ca un sistem de anunțuri între aplicații: una publică un mesaj, iar altele care sunt abonate îl primesc instant.",
        "professional": "Google Cloud Pub/Sub este un serviciu de mesagerie asincronă, scalabil, care permite transmiterea de mesaje între aplicații, cu suport pentru at-least-once și exactly-once.",
        "expert": "Pub/Sub: topic-uri, abonamente, pull/push, ordering, retry policies, dead-letter topics. Integrare cu Cloud Functions, Dataflow, GKE.",
        "code": "# Python client pentru Pub/Sub\nfrom google.cloud import pubsub_v1\npublisher = pubsub_v1.PublisherClient()\ntopic_path = publisher.topic_path('project', 'topic')\nfuture = publisher.publish(topic_path, b'data')",
        "real_world": "Spotify, Twitter, Google folosesc Pub/Sub pentru a decupla microserviciile și a construi sisteme event-driven.",
        "quiz": {"question": "Pub/Sub este un serviciu de...?",
                 "options": ["mesagerie asincronă", "bază de date", "streaming video", "calcul serverless"],
                 "answer": "mesagerie asincronă"},
        "related": ["gcp", "message queue", "kafka", "rabbitmq", "event driven"]
    },
    "rabbitmq": {
        "beginner": "RabbitMQ e ca un poștaș pentru mesaje între aplicații. Trimiți o scrisoare (mesaj), iar el se asigură că ajunge la destinația corectă.",
        "professional": "RabbitMQ este un message broker open-source, care implementează AMQP (Advanced Message Queuing Protocol), folosit pentru comunicare asincronă între servicii.",
        "expert": "RabbitMQ: exchange (direct, topic, fanout, headers), queue, binding, durable messages, confirm, prefetch, cluster, management UI.",
        "code": "# Python pika pentru RabbitMQ\nimport pika\nconnection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))\nchannel = connection.channel()\nchannel.queue_declare(queue='aegis')\nchannel.basic_publish(exchange='', routing_key='aegis', body='Hello')",
        "real_world": "Reddit, Instagram, Pinterest folosesc RabbitMQ pentru a gestiona cozi de sarcini și actualizări în timp real.",
        "quiz": {"question": "RabbitMQ implementează protocolul...?", "options": ["AMQP", "MQTT", "HTTP", "gRPC"],
                 "answer": "AMQP"},
        "related": ["message queue", "broker", "amqp", "celery", "microservices"]
    },
    "activemq": {
        "beginner": "ActiveMQ e ca un alt poștaș pentru mesaje, asemănător cu RabbitMQ, dar mai vechi și folosit în aplicații enterprise Java.",
        "professional": "Apache ActiveMQ este un message broker open-source, bazat pe Java, care suportă multiple protocoale: AMQP, MQTT, STOMP, OpenWire.",
        "expert": "ActiveMQ: persistent messages, virtual topics, network of brokers, JMS (Java Message Service) compliant, integrare cu Spring.",
        "code": "// Java JMS cu ActiveMQ\nimport javax.jms.*;\nConnectionFactory factory = new ActiveMQConnectionFactory(\"tcp://localhost:61616\");\nConnection conn = factory.createConnection();\nSession session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);\nMessageProducer producer = session.createProducer(new ActiveMQQueue(\"aegis\"));",
        "real_world": "Folosit în multe aplicații enterprise Java, în special în sistemele bancare și de logistică.",
        "quiz": {"question": "ActiveMQ este scris în...?", "options": ["Java", "C++", "Python", "Go"],
                 "answer": "Java"},
        "related": ["jms", "message queue", "broker", "activemq artemis", "stomp"]
    }
}


        
       
        
EXPERT_TERMS = {

"variable": {
    "beginner": "O variabilă este ca o cutie în care pui o valoare. Poți schimba ce e în cutie oricând vrei.",
    "professional": "O variabilă este un identificator care referă o zonă de memorie ce conține o valoare. Tipul și durata ei depind de limbajul de programare.",
    "expert": "O variabilă reprezintă un binding între un nume și o locație de memorie, gestionată prin reguli de scope, lifetime și tipare statice sau dinamice. În runtime, poate fi optimizată prin register allocation, escape analysis și constant folding."
},
"function": {
    "beginner": "O funcție este ca o rețetă: îi dai ingrediente și îți dă un rezultat.",
    "professional": "O funcție este un bloc de cod reutilizabil care primește argumente și returnează o valoare.",
    "expert": "O funcție este o abstracție de ordin superior, suportând closures, currying și optimizări precum inlining."
},
"class": {
    "beginner": "O clasă este un plan după care construiești obiecte.",
    "professional": "O clasă definește proprietăți și metode pentru obiecte într-un sistem OOP.",
    "expert": "O clasă este un tip compus cu mecanisme de meta‑programare, moștenire, polimorfism și reflecție."
},
"object": {
    "beginner": "Un obiect este ceva construit după o clasă.",
    "professional": "Un obiect este o instanță cu stare și comportament definit de clasă.",
    "expert": "Un obiect este o entitate cu identitate, stare și metode, gestionată prin referințe și model de memorie."
},

"list": {
    "beginner": "O listă este o colecție de valori puse una după alta.",
    "professional": "O listă este o structură de date dinamică ce poate crește sau micșora.",
    "expert": "O listă poate fi implementată ca array dinamic sau linked list, cu trade‑off-uri între acces și inserare."
},
"dictionary": {
    "beginner": "Un dicționar păstrează informații în perechi: cheie și valoare.",
    "professional": "Un dictionary este o mapare hash între chei unice și valori.",
    "expert": "Un dictionary folosește hashing, rezolvarea coliziunilor și rehashing pentru performanță amortizată O(1)."
},
"string": {
    "beginner": "Un string este un șir de litere.",
    "professional": "Un string este o secvență de caractere, de obicei imutabilă.",
    "expert": "Un string este o structură optimizată pentru encoding, slicing și interning, cu modele de memorie specifice limbajului."
},
"boolean": {
    "beginner": "Un boolean poate fi doar adevărat sau fals.",
    "professional": "Un boolean reprezintă o valoare logică binară.",
    "expert": "Un boolean este o reprezentare logică optimizată pentru branching, short‑circuiting și evaluare condițională."
},
"if_statement": {
    "beginner": "Un if verifică o condiție și decide ce se întâmplă.",
    "professional": "Un if controlează fluxul programului în funcție de expresii logice.",
    "expert": "Un if este o ramificație condițională ce poate afecta predicția de ramură și performanța CPU."
},

"oop": {
    "beginner": "OOP este modul de a organiza codul în obiecte.",
    "professional": "OOP folosește clase, obiecte și principii ca moștenirea și polimorfismul.",
    "expert": "OOP este un model bazat pe abstracții, cu dispatch dinamic, encapsulare și meta‑programe."
},
"inheritance": {
    "beginner": "Moștenirea permite unei clase să preia lucruri din altă clasă.",
    "professional": "Moștenirea permite reutilizarea codului și extinderea comportamentului.",
    "expert": "Moștenirea implementează ierarhii de tipuri, cu multiple inheritance, virtualizare și probleme ca diamond pattern."
},
"polymorphism": {
    "beginner": "Polimorfismul permite aceluiași lucru să se comporte diferit.",
    "professional": "Polimorfismul permite apelarea aceleiași metode pe obiecte diferite.",
    "expert": "Polimorfismul include dynamic dispatch, overloading, overriding și sisteme avansate de tipare."
},
"encapsulation": {
    "beginner": "Încapsularea ascunde detaliile și arată doar ce e important.",
    "professional": "Încapsularea protejează datele prin acces controlat.",
    "expert": "Încapsularea definește limite clare între API și implementare, permițând invariants și optimizări interne."
},
"abstraction": {
    "beginner": "Abstracția simplifică lucrurile complicate.",
    "professional": "Abstracția ascunde detaliile interne și expune doar funcționalitatea.",
    "expert": "Abstracția creează niveluri conceptuale, reducând complexitatea prin contracte și interfețe."
},
"exception_handling": {
    "beginner": "Gestionarea excepțiilor te ajută când apare o eroare.",
    "professional": "Exception handling tratează erorile prin try, catch și finally.",
    "expert": "Exception handling gestionează fluxul de control în situații anormale, cu costuri de runtime și modele de propagare."
},
"compiler": {
    "beginner": "Un compiler transformă codul tău în ceva ce înțelege calculatorul.",
    "professional": "Un compiler traduce codul sursă în cod mașină sau bytecode.",
    "expert": "Un compiler implementează parsing, semantic analysis, optimizări IR și generare de cod pentru arhitecturi specifice."
},
"interpreter": {
    "beginner": "Un interpreter execută codul linie cu linie.",
    "professional": "Un interpreter analizează și rulează codul direct, fără compilare prealabilă.",
    "expert": "Un interpreter poate folosi JIT, bytecode și optimizări dinamice pentru performanță."
},
"syntax": {
    "beginner": "Sintaxa este modul corect de a scrie cod.",
    "professional": "Sintaxa definește regulile formale ale limbajului.",
    "expert": "Sintaxa este descrisă prin gramatici formale precum BNF și analizată prin parsere LL/LR."
},
"runtime": {
    "beginner": "Runtime-ul este momentul când codul rulează.",
    "professional": "Runtime-ul este mediul care gestionează execuția programului.",
    "expert": "Runtime-ul include memory model, GC, thread scheduling și ABI‑uri specifice platformei."
},
"debugger": {
    "beginner": "Un debugger te ajută să găsești greșeli în cod.",
    "professional": "Un debugger permite inspectarea variabilelor și execuției pas cu pas.",
    "expert": "Un debugger interacționează cu simboluri, breakpoints hardware și registre CPU."
},
"framework": {
    "beginner": "Un framework te ajută să construiești aplicații mai ușor.",
    "professional": "Un framework oferă structuri și reguli pentru dezvoltare.",
    "expert": "Un framework definește un inversion of control, lifecycle hooks și extensibilitate modulară."
},
"library": {
    "beginner": "O librărie este o colecție de funcții gata făcute.",
    "professional": "O librărie oferă funcționalități reutilizabile pentru aplicații.",
    "expert": "O librărie poate fi statică sau dinamică, cu ABI stabil și linking la runtime."
},
"api_call": {
    "beginner": "Un API call este când ceri informații de la alt program.",
    "professional": "Un API call este o cerere către un endpoint pentru date sau acțiuni.",
    "expert": "Un API call implică protocoale, serializare, rate limiting și modele de autentificare."
},

"pointer": {
    "beginner": "Un pointer arată către o locație din memorie.",
    "professional": "Un pointer stochează adresa unei valori.",
    "expert": "Pointerii permit aritmetică, dereferențiere și control fin al memoriei, dar implică riscuri precum dangling pointers."
},
"memory_allocation": {
    "beginner": "Alocarea memoriei înseamnă să rezervi spațiu pentru date.",
    "professional": "Memory allocation gestionează heap și stack.",
    "expert": "Include algoritmi precum buddy system, slab allocator și garbage collection generational."
},
"garbage_collection": {
    "beginner": "GC curăță memoria pe care nu o mai folosești.",
    "professional": "Garbage collection eliberează automat obiectele neutilizate.",
    "expert": "GC implementează mark‑and‑sweep, generational GC, compaction și write barriers."
},
"module": {
    "beginner": "Un modul este un fișier cu cod organizat.",
    "professional": "Un modul este o unitate logică de cod reutilizabil.",
    "expert": "Modulele definesc namespace-uri, sisteme de import și izolare a dependențelor."
},
"package": {
    "beginner": "Un pachet este o colecție de module.",
    "professional": "Un package organizează modulele într-o structură coerentă.",
    "expert": "Include metadata, versionare semantică și sisteme de distribuție precum pip sau npm."
},

"commit": {
    "beginner": "Un commit salvează o schimbare în cod.",
    "professional": "Un commit reprezintă un snapshot al proiectului.",
    "expert": "Un commit este un nod într-un DAG Git, cu hash SHA‑1 și metadate."
},
"branch": {
    "beginner": "Un branch este o linie separată de lucru.",
    "professional": "Un branch permite dezvoltarea paralelă.",
    "expert": "Un branch este un pointer mutabil către un commit, optimizat pentru operații O(1)."
},
"merge": {
    "beginner": "Merge combină două linii de cod.",
    "professional": "Merge integrează schimbările dintr-un branch în altul.",
    "expert": "Merge folosește algoritmi de diff, trei‑căi și rezolvarea conflictelor."
},
"pull_request": {
    "beginner": "Un pull request cere aprobarea pentru a adăuga cod.",
    "professional": "Un PR permite review și integrare controlată.",
    "expert": "Un PR include CI pipelines, code review și politici de protecție a branch‑urilor."
},
"deployment": {
    "beginner": "Deployment înseamnă să pui aplicația online.",
    "professional": "Deployment este procesul de livrare a aplicației către utilizatori.",
    "expert": "Include CI/CD, rollback, blue‑green și canary releases."
},

"design_pattern": {
    "beginner": "Un pattern este o soluție gata făcută pentru o problemă comună.",
    "professional": "Design patterns sunt modele reutilizabile de arhitectură.",
    "expert": "Include creational, structural și behavioral patterns, cu trade‑off-uri clare."
},
"event_loop": {
    "beginner": "Event loop-ul gestionează acțiuni care se întâmplă în timp.",
    "professional": "Event loop-ul procesează evenimente asincrone.",
    "expert": "Implementat prin queue-uri, epoll/kqueue și cooperative scheduling."
},
"async_await": {
    "beginner": "Async/await te ajută să faci lucruri în paralel.",
    "professional": "Async/await gestionează operații asincrone fără blocking.",
    "expert": "Implică coroutines, state machines și event-driven concurrency."
},
"lambda_function": {
    "beginner": "O lambda este o funcție scurtă scrisă rapid.",
    "professional": "O lambda este o funcție anonimă folosită pentru operații simple.",
    "expert": "Lambda-urile sunt closures cu captură lexicală și optimizări inline."
},
"immutable": {
    "beginner": "Imutabil înseamnă că nu poți schimba valoarea.",
    "professional": "Un obiect imutabil nu poate fi modificat după creare.",
    "expert": "Imutabilitatea permite optimizări, thread safety și structural sharing."
},
"mutable": {
    "beginner": "Mutabil înseamnă că poți schimba valoarea.",
    "professional": "Un obiect mutabil își poate modifica starea.",
    "expert": "Mutabilitatea implică modele de memorie, aliasing și sincronizare."
},
"reconnaissance": {
    "beginner": "Reconnaissance înseamnă să aduni informații despre o țintă.",
    "professional": "Reconnaissance colectează date pasive și active pentru a înțelege suprafața de atac.",
    "expert": "Reconnaissance include OSINT, footprinting, enumeration, passive DNS și tehnici stealth pentru evitarea detecției."
},
"footprinting": {
    "beginner": "Footprinting înseamnă să afli detalii despre o companie sau un sistem.",
    "professional": "Footprinting identifică domenii, IP-uri, servere și tehnologii expuse pentru a înțelege suprafața de atac.",
    "expert": "Footprinting folosește DNS zone transfers, ASN mapping, certificate transparency, passive DNS și extragere de metadata pentru profilarea completă a țintei."
},
"enumeration": {
    "beginner": "Enumeration înseamnă să descoperi ce servicii are o țintă.",
    "professional": "Enumeration extrage utilizatori, porturi, servicii și versiuni.",
    "expert": "Include SMB enumeration, LDAP queries, SNMP walks și protocol fingerprinting."
},

"vulnerability_scanning": {
    "beginner": "Scanezi ca să vezi dacă există probleme.",
    "professional": "Detectează versiuni vulnerabile și configurări greșite.",
    "expert": "Folosește CVE mapping, plugin engines, authenticated scans și scoring CVSS."
},

"penetration_testing": {
    "beginner": "Penetration testing testează securitatea unui sistem.",
    "professional": "Simulează atacuri reale pentru a identifica vulnerabilități.",
    "expert": "Include OSSTMM, PTES, chain-exploits, pivoting și privilege escalation."
},

"exploit_development": {
    "beginner": "Exploit înseamnă să profiți de o problemă.",
    "professional": "Creează cod care declanșează vulnerabilități.",
    "expert": "Include ROP chains, shellcode crafting, heap spraying și bypass-uri ASLR/DEP."
},

"buffer_overflow": {
    "beginner": "Apare când bagi prea multe date într-un spațiu mic.",
    "professional": "Poate suprascrie memorie și executa cod arbitrar.",
    "expert": "Include stack smashing, return-to-libc, NX bypass și mitigări moderne."
},

"sql_injection": {
    "beginner": "SQL injection păcălește baza de date.",
    "professional": "Manipulează interogări SQL prin input nevalidat.",
    "expert": "Include UNION-based, error-based, blind, time-based și WAF evasion."
},

"xss": {
    "beginner": "XSS permite injectarea de cod în pagini web.",
    "professional": "Exploatează lipsa sanitizării inputului.",
    "expert": "Include reflected, stored, DOM-based, CSP bypass și payload chaining."
},

"csrf": {
    "beginner": "CSRF păcălește un utilizator să facă acțiuni fără să vrea.",
    "professional": "Exploatează sesiuni active prin cereri forțate.",
    "expert": "Include SameSite bypass, token prediction și pre-flight manipulation."
},

"rce": {
    "beginner": "RCE permite atacatorului să execute comenzi.",
    "professional": "Remote Code Execution compromite complet sistemul.",
    "expert": "Include gadget chains, deserialization attacks și sandbox escapes."
},

"privilege_escalation": {
    "beginner": "Obții acces mai mare decât ar trebui.",
    "professional": "Exploatează configurări greșite sau vulnerabilități.",
    "expert": "Include kernel exploits, token impersonation și misconfig chaining."
},

"pivoting": {
    "beginner": "Pivoting înseamnă să treci dintr-o rețea în alta.",
    "professional": "Folosești un sistem compromis ca punct de acces.",
    "expert": "Include tunneling, SOCKS proxies, port forwarding și lateral movement."
},

"lateral_movement": {
    "beginner": "Te muți prin rețea.",
    "professional": "Extinzi accesul folosind credențiale și sesiuni.",
    "expert": "Include Pass-the-Hash, Kerberoasting, DCSync și AD abuse."
},

"malware_analysis": {
    "beginner": "Analizezi cum funcționează un virus.",
    "professional": "Include analiză statică și dinamică.",
    "expert": "Folosește disassembly, sandboxing, unpacking și behavior signatures."
},

"reverse_engineering": {
    "beginner": "Vezi cum e făcut un program.",
    "professional": "Analizezi binare, protocoale și structuri interne.",
    "expert": "Include decompilare, debugging avansat, hooking și patching."
},

"siem": {
    "beginner": "SIEM colectează loguri.",
    "professional": "Corelează evenimente pentru detectarea atacurilor.",
    "expert": "Include rule engines, UEBA, threat intel feeds și real-time correlation."
},

"ids_ips": {
    "beginner": "IDS/IPS detectează sau blochează atacuri.",
    "professional": "IDS monitorizează, IPS previne.",
    "expert": "Include signature-based, anomaly-based, packet inspection și tuning."
},

"edr": {
    "beginner": "EDR protejează calculatoarele.",
    "professional": "Monitorizează comportamente și activități suspecte.",
    "expert": "Include telemetry, behavioral analytics, memory scanning și rollback."
},

"zero_day": {
    "beginner": "O vulnerabilitate necunoscută.",
    "professional": "Exploatată înainte de patch.",
    "expert": "Include exploit chains, brokers, weaponization și obfuscation."
},

"threat_hunting": {
    "beginner": "Cauți atacuri ascunse.",
    "professional": "Analizezi loguri și comportamente pentru anomalii.",
    "expert": "Include hypothesis-driven hunting, YARA rules și memory forensics."
},

"forensics": {
    "beginner": "Investighezi ce s-a întâmplat pe un sistem.",
    "professional": "Colectezi și analizezi dovezi digitale.",
    "expert": "Include chain of custody, timeline analysis, carving și volatile memory forensics."
},

"mitre_attck": {
    "beginner": "O listă cu tehnici folosite de hackeri.",
    "professional": "Framework pentru clasificarea tacticilor și tehnicilor adversarilor.",
    "expert": "Include mapping, detection engineering și adversary emulation."
},

"ddos": {
    "beginner": "Atac care supraîncarcă un server.",
    "professional": "Folosește trafic masiv pentru a bloca servicii.",
    "expert": "Include botnets, amplification, reflection și mitigări CDN/WAF."
},

"botnet": {
    "beginner": "Rețea de calculatoare controlate de un hacker.",
    "professional": "Botnet-urile execută atacuri coordonate.",
    "expert": "Include C2 servers, fast-flux DNS și peer-to-peer botnets."
},

"phishing": {
    "beginner": "Mesaje false care încearcă să te păcălească.",
    "professional": "Atac ce fură date prin social engineering.",
    "expert": "Include spear phishing, whaling, clone phishing și payload obfuscation."
},

"social_engineering": {
    "beginner": "Atacatorul te păcălește să îi dai informații.",
    "professional": "Manipulează comportamentul uman pentru acces.",
    "expert": "Include pretexting, elicitation, vishing și psychological profiling."
},

"ransomware": {
    "beginner": "Virus care îți blochează fișierele.",
    "professional": "Criptează date și cere răscumpărare.",
    "expert": "Include double extortion, lateral spread, encryption routines și negotiation tactics."
},

"keylogger": {
    "beginner": "Program care îți înregistrează tastele.",
    "professional": "Monitorizează input-ul utilizatorului.",
    "expert": "Include kernel-level hooks, API interception și stealth persistence."
},

"rootkit": {
    "beginner": "Software ascuns care controlează sistemul.",
    "professional": "Ascunde procese, fișiere și activități.",
    "expert": "Include kernel patching, hypervisor rootkits și firmware persistence."
},

"supply_chain_attack": {
    "beginner": "Atac printr-un furnizor.",
    "professional": "Compromite un element din lanțul software.",
    "expert": "Include dependency poisoning, CI/CD compromise și signed malware injection."
},

"waf": {
    "beginner": "Protejează site-urile de atacuri.",
    "professional": "Filtrează trafic HTTP pentru atacuri web.",
    "expert": "Include rule tuning, anomaly detection și bypass techniques."
},

"honeypot": {
    "beginner": "Sistem capcană pentru hackeri.",
    "professional": "Atrag atacatori pentru analiză.",
    "expert": "Include high-interaction honeypots, deception grids și threat intelligence feeds."
},

"tls": {
    "beginner": "Criptează conexiunile.",
    "professional": "Asigură confidențialitate și integritate.",
    "expert": "Include handshake, cipher suites, PFS și certificate pinning."
},

"hashing": {
    "beginner": "Transformă datele într-un cod unic.",
    "professional": "Asigură integritate și verificare.",
    "expert": "Include SHA‑256, salting, peppering și collision resistance."
},

"firewall": {
    "beginner": "Blochează accesul nedorit.",
    "professional": "Controlează traficul între rețele.",
    "expert": "Include stateful inspection, NGFW, DPI și segmentation."
},

"vpn": {
    "beginner": "Ascunde traficul tău online.",
    "professional": "Creează tunel criptat între două puncte.",
    "expert": "Include IPSec, OpenVPN, WireGuard și key exchange."
},

"incident_response": {
    "beginner": "Reacționezi la un atac.",
    "professional": "Urmezi proceduri pentru a limita daunele.",
    "expert": "Include triage, containment, eradication, recovery și post-mortem."
},

"threat_intelligence": {
    "beginner": "Informații despre hackeri.",
    "professional": "Analizează indicatori și campanii.",
    "expert": "Include IOC feeds, TTP mapping, enrichment și automation."
},

"data_exfiltration": {
    "beginner": "Furt de date.",
    "professional": "Transfer neautorizat de informații.",
    "expert": "Include covert channels, DNS tunneling și encrypted exfil."
},

"air_gap_bypass": {
    "beginner": "Treci de un sistem fără internet.",
    "professional": "Exploatezi canale fizice sau electromagnetice.",
    "expert": "Include ultrasonic exfil, LED modulation și power-line signaling."
},

"bruteforce": {
    "beginner": "Încerci toate parolele până găsești una bună.",
    "professional": "Atac automatizat asupra autentificării.",
    "expert": "Include credential stuffing, rate limiting bypass și GPU cracking."
},

"password_spraying": {
    "beginner": "Încerci o parolă pe mulți utilizatori.",
    "professional": "Evită blocarea conturilor.",
    "expert": "Include timing attacks, federation abuse și stealth automation."
},

"kerberoasting": {
    "beginner": "Atac asupra autentificării Windows.",
    "professional": "Extrage bilete Kerberos pentru crack.",
    "expert": "Include SPN enumeration, RC4-HMAC cracking și AD privilege escalation."
},

"dns_spoofing": {
    "beginner": "Redirecționezi utilizatorii către site-uri false.",
    "professional": "Manipulezi răspunsurile DNS.",
    "expert": "Include cache poisoning, MITM și DNSSEC bypass."
},

"mitm": {
    "beginner": "Te pui între două persoane care comunică.",
    "professional": "Interceptezi și modifici traficul.",
    "expert": "Include ARP spoofing, SSL stripping și rogue APs."
},

"session_hijacking": {
    "beginner": "Furi sesiunea unui utilizator.",
    "professional": "Exploatezi cookie-uri sau token-uri.",
    "expert": "Include fixation, prediction și token replay."
},

"secure_coding": {
    "beginner": "Scrii cod fără vulnerabilități.",
    "professional": "Aplici reguli pentru a preveni atacuri.",
    "expert": "Include input validation, sanitization, memory safety și threat modeling."
},
"machine_learning": {
    "beginner": "Machine learning înseamnă să înveți calculatorul să recunoască modele.",
    "professional": "ML folosește algoritmi care învață din date pentru a face predicții.",
    "expert": "Include supervised, unsupervised, reinforcement learning, optimizări și tuning avansat."
},

"deep_learning": {
    "beginner": "Deep learning folosește rețele neuronale mari.",
    "professional": "DL antrenează modele cu multe straturi pentru sarcini complexe.",
    "expert": "Include CNN, RNN, Transformers, backpropagation și optimizări GPU."
},

"neural_network": {
    "beginner": "O rețea neuronală imită creierul.",
    "professional": "Este formată din straturi de neuroni artificiali conectați.",
    "expert": "Include activări, regularizare, initialization strategies și gradient flow."
},

"supervised_learning": {
    "beginner": "Modelul învață din exemple cu răspuns corect.",
    "professional": "Folosește date etichetate pentru clasificare și regresie.",
    "expert": "Include loss functions, sampling, imbalance handling și generalization theory."
},

"unsupervised_learning": {
    "beginner": "Modelul învață fără răspunsuri corecte.",
    "professional": "Descoperă structuri ascunse în date.",
    "expert": "Include clustering, dimensionality reduction și density estimation."
},

"reinforcement_learning": {
    "beginner": "Modelul învață prin încercări și greșeli.",
    "professional": "Optimizează acțiuni pentru a maximiza o recompensă.",
    "expert": "Include Q-learning, policy gradients, actor-critic și exploration strategies."
},

"transformer": {
    "beginner": "Transformer-ul este un model folosit în AI modern.",
    "professional": "Folosește self-attention pentru procesarea secvențelor.",
    "expert": "Include multi-head attention, positional encoding și arhitecturi encoder-decoder."
},

"self_attention": {
    "beginner": "Modelul se uită la toate cuvintele din propoziție.",
    "professional": "Calculează relații între tokeni pentru context.",
    "expert": "Include scaled dot-product attention, masking și optimizări hardware."
},

"embedding": {
    "beginner": "Embedding-ul transformă cuvintele în numere.",
    "professional": "Reprezintă datele în vectori densi cu semnificație semantică.",
    "expert": "Include word2vec, GloVe, positional embeddings și vector spaces."
},

"tokenization": {
    "beginner": "Împarte textul în bucăți mici.",
    "professional": "Transformă textul în tokeni pentru modele.",
    "expert": "Include BPE, WordPiece, SentencePiece și subword segmentation."
},

"optimizer": {
    "beginner": "Optimizer-ul ajută modelul să învețe.",
    "professional": "Ajustează parametrii pentru a minimiza loss-ul.",
    "expert": "Include AdamW, momentum, learning rate schedules și gradient clipping."
},
"regularization": {
    "beginner": "Ajută modelul să nu învețe greșit.",
    "professional": "Previne overfitting prin penalizări.",
    "expert": "Include dropout, L1/L2, early stopping și data augmentation."
},

"overfitting": {
    "beginner": "Modelul învață prea mult și greșește pe date noi.",
    "professional": "Se potrivește excesiv pe setul de antrenare.",
    "expert": "Include variance analysis, complexity control și validation strategies."
},

"underfitting": {
    "beginner": "Modelul nu învață destul.",
    "professional": "Nu capturează structura datelor.",
    "expert": "Include bias analysis, model capacity și feature engineering."
},
"backpropagation": {
    "beginner": "Modelul află unde a greșit.",
    "professional": "Calculează gradientul pentru fiecare parametru.",
    "expert": "Include chain rule, computational graphs și gradient stability."
},

"batch_normalization": {
    "beginner": "Stabilizează învățarea.",
    "professional": "Normalizează activările pe batch.",
    "expert": "Include internal covariate shift, inference mode și training dynamics."
},

"layer_normalization": {
    "beginner": "Normalizează fiecare strat.",
    "professional": "Funcționează bine în Transformers.",
    "expert": "Include per-token normalization și stabilitate în modele mari."
},

"dropout": {
    "beginner": "Oprește temporar neuroni.",
    "professional": "Previne overfitting prin randomizare.",
    "expert": "Include dropout masks, inference scaling și variational dropout."
},

"cnn": {
    "beginner": "CNN procesează imagini.",
    "professional": "Folosește filtre pentru a extrage caracteristici.",
    "expert": "Include convoluții, pooling, receptive fields și arhitecturi moderne."
},

"rnn": {
    "beginner": "RNN procesează text sau secvențe.",
    "professional": "Păstrează contextul în timp.",
    "expert": "Include LSTM, GRU, vanishing gradients și sequence modeling."
},

"lstm": {
    "beginner": "LSTM ține minte mai mult timp.",
    "professional": "Folosește celule cu gating pentru memorie.",
    "expert": "Include forget/input/output gates și stabilitate pe secvențe lungi."
},

"gru": {
    "beginner": "GRU e ca LSTM dar mai simplu.",
    "professional": "Folosește două gate-uri pentru memorie.",
    "expert": "Include update/reset gates și eficiență computațională."
},

"autoencoder": {
    "beginner": "Autoencoderul comprimă și reconstruiește date.",
    "professional": "Învață reprezentări latente.",
    "expert": "Include variational autoencoders, bottlenecks și latent space modeling."
},

"vae": {
    "beginner": "VAE generează date noi.",
    "professional": "Folosește distribuții probabilistice.",
    "expert": "Include reparametrization trick, KL loss și latent sampling."
},

"gan": {
    "beginner": "GAN generează imagini sau date.",
    "professional": "Folosește generator și discriminator.",
    "expert": "Include training instability, mode collapse și arhitecturi moderne."
},

"diffusion_model": {
    "beginner": "Model care generează imagini foarte realiste.",
    "professional": "Inversează un proces de zgomot pentru a crea date.",
    "expert": "Include UNet, noise schedulers, sampling steps și guidance."
},

"prompt_engineering": {
    "beginner": "Scrii instrucțiuni pentru AI.",
    "professional": "Optimizezi inputul pentru rezultate mai bune.",
    "expert": "Include chain-of-thought, few-shot, role prompting și control al modelelor mari."
},

"fine_tuning": {
    "beginner": "Îmbunătățești un model deja antrenat.",
    "professional": "Adaptezi modelul la un set nou de date.",
    "expert": "Include LoRA, QLoRA, PEFT și training eficient pe GPU."
},

"lora": {
    "beginner": "Metodă de antrenare rapidă.",
    "professional": "Adaugă straturi mici pentru a modifica modelul.",
    "expert": "Include rank decomposition, adapters și memory-efficient training."
},

"quantization": {
    "beginner": "Face modelul mai mic.",
    "professional": "Reduce precizia numerelor pentru performanță.",
    "expert": "Include INT8, FP8, GPTQ și quantization-aware training."
},

"model_compression": {
    "beginner": "Micșorezi modelul.",
    "professional": "Optimizezi parametrii și structura.",
    "expert": "Include pruning, distillation și weight sharing."
},

"knowledge_distillation": {
    "beginner": "Un model mare învață un model mic.",
    "professional": "Transferă cunoștințe între modele.",
    "expert": "Include teacher-student training, soft targets și compression pipelines."
},

"rag": {
    "beginner": "Modelul caută informații înainte să răspundă.",
    "professional": "Combină LLM cu un sistem de căutare.",
    "expert": "Include vector stores, embeddings, retrievers și context optimization."
},

"vector_database": {
    "beginner": "Stochează informații ca vectori.",
    "professional": "Permite căutare semantică rapidă.",
    "expert": "Include HNSW, IVF, PQ și indexing avansat."
},

"semantic_search": {
    "beginner": "Căutare după sens, nu după cuvinte.",
    "professional": "Folosește embeddings pentru relevanță.",
    "expert": "Include similarity metrics, ANN search și reranking."
},

"model_serving": {
    "beginner": "Pui modelul online.",
    "professional": "Servești inferențe prin API.",
    "expert": "Include batching, quantization, GPU scheduling și autoscaling."
},

"inference_optimization": {
    "beginner": "Modelul răspunde mai repede.",
    "professional": "Optimizezi latența și costul.",
    "expert": "Include tensor fusion, KV caching, speculative decoding și graph optimization."
},

"speculative_decoding": {
    "beginner": "Modelul ghicește mai repede următoarele cuvinte.",
    "professional": "Folosește modele mici pentru accelerare.",
    "expert": "Include draft models, verification steps și parallel decoding."
},

"multimodal_ai": {
    "beginner": "AI care înțelege imagini, text și sunet.",
    "professional": "Combină mai multe tipuri de date.",
    "expert": "Include cross-attention, fusion layers și alignment training."
},

"alignment": {
    "beginner": "AI-ul trebuie să se comporte corect.",
    "professional": "Asiguri că modelul respectă reguli.",
    "expert": "Include RLHF, preference modeling și safety constraints."
},

"rlhf": {
    "beginner": "Oamenii învață AI-ul cum să răspundă.",
    "professional": "Optimizează modelul după preferințe umane.",
    "expert": "Include reward models, PPO și feedback loops."
},

"hallucination": {
    "beginner": "AI-ul inventează lucruri.",
    "professional": "Apare când modelul nu are informații corecte.",
    "expert": "Include uncertainty modeling, retrieval grounding și consistency checks."
},

"ai_safety": {
    "beginner": "AI-ul trebuie să fie sigur.",
    "professional": "Previne comportamente nedorite.",
    "expert": "Include red-teaming, guardrails, interpretability și risk mitigation."
},
"cloud_computing": {
    "beginner": "Cloud-ul îți permite să folosești servere pe internet.",
    "professional": "Cloud computing oferă resurse scalabile: compute, storage, networking.",
    "expert": "Include arhitecturi cloud-native, autoscaling, multi-region, cost optimization și microservicii."
},

"iaas": {
    "beginner": "Primești servere virtuale în cloud.",
    "professional": "Infrastructure as a Service oferă VM-uri, rețele și stocare.",
    "expert": "Include provisioning automat, VPC design, load balancing și securitate granulară."
},

"paas": {
    "beginner": "Primești o platformă gata pentru aplicații.",
    "professional": "Platform as a Service gestionează runtime, scaling și deployment.",
    "expert": "Include buildpacks, managed runtimes, autoscaling și CI/CD integrat."
},

"saas": {
    "beginner": "Folosești aplicații direct din browser.",
    "professional": "Software as a Service livrează aplicații complet gestionate.",
    "expert": "Include multi-tenancy, API integration, SSO și SLA-uri enterprise."
},
"cicd": {
    "beginner": "CI/CD livrează cod automat.",
    "professional": "Automatizează build, test și deployment.",
    "expert": "Include pipelines declarative, canary releases, blue-green și rollback automat."
},

"docker": {
    "beginner": "Docker pune aplicațiile în containere.",
    "professional": "Containerele rulează izolat și portabil.",
    "expert": "Include images, layers, registries, multi-stage builds și security hardening."
},

"container": {
    "beginner": "Un container e o aplicație împachetată complet.",
    "professional": "Rulează izolat folosind namespace-uri și cgroups.",
    "expert": "Include OCI standards, runtime-uri și optimizări de resurse."
},

"kubernetes": {
    "beginner": "Kubernetes gestionează containerele.",
    "professional": "Orchestrează deployment, scaling și networking.",
    "expert": "Include control plane, pods, services, ingress, operators și service mesh."
},

"helm": {
    "beginner": "Helm instalează aplicații în Kubernetes.",
    "professional": "Folosește charts pentru deployment-uri complexe.",
    "expert": "Include templating, versioning, releases și dependency management."
},

"terraform": {
    "beginner": "Terraform construiește infrastructură automat.",
    "professional": "IaC declarativ pentru cloud providers.",
    "expert": "Include state management, modules, workspaces și pipelines GitOps."
},

"ansible": {
    "beginner": "Ansible configurează servere automat.",
    "professional": "Folosește playbooks pentru provisioning.",
    "expert": "Include idempotency, roles, inventories și orchestration avansat."
},

"gitops": {
    "beginner": "Git controlează infrastructura.",
    "professional": "Deployment-urile sunt gestionate prin Git.",
    "expert": "Include ArgoCD, Flux, reconciliation loops și declarative operations."
},

"serverless": {
    "beginner": "Rulezi cod fără servere.",
    "professional": "Funcțiile se execută la cerere.",
    "expert": "Include event-driven design, cold starts, concurrency și cost optimization."
},

"lambda": {
    "beginner": "Lambda rulează funcții în AWS.",
    "professional": "Funcții serverless integrate cu AWS services.",
    "expert": "Include triggers, layers, IAM policies și orchestration Step Functions."
},

"load_balancer": {
    "beginner": "Împarte traficul între servere.",
    "professional": "Asigură disponibilitate și performanță.",
    "expert": "Include L4/L7 balancing, health checks, sticky sessions și autoscaling."
},

"autoscaling": {
    "beginner": "Serverele cresc sau scad automat.",
    "professional": "Scalează resursele în funcție de trafic.",
    "expert": "Include predictive scaling, HPA, VPA și cluster autoscaler."
},


"service_mesh": {
    "beginner": "Controlează traficul dintre microservicii.",
    "professional": "Oferă observability, routing și securitate.",
    "expert": "Include sidecars, mTLS, retries, circuit breaking și Istio/Linkerd."
},

"api_gateway": {
    "beginner": "Un singur punct de intrare pentru API-uri.",
    "professional": "Gestionează routing, rate limiting și auth.",
    "expert": "Include JWT validation, caching, transformations și multi-region routing."
},


"monitoring": {
    "beginner": "Monitorizezi serverele.",
    "professional": "Colectezi metrici și alerte.",
    "expert": "Include Prometheus, Grafana, exporters și alert rules."
},

"distributed_tracing": {
    "beginner": "Urmărești cererile prin microservicii.",
    "professional": "Analizezi latența și erorile.",
    "expert": "Include spans, context propagation și Jaeger/Zipkin."
},

"high_availability": {
    "beginner": "Sistemul nu cade.",
    "professional": "Folosește redundanță și failover.",
    "expert": "Include multi-AZ, multi-region, quorum și replication."
},

"fault_tolerance": {
    "beginner": "Sistemul rezistă la probleme.",
    "professional": "Continuă să funcționeze chiar dacă ceva cade.",
    "expert": "Include retries, circuit breakers și redundancy patterns."
},

"blue_green_deployment": {
    "beginner": "Două versiuni ale aplicației, una activă.",
    "professional": "Schimbi traficul între versiuni fără downtime.",
    "expert": "Include traffic shifting, rollback instant și environment parity."
},

"canary_deployment": {
    "beginner": "Testezi noua versiune pe puțini utilizatori.",
    "professional": "Monitorizezi impactul înainte de rollout complet.",
    "expert": "Include progressive delivery, metrics gating și automated rollback."
},

"rolling_update": {
    "beginner": "Actualizezi serverele pe rând.",
    "professional": "Eviți downtime-ul.",
    "expert": "Include surge/availability settings și batch strategies."
},

"reverse_proxy": {
    "beginner": "Trimite cererile către servere.",
    "professional": "Optimizează routing și caching.",
    "expert": "Include Nginx, Envoy, TLS termination și load distribution."
},

"cdn": {
    "beginner": "Face site-urile mai rapide.",
    "professional": "Servește conținut din locații apropiate.",
    "expert": "Include edge caching, invalidation și global routing."
},

"vpc": {
    "beginner": "Rețea privată în cloud.",
    "professional": "Controlezi subrețele, rute și securitate.",
    "expert": "Include NACLs, security groups, peering și private endpoints."
},

"subnet": {
    "beginner": "O parte din rețea.",
    "professional": "Împarte VPC-ul în zone logice.",
    "expert": "Include public/private subnets, routing și isolation."
},

"iam": {
    "beginner": "Controlezi cine are acces.",
    "professional": "Gestionezi permisiuni și roluri.",
    "expert": "Include least privilege, policies, STS și identity federation."
},

"secrets_manager": {
    "beginner": "Ține parolele în siguranță.",
    "professional": "Stochează și rotește secrete.",
    "expert": "Include encryption, rotation policies și audit logging."
},

"load_testing": {
    "beginner": "Testezi cât trafic suportă aplicația.",
    "professional": "Simulezi utilizatori reali.",
    "expert": "Include stress, soak, spike testing și performance baselines."
},

"edge_computing": {
    "beginner": "Procesare aproape de utilizator.",
    "professional": "Reduce latența și traficul.",
    "expert": "Include edge nodes, caching, serverless edge și IoT integration."
},

"multi_cloud": {
    "beginner": "Folosești mai mulți provideri cloud.",
    "professional": "Distribui workload-uri între platforme.",
    "expert": "Include portability, abstraction layers și failover cross-cloud."
},

"hybrid_cloud": {
    "beginner": "Combini cloud-ul cu serverele tale.",
    "professional": "Integrezi on-prem cu cloud public.",
    "expert": "Include VPN, Direct Connect, identity sync și workload migration."
},

"orchestration": {
    "beginner": "Automatizezi procese.",
    "professional": "Coordonezi servicii și resurse.",
    "expert": "Include workflows, DAGs, Airflow și event-driven pipelines."
},

"configuration_management": {
    "beginner": "Configurezi servere automat.",
    "professional": "Menții consistența mediilor.",
    "expert": "Include Ansible, Puppet, Chef și declarative configs."
},

"release_management": {
    "beginner": "Controlezi lansările aplicației.",
    "professional": "Planifici și automatizezi release-uri.",
    "expert": "Include versioning, approvals, rollback și governance."
},

"finops": {
    "beginner": "Controlezi costurile din cloud.",
    "professional": "Optimizezi consumul și bugetele.",
    "expert": "Include cost allocation, rightsizing și forecasting."
},
"networking": {
    "beginner": "Networking înseamnă conectarea calculatoarelor între ele.",
    "professional": "Networking gestionează comunicarea între dispozitive prin protocoale și infrastructură.",
    "expert": "Include routing, switching, subnetting, QoS, SDN și arhitecturi enterprise."
},

"ip_address": {
    "beginner": "IP-ul este adresa calculatorului tău pe internet.",
    "professional": "IP identifică unic un dispozitiv într-o rețea. Versiuni: IPv4, IPv6.",
    "expert": "Include subnetting, CIDR, NAT traversal și IPv6 addressing schemes."
},

"subnetting": {
    "beginner": "Împarți o rețea în bucăți mai mici.",
    "professional": "Subnetting optimizează utilizarea adreselor IP.",
    "expert": "Include VLSM, CIDR, route summarization și design enterprise."
},

"cidr": {
    "beginner": "CIDR arată câte adrese are o rețea.",
    "professional": "Classless Inter-Domain Routing definește prefixele IP.",
    "expert": "Include route aggregation, efficient addressing și ISP-level routing."
},

"mac_address": {
    "beginner": "MAC este numărul unic al plăcii de rețea.",
    "professional": "Identificator hardware de 48 biți pentru nivelul 2.",
    "expert": "Include OUI lookup, spoofing, filtering și L2 security."
},

"arp": {
    "beginner": "ARP găsește adresa MAC după IP.",
    "professional": "Address Resolution Protocol mapează IP → MAC.",
    "expert": "Include ARP cache poisoning, mitigation și gratuitous ARP."
},

"dhcp": {
    "beginner": "DHCP dă automat IP-uri.",
    "professional": "Dynamic Host Configuration Protocol alocă IP, gateway, DNS.",
    "expert": "Include DHCP relay, reservations, scopes și security hardening."
},

"dns": {
    "beginner": "DNS traduce nume în IP-uri.",
    "professional": "Domain Name System rezolvă domenii prin zone și recorduri.",
    "expert": "Include DNSSEC, caching, zone transfers și load balancing."
},

"routing": {
    "beginner": "Routing-ul trimite datele pe drumul corect.",
    "professional": "Routerele decid traseul pachetelor între rețele.",
    "expert": "Include static/dynamic routing, ECMP, BGP, OSPF și convergence."
},

"switching": {
    "beginner": "Switch-ul conectează dispozitive într-o rețea locală.",
    "professional": "Switching operează la Layer 2 folosind MAC forwarding.",
    "expert": "Include VLANs, STP, trunking, LACP și port security."
},

"vlan": {
    "beginner": "VLAN împarte rețeaua în zone separate.",
    "professional": "Virtual LAN izolează traficul logic.",
    "expert": "Include tagging 802.1Q, trunking, inter-VLAN routing și segmentation."
},

"stp": {
    "beginner": "STP previne buclele în rețea.",
    "professional": "Spanning Tree Protocol creează o topologie fără bucle.",
    "expert": "Include RSTP, MSTP, BPDU guard și root bridge optimization."
},

"lacp": {
    "beginner": "LACP combină mai multe cabluri într-unul mai rapid.",
    "professional": "Link Aggregation Control Protocol crește banda și redundanța.",
    "expert": "Include LAG hashing, active/passive modes și failover."
},

"nat": {
    "beginner": "NAT ascunde IP-urile interne.",
    "professional": "Network Address Translation mapează IP-uri private ↔ publice.",
    "expert": "Include PAT, static NAT, hairpinning și firewall integration."
},

"firewall_rules": {
    "beginner": "Regulile firewall decid ce intră și ce iese.",
    "professional": "Permit/deny pe porturi, IP-uri și protocoale.",
    "expert": "Include L3/L4 filtering, stateful inspection și zero trust."
},

"tcp": {
    "beginner": "TCP trimite date în ordine și fără pierderi.",
    "professional": "Protocol orientat pe conexiune cu handshake 3-way.",
    "expert": "Include congestion control, window scaling și retransmission logic."
},

"udp": {
    "beginner": "UDP trimite date rapid, fără verificări.",
    "professional": "Protocol fără conexiune, folosit pentru streaming.",
    "expert": "Include packet loss handling, NAT traversal și low-latency design."
},

"http": {
    "beginner": "HTTP este limbajul web-ului.",
    "professional": "Protocol pentru transferul paginilor web.",
    "expert": "Include HTTP/2 multiplexing, HTTP/3 QUIC și caching strategies."
},

"https": {
    "beginner": "HTTPS este HTTP securizat.",
    "professional": "Folosește TLS pentru criptare.",
    "expert": "Include certificate pinning, HSTS și handshake optimization."
},

"load_balancing": {
    "beginner": "Împarte traficul între servere.",
    "professional": "Crește performanța și disponibilitatea.",
    "expert": "Include L4/L7 balancing, health checks și global load balancing."
},

"qos": {
    "beginner": "QoS prioritizează traficul important.",
    "professional": "Quality of Service gestionează latența și banda.",
    "expert": "Include DSCP, shaping, policing și queue management."
},

"mtu": {
    "beginner": "MTU este mărimea maximă a unui pachet.",
    "professional": "Afectează performanța și fragmentarea.",
    "expert": "Include jumbo frames, PMTUD și optimization."
},

"packet_sniffing": {
    "beginner": "Sniffing înseamnă să vezi traficul din rețea.",
    "professional": "Analizezi pachete cu Wireshark.",
    "expert": "Include deep packet inspection, filters și protocol analysis."
},

"wireshark": {
    "beginner": "Wireshark arată tot traficul din rețea.",
    "professional": "Analizor de pachete pentru debugging.",
    "expert": "Include display filters, dissectors și capture optimization."
},

"bgp": {
    "beginner": "BGP conectează internetul.",
    "professional": "Border Gateway Protocol gestionează rutele globale.",
    "expert": "Include AS paths, route reflectors, peering și traffic engineering."
},

"ospf": {
    "beginner": "OSPF găsește cel mai scurt drum.",
    "professional": "Protocol interior de routing pe link-state.",
    "expert": "Include areas, LSAs, DR/BDR și fast convergence."
},

"ethernet": {
    "beginner": "Ethernet este cablul de rețea.",
    "professional": "Standard pentru rețele LAN.",
    "expert": "Include 802.3 standards, PoE, full-duplex și frame structure."
},

"poe": {
    "beginner": "PoE trimite curent prin cablul de rețea.",
    "professional": "Power over Ethernet alimentează camere, AP-uri, telefoane.",
    "expert": "Include PoE+, PoE++, power budgets și negotiation."
},

"vpn_tunnel": {
    "beginner": "VPN creează un tunel securizat.",
    "professional": "Criptează traficul între două locații.",
    "expert": "Include IPSec, SSL VPN, IKEv2 și split tunneling."
},

"ssid": {
    "beginner": "SSID este numele rețelei Wi-Fi.",
    "professional": "Identifică un WLAN.",
    "expert": "Include hidden SSID, multi-SSID și VLAN mapping."
},

"wpa3": {
    "beginner": "WPA3 securizează Wi-Fi-ul.",
    "professional": "Standard modern de criptare wireless.",
    "expert": "Include SAE handshake, forward secrecy și enterprise mode."
},

"mesh_network": {
    "beginner": "Mesh conectează mai multe routere între ele.",
    "professional": "Extinde acoperirea Wi-Fi.",
    "expert": "Include dynamic routing, self-healing și multi-hop optimization."
},

"latency": {
    "beginner": "Latența este timpul de răspuns.",
    "professional": "Afectează gaming, streaming și VoIP.",
    "expert": "Include jitter, bufferbloat și QoS tuning."
},

"bandwidth": {
    "beginner": "Banda este cât trafic poate trece.",
    "professional": "Măsurată în Mbps sau Gbps.",
    "expert": "Include throughput, congestion și capacity planning."
},

"throughput": {
    "beginner": "Throughput este viteza reală.",
    "professional": "Cantitatea efectivă de date transferate.",
    "expert": "Include TCP efficiency, retransmissions și bottlenecks."
},

"packet_loss": {
    "beginner": "Pachetele se pierd pe drum.",
    "professional": "Afectează calitatea conexiunii.",
    "expert": "Include diagnostics, jitter buffers și redundancy."
},

"icmp": {
    "beginner": "ICMP testează conexiuni.",
    "professional": "Protocol pentru mesaje de control.",
    "expert": "Include ping, traceroute, rate limiting și filtering."
},

"traceroute": {
    "beginner": "Traceroute arată drumul pachetelor.",
    "professional": "Diagnostică probleme de rețea.",
    "expert": "Include TTL manipulation, ICMP/UDP modes și path analysis."
},

"sdn": {
    "beginner": "SDN controlează rețeaua prin software.",
    "professional": "Software-Defined Networking separă control plane de data plane.",
    "expert": "Include OpenFlow, controllers și network automation."
},

"load_sharing": {
    "beginner": "Împarți traficul pe mai multe rute.",
    "professional": "Crește performanța și redundanța.",
    "expert": "Include ECMP, hashing și failover."
},

"ipv6": {
    "beginner": "IPv6 este noua versiune de IP.",
    "professional": "128 biți, spațiu imens de adrese.",
    "expert": "Include SLAAC, link-local, dual-stack și transition mechanisms."
},

"proxy": {
    "beginner": "Proxy-ul trimite cererile în locul tău.",
    "professional": "Ascunde identitatea și filtrează traficul.",
    "expert": "Include forward/reverse proxy, caching și filtering."
},

"nat_traversal": {
    "beginner": "NAT traversal ajută dispozitivele să se conecteze prin NAT.",
    "professional": "Folosit în VoIP și gaming.",
    "expert": "Include STUN, TURN, ICE și hole punching."
},

"wan": {
    "beginner": "WAN conectează orașe sau țări.",
    "professional": "Wide Area Network folosește linkuri mari.",
    "expert": "Include MPLS, SD-WAN, QoS și redundancy."
},

"lan": {
    "beginner": "LAN este rețeaua din casă sau birou.",
    "professional": "Local Area Network conectează dispozitive apropiate.",
    "expert": "Include switching, VLANs și segmentation."
},

"sd_wan": {
    "beginner": "SD-WAN optimizează conexiunile între locații.",
    "professional": "Folosește software pentru routing inteligent.",
    "expert": "Include path selection, encryption și cloud integration."
},
"web_components": {
    "beginner": "Web Components sunt elemente personalizate pe care le poți folosi ca piese LEGO în pagini web.",
    "professional": "Web Components folosesc Custom Elements, Shadow DOM și HTML Templates pentru UI reutilizabil.",
    "expert": "Shadow DOM oferă izolare, Custom Elements definesc lifecycle hooks, iar Templates optimizează rendering-ul."
},

"shadow_dom": {
    "beginner": "Shadow DOM este o zonă ascunsă în interiorul unui element HTML.",
    "professional": "Shadow DOM izolează stilurile și structura internă a unui component.",
    "expert": "Include encapsulation strictă, event retargeting și moduri open/closed pentru controlul accesului."
},

"isomorphic_javascript": {
    "beginner": "Același cod rulează și pe server, și în browser.",
    "professional": "Isomorphic JS permite partajarea logicii între Node.js și client.",
    "expert": "Folosit în SSR frameworks, implică hydration, environment differences și optimizări de performanță."
},

"hydration": {
    "beginner": "Browserul activează HTML-ul generat pe server.",
    "professional": "Hydration atașează event listeners peste markup-ul SSR.",
    "expert": "Include partial hydration, resumability, mismatch detection și optimizări pentru LCP."
},

"micro_frontends": {
    "beginner": "Un site mare împărțit în bucăți independente.",
    "professional": "Arhitectură unde echipe diferite livrează module separate.",
    "expert": "Include Module Federation, runtime integration, shared dependencies și isolation patterns."
},

"module_federation": {
    "beginner": "Două aplicații își pot împărți codul.",
    "professional": "Webpack 5 permite încărcarea dinamică a modulelor remote.",
    "expert": "Include version negotiation, host/remote architecture și runtime sharing."
},

"vite": {
    "beginner": "Un tool foarte rapid pentru proiecte web.",
    "professional": "Dev server bazat pe ES Modules și Rollup pentru build.",
    "expert": "Include HMR instant, pre-bundling cu esbuild și plugin API avansat."
},

"astro_islands": {
    "beginner": "Doar părțile interactive ale paginii primesc JavaScript.",
    "professional": "Island architecture combină HTML static cu componente interactive izolate.",
    "expert": "Include partial hydration, zero-JS by default și rendering multi-framework."
},

"service_worker_lifecycle": {
    "beginner": "Un mic robot care rulează în fundal.",
    "professional": "Stări: install, activate, idle, fetch, terminate.",
    "expert": "Include caching strategies, background sync, skipWaiting și clients.claim."
},

"background_sync": {
    "beginner": "Site-ul sincronizează datele când revii online.",
    "professional": "API pentru retry logic al request-urilor eșuate.",
    "expert": "Include periodic sync, permission model și optimizări pentru consumul de baterie."
},

"pwa": {
    "beginner": "Site-uri care se comportă ca aplicații.",
    "professional": "Progressive Web Apps folosesc manifest, service workers și caching.",
    "expert": "Include offline-first, background sync, push notifications și installability."
},

"web_manifest": {
    "beginner": "Fișier care spune browserului cum arată aplicația.",
    "professional": "Definește iconuri, culori, orientare și mod de afișare.",
    "expert": "Include adaptive icons, shortcuts, scope control și integration cu OS."
},

"responsive_design": {
    "beginner": "Site-ul se adaptează la orice ecran.",
    "professional": "Folosește media queries, layout fluid și unități relative.",
    "expert": "Include container queries, fluid typography și mobile-first architecture."
},

"css_grid": {
    "beginner": "O metodă de a aranja elementele în grilă.",
    "professional": "CSS Grid oferă layout bidimensional flexibil.",
    "expert": "Include subgrid, named areas, auto-placement și responsive patterns."
},

"flexbox": {
    "beginner": "Flexbox aliniază elementele ușor.",
    "professional": "Oferă control asupra direcției, alinierii și distribuției spațiului.",
    "expert": "Include flex-flow, alignment strategies și complex nesting."
},

"dom": {
    "beginner": "DOM este structura paginii web.",
    "professional": "Document Object Model reprezintă elementele ca noduri.",
    "expert": "Include tree traversal, mutation observers și virtual DOM optimizations."
},

"virtual_dom": {
    "beginner": "O copie rapidă a paginii pentru actualizări eficiente.",
    "professional": "Framework-urile folosesc VDOM pentru diffing și rendering optim.",
    "expert": "Include reconciliation, fiber architecture și batching updates."
},

"reactivity": {
    "beginner": "Pagina se actualizează automat când datele se schimbă.",
    "professional": "Reactivitatea urmărește dependențele și actualizează UI-ul.",
    "expert": "Include fine-grained reactivity, signals, proxies și dependency tracking."
},

"spa": {
    "beginner": "Site care se încarcă o singură dată.",
    "professional": "Single Page Applications folosesc routing client-side.",
    "expert": "Include hydration, code splitting, prefetching și state management."
},

"ssr": {
    "beginner": "Serverul generează HTML-ul înainte să ajungă la tine.",
    "professional": "Server-Side Rendering îmbunătățește SEO și TTFB.",
    "expert": "Include streaming SSR, partial hydration și edge rendering."
},

"csr": {
    "beginner": "Browserul construiește pagina din JavaScript.",
    "professional": "Client-Side Rendering oferă interactivitate completă.",
    "expert": "Include lazy loading, bundling optimizat și hydration strategies."
},

"nextjs": {
    "beginner": "Un framework modern pentru React.",
    "professional": "Oferă SSR, SSG, API routes și routing avansat.",
    "expert": "Include app router, server components, edge functions și RSC streaming."
},

"nuxt": {
    "beginner": "Framework pentru Vue.",
    "professional": "Oferă SSR, SSG, routing automat și module.",
    "expert": "Include Nitro engine, hybrid rendering și server islands."
},

"svelte": {
    "beginner": "Framework foarte rapid pentru UI.",
    "professional": "Compilează componentele în cod minimal.",
    "expert": "Include reactivity granulară, transitions și zero-VDOM architecture."
},

"sveltekit": {
    "beginner": "Framework complet pentru Svelte.",
    "professional": "Oferă routing, SSR, endpoints și adaptors.",
    "expert": "Include server actions, streaming, edge deployment și hybrid rendering."
},

"tailwind_css": {
    "beginner": "CSS gata făcut, doar îl combini.",
    "professional": "Utility-first CSS pentru styling rapid.",
    "expert": "Include JIT engine, design tokens și theming avansat."
},

"css_variables": {
    "beginner": "Variabile în CSS.",
    "professional": "Permit reutilizarea valorilor și theming.",
    "expert": "Include dynamic updates, cascading și integration cu JS."
},

"web_sockets": {
    "beginner": "Conexiune live între client și server.",
    "professional": "Protocol full-duplex pentru comunicare în timp real.",
    "expert": "Include multiplexing, binary frames și fallback strategies."
},

"web_rtc": {
    "beginner": "Video și audio direct între două browsere.",
    "professional": "Real-Time Communication cu STUN/TURN.",
    "expert": "Include ICE negotiation, SDP și peer-to-peer optimization."
},

"fetch_api": {
    "beginner": "Metodă modernă de a cere date de la server.",
    "professional": "Promisiuni, streaming și control al request-urilor.",
    "expert": "Include AbortController, caching, retries și progressive streaming."
},

"rest_api": {
    "beginner": "API care folosește HTTP.",
    "professional": "Folosește resurse, metode și status codes.",
    "expert": "Include pagination, rate limiting, versioning și HATEOAS."
},

"graphql": {
    "beginner": "API unde ceri exact datele de care ai nevoie.",
    "professional": "Query language pentru API-uri flexibile.",
    "expert": "Include resolvers, schema stitching și caching avansat."
},

"web_assembly": {
    "beginner": "Cod foarte rapid în browser.",
    "professional": "WASM rulează aproape nativ în sandbox.",
    "expert": "Include memory management, imports/exports și streaming compilation."
},

"bundling": {
    "beginner": "Împachetezi fișierele într-unul singur.",
    "professional": "Optimizezi codul pentru producție.",
    "expert": "Include tree-shaking, code splitting și minification."
},

"minification": {
    "beginner": "Micșorezi fișierele.",
    "professional": "Elimini spații, comentarii și nume lungi.",
    "expert": "Include dead code removal și compression pipelines."
},

"code_splitting": {
    "beginner": "Împarți codul în bucăți mai mici.",
    "professional": "Încărcare la cerere pentru performanță.",
    "expert": "Include dynamic imports, route-based splitting și prefetching."
},

"lazy_loading": {
    "beginner": "Încarci ceva doar când ai nevoie.",
    "professional": "Optimizează performanța și reduce TTI.",
    "expert": "Include intersection observers, priority hints și predictive loading."
},

"dom_events": {
    "beginner": "Acțiuni precum click sau tastare.",
    "professional": "Event bubbling, capturing și listeners.",
    "expert": "Include delegation, passive listeners și event optimization."
},

"cookies": {
    "beginner": "Fișiere mici salvate de site-uri.",
    "professional": "Folosite pentru sesiuni și preferințe.",
    "expert": "Include SameSite, HttpOnly, Secure și expirare controlată."
},

"local_storage": {
    "beginner": "Salvezi date în browser.",
    "professional": "Persistă până la ștergere manuală.",
    "expert": "Include quotas, serialization și security considerations."
},

"session_storage": {
    "beginner": "Date salvate doar cât timp ai pagina deschisă.",
    "professional": "Scope per-tab, izolare strictă.",
    "expert": "Include storage events și fallback strategies."
},

"indexeddb": {
    "beginner": "O bază de date în browser.",
    "professional": "Stochează obiecte mari și structurate.",
    "expert": "Include transactions, cursors și versioning."
},

"csp": {
    "beginner": "Reguli care protejează site-ul.",
    "professional": "Content Security Policy previne XSS.",
    "expert": "Include nonce-uri, hashing și strict-dynamic."
},

"web_performance": {
    "beginner": "Cât de rapid se încarcă site-ul.",
    "professional": "Metrici: LCP, FID, CLS.",
    "expert": "Include preloading, compression, caching și edge rendering."
},

"seo": {
    "beginner": "Cum te găsește Google.",
    "professional": "Optimizare pentru crawlere și ranking.",
    "expert": "Include structured data, sitemaps și canonicalization."
},

"accessibility": {
    "beginner": "Site-uri ușor de folosit pentru toți.",
    "professional": "WCAG, ARIA roles și semantic HTML.",
    "expert": "Include keyboard navigation, screen readers și contrast rules."
},
"cpu_architecture": {
    "beginner": "Arhitectura CPU este modul în care este construit procesorul.",
    "professional": "Definește setul de instrucțiuni, pipeline-ul, cache-urile și modul de execuție.",
    "expert": "Include superscalar, out-of-order execution, branch prediction și micro-op fusion."
},

"gpu": {
    "beginner": "GPU-ul desenează imaginile pe ecran.",
    "professional": "Procesor paralel optimizat pentru calcule grafice și AI.",
    "expert": "Include CUDA cores, tensor cores, rasterization, ray tracing și compute shaders."
},

"npu": {
    "beginner": "NPU accelerează AI-ul.",
    "professional": "Neural Processing Unit optimizează inferența modelelor.",
    "expert": "Include INT8/FP8 pipelines, tensor accelerators și low-power AI compute."
},

"ram": {
    "beginner": "RAM este memoria rapidă a calculatorului.",
    "professional": "Stochează date temporare pentru procese active.",
    "expert": "Include DDR5, dual-channel, latency CL, bandwidth și XMP/EXPO profiles."
},

"ddr5": {
    "beginner": "DDR5 este cea mai nouă memorie RAM.",
    "professional": "Oferă frecvențe mari și eficiență energetică.",
    "expert": "Include PMIC onboard, dual 32-bit channels și on-die ECC."
},

"cache_memory": {
    "beginner": "Cache-ul este memoria ultra-rapidă a CPU-ului.",
    "professional": "Niveluri: L1, L2, L3 pentru reducerea latenței.",
    "expert": "Include inclusive/exclusive cache, victim cache și prefetching."
},

"motherboard": {
    "beginner": "Placa de bază leagă toate componentele.",
    "professional": "Conține chipset, sloturi RAM, PCIe, VRM și conectori.",
    "expert": "Include PCIe 5.0 lanes, DDR5 topology, VRM phases și BIOS/UEFI firmware."
},

"chipset": {
    "beginner": "Chipset-ul controlează comunicarea componentelor.",
    "professional": "Determină suportul pentru CPU, RAM și PCIe.",
    "expert": "Include PCH architecture, DMI bandwidth și lane allocation."
},

"pcie": {
    "beginner": "PCIe conectează plăcile video și SSD-urile.",
    "professional": "Standard de comunicație de mare viteză.",
    "expert": "Include PCIe 4.0/5.0, lane bifurcation și resizable BAR."
},

"nvme": {
    "beginner": "NVMe este un tip rapid de SSD.",
    "professional": "Folosește PCIe pentru viteze mari.",
    "expert": "Include NVMe 2.0, queue depth, ZNS și low-latency controllers."
},

"thermal_paste": {
    "beginner": "Pasta termică ajută procesorul să se răcească.",
    "professional": "Umple golurile dintre CPU și cooler.",
    "expert": "Include compuși metalici, ceramic, liquid metal și conductivitate W/mK."
},

"cooler": {
    "beginner": "Cooler-ul răcește procesorul.",
    "professional": "Tipuri: air cooling, AIO liquid cooling.",
    "expert": "Include heatpipes, pump RPM, radiator FPI și airflow optimization."
},

"psu": {
    "beginner": "PSU este sursa de alimentare.",
    "professional": "Transformă curentul pentru componente.",
    "expert": "Include 80+ ratings, single/multi-rail, ripple suppression și OCP/OVP protecții."
},

"vrm": {
    "beginner": "VRM controlează energia pentru CPU.",
    "professional": "Voltage Regulator Module stabilizează tensiunea.",
    "expert": "Include phases, MOSFETs, chokes și load-line calibration."
},

"bios": {
    "beginner": "BIOS pornește calculatorul.",
    "professional": "Inițializează hardware-ul și bootloader-ul.",
    "expert": "Include UEFI, secure boot, ACPI tables și firmware modules."
},

"uefi": {
    "beginner": "UEFI este versiunea modernă a BIOS-ului.",
    "professional": "Oferă interfață grafică și suport GPT.",
    "expert": "Include drivers, secure boot keys și runtime services."
},

"storage_controller": {
    "beginner": "Controlează stocarea.",
    "professional": "Gestionează SATA, NVMe și RAID.",
    "expert": "Include AHCI, NVMe queues și hardware RAID accelerators."
},

"raid": {
    "beginner": "RAID protejează datele.",
    "professional": "Combinație de discuri pentru performanță sau redundanță.",
    "expert": "Include RAID 0/1/5/10, parity calculations și hot spare."
},

"hdd": {
    "beginner": "HDD este un hard disk cu piese care se învârt.",
    "professional": "Stocare magnetică de capacitate mare.",
    "expert": "Include platters, RPM, seek time și SMR/CMR technologies."
},

"fan_curve": {
    "beginner": "Controlează viteza ventilatoarelor.",
    "professional": "Reglează RPM în funcție de temperatură.",
    "expert": "Include hysteresis, PWM tuning și noise optimization."
},

"thermal_throttling": {
    "beginner": "Procesorul încetinește când se încălzește.",
    "professional": "Protecție automată împotriva supraîncălzirii.",
    "expert": "Include power limits, temperature targets și dynamic frequency scaling."
},

"power_limit": {
    "beginner": "Limita de energie a procesorului.",
    "professional": "PL1/PL2 controlează performanța CPU.",
    "expert": "Include tau timing, EPP profiles și adaptive boost."
},

"overclocking": {
    "beginner": "Faci procesorul să meargă mai repede.",
    "professional": "Crești frecvența și tensiunea.",
    "expert": "Include voltage curves, LLC, stability testing și thermal headroom."
},

"undervolting": {
    "beginner": "Procesorul consumă mai puțin.",
    "professional": "Reduci tensiunea pentru eficiență.",
    "expert": "Include V/F curves, stability margins și power efficiency tuning."
},

"integrated_graphics": {
    "beginner": "GPU-ul integrat în procesor.",
    "professional": "Folosește RAM-ul sistemului.",
    "expert": "Include Xe graphics, RDNA iGPU și shared memory bandwidth."
},

"dedicated_gpu": {
    "beginner": "Placă video separată.",
    "professional": "Are memorie și procesor propriu.",
    "expert": "Include VRAM GDDR6X, PCIe bandwidth și cooling triple-fan."
},

"vram": {
    "beginner": "Memoria plăcii video.",
    "professional": "Stochează texturi și cadre.",
    "expert": "Include GDDR6X, memory bus width și effective bandwidth."
},

"die_shrink": {
    "beginner": "Procesorul devine mai mic și mai eficient.",
    "professional": "Reducerea nanometrilor crește performanța.",
    "expert": "Include 3nm, EUV lithography și transistor density."
},

"lithography": {
    "beginner": "Tehnologia de fabricare a cipului.",
    "professional": "Definește dimensiunea tranzistorilor.",
    "expert": "Include EUV, DUV, FinFET și GAAFET."
},

"gaafet": {
    "beginner": "Un tip nou de tranzistor.",
    "professional": "Gate-All-Around îmbunătățește controlul curentului.",
    "expert": "Include nanosheets, stacking și leakage reduction."
},

"finfet": {
    "beginner": "Tranzistor 3D modern.",
    "professional": "Reduce consumul și crește performanța.",
    "expert": "Include fin pitch, gate length și scaling limits."
},

"chiplet": {
    "beginner": "Procesor format din bucăți mai mici.",
    "professional": "Chiplet design îmbunătățește costul și scalabilitatea.",
    "expert": "Include Infinity Fabric, interposers și 3D stacking."
},

"3d_vcache": {
    "beginner": "Cache pus unul peste altul.",
    "professional": "Crește masiv memoria L3.",
    "expert": "Include TSV bonding, latency optimization și thermal constraints."
},

"memory_controller": {
    "beginner": "Controlează memoria RAM.",
    "professional": "Integrează canale și frecvențe.",
    "expert": "Include IMC tuning, gear modes și signal integrity."
},

"signal_integrity": {
    "beginner": "Semnalele trebuie să fie clare.",
    "professional": "Afectează stabilitatea componentelor.",
    "expert": "Include impedance matching, crosstalk și trace routing."
},

"pcb_layers": {
    "beginner": "Placa de bază are mai multe straturi.",
    "professional": "Straturile transportă semnale și energie.",
    "expert": "Include 6–12 layer stackups, ground planes și EMI shielding."
},

"emi": {
    "beginner": "Interferențe electrice.",
    "professional": "Afectează semnalele hardware.",
    "expert": "Include shielding, filtering și compliance standards."
},

"power_delivery": {
    "beginner": "Energia ajunge la componente.",
    "professional": "Include VRM, MOSFETs și cabluri.",
    "expert": "Include transient response, load balancing și PSU rail design."
},

"heatpipe": {
    "beginner": "Țeavă care mută căldura.",
    "professional": "Folosește evaporare și condensare.",
    "expert": "Include capillary action, vapor chambers și thermal conductivity."
},

"vapor_chamber": {
    "beginner": "Placă care răcește uniform.",
    "professional": "Distribuie căldura pe suprafață mare.",
    "expert": "Include wick structure, phase change și high-TDP cooling."
},

"fan_bearing": {
    "beginner": "Mecanismul ventilatorului.",
    "professional": "Tipuri: sleeve, ball, fluid dynamic.",
    "expert": "Include lifespan, noise curves și lubrication systems."
},

"power_connector": {
    "beginner": "Cablurile care alimentează componentele.",
    "professional": "Tipuri: ATX, EPS, PCIe.",
    "expert": "Include 12VHPWR, current limits și pin durability."
},

"12vhpwr": {
    "beginner": "Conector nou pentru plăci video.",
    "professional": "Suportă până la 600W.",
    "expert": "Include sense pins, cable bending rules și safety specs."
},

"firmware": {
    "beginner": "Software-ul din hardware.",
    "professional": "Controlează funcțiile de bază.",
    "expert": "Include microcode updates, secure firmware și hardware abstraction."
},

"microcode": {
    "beginner": "Instrucțiuni interne ale CPU.",
    "professional": "Corectează erori și optimizează execuția.",
    "expert": "Include patching, speculative execution fixes și ISA translation."
},
"operating_system": {
    "beginner": "Un sistem de operare este programul principal care controlează calculatorul.",
    "professional": "OS gestionează hardware-ul, procesele, memoria, fișierele și securitatea.",
    "expert": "Include kernel design, scheduling, memory management, IPC, drivers și virtualization."
},

"kernel": {
    "beginner": "Kernelul este inima sistemului de operare.",
    "professional": "Gestionează resursele hardware și comunicarea cu aplicațiile.",
    "expert": "Include monolithic kernels, microkernels, hybrid kernels și modular drivers."
},

"monolithic_kernel": {
    "beginner": "Kernel mare cu multe funcții în interior.",
    "professional": "Toate serviciile rulează în spațiul kernel pentru performanță.",
    "expert": "Include Linux kernel, syscall interface, module loading și low-level memory control."
},

"microkernel": {
    "beginner": "Kernel mic cu funcții minime.",
    "professional": "Majoritatea serviciilor rulează în user space pentru stabilitate.",
    "expert": "Include message passing IPC, fault isolation și modular OS design."
},

"process": {
    "beginner": "Un proces este un program care rulează.",
    "professional": "Include cod, memorie, resurse și thread-uri.",
    "expert": "Include PCB, scheduling states, context switching și isolation."
},

"thread": {
    "beginner": "Un thread este o parte dintr-un proces.",
    "professional": "Rulează în paralel în același spațiu de memorie.",
    "expert": "Include multithreading, synchronization, race conditions și thread pools."
},

"context_switch": {
    "beginner": "Calculatorul schimbă între procese.",
    "professional": "Salvează și restaurează starea proceselor.",
    "expert": "Include register saving, TLB flush, scheduling overhead și optimization."
},

"scheduler": {
    "beginner": "Decide ce proces rulează.",
    "professional": "Folosește algoritmi precum RR, FIFO, priority scheduling.",
    "expert": "Include CFS (Linux), preemption, load balancing și CPU affinity."
},

"memory_management": {
    "beginner": "OS gestionează memoria RAM.",
    "professional": "Include paginare, segmente și alocare.",
    "expert": "Include virtual memory, TLB, page faults și NUMA optimization."
},

"virtual_memory": {
    "beginner": "Memorie mai mare decât RAM-ul real.",
    "professional": "Folosește pagini și swap pentru extindere.",
    "expert": "Include demand paging, copy-on-write și memory overcommit."
},

"paging": {
    "beginner": "Împarte memoria în pagini mici.",
    "professional": "Mapează pagini virtuale la pagini fizice.",
    "expert": "Include multi-level page tables, huge pages și TLB caching."
},

"swap": {
    "beginner": "Spațiu pe disc folosit ca memorie.",
    "professional": "Mută pagini inactive pe storage.",
    "expert": "Include swap partitions, zswap, zram și memory pressure handling."
},

"filesystem": {
    "beginner": "Organizează fișierele pe disc.",
    "professional": "Include directoare, permisiuni și metadata.",
    "expert": "Include journaling, inodes, ext4, NTFS, APFS și copy-on-write."
},

"inode": {
    "beginner": "Un inode descrie un fișier.",
    "professional": "Conține metadata: owner, size, timestamps.",
    "expert": "Include block pointers, indirect blocks și filesystem indexing."
},

"permissions": {
    "beginner": "Controlează cine poate accesa fișierele.",
    "professional": "Include read/write/execute pentru user, group, others.",
    "expert": "Include ACLs, SELinux, AppArmor și capability-based security."
},

"bootloader": {
    "beginner": "Programul care pornește sistemul.",
    "professional": "Încarcă kernelul în memorie.",
    "expert": "Include GRUB, UEFI boot manager, chainloading și secure boot."
},

"system_call": {
    "beginner": "Aplicațiile cer ajutor de la OS.",
    "professional": "Syscalls oferă acces la kernel: read, write, fork.",
    "expert": "Include syscall tables, traps, interrupts și context transitions."
},

"interrupt": {
    "beginner": "Semnal care întrerupe procesorul.",
    "professional": "Folosit pentru hardware events și scheduling.",
    "expert": "Include ISR, interrupt vector table, masking și prioritization."
},

"driver": {
    "beginner": "Driverul ajută OS-ul să comunice cu hardware-ul.",
    "professional": "Software low-level pentru dispozitive.",
    "expert": "Include kernel modules, DMA, interrupts și hardware abstraction."
},

"dma": {
    "beginner": "Transfer de date fără CPU.",
    "professional": "Direct Memory Access optimizează performanța.",
    "expert": "Include DMA channels, burst mode și zero-copy operations."
},

"semaphore": {
    "beginner": "Ajută thread-urile să nu se calce pe picioare.",
    "professional": "Mecanism de sincronizare cu contor.",
    "expert": "Include binary semaphores, deadlocks și priority inversion."
},

"mutex": {
    "beginner": "Un lacăt pentru thread-uri.",
    "professional": "Permite acces exclusiv la resurse.",
    "expert": "Include spinlocks, recursive mutexes și lock contention."
},

"deadlock": {
    "beginner": "Două procese se blochează reciproc.",
    "professional": "Apare când resursele sunt cerute circular.",
    "expert": "Include avoidance, detection și recovery algorithms."
},

"init_system": {
    "beginner": "Programul care pornește serviciile.",
    "professional": "Init gestionează procesele de boot.",
    "expert": "Include systemd, runlevels, targets și service supervision."
},

"systemd": {
    "beginner": "Manager modern de servicii.",
    "professional": "Controlează boot-ul, logurile și procesele.",
    "expert": "Include unit files, journald, timers și cgroups integration."
},

"cgroups": {
    "beginner": "Limitează resursele pentru procese.",
    "professional": "Control groups gestionează CPU, RAM, I/O.",
    "expert": "Include cgroups v2, unified hierarchy și container isolation."
},

"namespaces": {
    "beginner": "Separă resursele între procese.",
    "professional": "Folosit în containere pentru izolare.",
    "expert": "Include PID, NET, MNT, IPC, UTS și USER namespaces."
},

"containerization": {
    "beginner": "Rulezi aplicații izolate.",
    "professional": "Containerele folosesc kernel-ul hostului.",
    "expert": "Include OCI runtime, overlayfs și namespace isolation."
},

"hypervisor": {
    "beginner": "Software care rulează mașini virtuale.",
    "professional": "Tipuri: Type 1 (bare-metal), Type 2 (hosted).",
    "expert": "Include KVM, Xen, VMware ESXi, VT-x și nested virtualization."
},

"virtual_machine": {
    "beginner": "Calculator în interiorul altui calculator.",
    "professional": "Rulează un OS complet izolat.",
    "expert": "Include virtual hardware, snapshots, passthrough și paravirtualization."
},

"paravirtualization": {
    "beginner": "VM care colaborează cu hypervisorul.",
    "professional": "OS-ul știe că rulează virtualizat.",
    "expert": "Include Xen PV, virtio drivers și optimized I/O."
},

"filesystem_journaling": {
    "beginner": "Protejează fișierele în caz de oprire bruscă.",
    "professional": "Jurnalizează operațiile înainte de scriere.",
    "expert": "Include ordered mode, writeback mode și metadata journaling."
},

"copy_on_write": {
    "beginner": "Copiază doar când modifici.",
    "professional": "Optimizează memoria și storage-ul.",
    "expert": "Include Btrfs, ZFS, snapshots și deduplication."
},

"zfs": {
    "beginner": "Un sistem de fișiere foarte avansat.",
    "professional": "Include RAID, snapshots și verificare integrității.",
    "expert": "Include ARC cache, copy-on-write, scrubbing și self-healing."
},

"btrfs": {
    "beginner": "Sistem modern de fișiere Linux.",
    "professional": "Oferă snapshots și subvolumes.",
    "expert": "Include COW, RAID, send/receive și checksumming."
},

"ntfs": {
    "beginner": "Sistemul de fișiere Windows.",
    "professional": "Include ACLs, journaling și compression.",
    "expert": "Include MFT, reparse points și transactional NTFS."
},

"apfs": {
    "beginner": "Sistemul de fișiere Apple.",
    "professional": "Optimizat pentru SSD-uri.",
    "expert": "Include snapshots, clones, encryption și space sharing."
},

"process_isolation": {
    "beginner": "Procesele nu se amestecă între ele.",
    "professional": "OS protejează memoria fiecărui proces.",
    "expert": "Include ASLR, DEP, sandboxing și seccomp."
},

"sandboxing": {
    "beginner": "Rulezi programe în siguranță.",
    "professional": "Izolează aplicațiile de sistem.",
    "expert": "Include App Sandbox, Flatpak, Snap și browser sandboxes."
},

"aslr": {
    "beginner": "Mută memoria ca hackerii să nu o ghicească.",
    "professional": "Address Space Layout Randomization previne exploit-uri.",
    "expert": "Include PIE binaries, stack randomization și entropy tuning."
},

"dep": {
    "beginner": "Blochează executarea codului rău.",
    "professional": "Data Execution Prevention protejează memoria.",
    "expert": "Include NX bit, W^X policies și hardware enforcement."
},

"ipc": {
    "beginner": "Procesele comunică între ele.",
    "professional": "Include pipes, sockets, shared memory.",
    "expert": "Include message queues, futexes și high-performance IPC."
},

"shell": {
    "beginner": "Programul unde scrii comenzi.",
    "professional": "Interpretează comenzi și rulează procese.",
    "expert": "Include Bash, Zsh, shellscripting și job control."
},

"initrd": {
    "beginner": "Mini-sistem care pornește înainte de OS.",
    "professional": "Conține drivere și scripturi de boot.",
    "expert": "Include initramfs, early userspace și kernel modules loading."
},
"database": {
    "beginner": "O bază de date stochează informații organizate.",
    "professional": "Gestionează date structurate sau nestructurate prin modele și interfețe.",
    "expert": "Include ACID, CAP, replicare, sharding, indexing și optimizare de performanță."
},

"sql": {
    "beginner": "SQL este limbajul pentru baze de date.",
    "professional": "Structured Query Language permite interogări, inserări și actualizări.",
    "expert": "Include query planning, joins complexe, indexing și optimizări de execuție."
},

"nosql": {
    "beginner": "NoSQL stochează date fără tabele.",
    "professional": "Modele: document, key-value, columnar, graph.",
    "expert": "Include sharding automat, replicare, consistency tuning și distributed queries."
},

"acid": {
    "beginner": "ACID garantează că datele sunt corecte.",
    "professional": "Atomicity, Consistency, Isolation, Durability.",
    "expert": "Include isolation levels, write-ahead logging și recovery algorithms."
},

"cap_theorem": {
    "beginner": "Nu poți avea totul în același timp.",
    "professional": "CAP: Consistency, Availability, Partition Tolerance.",
    "expert": "Include trade-offs pentru sisteme distribuite și modele CP/AP."
},

"index": {
    "beginner": "Indexul face căutările mai rapide.",
    "professional": "Structuri precum B-Tree și Hash Index optimizează query-urile.",
    "expert": "Include covering indexes, partial indexes și index selectivity."
},

"b_tree": {
    "beginner": "O structură de date pentru căutări rapide.",
    "professional": "Folosită în majoritatea indexurilor SQL.",
    "expert": "Include B+Tree, node splitting și disk page optimization."
},

"query_optimizer": {
    "beginner": "Optimizerul decide cum rulează o interogare.",
    "professional": "Creează planuri de execuție eficiente.",
    "expert": "Include cost-based optimization, statistics și join reordering."
},

"join": {
    "beginner": "Join combină date din două tabele.",
    "professional": "Tipuri: INNER, LEFT, RIGHT, FULL.",
    "expert": "Include hash join, merge join, nested loops și join elimination."
},

"normalization": {
    "beginner": "Organizezi datele ca să nu se repete.",
    "professional": "Forme normale: 1NF, 2NF, 3NF, BCNF.",
    "expert": "Include dependency analysis și schema optimization."
},

"denormalization": {
    "beginner": "Uneori duplici date pentru viteză.",
    "professional": "Reduce join-urile pentru performanță.",
    "expert": "Include materialized views și precomputed aggregates."
},

"replication": {
    "beginner": "Creezi copii ale bazei de date.",
    "professional": "Tipuri: master-slave, multi-master.",
    "expert": "Include sync/async replication, quorum și conflict resolution."
},

"sharding": {
    "beginner": "Împarți baza de date în bucăți.",
    "professional": "Distribuie datele pe mai multe servere.",
    "expert": "Include range/hash sharding, rebalancing și routing logic."
},

"partitioning": {
    "beginner": "Împarți tabelele mari în părți.",
    "professional": "Tipuri: range, list, hash.",
    "expert": "Include pruning, partition keys și hot partition mitigation."
},

"transaction": {
    "beginner": "Un set de operații care se execută împreună.",
    "professional": "Asigură consistență și rollback.",
    "expert": "Include isolation levels, locks și concurrency control."
},

"isolation_levels": {
    "beginner": "Controlează cum procesele văd datele.",
    "professional": "Read Uncommitted, Read Committed, Repeatable Read, Serializable.",
    "expert": "Include phantom reads, MVCC și snapshot isolation."
},

"mvcc": {
    "beginner": "Fiecare vede versiunea lui de date.",
    "professional": "Multi-Version Concurrency Control evită blocările.",
    "expert": "Include vacuuming, tuple versions și conflict detection."
},

"locking": {
    "beginner": "Blocările previn conflictele.",
    "professional": "Shared vs exclusive locks.",
    "expert": "Include deadlocks, lock escalation și row-level locking."
},

"write_ahead_log": {
    "beginner": "Scrii întâi în jurnal, apoi în disc.",
    "professional": "WAL asigură durabilitate.",
    "expert": "Include checkpoints, fsync și crash recovery."
},

"materialized_view": {
    "beginner": "O vedere salvată ca tabel.",
    "professional": "Optimizează interogările complexe.",
    "expert": "Include refresh strategies și incremental updates."
},

"stored_procedure": {
    "beginner": "Cod salvat în baza de date.",
    "professional": "Rulează logică pe server.",
    "expert": "Include triggers, execution plans și security contexts."
},

"trigger": {
    "beginner": "Cod care rulează automat.",
    "professional": "Se execută la insert/update/delete.",
    "expert": "Include cascading triggers și audit logic."
},

"cursor": {
    "beginner": "Parcurgi rândurile unul câte unul.",
    "professional": "Folosit pentru procesare secvențială.",
    "expert": "Include performance tuning și cursor types."
},

"redis": {
    "beginner": "Redis este o bază de date foarte rapidă.",
    "professional": "Key-value store în memorie.",
    "expert": "Include persistence, clustering, pub/sub și Lua scripting."
},

"mongodb": {
    "beginner": "MongoDB stochează documente JSON.",
    "professional": "Document store cu schema flexibilă.",
    "expert": "Include aggregation pipeline, sharding și replica sets."
},

"postgresql": {
    "beginner": "PostgreSQL este o bază de date puternică.",
    "professional": "SQL avansat, extensibil, open-source.",
    "expert": "Include JSONB, full-text search, partitioning și logical replication."
},

"mysql": {
    "beginner": "MySQL este o bază de date populară.",
    "professional": "Folosită în aplicații web.",
    "expert": "Include InnoDB engine, replication și query optimization."
},

"sqlite": {
    "beginner": "SQLite este o bază de date mică.",
    "professional": "Stochează totul într-un singur fișier.",
    "expert": "Include WAL mode, virtual tables și embedded usage."
},

"cassandra": {
    "beginner": "Cassandra este o bază de date distribuită.",
    "professional": "Column-family NoSQL pentru scalare masivă.",
    "expert": "Include tunable consistency, gossip protocol și LSM trees."
},

"elastic_search": {
    "beginner": "Elastic caută rapid în date.",
    "professional": "Engine de căutare bazat pe documente.",
    "expert": "Include inverted indexes, analyzers și distributed search."
},

"graph_database": {
    "beginner": "Stochează date ca noduri și conexiuni.",
    "professional": "Ideal pentru relații complexe.",
    "expert": "Include Cypher, traversal optimization și graph algorithms."
},

"neo4j": {
    "beginner": "Neo4j este o bază de date grafică.",
    "professional": "Folosește limbajul Cypher.",
    "expert": "Include clustering, pathfinding și graph analytics."
},

"columnar_database": {
    "beginner": "Stochează date pe coloane.",
    "professional": "Ideal pentru analytics.",
    "expert": "Include vectorized execution și compression encoding."
},

"bigquery": {
    "beginner": "BigQuery analizează date mari.",
    "professional": "Data warehouse serverless Google.",
    "expert": "Include columnar storage, Dremel engine și distributed execution."
},

"snowflake": {
    "beginner": "Snowflake este un depozit de date în cloud.",
    "professional": "Separă compute de storage.",
    "expert": "Include micro-partitions, time travel și zero-copy cloning."
},

"data_warehouse": {
    "beginner": "Stochează date pentru analiză.",
    "professional": "Optimizat pentru query-uri complexe.",
    "expert": "Include ETL/ELT, star schema și OLAP cubes."
},

"oltp": {
    "beginner": "Pentru tranzacții rapide.",
    "professional": "Online Transaction Processing.",
    "expert": "Include row storage, ACID și high concurrency."
},

"olap": {
    "beginner": "Pentru analiză de date.",
    "professional": "Online Analytical Processing.",
    "expert": "Include cubes, rollup, drill-down și columnar storage."
},

"etl": {
    "beginner": "Extragi, transformi și încarci date.",
    "professional": "Folosit în data warehouses.",
    "expert": "Include pipelines, orchestration și incremental loads."
},

"elt": {
    "beginner": "Extragi, încarci și apoi transformi.",
    "professional": "Folosit în cloud data warehouses.",
    "expert": "Include pushdown optimization și distributed compute."
},

"data_lake": {
    "beginner": "Un loc mare pentru toate datele.",
    "professional": "Stochează date brute în orice format.",
    "expert": "Include lakehouse, Delta Lake și schema-on-read."
},

"consistency_model": {
    "beginner": "Cum vede fiecare datele.",
    "professional": "Tipuri: strong, eventual, causal.",
    "expert": "Include quorum reads, vector clocks și CRDTs."
},

"crdt": {
    "beginner": "Structuri care se sincronizează singure.",
    "professional": "Conflict-free replicated data types.",
    "expert": "Include G-Counter, OR-Set și distributed convergence."
},

"lsm_tree": {
    "beginner": "Structură pentru scrieri rapide.",
    "professional": "Folosită în Cassandra, RocksDB.",
    "expert": "Include compaction, SSTables și bloom filters."
},

"bloom_filter": {
    "beginner": "Test rapid dacă ceva există.",
    "professional": "Probabilistic data structure.",
    "expert": "Include false positives, hashing și memory optimization."
},
"abacus": {
    "beginner": "Abacul este unul dintre primele instrumente de calcul.",
    "professional": "Folosit pentru operații aritmetice în civilizații antice.",
    "expert": "A influențat dezvoltarea algoritmilor timpurii și a conceptelor de numărare pozițională."
},

"analytical_engine": {
    "beginner": "O mașină de calcul imaginată de Charles Babbage.",
    "professional": "Primul design de calculator programabil mecanic.",
    "expert": "Include unitate aritmetică, memorie, control logic și conceptul de program stocat."
},

"ada_lovelace": {
    "beginner": "Ada Lovelace a fost prima programatoare.",
    "professional": "A scris primul algoritm pentru Analytical Engine.",
    "expert": "A introdus conceptul de programare simbolică și ideea de mașini generice."
},

"turing_machine": {
    "beginner": "Un model teoretic de calculator.",
    "professional": "Alan Turing a definit un sistem abstract pentru procesarea logică.",
    "expert": "Fundamentul calculabilității, al algoritmilor și al complexității computaționale."
},

"eniac": {
    "beginner": "Primul calculator electronic general-purpose.",
    "professional": "Folosea tuburi vidate și era programat manual.",
    "expert": "A introdus arhitecturi paralele și a influențat designul calculatoarelor moderne."
},

"transistor": {
    "beginner": "Transistorul a înlocuit tuburile vidate.",
    "professional": "Componentă electronică esențială pentru circuite moderne.",
    "expert": "A permis miniaturizarea, fiabilitatea și apariția microprocesoarelor."
},

"integrated_circuit": {
    "beginner": "Un cip care conține multe componente electronice.",
    "professional": "A integrat tranzistori pe o singură plăcuță de siliciu.",
    "expert": "A permis scalarea exponențială conform Legii lui Moore."
},

"moores_law": {
    "beginner": "Puterea calculatoarelor se dublează periodic.",
    "professional": "Numărul tranzistorilor se dublează la ~2 ani.",
    "expert": "A ghidat industria semiconductorilor timp de decenii."
},

"arpanet": {
    "beginner": "Precursorul internetului.",
    "professional": "Rețea creată pentru comunicații reziliente.",
    "expert": "A introdus packet switching și protocoale distribuite."
},

"http_protocol": {
    "beginner": "Protocolul care permite paginilor web să funcționeze.",
    "professional": "HyperText Transfer Protocol definește cereri și răspunsuri.",
    "expert": "A evoluat în HTTP/2 și HTTP/3 pentru performanță și multiplexare."
},

"world_wide_web": {
    "beginner": "Web-ul este colecția de site-uri de pe internet.",
    "professional": "Inventat de Tim Berners-Lee în 1989.",
    "expert": "A introdus HTML, URL și HTTP, fundamentul internetului modern."
},

"first_browser": {
    "beginner": "Primul browser web.",
    "professional": "WorldWideWeb (1990) a fost primul client web.",
    "expert": "A stabilit paradigma hyperlinkurilor și navigării vizuale."
},

"unix": {
    "beginner": "Un sistem de operare vechi și influent.",
    "professional": "Creat la Bell Labs, bazat pe simplitate și portabilitate.",
    "expert": "A inspirat Linux, macOS și standardele POSIX."
},

"linux": {
    "beginner": "Un sistem de operare open-source.",
    "professional": "Creat de Linus Torvalds în 1991.",
    "expert": "A devenit fundamentul serverelor, cloud-ului și dispozitivelor embedded."
},

"open_source_movement": {
    "beginner": "Software gratuit și deschis pentru toți.",
    "professional": "Promovează colaborarea și transparența.",
    "expert": "Include GPL, BSD, MIT și ecosisteme globale de contribuție."
},

"first_microprocessor": {
    "beginner": "Primul procesor pe un singur cip.",
    "professional": "Intel 4004 (1971) a integrat toate funcțiile CPU.",
    "expert": "A deschis era calculatoarelor personale și a embedded systems."
},

"apple_1": {
    "beginner": "Primul computer Apple.",
    "professional": "Creat de Steve Wozniak în 1976.",
    "expert": "A influențat designul PC-urilor și cultura hackerilor."
},

"ibm_pc": {
    "beginner": "Primul PC standardizat.",
    "professional": "IBM PC (1981) a definit arhitectura x86.",
    "expert": "A creat ecosistemul compatibil PC care domină piața."
},

"gui": {
    "beginner": "Interfață cu ferestre și iconițe.",
    "professional": "GUI a fost popularizată de Xerox, Apple și Microsoft.",
    "expert": "A schimbat paradigma interacțiunii om-calculator."
},

"smartphone_revolution": {
    "beginner": "Telefoanele au devenit computere.",
    "professional": "iPhone (2007) a redefinit mobile computing.",
    "expert": "A creat ecosisteme de aplicații, touch UI și conectivitate permanentă."
},

"cloud_computing_history": {
    "beginner": "Cloud-ul a schimbat modul în care folosim computerele.",
    "professional": "AWS (2006) a introdus infrastructura ca serviciu.",
    "expert": "A permis scalare globală, serverless și microservicii."
},

"ai_winter": {
    "beginner": "Perioade când AI-ul a stagnat.",
    "professional": "Lipsa progresului și finanțării în anii '70 și '90.",
    "expert": "A influențat cercetarea modernă și modelele statistice."
},

"deep_learning_revival": {
    "beginner": "AI-ul a devenit din nou popular.",
    "professional": "Rețelele neuronale au renăscut datorită GPU-urilor.",
    "expert": "Include ImageNet (2012), backprop modern și arhitecturi avansate."
},

"transformer_revolution": {
    "beginner": "Modelele AI au devenit mult mai inteligente.",
    "professional": "Transformers au înlocuit RNN-urile.",
    "expert": "Au permis LLM-uri, multimodalitate și scaling laws."
},

"first_programming_language": {
    "beginner": "Primul limbaj de programare.",
    "professional": "Fortran (1957) pentru calcule științifice.",
    "expert": "A introdus compilatoare, optimizări și paradigme moderne."
},

"c_language_history": {
    "beginner": "C este un limbaj vechi și puternic.",
    "professional": "Creat la Bell Labs pentru Unix.",
    "expert": "A influențat C++, Java, Rust și arhitectura sistemelor."
},

"object_oriented_history": {
    "beginner": "Programarea orientată pe obiecte.",
    "professional": "Smalltalk și Simula au introdus OOP.",
    "expert": "A influențat design patterns, encapsulation și arhitecturi enterprise."
},

"javascript_history": {
    "beginner": "JavaScript a fost creat pentru web.",
    "professional": "Lansat în 1995 de Brendan Eich.",
    "expert": "A evoluat în ecosistem global cu Node.js și framework-uri moderne."
},

"python_history": {
    "beginner": "Python este un limbaj ușor de învățat.",
    "professional": "Creat de Guido van Rossum în 1991.",
    "expert": "A devenit dominant în AI, scripting și educație."
},

"first_database_system": {
    "beginner": "Primele baze de date erau simple.",
    "professional": "IBM IMS (1966) a introdus modele ierarhice.",
    "expert": "A influențat SQL, relaționalul și NoSQL."
},

"relational_model": {
    "beginner": "Modelul relațional folosește tabele.",
    "professional": "Propus de Edgar Codd în 1970.",
    "expert": "A definit SQL, normalizarea și teoria bazelor de date."
},

"first_video_game": {
    "beginner": "Primul joc video.",
    "professional": "Pong (1972) a popularizat gaming-ul.",
    "expert": "A creat industria jocurilor și hardware dedicat."
},

"gpu_history": {
    "beginner": "GPU-urile au început cu grafică simplă.",
    "professional": "NVIDIA a introdus GPU-ul programabil.",
    "expert": "A dus la AI accelerators și ray tracing."
},

"semiconductor_revolution": {
    "beginner": "Cipurile au schimbat lumea.",
    "professional": "Tranzistorii au înlocuit tuburile vidate.",
    "expert": "A permis miniaturizare, mobilitate și computere personale."
},

"dotcom_bubble": {
    "beginner": "O perioadă de boom pe internet.",
    "professional": "Companiile tech au crescut rapid între 1995–2000.",
    "expert": "A dus la investiții masive, eșecuri și maturizarea industriei."
},

"social_media_evolution": {
    "beginner": "Rețelele sociale au schimbat comunicarea.",
    "professional": "MySpace, Facebook, Twitter au redefinit interacțiunea.",
    "expert": "Au influențat marketing, politică și comportamentul global."
},

"smart_home_history": {
    "beginner": "Casele au devenit inteligente.",
    "professional": "IoT a conectat dispozitivele casnice.",
    "expert": "Include protocoale, edge computing și automatizare."
},

"robotics_history": {
    "beginner": "Primele roboți erau simpli.",
    "professional": "Industrial robots au apărut în anii '60.",
    "expert": "Include autonomie, senzori, actuatori și AI integrat."
},

"quantum_computing_history": {
    "beginner": "Calculatoarele cuantice sunt foarte diferite.",
    "professional": "Bazate pe qubiți și superpoziție.",
    "expert": "Include algoritmi Shor, Grover și erori cuantice."
},

"encryption_history": {
    "beginner": "Criptarea protejează informațiile.",
    "professional": "De la cifrul lui Caesar la RSA.",
    "expert": "Include criptografie modernă, ECC și quantum-safe algorithms."
},

"blockchain_history": {
    "beginner": "Blockchain stochează date în lanțuri.",
    "professional": "Bitcoin (2009) a introdus ledger-ul distribuit.",
    "expert": "Include PoW, PoS, smart contracts și Web3."
},

"vr_history": {
    "beginner": "VR te pune într-o lume virtuală.",
    "professional": "Primele sisteme au apărut în anii '90.",
    "expert": "Include tracking, rendering și haptics."
},

"ar_history": {
    "beginner": "AR adaugă elemente digitale în lumea reală.",
    "professional": "Google Glass și HoloLens au popularizat conceptul.",
    "expert": "Include SLAM, spatial mapping și occlusion."
},

"ai_assistant_history": {
    "beginner": "Asistenții AI ajută utilizatorii.",
    "professional": "De la Siri la modele mari de limbaj.",
    "expert": "Include NLP, multimodalitate și reasoning avansat."
},
"software_engineering": {
    "beginner": "Software engineering înseamnă să construiești programe într-un mod organizat.",
    "professional": "Aplică principii, procese și metodologii pentru dezvoltarea software-ului.",
    "expert": "Include arhitectură, design patterns, CI/CD, testare, scalabilitate și mentenanță pe termen lung."
},

"software_development_lifecycle": {
    "beginner": "Ciclul de viață al software-ului arată pașii de la idee la produs.",
    "professional": "Faze: planificare, analiză, design, implementare, testare, deployment, mentenanță.",
    "expert": "Include SDLC models, governance, risk management și continuous improvement."
},

"agile": {
    "beginner": "Agile înseamnă să lucrezi rapid și flexibil.",
    "professional": "Metodologie bazată pe iterații, feedback și colaborare.",
    "expert": "Include Scrum, Kanban, ceremonies, velocity și incremental delivery."
},

"scrum": {
    "beginner": "Scrum este o metodă de lucru în echipă.",
    "professional": "Roluri: Product Owner, Scrum Master, Development Team.",
    "expert": "Include sprint planning, backlog refinement, burndown charts și empirical process control."
},

"kanban": {
    "beginner": "Kanban folosește un panou cu coloane pentru a urmări munca.",
    "professional": "Optimizează fluxul de lucru prin limitarea WIP.",
    "expert": "Include lead time, cycle time, throughput și continuous flow."
},

"waterfall": {
    "beginner": "Waterfall este un proces în pași fixați.",
    "professional": "Fiecare fază trebuie terminată înainte de următoarea.",
    "expert": "Include requirements freeze, documentation-heavy workflows și predictability trade-offs."
},

"requirements_engineering": {
    "beginner": "Stabilești ce trebuie să facă software-ul.",
    "professional": "Include elicitation, analiză, documentare și validare.",
    "expert": "Include use cases, user stories, acceptance criteria și traceability."
},

"use_case": {
    "beginner": "Un use case descrie cum folosește cineva aplicația.",
    "professional": "Definește interacțiuni între actor și sistem.",
    "expert": "Include scenarios, extensions și UML diagrams."
},

"user_story": {
    "beginner": "O propoziție care spune ce vrea utilizatorul.",
    "professional": "Format: As a…, I want…, so that…",
    "expert": "Include acceptance criteria, INVEST principles și backlog refinement."
},

"acceptance_criteria": {
    "beginner": "Reguli care spun când o funcție e gata.",
    "professional": "Definește comportamentul așteptat.",
    "expert": "Include Gherkin syntax, BDD și testable requirements."
},

"system_design": {
    "beginner": "Planul pentru cum funcționează un sistem mare.",
    "professional": "Include arhitectură, baze de date, API-uri și scalare.",
    "expert": "Include load balancing, caching, queues, microservices și distributed systems."
},

"architecture_patterns": {
    "beginner": "Modele pentru a organiza software-ul.",
    "professional": "Include layered, microservices, event-driven.",
    "expert": "Include CQRS, hexagonal architecture și domain-driven design."
},

"design_patterns": {
    "beginner": "Soluții gata făcute pentru probleme comune.",
    "professional": "Categorii: creational, structural, behavioral.",
    "expert": "Include Singleton, Factory, Adapter, Observer, Strategy."
},

"solid": {
    "beginner": "Reguli pentru a scrie cod bun.",
    "professional": "Principii pentru design modular și extensibil.",
    "expert": "Include SRP, OCP, LSP, ISP, DIP aplicate în arhitecturi mari."
},

"clean_code": {
    "beginner": "Cod ușor de citit.",
    "professional": "Include naming, structuri clare și evitarea duplicării.",
    "expert": "Include refactoring, readability metrics și maintainability."
},

"refactoring": {
    "beginner": "Îmbunătățești codul fără să schimbi funcționalitatea.",
    "professional": "Elimini duplicări și complexitate.",
    "expert": "Include code smells, patterns și continuous refactoring."
},

"technical_debt": {
    "beginner": "Lucruri făcute rapid care trebuie reparate mai târziu.",
    "professional": "Compromisuri care afectează mentenanța.",
    "expert": "Include debt tracking, prioritization și remediation strategies."
},

"version_control": {
    "beginner": "Un sistem care salvează toate versiunile codului.",
    "professional": "Git este standardul industriei.",
    "expert": "Include branching strategies, merge conflicts și CI integration."
},

"git_flow": {
    "beginner": "O metodă de a organiza branch-urile.",
    "professional": "Include develop, feature, release, hotfix.",
    "expert": "Include automation, tagging și release governance."
},

"continuous_integration": {
    "beginner": "Codul este testat automat când îl trimiți.",
    "professional": "CI rulează build-uri și teste la fiecare commit.",
    "expert": "Include pipelines, caching, parallel jobs și quality gates."
},

"continuous_delivery": {
    "beginner": "Software-ul poate fi lansat oricând.",
    "professional": "Automatizează deploy-ul până la producție.",
    "expert": "Include blue-green, canary, approvals și rollback."
},

"continuous_deployment": {
    "beginner": "Software-ul se lansează automat.",
    "professional": "Fiecare commit valid ajunge în producție.",
    "expert": "Include monitoring, auto-rollback și deployment safety."
},

"testing": {
    "beginner": "Testezi ca să vezi dacă software-ul merge.",
    "professional": "Tipuri: unit, integration, system, acceptance.",
    "expert": "Include TDD, mocks, coverage, flaky test mitigation."
},

"unit_test": {
    "beginner": "Testezi bucăți mici de cod.",
    "professional": "Izolezi funcții și clase.",
    "expert": "Include mocking, stubbing și deterministic tests."
},

"integration_test": {
    "beginner": "Testezi cum lucrează părțile împreună.",
    "professional": "Include API-uri, baze de date și servicii.",
    "expert": "Include contract testing și environment parity."
},

"system_test": {
    "beginner": "Testezi tot sistemul.",
    "professional": "Simulezi scenarii reale.",
    "expert": "Include end-to-end automation și performance validation."
},

"tdd": {
    "beginner": "Scrii testul înainte de cod.",
    "professional": "Ciclul: Red → Green → Refactor.",
    "expert": "Include test design, mocking strategies și maintainability."
},

"bdd": {
    "beginner": "Teste scrise ca propoziții.",
    "professional": "Behavior-Driven Development folosește Gherkin.",
    "expert": "Include living documentation și collaboration workflows."
},

"code_review": {
    "beginner": "Cineva verifică codul tău.",
    "professional": "Îmbunătățește calitatea și găsește erori.",
    "expert": "Include review guidelines, automation și knowledge sharing."
},

"api_design": {
    "beginner": "Creezi reguli pentru cum comunică aplicațiile.",
    "professional": "Include endpoints, metode, status codes.",
    "expert": "Include versioning, pagination, rate limiting și OpenAPI."
},

"microservices": {
    "beginner": "Aplicația e împărțită în bucăți mici.",
    "professional": "Servicii independente comunică prin API-uri.",
    "expert": "Include service discovery, resilience, observability și distributed tracing."
},

"monolith": {
    "beginner": "Totul într-o singură aplicație.",
    "professional": "Simplu de început, greu de scalat.",
    "expert": "Include modular monolith, boundaries și refactoring către microservices."
},

"event_driven_architecture": {
    "beginner": "Sistemele reacționează la evenimente.",
    "professional": "Folosește mesaje și pub/sub.",
    "expert": "Include Kafka, event sourcing și eventual consistency."
},

"domain_driven_design": {
    "beginner": "Construiești software după reguli de business.",
    "professional": "Include entities, value objects, aggregates.",
    "expert": "Include bounded contexts, ubiquitous language și strategic design."
},

"scalability": {
    "beginner": "Sistemul poate crește când ai mulți utilizatori.",
    "professional": "Scale vertical sau orizontal.",
    "expert": "Include sharding, caching, load balancing și distributed systems."
},

"performance_engineering": {
    "beginner": "Optimizezi ca software-ul să fie rapid.",
    "professional": "Include profiling, caching și optimizări.",
    "expert": "Include latency budgets, throughput tuning și bottleneck analysis."
},

"observability": {
    "beginner": "Vezi ce face aplicația.",
    "professional": "Include logs, metrics, traces.",
    "expert": "Include OpenTelemetry, dashboards și SLO management."
},

"logging": {
    "beginner": "Salvezi ce se întâmplă în aplicație.",
    "professional": "Include nivele: info, warn, error.",
    "expert": "Include structured logs, correlation IDs și retention policies."
},

"metrics": {
    "beginner": "Numere care arată cum merge aplicația.",
    "professional": "Include CPU, memorie, trafic.",
    "expert": "Include RED/USE metrics și time-series databases."
},

"tracing": {
    "beginner": "Urmărești cererile prin sistem.",
    "professional": "Analizezi latența și erorile.",
    "expert": "Include spans, context propagation și distributed tracing."
},

"security_engineering": {
    "beginner": "Protejezi aplicația.",
    "professional": "Include autentificare, autorizare, criptare.",
    "expert": "Include threat modeling, secure coding și zero trust."
},

"devops": {
    "beginner": "DevOps unește programatorii și administratorii.",
    "professional": "Automatizează livrarea software-ului.",
    "expert": "Include CI/CD, IaC, monitoring și release automation."
},

"site_reliability_engineering": {
    "beginner": "SRE menține site-urile în viață.",
    "professional": "Include SLO, SLA, error budgets.",
    "expert": "Include incident response, on-call, chaos engineering."
},

"chaos_engineering": {
    "beginner": "Testezi ce se întâmplă când ceva se strică.",
    "professional": "Simulezi erori pentru a crește reziliența.",
    "expert": "Include fault injection, chaos experiments și steady-state validation."
},

"documentation": {
    "beginner": "Scrii explicații pentru software.",
    "professional": "Include README, API docs, arhitectură.",
    "expert": "Include living documentation, ADRs și knowledge bases."
},

"software_maintenance": {
    "beginner": "Ai grijă de software după lansare.",
    "professional": "Include bug fixing, updates, improvements.",
    "expert": "Include lifecycle management, refactoring și long-term support."
},

"algorithm": {
    "beginner": "Un algoritm este un set de pași pentru a rezolva o problemă.",
    "professional": "Algoritmii sunt proceduri bine definite cu complexitate temporală și spațială.",
    "expert": "Include analiză Big-O, amortizare, probabilistic behavior și optimizări avansate."
},

"time_complexity": {
    "beginner": "Arată cât durează un algoritm.",
    "professional": "Măsoară creșterea timpului în funcție de input.",
    "expert": "Include O(1), O(n), O(n log n), O(n²), best/average/worst case și lower bounds."
},

"space_complexity": {
    "beginner": "Arată câtă memorie folosește un algoritm.",
    "professional": "Include memorie auxiliară și totală.",
    "expert": "Include trade-off-uri timp–spațiu și optimizări de memorie."
},

"big_o_notation": {
    "beginner": "Big-O arată cât de repede crește timpul unui algoritm.",
    "professional": "Măsoară limite superioare ale performanței.",
    "expert": "Include O, Ω, Θ, analiza amortizată și comparații între clase de complexitate."
},

"recursion": {
    "beginner": "Recursia este când o funcție se apelează pe ea însăși.",
    "professional": "Rezolvă probleme împărțindu-le în subprobleme.",
    "expert": "Include call stack, tail-call optimization și transformări în iterație."
},

"divide_and_conquer": {
    "beginner": "Împarți problema în bucăți mai mici.",
    "professional": "Folosit în algoritmi precum merge sort și quicksort.",
    "expert": "Include recurențe, Master Theorem și optimizări pentru subprobleme."
},

"dynamic_programming": {
    "beginner": "Salvezi rezultatele ca să nu le calculezi din nou.",
    "professional": "Folosește memoizare și tabulare.",
    "expert": "Include optimizări spațiale, DP pe grafuri și tehnici avansate precum bitmask DP."
},

"greedy_algorithm": {
    "beginner": "Alegi mereu cea mai bună opțiune la fiecare pas.",
    "professional": "Funcționează când soluția locală duce la soluția globală.",
    "expert": "Include matroizi, greedy choice property și optimizări pentru grafuri."
},

"backtracking": {
    "beginner": "Încerci soluții și te întorci dacă nu merg.",
    "professional": "Folosit în probleme combinatoriale.",
    "expert": "Include pruning, branch-and-bound și optimizări pentru search space."
},

"branch_and_bound": {
    "beginner": "Tai ramurile care nu duc la soluție.",
    "professional": "Optimizează căutarea în spații mari.",
    "expert": "Include bounding functions, heuristici și reducerea complexității."
},

"data_structure": {
    "beginner": "O structură de date organizează informația.",
    "professional": "Definește modul de stocare și acces al datelor.",
    "expert": "Include trade-off-uri între timp și memorie, implementări optimizate și structuri hibride."
},

"array": {
    "beginner": "O listă de elemente puse unul lângă altul.",
    "professional": "Acces O(1), inserare/ștergere costisitoare.",
    "expert": "Include cache locality, slicing și optimizări pentru vectori mari."
},

"linked_list": {
    "beginner": "Elemente legate între ele prin pointeri.",
    "professional": "Inserare/ștergere rapidă, acces lent.",
    "expert": "Include doubly linked lists, sentinel nodes și memory fragmentation."
},

"stack": {
    "beginner": "Structură LIFO: ultimul intrat, primul ieșit.",
    "professional": "Folosit în recursie, parsing și evaluarea expresiilor.",
    "expert": "Include stack frames, overflow/underflow și implementări optimizate."
},

"queue": {
    "beginner": "Structură FIFO: primul intrat, primul ieșit.",
    "professional": "Folosit în scheduling și BFS.",
    "expert": "Include circular buffers, deque și lock-free queues."
},

"deque": {
    "beginner": "Coada cu acces la ambele capete.",
    "professional": "Inserare/ștergere O(1) la ambele capete.",
    "expert": "Include implementări double-ended și optimizări pentru sliding window."
},

"hash_table": {
    "beginner": "Structură care găsește rapid elemente.",
    "professional": "Folosește hashing și buckets.",
    "expert": "Include collision resolution, rehashing și load factor tuning."
},

"binary_tree": {
    "beginner": "Fiecare nod are maxim doi copii.",
    "professional": "Folosit pentru căutare și organizare.",
    "expert": "Include traversări, balansare și optimizări pentru memorie."
},

"binary_search_tree": {
    "beginner": "Arbore unde stânga < nod < dreapta.",
    "professional": "Căutare, inserare, ștergere O(log n) în medie.",
    "expert": "Include balansare, rotații și degenerare în listă."
},

"avl_tree": {
    "beginner": "Arbore care se auto-balansază.",
    "professional": "Menține diferența de înălțime între subarbori.",
    "expert": "Include rotații, rebalancing și complexitate garantată."
},

"red_black_tree": {
    "beginner": "Arbore balansat cu reguli de culoare.",
    "professional": "Folosit în multe biblioteci standard.",
    "expert": "Include invariants, rotații și garantarea O(log n)."
},

"heap": {
    "beginner": "Structură unde elementul cel mai mare sau mic e sus.",
    "professional": "Folosit în priority queues.",
    "expert": "Include binary heap, Fibonacci heap și optimizări pentru Dijkstra."
},

"priority_queue": {
    "beginner": "Coada unde elementele au prioritate.",
    "professional": "Folosește heap pentru extragere rapidă.",
    "expert": "Include pairing heaps, binomial heaps și lazy deletion."
},

"trie": {
    "beginner": "Arbore pentru cuvinte.",
    "professional": "Folosit în autocomplete și căutări rapide.",
    "expert": "Include compressed tries, suffix tries și optimizări de memorie."
},

"suffix_array": {
    "beginner": "Listă cu toate sufixele unui șir.",
    "professional": "Folosit în căutări rapide în text.",
    "expert": "Include LCP array, Kasai algorithm și pattern matching avansat."
},

"suffix_tree": {
    "beginner": "Arbore care conține toate sufixele.",
    "professional": "Căutare în O(m).",
    "expert": "Include Ukkonen’s algorithm și aplicații în bioinformatică."
},

"graph": {
    "beginner": "Noduri conectate prin muchii.",
    "professional": "Poate fi orientat sau neorientat.",
    "expert": "Include reprezentări, traversări și algoritmi avansați."
},

"bfs": {
    "beginner": "Parcurge graful pe niveluri.",
    "professional": "Folosit pentru distanțe minime în grafuri neponderate.",
    "expert": "Include BFS bidirecțional și optimizări pentru grafuri sparse."
},

"dfs": {
    "beginner": "Parcurge graful în adâncime.",
    "professional": "Folosit pentru componente conexe și detectarea ciclurilor.",
    "expert": "Include DFS recursiv/iterativ și tree/forward/back edges."
},

"dijkstra": {
    "beginner": "Găsește cel mai scurt drum.",
    "professional": "Folosește priority queue.",
    "expert": "Include optimizări cu Fibonacci heap și grafuri sparse."
},

"bellman_ford": {
    "beginner": "Găsește drumuri scurte chiar cu valori negative.",
    "professional": "Mai lent decât Dijkstra.",
    "expert": "Include detectarea ciclurilor negative și optimizări."
},

"floyd_warshall": {
    "beginner": "Găsește toate drumurile scurte între toate nodurile.",
    "professional": "Algoritm O(n³).",
    "expert": "Include path reconstruction și optimizări pentru matrici."
},

"topological_sort": {
    "beginner": "Ordine pentru grafuri fără cicluri.",
    "professional": "Folosit în scheduling și compilatoare.",
    "expert": "Include Kahn’s algorithm și detectarea ciclurilor."
},

"minimum_spanning_tree": {
    "beginner": "Cel mai ieftin arbore care conectează toate nodurile.",
    "professional": "Algoritmi: Kruskal, Prim.",
    "expert": "Include DSU optimizat și implementări pentru grafuri dense."
},

"kruskal": {
    "beginner": "Construiește MST alegând muchii mici.",
    "professional": "Folosește sortare și DSU.",
    "expert": "Include union by rank și path compression."
},

"prim": {
    "beginner": "Construiește MST extinzând un nod.",
    "professional": "Folosește priority queue.",
    "expert": "Include implementări optimizate pentru grafuri sparse."
},

"disjoint_set_union": {
    "beginner": "Structură care unește grupuri.",
    "professional": "Operații: find, union.",
    "expert": "Include path compression și union by rank."
},

"string_matching": {
    "beginner": "Cauți un cuvânt într-un text.",
    "professional": "Algoritmi: KMP, Rabin-Karp.",
    "expert": "Include automata, suffix arrays și Z-algorithm."
},

"kmp": {
    "beginner": "Căutare rapidă în text.",
    "professional": "Folosește prefix function.",
    "expert": "Include optimizări pentru pattern-uri repetitive."
},

"rabin_karp": {
    "beginner": "Căutare cu hashing.",
    "professional": "Rapid pentru multiple pattern-uri.",
    "expert": "Include rolling hash și collision handling."
},

"z_algorithm": {
    "beginner": "Calculează potriviri în text.",
    "professional": "Folosit în pattern matching.",
    "expert": "Include Z-array și optimizări pentru string processing."
},

"bit_manipulation": {
    "beginner": "Lucrezi direct cu biți.",
    "professional": "Folosit pentru optimizări și structuri compacte.",
    "expert": "Include bitmasks, popcount și trick-uri avansate."
},

"sliding_window": {
    "beginner": "Te miști printr-un șir cu o fereastră.",
    "professional": "Optimizează probleme cu subsecvențe.",
    "expert": "Include two-pointer techniques și optimizări pentru O(n)."
},

"two_pointers": {
    "beginner": "Folosești doi indici care se mișcă.",
    "professional": "Folosit în probleme cu șiruri și intervale.",
    "expert": "Include optimizări pentru sortare și căutare."
},

"binary_search": {
    "beginner": "Cauți rapid într-o listă sortată.",
    "professional": "Împarte intervalul în două.",
    "expert": "Include lower_bound, upper_bound și aplicații pe răspuns."
},

"segment_tree": {
    "beginner": "Structură pentru intervale.",
    "professional": "Suportă query-uri și update-uri rapide.",
    "expert": "Include lazy propagation și structuri hibride."
},

"fenwick_tree": {
    "beginner": "Structură pentru sume parțiale.",
    "professional": "Fenwick Tree oferă update și query în O(log n).",
    "expert": "Include optimizări pentru prefix sums și memory layout."
},

"mathematics_for_cs": {
    "beginner": "Matematica pentru informatică te ajută să înțelegi cum funcționează algoritmii și calculatoarele.",
    "professional": "Include logică, probabilități, algebră, grafuri, combinatorică și analiză.",
    "expert": "Fundamentul AI, criptografiei, optimizării, complexității și sistemelor distribuite."
},

"set_theory": {
    "beginner": "Mulțimile sunt colecții de obiecte.",
    "professional": "Include operații: uniune, intersecție, diferență.",
    "expert": "Include cardinalitate, relații, funcții și infinite sets."
},

"logic": {
    "beginner": "Logica te ajută să iei decizii corecte.",
    "professional": "Include propoziții, predicate, tabele de adevăr.",
    "expert": "Include logică de ordinul întâi, cuantificatori și demonstrații formale."
},

"boolean_algebra": {
    "beginner": "Lucrezi cu adevărat și fals.",
    "professional": "Operații: AND, OR, NOT.",
    "expert": "Include simplificare, Karnaugh maps și circuite logice."
},

"proof_methods": {
    "beginner": "Demonstrezi că ceva e adevărat.",
    "professional": "Metode: inducție, contradicție, contrapozitivă.",
    "expert": "Include dovezi constructive, non-constructive și reducții."
},

"induction": {
    "beginner": "Demonstrezi ceva pentru toate numerele.",
    "professional": "Include baza și pasul inductiv.",
    "expert": "Include inducție puternică și inducție structurală."
},

"combinatorics": {
    "beginner": "Numărăm posibilități.",
    "professional": "Include permutări, combinații, aranjamente.",
    "expert": "Include principii avansate, counting arguments și bijections."
},

"permutations": {
    "beginner": "Ordine diferite ale acelorași elemente.",
    "professional": "n! permutări pentru n elemente.",
    "expert": "Include permutări cu repetiție și cicluri."
},

"combinations": {
    "beginner": "Alegi elemente fără să conteze ordinea.",
    "professional": "Formula C(n, k).",
    "expert": "Include identități combinatorice și binomial theorem."
},

"binomial_theorem": {
    "beginner": "Extinzi (a + b)^n.",
    "professional": "Coeficienții sunt numere binomiale.",
    "expert": "Include Pascal triangle, combinatorics și probabilități."
},

"probability": {
    "beginner": "Probabilitatea arată cât de posibil e un eveniment.",
    "professional": "Include evenimente, distribuții, independență.",
    "expert": "Include Bayes, Markov chains și probabilități condiționate."
},


"random_variable": {
    "beginner": "O variabilă care ia valori la întâmplare.",
    "professional": "Include discrete și continue.",
    "expert": "Include distribuții, așteptare și varianță."
},

"distributions": {
    "beginner": "Moduri în care apar valorile.",
    "professional": "Distribuții: uniformă, normală, binomială.",
    "expert": "Include Poisson, exponentială, gamma și heavy-tailed."
},

"normal_distribution": {
    "beginner": "Curba în formă de clopot.",
    "professional": "Media și deviația standard definesc forma.",
    "expert": "Include CLT, Z-scores și probabilități continue."
},

"linear_algebra": {
    "beginner": "Lucrezi cu vectori și matrici.",
    "professional": "Include operații, transformări și sisteme liniare.",
    "expert": "Include eigenvalues, SVD și optimizări pentru ML."
},

"vector": {
    "beginner": "O listă de numere.",
    "professional": "Reprezintă direcții și mărimi.",
    "expert": "Include spații vectoriale și norme."
},

"matrix": {
    "beginner": "O tabelă de numere.",
    "professional": "Folosită în transformări și sisteme liniare.",
    "expert": "Include factorizări, inversare și decompoziții."
},

"matrix_multiplication": {
    "beginner": "Combini două matrici.",
    "professional": "Folosit în grafuri și ML.",
    "expert": "Include optimizări, Strassen și algoritmi rapizi."
},

"determinant": {
    "beginner": "Un număr asociat unei matrici.",
    "professional": "Arată dacă matricea e invertibilă.",
    "expert": "Include proprietăți, cofactori și aplicații geometrice."
},

"calculus": {
    "beginner": "Studiul schimbării.",
    "professional": "Include derivate și integrale.",
    "expert": "Include optimizare, limite și analize avansate."
},

"derivative": {
    "beginner": "Cât de repede se schimbă ceva.",
    "professional": "Folosit în optimizare.",
    "expert": "Include gradient, Hessian și optimizare convexă."
},

"lagrange_multipliers": {
    "beginner": "Optimizezi cu restricții.",
    "professional": "Include funcția Lagrangian.",
    "expert": "Include KKT conditions și optimizare avansată."
},

"number_theory": {
    "beginner": "Studiul numerelor.",
    "professional": "Include divizibilitate, prime și congruențe.",
    "expert": "Fundamental în criptografie."
},

"prime_numbers": {
    "beginner": "Numere care se împart doar la ele și la 1.",
    "professional": "Folosite în algoritmi și criptografie.",
    "expert": "Include primality testing și distribuția primelor."
},

"modular_arithmetic": {
    "beginner": "Aritmetică pe resturi.",
    "professional": "Folosită în hashing și criptografie.",
    "expert": "Include invers modular, RSA și grupuri finite."
},

"gcd": {
    "beginner": "Cel mai mare divizor comun.",
    "professional": "Folosit în simplificări.",
    "expert": "Include algoritmul Euclid și extins."
},

"euclidean_algorithm": {
    "beginner": "Găsește GCD rapid.",
    "professional": "Folosește împărțiri repetate.",
    "expert": "Include versiunea extinsă pentru RSA."
},

"cryptographic_math": {
    "beginner": "Matematica din spatele criptării.",
    "professional": "Include modulo, exponențiere și prime.",
    "expert": "Include ECC, RSA și discrete logarithms."
},
"tree": {
    "beginner": "Un graf fără cicluri.",
    "professional": "Folosit în structuri de date.",
    "expert": "Include arbori binari, AVL și spanning trees."
},

"markov_chain": {
    "beginner": "Proces unde următorul pas depinde doar de cel curent.",
    "professional": "Include matrice de tranziție.",
    "expert": "Include steady-state, ergodicitate și modele probabilistice."
},

"information_theory": {
    "beginner": "Studiul informației.",
    "professional": "Include entropie și codare.",
    "expert": "Include mutual information și limite fundamentale."
},

"complex_numbers": {
    "beginner": "Numere cu partea imaginară.",
    "professional": "Folosit în semnale și fizică.",
    "expert": "Include planul complex și transformări."
},

"matrices_in_ml": {
    "beginner": "Matricile sunt folosite în AI.",
    "professional": "Reprezintă date și modele.",
    "expert": "Include operații tensoriale și GPU acceleration."
},

"tensors": {
    "beginner": "Un tensor este ca o matrice extinsă în mai multe dimensiuni.",
    "professional": "Un tensor este o structură multidimensională de date folosită în calcule numerice și rețele neuronale.",
    "expert": "Tensori reprezintă obiecte multilineare definite pe spații vectoriale, optimizate pentru operații GPU și paralelizare."
},

"vector_spaces": {
    "beginner": "Un spațiu vectorial este un loc unde vectorii pot fi adunați și înmulțiți cu numere.",
    "professional": "Un vector space este o structură algebrică definită prin axiome de adunare și scalare.",
    "expert": "Spațiile vectoriale sunt fundația pentru transformări liniare, baze, dimensiuni și decompoziții spectrale."
},

"dot_product": {
    "beginner": "Dot product arată cât de asemănați sunt doi vectori.",
    "professional": "Produsul scalar este suma produselor componentelor vectorilor.",
    "expert": "Dot product este o formă biliniară ce definește unghiuri, norme și proiecții în spații euclidiene."
},

"cross_product": {
    "beginner": "Cross product dă un vector perpendicular pe doi vectori.",
    "professional": "Produsul vectorial returnează un vector ortogonal cu magnitudine proporțională cu aria paralelogramului.",
    "expert": "Cross product este o operație specifică spațiului tridimensional, derivată din algebra exterioră."
},

"norms": {
    "beginner": "Norma arată cât de mare este un vector.",
    "professional": "O normă este o funcție care măsoară lungimea unui vector.",
    "expert": "Normele L1, L2 și L∞ definesc geometrii diferite și influențează regularizarea în ML."
},

"eigenvalues": {
    "beginner": "Un eigenvalue arată cât de mult se întinde un vector după o transformare.",
    "professional": "Eigenvalue este un scalar asociat unei transformări liniare care scalează un eigenvector.",
    "expert": "Spectrul unei matrice determină stabilitatea, convergența și comportamentul sistemelor dinamice."
},

"eigenvectors": {
    "beginner": "Un eigenvector își păstrează direcția după transformare.",
    "professional": "Un eigenvector este un vector care este scalat, nu rotit, de o matrice.",
    "expert": "Eigenvectorii formează baze spectrale folosite în PCA, diagonalizare și decompoziții ortogonale."
},

"jacobian": {
    "beginner": "Jacobianul arată cum se schimbă o funcție cu multe variabile.",
    "professional": "Jacobianul este matricea derivatelor parțiale ale unei funcții vectoriale.",
    "expert": "Jacobianul este esențial în optimizare, transformări de coordonate și backpropagation."
},

"hessian": {
    "beginner": "Hessianul arată cât de curbată este o funcție.",
    "professional": "Hessianul este matricea derivatelor parțiale de ordinul doi.",
    "expert": "Hessianul determină convexitatea, punctele de șa și direcțiile de curbură în optimizare."
},

"gradient": {
    "beginner": "Gradientul arată direcția în care crește cel mai mult o funcție.",
    "professional": "Gradientul este vectorul derivatelor parțiale ale unei funcții.",
    "expert": "Gradientul este folosit în optimizare, descent methods și analiza suprafețelor de pierdere."
},

"derivatives": {
    "beginner": "Derivata arată cât de repede se schimbă ceva.",
    "professional": "Derivata măsoară rata de variație a unei funcții.",
    "expert": "Derivatele sunt fundamentale în analiza funcțională, optimizare și modele continue."
},

"partial_derivatives": {
    "beginner": "O derivată parțială arată cum se schimbă o funcție când modifici doar o variabilă.",
    "professional": "Derivatele parțiale sunt derivate aplicate funcțiilor cu mai multe variabile.",
    "expert": "Sunt esențiale în gradient descent, optimizare multivariată și modele probabilistice."
},

"optimization": {
    "beginner": "Optimizarea înseamnă să găsești cea mai bună soluție.",
    "professional": "Optimization caută minimul sau maximul unei funcții.",
    "expert": "Optimizarea convexă, neliniară și stocastică stă la baza ML modern."
},

"convexity": {
    "beginner": "O funcție convexă are forma unui bol.",
    "professional": "Convexitatea garantează existența unui minim global unic.",
    "expert": "Analiza convexă permite optimizare eficientă și stabilitate în algoritmi ML."
},

"probability_distributions": {
    "beginner": "O distribuție arată cât de probabil este un rezultat.",
    "professional": "Distribuțiile modelează variabile aleatoare discrete sau continue.",
    "expert": "Distribuțiile Gauss, Bernoulli, Poisson și Exponential sunt fundamentale în ML și statistici."
},

"bayes_theorem": {
    "beginner": "Teorema lui Bayes arată cum se schimbă probabilitatea când aflăm informații noi.",
    "professional": "Bayes combină probabilități condiționate pentru a actualiza credințe.",
    "expert": "Bayesian inference stă la baza modelelor probabilistice și a ML generativ."
},

"expected_value": {
    "beginner": "Valoarea așteptată este media rezultatelor posibile.",
    "professional": "Expected value este media ponderată a tuturor valorilor posibile.",
    "expert": "EV este un operator liniar esențial în decizii, risc și modele statistice."
},

"variance": {
    "beginner": "Varianța arată cât de împrăștiate sunt valorile.",
    "professional": "Variance măsoară dispersia unei distribuții.",
    "expert": "Varianța este critică în ML pentru bias-variance tradeoff și regularizare."
},

"covariance": {
    "beginner": "Covarianța arată dacă două lucruri cresc împreună.",
    "professional": "Covariance măsoară relația liniară dintre două variabile.",
    "expert": "Covarianța este baza PCA, decompozițiilor spectrale și modelelor multivariate."
},

"correlation": {
    "beginner": "Corelația arată cât de legate sunt două variabile.",
    "professional": "Correlation este covarianța normalizată între două variabile.",
    "expert": "Corelația Pearson, Spearman și Kendall sunt folosite în analiză statistică avansată."
},

"svd": {
    "beginner": "SVD împarte o matrice în trei părți mai simple.",
    "professional": "Singular Value Decomposition exprimă o matrice ca UΣVᵀ.",
    "expert": "SVD este fundamental în reducerea dimensionalității, regularizare și analiza spectrului matricial."
},

"pca": {
    "beginner": "PCA reduce numărul de informații păstrând ce e important.",
    "professional": "Principal Component Analysis proiectează datele pe direcții de variație maximă.",
    "expert": "PCA folosește eigenvectors ai matricei de covarianță pentru compresie și noise reduction."
},

"entropy": {
    "beginner": "Entropia arată cât de haotice sunt datele.",
    "professional": "Entropy măsoară incertitudinea unei distribuții.",
    "expert": "Entropia Shannon este baza teoriei informației și a modelelor generative."
},

"kl_divergence": {
    "beginner": "KL arată cât de diferite sunt două distribuții.",
    "professional": "KL Divergence măsoară pierderea de informație între două distribuții.",
    "expert": "KL este folosit în VAEs, optimizare variatională și modele probabilistice."
},

"softmax": {
    "beginner": "Softmax transformă numerele în probabilități.",
    "professional": "Softmax normalizează vectori în distribuții discrete.",
    "expert": "Softmax este derivabil, stabil numeric și folosit în clasificare multi‑clasă."
},

"sigmoid": {
    "beginner": "Sigmoid transformă orice număr într-o valoare între 0 și 1.",
    "professional": "Sigmoid este o funcție logistică folosită în modele binare.",
    "expert": "Sigmoid suferă de vanishing gradients și este înlocuită în rețele profunde."
},

"relu": {
    "beginner": "ReLU lasă doar valorile pozitive.",
    "professional": "ReLU este o funcție de activare rapidă și simplă.",
    "expert": "ReLU îmbunătățește convergența, dar poate cauza dead neurons."
},

"leaky_relu": {
    "beginner": "Leaky ReLU lasă și valori negative mici.",
    "professional": "Leaky ReLU previne blocarea neuronilor la zero.",
    "expert": "Este o variantă stabilă pentru rețele adânci și modele generative."
},

"loss_function": {
    "beginner": "Loss arată cât de greșește modelul.",
    "professional": "Loss function măsoară diferența dintre predicții și valori reale.",
    "expert": "Loss-ul definește suprafața de optimizare și influențează convergența."
},

"mse": {
    "beginner": "MSE măsoară cât de departe sunt predicțiile de valori reale.",
    "professional": "Mean Squared Error penalizează erorile mari.",
    "expert": "MSE este convex, derivabil și folosit în regresie și optimizare numerică."
},

"cross_entropy": {
    "beginner": "Cross-entropy măsoară cât de bine prezice modelul clasele.",
    "professional": "Este o măsură între distribuția reală și cea prezisă.",
    "expert": "Cross-entropy este standard în clasificare și modele probabilistice."
},

"gradient_descent": {
    "beginner": "Gradient descent caută minimul unei funcții pas cu pas.",
    "professional": "GD actualizează parametrii în direcția opusă gradientului.",
    "expert": "GD are variante precum SGD, Momentum, RMSProp și Adam pentru convergență rapidă."
},

"learning_rate": {
    "beginner": "Learning rate spune cât de mari sunt pașii în învățare.",
    "professional": "LR controlează viteza de actualizare a parametrilor.",
    "expert": "LR scheduling, warmup și decay sunt critice pentru stabilitate."
},

"momentum": {
    "beginner": "Momentum ajută modelul să nu se blocheze.",
    "professional": "Momentum adaugă o componentă din gradientul anterior.",
    "expert": "Reduce oscilațiile și accelerează convergența în direcții consistente."
},

"adam_optimizer": {
    "beginner": "Adam este un optimizer foarte folosit în AI.",
    "professional": "Adam combină momentum cu adaptarea ratei de învățare.",
    "expert": "Adam folosește estimări ale momentelor gradientului pentru stabilitate și performanță."
},

"l1_regularization": {
    "beginner": "L1 ajută modelul să fie mai simplu.",
    "professional": "L1 penalizează valorile mari ale parametrilor.",
    "expert": "L1 produce modele sparse și selectează automat caracteristici."
},

"l2_regularization": {
    "beginner": "L2 previne supraînvățarea.",
    "professional": "L2 penalizează pătratul parametrilor.",
    "expert": "L2 stabilizează optimizarea și reduce variabilitatea modelului."
},

"bias_variance_tradeoff": {
    "beginner": "Bias-variance arată de ce un model poate greși.",
    "professional": "Este echilibrul între simplitate și flexibilitate.",
    "expert": "Tradeoff-ul determină generalizarea și performanța modelelor ML."
},

"stochastic_processes": {
    "beginner": "Un proces stocastic este ceva care se schimbă aleator în timp.",
    "professional": "Procesele stocastice modelează evoluții aleatoare.",
    "expert": "Markov chains, Brownian motion și procesele Gaussiene sunt fundamentale în ML."
},

"markov_chains": {
    "beginner": "Un lanț Markov depinde doar de starea curentă.",
    "professional": "Markov chains modelează tranziții între stări cu probabilități fixe.",
    "expert": "Sunt baza modelelor secvențiale, RL și generative probabilistice."
},

"gaussian_distribution": {
    "beginner": "Distribuția Gaussiană arată ca un clopot.",
    "professional": "Distribuția normală este definită de media și deviația standard.",
    "expert": "Gaussianele sunt fundamentale în inferență, modele liniare și procese stocastice."
},

"standard_deviation": {
    "beginner": "Deviația standard arată cât de împrăștiate sunt valorile.",
    "professional": "Este rădăcina pătrată a varianței.",
    "expert": "Deviația standard este esențială în estimări, intervale de încredere și ML statistic."
},

"z_score": {
    "beginner": "Z-score arată cât de departe e o valoare de medie.",
    "professional": "Z-score normalizează datele în funcție de deviația standard.",
    "expert": "Z-score este folosit în detectarea anomaliilor și standardizarea dataset-urilor."
},

"covariance_matrix": {
    "beginner": "O matrice de covarianță arată cum se mișcă variabilele împreună.",
    "professional": "Este o matrice simetrică ce conține covarianțele tuturor perechilor de variabile.",
    "expert": "Covariance matrix este baza PCA, SVD și modelelor multivariate Gaussiene."
},

"correlation_matrix": {
    "beginner": "O matrice de corelație arată cât de legate sunt variabilele.",
    "professional": "Normalizează covarianțele pentru a obține valori între -1 și 1.",
    "expert": "Este folosită în statistici, ML, finanțe și analiza dependențelor."
},

"law_of_large_numbers": {
    "beginner": "Cu cât faci mai multe măsurători, cu atât media devine mai precisă.",
    "professional": "LLN spune că media eșantionului converge către media populației.",
    "expert": "Este fundamentul estimării statistice și al modelelor probabilistice."
},

"central_limit_theorem": {
    "beginner": "Media multor valori devine o distribuție în formă de clopot.",
    "professional": "CLT spune că suma variabilelor independente converge spre o distribuție normală.",
    "expert": "Este baza inferenței statistice și a aproximărilor Gaussiene."
},

"log_likelihood": {
    "beginner": "Log-likelihood arată cât de bine se potrivește un model cu datele.",
    "professional": "Este logaritmul funcției de verosimilitate.",
    "expert": "Maximization of log-likelihood este fundamentul ML statistic și al modelelor generative."
},

"maximum_likelihood_estimation": {
    "beginner": "MLE găsește valorile care explică cel mai bine datele.",
    "professional": "MLE maximizează funcția de verosimilitate pentru parametri.",
    "expert": "MLE este baza modelelor statistice, regresiei și distribuțiilor parametrice."
},

"gradient_flow": {
    "beginner": "Gradient flow arată cum se schimbă parametrii în timp.",
    "professional": "Este o formulare continuă a gradient descent.",
    "expert": "Gradient flow analizează dinamica optimizării și stabilitatea modelelor."
},

"laplace_distribution": {
    "beginner": "Laplace seamănă cu o distribuție normală, dar cu cozi mai groase.",
    "professional": "Este o distribuție cu densitate exponențială simetrică.",
    "expert": "Laplace este folosită în L1 regularization și modele robuste."
},

"poisson_distribution": {
    "beginner": "Poisson modelează evenimente rare.",
    "professional": "Este o distribuție discretă pentru număr de evenimente într-un interval.",
    "expert": "Poisson este folosită în modele de trafic, rețele și procese stocastice."
},

"exponential_distribution": {
    "beginner": "Exponențiala modelează timpul până la un eveniment.",
    "professional": "Este o distribuție continuă cu rată constantă.",
    "expert": "Este baza proceselor Poisson și a modelelor de hazard."
},

"markov_property": {
    "beginner": "Markov înseamnă că viitorul depinde doar de prezent.",
    "professional": "Markov property definește procese cu memorie zero.",
    "expert": "Este fundamentul lanțurilor Markov, RL și modelelor secvențiale."
},

"bayesian_inference": {
    "beginner": "Bayesian înseamnă să actualizezi probabilitățile când afli informații noi.",
    "professional": "Bayesian inference folosește prior, likelihood și posterior.",
    "expert": "Este baza modelelor probabilistice, MCMC și variational inference."
},

"monte_carlo_methods": {
    "beginner": "Monte Carlo folosește aleatorul ca să rezolve probleme.",
    "professional": "Metodele Monte Carlo estimează valori prin eșantionare repetată.",
    "expert": "Sunt folosite în integrare, simulări, MCMC și modele generative."
},

"mcmc": {
    "beginner": "MCMC generează valori aleatorii care respectă o distribuție.",
    "professional": "Markov Chain Monte Carlo eșantionează distribuții complexe.",
    "expert": "Algoritmi: Metropolis-Hastings, Gibbs Sampling, HMC."
},

"information_gain": {
    "beginner": "Information gain arată câtă informație câștigi când afli ceva.",
    "professional": "IG măsoară reducerea entropiei după o împărțire.",
    "expert": "Este folosit în decizii, arbori de clasificare și teoria informației."
},

"fisher_information": {
    "beginner": "Fisher arată cât de multă informație conțin datele despre un parametru.",
    "professional": "Fisher Information măsoară sensibilitatea likelihood-ului.",
    "expert": "Este baza estimării eficiente și a teoriei statistice avansate."
},

"chi_square_distribution": {
    "beginner": "Chi-square este folosit pentru teste statistice.",
    "professional": "Este distribuția sumei pătratelor variabilelor normale standard.",
    "expert": "Este folosită în testele de independență, varianță și modele statistice."
},

"fourier_transform": {
    "beginner": "Fourier transform împarte un semnal în frecvențe.",
    "professional": "Transformata Fourier convertește funcții din domeniul timp în domeniul frecvență.",
    "expert": "FT este baza procesării semnalelor, convoluțiilor și modelelor spectrale."
},

"discrete_fourier_transform": {
    "beginner": "DFT analizează frecvențele dintr-un set finit de valori.",
    "professional": "DFT este versiunea discretă a transformatei Fourier.",
    "expert": "DFT este implementată eficient prin FFT și folosită în ML, audio și imagini."
},

"fft": {
    "beginner": "FFT este o metodă rapidă de a calcula DFT.",
    "professional": "Fast Fourier Transform reduce complexitatea de la O(n²) la O(n log n).",
    "expert": "FFT este esențială în procesare de semnal, convoluții rapide și modele spectrale."
},

"laplacian_operator": {
    "beginner": "Laplacianul arată cât de mult se schimbă o funcție în jurul unui punct.",
    "professional": "Operatorul Laplace este suma derivatelor parțiale de ordinul doi.",
    "expert": "Este folosit în PDEs, optimizare, grafuri și regularizare geometrică."
},

"gradient_norm": {
    "beginner": "Norma gradientului arată cât de abruptă e o funcție.",
    "professional": "Gradient norm măsoară magnitudinea vectorului gradient.",
    "expert": "Este folosită în stabilitate, optimizare și detectarea platourilor."
},

"jacobian_determinant": {
    "beginner": "Jacobian determinant arată cât se întinde spațiul după o transformare.",
    "professional": "Determinantul Jacobianului măsoară schimbarea volumului.",
    "expert": "Este esențial în schimbări de variabile, modele generative și fluxuri normale."
},

"normalizing_flows": {
    "beginner": "Normalizing flows transformă distribuții simple în unele complexe.",
    "professional": "Sunt modele generative bazate pe transformări invertibile cu Jacobian calculabil.",
    "expert": "NF folosesc bijecții parametrizate pentru modelarea densităților complexe."
},

"softplus": {
    "beginner": "Softplus este o versiune netedă a ReLU.",
    "professional": "Softplus este o funcție de activare derivabilă peste tot.",
    "expert": "Este folosită în modele probabilistice și rețele stabile numeric."
},

"swish": {
    "beginner": "Swish este o funcție de activare modernă.",
    "professional": "Swish = x * sigmoid(x), oferind tranziții line.",
    "expert": "Swish îmbunătățește performanța în rețele adânci și modele vizuale."
},

"elu": {
    "beginner": "ELU ajută rețelele să învețe mai repede.",
    "professional": "Exponential Linear Unit reduce biasul activărilor negative.",
    "expert": "ELU stabilizează gradientul și accelerează convergența în rețele profunde."
},

"hinge_loss": {
    "beginner": "Hinge loss este folosit în clasificare.",
    "professional": "Este funcția de pierdere pentru SVM-uri.",
    "expert": "Hinge loss maximizează marginile și îmbunătățește separabilitatea."
},

"logistic_loss": {
    "beginner": "Logistic loss este folosit pentru clasificare binară.",
    "professional": "Este derivat din log-likelihood pentru distribuția Bernoulli.",
    "expert": "Este baza regresiei logistice și a modelelor probabilistice binare."
},

"jacobi_method": {
    "beginner": "Jacobi rezolvă sisteme de ecuații pas cu pas.",
    "professional": "Este o metodă iterativă pentru sisteme liniare Ax=b.",
    "expert": "Jacobi este folosit în optimizare numerică și metode iterative paralele."
},

"gauss_seidel": {
    "beginner": "Gauss-Seidel îmbunătățește metoda Jacobi.",
    "professional": "Folosește valori actualizate imediat pentru convergență mai rapidă.",
    "expert": "Este eficient în sisteme sparse și metode numerice avansate."
},

"newton_method": {
    "beginner": "Newton găsește rapid rădăcinile unei funcții.",
    "professional": "Folosește derivata pentru a aproxima soluții.",
    "expert": "Newton este baza optimizării de ordinul doi și a metodelor Hessian-based."
},

"bfgs": {
    "beginner": "BFGS este o metodă avansată de optimizare.",
    "professional": "Este un quasi-Newton method ce aproximează Hessianul.",
    "expert": "BFGS este standard în optimizare neliniară și ML numeric."
},

"line_search": {
    "beginner": "Line search caută cât de mare să fie pasul în optimizare.",
    "professional": "Optimizează step size pentru convergență stabilă.",
    "expert": "Folosește criterii precum Wolfe și Armijo pentru stabilitate numerică."
},

"lipschitz_continuity": {
    "beginner": "Lipschitz arată cât de repede poate crește o funcție.",
    "professional": "O funcție este Lipschitz dacă diferențele sunt limitate de o constantă.",
    "expert": "Este esențială în stabilitate, convergență și analiza modelelor ML."
},

"manifold_learning": {
    "beginner": "Manifold learning descoperă structuri ascunse în date.",
    "professional": "Modelele presupun că datele trăiesc pe o varietate de dimensiune mică.",
    "expert": "Este baza algoritmilor precum t-SNE, UMAP și embedding-urilor geometrice."
},

"t_sne": {
    "beginner": "t-SNE reduce dimensiunea datelor pentru vizualizare.",
    "professional": "t-SNE păstrează structura locală a datelor în spații mici.",
    "expert": "Folosește distribuții Student-t și gradient descent pentru embedding-uri ne-liniare."
},

"umap": {
    "beginner": "UMAP reduce dimensiunea datelor pentru vizualizare.",
    "professional": "UMAP folosește grafuri și topologie pentru embedding-uri.",
    "expert": "UMAP optimizează structura locală și globală prin manifold approximation."
},

"cosine_similarity": {
    "beginner": "Cosine similarity arată cât de asemănați sunt doi vectori.",
    "professional": "Este măsura unghiului dintre doi vectori normalizați.",
    "expert": "Cosine similarity este folosită în NLP, embeddings și modele vectoriale."
},

"matrix_rank": {
    "beginner": "Rank arată câte informații unice are o matrice.",
    "professional": "Rangul este numărul de coloane liniar independente.",
    "expert": "Rank determină soluțiile sistemelor liniare și proprietățile transformărilor."
},

"condition_number": {
    "beginner": "Condition number arată cât de sensibilă este o matrice.",
    "professional": "Este raportul dintre valorile singulare maxime și minime.",
    "expert": "Cond. number determină stabilitatea numerică și erorile în optimizare."
},

"matrix_inverse": {
    "beginner": "Inversele anulează efectul unei matrice.",
    "professional": "A⁻¹ există doar pentru matrici pătrate și ne-singulare.",
    "expert": "Inversarea este instabilă numeric; se preferă factorizări precum LU."
},

"lu_decomposition": {
    "beginner": "LU împarte o matrice în două părți mai simple.",
    "professional": "A = LU, unde L este triunghiulară inferioară și U superioară.",
    "expert": "LU este folosită în sisteme liniare, inversare și factorizări numerice."
},

"qr_decomposition": {
    "beginner": "QR împarte o matrice în rotații și scalări.",
    "professional": "A = QR, unde Q este ortogonală și R triunghiulară.",
    "expert": "QR este stabilă numeric și folosită în regresie și SVD."
},

"cholesky_decomposition": {
    "beginner": "Cholesky este o factorizare rapidă pentru matrici speciale.",
    "professional": "A = LLᵀ pentru matrici simetrice pozitive definite.",
    "expert": "Este extrem de eficientă în optimizare și modele Gaussiene."
},

"positive_definite_matrix": {
    "beginner": "O matrice pozitiv definită are valori pozitive speciale.",
    "professional": "xᵀAx > 0 pentru orice vector nenul.",
    "expert": "Este esențială în optimizare, kernel methods și modele Gaussiene."
},

"kernel_functions": {
    "beginner": "Kernelurile transformă datele în forme noi.",
    "professional": "Kernel trick permite modelelor să lucreze în spații de dimensiuni mari.",
    "expert": "Kernels definesc spații Hilbert reproducing și modele SVM avansate."
},

"hilbert_space": {
    "beginner": "Hilbert space este un spațiu matematic foarte mare.",
    "professional": "Este un spațiu vectorial complet cu produs scalar.",
    "expert": "Hilbert spaces sunt baza modelelor kernel și a analizei funcționale."
},

"l2_space": {
    "beginner": "L2 este spațiul funcțiilor cu energie finită.",
    "professional": "L2 conține funcții cu integrală pătratică finită.",
    "expert": "Este un Hilbert space fundamental în ML și procesarea semnalelor."
},

"convolution": {
    "beginner": "Convoluția combină două semnale.",
    "professional": "Convolution este o integrală ce măsoară suprapunerea funcțiilor.",
    "expert": "Este baza CNN-urilor, filtrării și procesării semnalelor."
},

"autocorrelation": {
    "beginner": "Autocorrelation arată cât de asemănător e un semnal cu el însuși.",
    "professional": "Măsoară dependența dintre valori la diferite momente.",
    "expert": "Este folosită în time series, semnale și modele ARIMA."
},

"cross_correlation": {
    "beginner": "Cross-correlation compară două semnale.",
    "professional": "Măsoară similaritatea dintre două serii temporale.",
    "expert": "Este folosită în NLP, audio, vizual și analiza semnalelor."
},

"arima": {
    "beginner": "ARIMA prezice valori viitoare dintr-o serie temporală.",
    "professional": "ARIMA combină autoregresie, diferențiere și medie mobilă.",
    "expert": "Este un model statistic avansat pentru time series forecasting."
},

"stationarity": {
    "beginner": "Stationarity înseamnă că datele nu se schimbă în timp.",
    "professional": "O serie este staționară dacă media și varianța sunt constante.",
    "expert": "Staționaritatea este necesară pentru ARIMA și modele stocastice."
},

"spectral_density": {
    "beginner": "Spectral density arată ce frecvențe există într-un semnal.",
    "professional": "Este distribuția energiei în funcție de frecvență.",
    "expert": "Este folosită în time series, semnale și modele Gaussiene."
},

"brownian_motion": {
    "beginner": "Brownian motion este o mișcare aleatorie continuă.",
    "professional": "Este un proces stocastic cu variație infinită.",
    "expert": "Este baza modelelor Gaussiene, SDEs și proceselor continue."
},

"stochastic_differential_equations": {
    "beginner": "SDE-urile descriu sisteme cu aleator în timp.",
    "professional": "SDE combină ecuații diferențiale cu zgomot stocastic.",
    "expert": "Sunt folosite în RL, modele financiare și procese Gaussiene."
},

"graph_theory": {
    "beginner": "Graph theory studiază noduri și conexiuni.",
    "professional": "Grafurile sunt structuri formate din noduri și muchii.",
    "expert": "Teoria grafurilor este baza algoritmilor de rețea, optimizare și ML pe grafuri."
},

"adjacency_matrix": {
    "beginner": "O matrice care arată ce noduri sunt conectate.",
    "professional": "Adjacency matrix reprezintă grafuri prin valori binare sau ponderi.",
    "expert": "Este folosită în GNN-uri, spectrul grafurilor și analiza structurală."
},

"laplacian_matrix": {
    "beginner": "Laplacianul unui graf arată cum se răspândesc lucrurile pe el.",
    "professional": "L = D - A, unde D este gradul și A matricea de adiacență.",
    "expert": "Laplacianul este baza spectral graph theory și GNN-urilor moderne."
},

"spectral_graph_theory": {
    "beginner": "Studiază grafurile folosind matematică avansată.",
    "professional": "Folosește valorile proprii ale Laplacianului pentru a analiza grafuri.",
    "expert": "Este esențială în clustering, GNN-uri și decompoziții spectrale."
},

"markov_decision_process": {
    "beginner": "MDP ajută la luarea deciziilor pas cu pas.",
    "professional": "MDP modelează acțiuni, stări, tranziții și recompense.",
    "expert": "Este baza Reinforcement Learning și a optimizării secvențiale."
},

"bellman_equation": {
    "beginner": "Bellman arată cum se calculează valoarea unei decizii.",
    "professional": "Bellman definește relația recursivă dintre stări și recompense.",
    "expert": "Este fundamentul RL, dynamic programming și optimizării secvențiale."
},

"value_iteration": {
    "beginner": "Value iteration găsește cea mai bună strategie.",
    "professional": "Actualizează valorile stărilor până la convergență.",
    "expert": "Este un algoritm esențial în MDP-uri și RL discret."
},

"policy_iteration": {
    "beginner": "Policy iteration îmbunătățește o strategie pas cu pas.",
    "professional": "Alternează între evaluarea și îmbunătățirea politicii.",
    "expert": "Converge rapid în MDP-uri și modele RL clasice."
},

"expected_return": {
    "beginner": "Expected return arată cât câștigi în medie.",
    "professional": "Este suma recompenselor viitoare ponderate.",
    "expert": "Este baza funcțiilor de valoare în RL și optimizare secvențială."
},

"discount_factor": {
    "beginner": "Discount factor spune cât valorează viitorul.",
    "professional": "Gamma controlează importanța recompenselor viitoare.",
    "expert": "Afectează stabilitatea, convergența și comportamentul politicilor."
},


"mutual_information": {
    "beginner": "Mutual information arată cât de mult știu două lucruri unul despre altul.",
    "professional": "MI măsoară dependența dintre două variabile.",
    "expert": "Este folosită în selecția caracteristicilor, clustering și modele generative."
},

"fisher_kernel": {
    "beginner": "Fisher kernel combină statistica cu ML.",
    "professional": "Folosește gradientul log-likelihood pentru reprezentări.",
    "expert": "Este folosit în modele generative, SVM-uri și embedding-uri statistice."
},

"borel_sigma_algebra": {
    "beginner": "O structură matematică pentru a defini probabilități.",
    "professional": "Sigma-algebra conține mulțimi măsurabile.",
    "expert": "Este baza teoriei măsurii și a probabilităților riguroase."
},

"measure_theory": {
    "beginner": "Measure theory spune cum măsurăm lucruri abstracte.",
    "professional": "Generalizează lungimea, aria și volumul.",
    "expert": "Este fundamentul probabilităților moderne și al modelelor continue."
},

"lebesgue_integral": {
    "beginner": "Lebesgue este o metodă avansată de integrare.",
    "professional": "Integrează funcții folosind măsuri, nu intervale.",
    "expert": "Este esențial în probabilități, ML continuu și analiza funcțională."
},

"functional_analysis": {
    "beginner": "Studiază funcții ca obiecte matematice.",
    "professional": "Analizează spații de funcții și operatori liniari.",
    "expert": "Este baza kernel methods, Hilbert spaces și modelelor avansate."
},

"banach_space": {
    "beginner": "Banach space este un spațiu matematic complet.",
    "professional": "Este un spațiu vectorial normat complet.",
    "expert": "Banach spaces sunt fundamentale în optimizare și analiza numerică."
},

"operator_norm": {
    "beginner": "Operator norm arată cât de mult poate întinde un operator.",
    "professional": "Măsoară magnitudinea transformărilor liniare.",
    "expert": "Este folosită în stabilitate, optimizare și analiza operatorilor."
},

"spectral_radius": {
    "beginner": "Spectral radius arată cât de puternică e o matrice.",
    "professional": "Este valoarea proprie cu magnitudinea maximă.",
    "expert": "Determină stabilitatea sistemelor dinamice și convergența metodelor iterative."
},

"riemannian_geometry": {
    "beginner": "Riemannian geometry studiază suprafețe curbate.",
    "professional": "Folosește metrici pentru a măsura distanțe pe varietăți.",
    "expert": "Este baza optimizării pe manifolduri și a modelelor geometrice în ML."
},

"manifold": {
    "beginner": "Un manifold este o suprafață care local arată ca un spațiu obișnuit.",
    "professional": "Este o structură topologică ce permite coordonate locale.",
    "expert": "Manifoldurile sunt fundamentale în geometrie, ML și embedding-uri."
},

"geodesic": {
    "beginner": "O geodezică este cel mai scurt drum pe o suprafață curbată.",
    "professional": "Geodesicele minimizează distanța în metrici Riemanniene.",
    "expert": "Sunt folosite în optimizare geometrică și modele pe manifolduri."
},

"jacobian_vector_product": {
    "beginner": "JVP arată cum se schimbă o funcție într-o direcție.",
    "professional": "Este produsul dintre Jacobian și un vector.",
    "expert": "JVP este esențial în backpropagation eficient și autodif."
},

"hessian_vector_product": {
    "beginner": "HVP arată cum se schimbă gradientul într-o direcție.",
    "professional": "Este produsul dintre Hessian și un vector.",
    "expert": "HVP permite optimizare de ordinul doi fără a calcula Hessianul complet."
},

"proximal_operator": {
    "beginner": "Proximal operator ajută la optimizare cu reguli speciale.",
    "professional": "Este o generalizare a proiecțiilor în optimizare convexă.",
    "expert": "Proximal methods sunt baza algoritmilor moderni de optimizare."
},

"subgradient": {
    "beginner": "Subgradientul este o versiune extinsă a gradientului.",
    "professional": "Este folosit pentru funcții care nu sunt derivabile.",
    "expert": "Subgradient methods sunt critice în optimizare convexă și L1."
},

"lagrange_multiplier": {
    "beginner": "Lagrange ajută la optimizare cu restricții.",
    "professional": "Folosește multipli pentru a încorpora constrângeri.",
    "expert": "Este baza optimizării neliniare și a dualității."
},

"duality_gap": {
    "beginner": "Duality gap arată cât de aproape e soluția de optim.",
    "professional": "Este diferența dintre soluția primală și duală.",
    "expert": "Este folosit în optimizare convexă și validarea soluțiilor."
},

"wasserstein_distance": {
    "beginner": "Wasserstein arată cât costă să transformi o distribuție în alta.",
    "professional": "Este o distanță între distribuții bazată pe transport optim.",
    "expert": "Este folosită în GAN-uri, modele generative și geometrie statistică."
},

"earth_movers_distance": {
    "beginner": "EMD arată cât efort trebuie să muți masa unei distribuții.",
    "professional": "Este o implementare practică a distanței Wasserstein.",
    "expert": "Este folosită în vizualizare, clustering și modele generative."
},

"barycenter": {
    "beginner": "Barycenter este media unor puncte.",
    "professional": "Este un punct care minimizează distanțele ponderate.",
    "expert": "Wasserstein barycenters sunt folosiți în modele generative și transport optim."
},

"sobolev_space": {
    "beginner": "Sobolev space este un spațiu de funcții speciale.",
    "professional": "Conține funcții cu derivate slabe integrabile.",
    "expert": "Este baza PDEs, optimizării și modelelor continue."
},

"fourier_series": {
    "beginner": "Fourier series descompune funcții în unde simple.",
    "professional": "Reprezintă funcții periodice ca sumă de sinusoide.",
    "expert": "Este folosită în semnale, PDEs și modele spectrale."
},

"bessel_functions": {
    "beginner": "Bessel functions apar în probleme circulare.",
    "professional": "Sunt soluții ale ecuațiilor diferențiale speciale.",
    "expert": "Apar în fizică, semnale și modele matematice avansate."
},

"gamma_function": {
    "beginner": "Gamma este o versiune extinsă a factorialului.",
    "professional": "Generalizează factorialul pentru numere reale și complexe.",
    "expert": "Este folosită în distribuții statistice și modele matematice."
},

"beta_function": {
    "beginner": "Beta este o funcție specială legată de Gamma.",
    "professional": "Este definită printr-o integrală simetrică.",
    "expert": "Apare în distribuții, probabilități și analiza funcțională."
},

"stirling_approximation": {
    "beginner": "Stirling aproximează factoriale mari.",
    "professional": "n! ≈ sqrt(2πn) (n/e)^n.",
    "expert": "Este folosită în entropie, combinatorică și ML statistic."
},


"generating_functions": {
    "beginner": "Generating functions transformă secvențe în funcții.",
    "professional": "Sunt instrumente pentru analiză combinatorică.",
    "expert": "Folosite în probabilități, recurențe și modele discrete."
},

"tensor_decomposition": {
    "beginner": "Tensor decomposition împarte un tensor în părți mai simple.",
    "professional": "Include CP, Tucker și alte factorizări pentru date multidimensionale.",
    "expert": "Este folosită în modele generative, compresie și analiză de date de ordin înalt."
},

"tucker_decomposition": {
    "beginner": "Tucker reduce dimensiunea unui tensor.",
    "professional": "Descompune tensorul în factori și un nucleu central.",
    "expert": "Este baza compresiei tensoriale și a modelelor multilineare."
},

"cp_decomposition": {
    "beginner": "CP împarte un tensor în componente simple.",
    "professional": "Canonical Polyadic decomposition exprimă tensorul ca sumă de produse exterioare.",
    "expert": "Este folosită în analiză latentă, recomandări și modele probabilistice."
},

"kronecker_product": {
    "beginner": "Kronecker combină două matrici într-una mare.",
    "professional": "Este un produs matricial special folosit în structuri bloc.",
    "expert": "Apare în modele tensoriale, grafuri și optimizare numerică."
},

"hadamard_product": {
    "beginner": "Hadamard înmulțește element cu element.",
    "professional": "Produsul Hadamard este operația element-wise între matrici.",
    "expert": "Este folosit în ML, convoluții și modele numerice."
},

"sparse_matrices": {
    "beginner": "Sparse matrices au multe zerouri.",
    "professional": "Sunt optimizate pentru memorie și viteză.",
    "expert": "Critice în grafuri, NLP, rețele mari și optimizare numerică."
},

"sparse_coding": {
    "beginner": "Sparse coding reprezintă datele cu cât mai puține valori.",
    "professional": "Optimizează reprezentări sparse pentru semnale și imagini.",
    "expert": "Este baza dictionary learning și modelelor generative sparse."
},

"wavelet_transform": {
    "beginner": "Wavelet transform analizează semnale la diferite scări.",
    "professional": "Folosește funcții wavelet pentru decompoziții multi‑rezoluție.",
    "expert": "Este folosită în compresie, denoising și modele spectrale."
},

"haar_wavelet": {
    "beginner": "Haar este cea mai simplă wavelet.",
    "professional": "Folosește funcții pătrate pentru decompoziții rapide.",
    "expert": "Este baza multor algoritmi de compresie și analiză discretă."
},

"sobol_sequences": {
    "beginner": "Sobol sequences sunt numere pseudo-aleatoare speciale.",
    "professional": "Sunt secvențe low-discrepancy pentru eșantionare eficientă.",
    "expert": "Folosite în Monte Carlo, simulări și optimizare globală."
},

"latin_hypercube_sampling": {
    "beginner": "LHS e o metodă de a alege puncte dintr-un spațiu.",
    "professional": "Împarte spațiul în intervale egale pentru eșantionare uniformă.",
    "expert": "Este folosită în optimizare, simulări și modele probabilistice."
},

"curse_of_dimensionality": {
    "beginner": "În dimensiuni mari, totul devine greu.",
    "professional": "Datele devin sparse, distanțele devin neintuitive.",
    "expert": "Afectează clustering, optimizare, ML și modele statistice."
},

"random_projection": {
    "beginner": "Random projection reduce dimensiunea datelor.",
    "professional": "Folosește matrici aleatoare pentru a păstra distanțele.",
    "expert": "Se bazează pe Johnson–Lindenstrauss lemma pentru embedding-uri eficiente."
},

"johnson_lindenstrauss_lemma": {
    "beginner": "JL spune că poți reduce dimensiunea fără să pierzi distanțele.",
    "professional": "Asigură păstrarea aproximativă a distanțelor în spații mici.",
    "expert": "Este baza random projections și a ML pe date mari."
},

"graph_embeddings": {
    "beginner": "Graph embeddings transformă nodurile în vectori.",
    "professional": "Reprezintă structura grafurilor în spații continue.",
    "expert": "Folosite în GNN-uri, recomandări și modele relaționale."
},

"positional_encoding": {
    "beginner": "Positional encoding arată ordinea elementelor.",
    "professional": "Transformers folosesc funcții sinusoidale pentru poziții.",
    "expert": "Este baza modelelor secvențiale moderne și a atenției."
},

"attention_weights": {
    "beginner": "Attention arată ce este important într-o secvență.",
    "professional": "Calculează relevanța dintre elemente prin produse scalare.",
    "expert": "Este fundamentul Transformers, LLM-urilor și modelelor moderne."
},

"soft_attention": {
    "beginner": "Soft attention este o versiune netedă a atenției.",
    "professional": "Folosește softmax pentru a normaliza scorurile.",
    "expert": "Este complet derivabil și folosit în toate modelele moderne."
},

"hard_attention": {
    "beginner": "Hard attention alege doar câteva elemente importante.",
    "professional": "Folosește selecție discretă și sampling.",
    "expert": "Necesită tehnici precum REINFORCE pentru antrenare."
},

"variational_inference": {
    "beginner": "VI aproximează distribuții greu de calculat.",
    "professional": "Optimizează o familie de distribuții pentru a apropia posteriorul.",
    "expert": "Este baza VAEs, modelelor probabilistice și ML generativ."
},
 
 }
        


# -----------------------------
 GESTIUNEA SESIUNII
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "user_level" not in st.session_state:
    st.session_state.user_level = "beginner"

if "failed_logins" not in st.session_state:
    st.session_state.failed_logins = {}

if "user_db" not in st.session_state:
    st.session_state.user_db = load_user_db()


# -----------------------------
 AUTENTIFICARE
# -----------------------------
MAX_FAILED = 5
LOCKOUT_SECONDS = 300

def is_locked(user):
    info = st.session_state.failed_logins.get(user)
    if not info:
        return False
    if info["count"] < MAX_FAILED:
        return False
    return time.time() - info["last"] < LOCKOUT_SECONDS

def register_failed(user):
    if not user:
        user = "unknown"
    info = st.session_state.failed_logins.get(user, {"count": 0, "last": 0})
    info["count"] += 1
    info["last"] = time.time()
    st.session_state.failed_logins[user] = info

def reset_failed(user):
    if user in st.session_state.failed_logins:
        del st.session_state.failed_logins[user]

if not st.session_state.logged_in:
    auth_choice_label = translate_text("Autentificare sau Înregistrare", lang_map[st.session_state.lang])
    st.subheader(auth_choice_label)

    auth_option_1 = translate_text("Autentificare", lang_map[st.session_state.lang])
    auth_option_2 = translate_text("Creează Cont Nou", lang_map[st.session_state.lang])

    auth_choice = st.radio(
        translate_text("Alege o opțiune:", lang_map[st.session_state.lang]),
        [auth_option_1, auth_option_2]
    )

    user_db = st.session_state.user_db

    if auth_choice == auth_option_1:
        user = st.text_input(translate_text("👤 Utilizator", lang_map[st.session_state.lang]))
        pin = st.text_input(translate_text("🔑 Parolă", lang_map[st.session_state.lang]), type="password")

        if user and is_locked(user):
            st.error(translate_text("Cont blocat temporar după prea multe încercări. Încearcă mai târziu.", lang_map[st.session_state.lang]))
        elif st.button(translate_text("Autentificare", lang_map[st.session_state.lang])):
            if user in user_db and verify_pwd(pin, user_db[user]["password"]):
                reset_failed(user)
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.messages = st.session_state.chat_history.get(user, [])
                st.success(translate_text(f"Bun venit, {user}!", lang_map[st.session_state.lang]))
                st.rerun()
            else:
                register_failed(user)
                st.error(translate_text("Autentificare eșuată.", lang_map[st.session_state.lang]))

    else:
        new_user = st.text_input(translate_text("👤 Alege un nume de utilizator", lang_map[st.session_state.lang]))
        new_pin = st.text_input(translate_text("🔑 Alege o parolă", lang_map[st.session_state.lang]), type="password")

        if st.button(translate_text("Creează Cont", lang_map[st.session_state.lang])):
            if not new_user or not new_pin:
                st.error(translate_text("Completează utilizator și parolă.", lang_map[st.session_state.lang]))
            elif new_user in user_db:
                st.error(translate_text("Utilizator existent.", lang_map[st.session_state.lang]))
            elif len(new_pin) < 8:
                st.error(translate_text("Parola minim 8 caractere.", lang_map[st.session_state.lang]))
            else:
                user_db[new_user] = {
                    "password": hash_pwd(new_pin),
                    "created_at": time.time()
                }
                st.session_state.user_db = user_db
                save_user_db(user_db)
                st.success(translate_text("Cont creat!", lang_map[st.session_state.lang]))


 -----------------------------
INTERFAȚA PRINCIPALĂ
 -----------------------------
else:
    if not fortress.verify():
        st.error("⚠️ AEGIS FORTRESS: Modificare neautorizată detectată!")
        st.code("Sistemul a fost blocat pentru protecție.")
        st.stop()

    level_map = {
        "beginner": "🟢 Începător",
        "professional": "🟡 Profesionist",
        "expert": "🔴 Expert"
    }

    st.session_state.user_level = st.selectbox(
        "📊 Nivelul tău:",
        ["beginner", "professional", "expert"],
        format_func=lambda x: level_map[x]
    )

    st.success(translate_text(f"Salut, {st.session_state.user}!", lang_map[st.session_state.lang]))

    if st.button(translate_text("➕ Chat Nou", lang_map[st.session_state.lang])):
        st.session_state.messages = []
        st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input(translate_text("Scrie un mesaj...", lang_map[st.session_state.lang])):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner(translate_text("AEGIS se gândește...", lang_map[st.session_state.lang])):
                prompt_ro = translate_text(prompt, "ro").lower()
                found = False
                response_ro = ""

                for key in st.session_state.knowledge:
                    if key in prompt_ro:
                        term_data = st.session_state.knowledge[key]

                        if isinstance(term_data, dict):
                            level = st.session_state.user_level
                            parts = [f"**📚 Definiție:**\n{term_data[level]}"]

                            if "code" in term_data:
                                parts.append(f"\n**💻 Cod:**\n```python\n{term_data['code']}\n```")

                            if "real_world" in term_data:
                                parts.append(f"\n**🌍 În viața reală:**\n{term_data['real_world']}")

                            if "quiz" in term_data:
                                q = term_data["quiz"]
                                parts.append(f"\n**🧠 Quiz:**\n{q['question']}")
                                for opt in q["options"]:
                                    parts.append(f"  {'✅' if opt == q['answer'] else '⬜'} {opt}")

                            if "related" in term_data:
                                parts.append(f"\n**🔗 Vezi și:** {', '.join(term_data['related'])}")

                            response_ro = "\n".join(parts)
                        else:
                            response_ro = term_data

                        found = True
                        break

                if not found:
                    web_result = kosandra_blade(prompt_ro)
                    response_ro = (
                        f"Am căutat în universul digital și am găsit: {web_result}"
                        if web_result else translate_text("Nu am această informație încă.", lang_map[st.session_state.lang])
                    )

                final_response = translate_text(response_ro, lang_map[st.session_state.lang])
                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})

        st.session_state.chat_history[st.session_state.user] = st.session_state.messages
