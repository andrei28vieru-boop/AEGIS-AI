import streamlit as st
import hashlib
import bcrypt
import json
import time
from pathlib import Path

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
        
         # ============================================
        # 💎 AEGIS LEVEL — Interactive Mentor (90 terms)
        # ============================================
        
        "api": {
            "beginner": "Un API e ca un chelner într-un restaurant. Tu comanzi mâncarea, el merge la bucătărie și îți aduce farfuria. API-ul duce cererea ta la un server și aduce răspunsul înapoi.",
            "professional": "Un API (Application Programming Interface) este un set de reguli și protocoale care permite două aplicații software să comunice. API-urile REST folosesc HTTP și JSON pentru a transfera date între client și server.",
            "expert": "La nivel arhitectural, un API trebuie proiectat cu versionare, rate limiting, autentificare OAuth 2.0, și documentație OpenAPI. Performanța depinde de caching strategies, paginare și optimizarea query-urilor.",
            "code": "# Exemplu Python: Apelarea unui API\nimport requests\nresponse = requests.get('https://api.example.com/data')\ndata = response.json()\nprint(data)",
            "real_world": "Când folosești aplicația Meteo, ea folosește un API să ceară date de la serverul de vreme. Când postezi pe Instagram, aplicația folosește API-ul Instagram să trimită poza ta.",
            "quiz": {"question": "Ce protocol folosesc majoritatea API-urilor moderne?", "options": ["HTTP", "FTP", "SMTP", "SSH"], "answer": "HTTP"},
            "related": ["api rest", "json", "oauth", "http"]
        },
        
        "python": {
            "beginner": "Python e ca un limbaj pe care îl vorbești cu computerul. E simplu, ca engleza. Scrii ce vrei să facă, iar el execută. E perfect pentru începători!",
            "professional": "Python este un limbaj de programare high-level, interpretat, cu tipare dinamică. Este folosit în web development, data science, AI/ML și automatizări.",
            "expert": "Python 3.x oferă async/await, GIL pentru thread safety, și un ecosistem vast prin PyPI. Arhitectura permite OOP și programare funcțională.",
            "code": "print('Salut, lume!')\n\ndef salut(nume):\n    return f'Bun venit, {nume}!'\n\nprint(salut('Andrei'))",
            "real_world": "Python e folosit de NASA, Google, Netflix și Spotify.",
            "quiz": {"question": "Ce keyword definește o funcție în Python?", "options": ["func", "def", "function", "define"], "answer": "def"},
            "related": ["variabilă", "funcție", "clasă", "pip", "django"]
        },
        
        "ai": {
            "beginner": "Inteligența Artificială e ca un copil care învață. Îi arăți multe poze cu pisici, și el învață să recunoască o pisică. AI face același lucru — învață din date.",
            "professional": "AI este simularea proceselor de inteligență umană. Subdomenii: Machine Learning, Deep Learning, NLP, Computer Vision.",
            "expert": "Implementările moderne folosesc Transformer, difuzie și reinforcement learning. Optimizarea necesită GPU-uri și tehnici de fine-tuning.",
            "code": "# Exemplu ML cu Scikit-learn\nfrom sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier()\nmodel.fit(X_train, y_train)\nprint(model.score(X_test, y_test))",
            "real_world": "AI e peste tot: Face ID, Google Maps, Netflix, Alexa, Siri.",
            "quiz": {"question": "Care este un subset al AI?", "options": ["Machine Learning", "Word", "Chrome", "Photoshop"], "answer": "Machine Learning"},
            "related": ["machine learning", "deep learning", "neural network", "nlp"]
        },
        
        "samsung": {
            "beginner": "Samsung e ca un magazin imens de tehnologie. Fac telefoane Galaxy, laptopuri Galaxy Book, ceasuri Galaxy Watch, și multe altele!",
            "professional": "Samsung Electronics este lider global în tehnologie: procesoare, ecrane AMOLED, memorii și dispozitive Galaxy.",
            "expert": "Samsung domină semiconductori (DRAM, NAND), display-uri și inovația pliabilă. Ecosistemul Galaxy integrează telefoane, tablete, laptopuri, watch-uri și IoT.",
            "code": "# Conectare SmartThings API\nimport requests\nheaders = {'Authorization': 'Bearer TOKEN'}\nr = requests.get('https://api.smartthings.com/v1/devices', headers=headers)",
            "real_world": "Samsung face de la telefoane la frigidere inteligente. Galaxy Book5 Pro 360 e laptopul tău viitor!",
            "quiz": {"question": "Cum se numește asistentul AI Samsung?", "options": ["Siri", "Alexa", "Bixby", "Cortana"], "answer": "Bixby"},
            "related": ["samsung galaxy book5 pro 360", "galaxy ai", "one ui 7"]
        },
        
        "cpu": {
            "beginner": "CPU-ul e creierul computerului. Tot ce faci — click, tastare, deschidere aplicație — trece prin CPU.",
            "professional": "CPU execută instrucțiuni prin ciclul fetch-decode-execute. Performanța: frecvență, core-uri, cache, arhitectură.",
            "expert": "Procesoarele moderne (Intel Core Ultra, Apple M4) folosesc 3nm, NPU pentru AI, DDR5 și PCIe 5.0.",
            "code": "import platform, os\nprint(platform.processor())\nprint(os.cpu_count())",
            "real_world": "CPU-ul e în laptop, telefon, PlayStation, mașini Tesla. Fiecare click e procesat de CPU.",
            "quiz": {"question": "Ce înseamnă CPU?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Power Utility", "Core Processing Utility"], "answer": "Central Processing Unit"},
            "related": ["gpu", "ram", "ssd", "intel", "amd"]
        },
        
        "samsung galaxy book5 pro 360": {
            "beginner": "E laptopul visurilor tale, Andrei! Subțire, se pliază, ecran superb, baterie toată ziua. Perfect pentru AEGIS!",
            "professional": "Laptop convertibil premium: AMOLED 2X 16\", Intel Core Ultra 7 Series 2, 16GB DDR5, 1TB SSD, S Pen, Wi-Fi 7, 25 ore baterie.",
            "expert": "Arhitectura Lunar Lake cu NPU 48 TOPS, display 500 nits HDR 120Hz, vapor chamber cooling, 1.66 kg.",
            "code": "book5 = {'display': '16 AMOLED 2X', 'cpu': 'Ultra 7 256V', 'ram': '16GB', 'ssd': '1TB', 'price': '13298 RON'}\nfor k,v in book5.items(): print(f'{k}: {v}')",
            "real_world": "Tu îl vei folosi pentru AEGIS — pe plajă în Spania, la Tucano în Sinaia, sau acasă noaptea.",
            "quiz": {"question": "Ce procesor are Book5 Pro 360?", "options": ["Ultra 7 256V", "M4", "Snapdragon", "Ryzen 9"], "answer": "Ultra 7 256V"},
            "related": ["samsung", "laptop", "intel", "windows 11"]
        },
        
        "cloud": {
            "beginner": "Cloud-ul e ca un hard disk uriaș pe internet. În loc să ții fișierele doar pe laptop, le pui 'în nor' și poți să le accesezi de oriunde, de pe orice dispozitiv.",
            "professional": "Cloud computing-ul livrează servicii de calcul (servere, stocare, baze de date, rețele) prin internet. Modele: IaaS (infrastructură), PaaS (platformă), SaaS (software). Lideri: AWS, Azure, Google Cloud.",
            "expert": "Arhitecturile cloud-native folosesc microservicii, containere (Docker, Kubernetes), serverless (AWS Lambda) și CI/CD. Optimizarea costurilor implică auto-scaling, reserved instances și FinOps.",
            "code": "# Upload fișier pe AWS S3\nimport boto3\ns3 = boto3.client('s3')\ns3.upload_file('fisier.txt', 'bucket', 'fisier.txt')\nprint('Upload complet!')",
            "real_world": "Google Drive, iCloud, Netflix, Instagram — toate folosesc cloud. Pozele tale de pe telefon sunt în cloud. AEGIS rulează pe Streamlit Cloud chiar acum!",
            "quiz": {"question": "Ce înseamnă SaaS?", "options": ["Software as a Service", "Storage as a System", "Server and Application Setup", "System as a Software"], "answer": "Software as a Service"},
            "related": ["aws", "azure", "google cloud", "saas", "docker", "serverless"]
        },

        "blockchain": {
            "beginner": "Blockchain-ul e ca un caiet de notițe pe care toată lumea poate scrie, dar nimeni nu poate șterge. Fiecare pagină e un 'bloc' legat de cel anterior — de aici 'lanț de blocuri'.",
            "professional": "Blockchain este un registru distribuit și descentralizat care înregistrează tranzacții immutable. Folosește consens (PoW, PoS), criptografie și smart contracts. Aplicații: criptomonede, DeFi, NFT-uri, supply chain.",
            "expert": "Implementările enterprise (Hyperledger, Corda) oferă blockchain privat. Scalabilitatea se rezolvă prin Layer 2 (Lightning Network, Polygon), sharding și rollups.",
            "code": "# Hash blockchain în Python\nimport hashlib, json\ndef create_block(data, prev):\n    block = {'data': data, 'prev': prev}\n    block['hash'] = hashlib.sha256(json.dumps(block).encode()).hexdigest()\n    return block",
            "real_world": "Bitcoin e cel mai faimos blockchain. Ethereum permite smart contracts. NFT-urile se vând pe blockchain.",
            "quiz": {"question": "Cine a creat Bitcoin?", "options": ["Elon Musk", "Satoshi Nakamoto", "Bill Gates", "Vitalik Buterin"], "answer": "Satoshi Nakamoto"},
            "related": ["bitcoin", "ethereum", "nft", "defi", "web3", "smart contract"]
        },
        
        "cybersecurity": {
            "beginner": "Securitatea cibernetică e ca o alarmă pentru casa ta digitală. Te protejează de hoți (hackeri), încuie ușile (parole) și te avertizează când cineva încearcă să intre.",
            "professional": "Cybersecurity protejează sisteme, rețele și date împotriva atacurilor digitale. Domenii: network security, application security, cryptography, incident response. Amenințări: malware, phishing, ransomware, DDoS, zero-day.",
            "expert": "Strategiile defense-in-depth implementează multiple layere: firewall (L3/L4), WAF (L7), IDS/IPS, SIEM, EDR/XDR. Zero Trust Architecture elimină perimetrul tradițional.",
            "code": "# Hash securizat parolă\nimport hashlib, os\ndef hash_pwd(p):\n    salt = os.urandom(32)\n    return salt + hashlib.pbkdf2_hmac('sha256', p.encode(), salt, 100000)",
            "real_world": "Când intri pe internet banking, conexiunea e criptată. WhatsApp folosește criptare end-to-end. Antivirusul blochează viruși.",
            "quiz": {"question": "Ce atac criptează fișierele și cere răscumpărare?", "options": ["Phishing", "Ransomware", "DDoS", "SQL Injection"], "answer": "Ransomware"},
            "related": ["firewall", "vpn", "encryption", "malware", "phishing"]
        },

        "docker": {
            "beginner": "Docker e ca o cutie magică în care pui codul tău cu tot ce are nevoie ca să ruleze. Poți să muți cutia pe orice computer și va funcționa la fel. Gata cu 'pe laptopul meu merge'!",
            "professional": "Docker este o platformă de containerizare care pachetează aplicațiile cu toate dependențele într-un container izolat. Containerele sunt lightweight față de VM-uri și rulează pe Docker Engine.",
            "expert": "Arhitectura Docker: Dockerfile → Image → Container. Orchestration cu Kubernetes, Docker Compose pentru multi-container, registry cu Docker Hub. Best practices: multi-stage builds, layer caching, non-root users.",
            "code": "# Dockerfile exemplu\nFROM python:3.11\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD ['streamlit', 'run', 'app.py']",
            "real_world": "AEGIS ar putea rula într-un container Docker! Așa l-ai putea deploya oriunde — pe orice server, în orice țară. Netflix, Spotify, Uber — toate folosesc containere.",
            "quiz": {"question": "Ce fișier definește un container Docker?", "options": ["Dockerfile", "docker.txt", "container.yml", "docker.cfg"], "answer": "Dockerfile"},
            "related": ["kubernetes", "docker compose", "container", "devops", "serverless"]
        },

        "machine learning": {
            "beginner": "Machine Learning e ca un copil care învață din exemple. Îi arăți 1000 de poze cu pisici, și el învață singur cum arată o pisică. Nu-i spui tu regulile — le descoperă singur!",
            "professional": "ML este un subset al AI unde algoritmii învață din date fără a fi programați explicit. Tipuri: supervised (date etichetate), unsupervised (pattern-uri ascunse), reinforcement (recompense).",
            "expert": "Algoritmi: Random Forest, XGBoost, SVM, Neural Networks. Optimizare: gradient descent, backpropagation. Evaluare: cross-validation, confusion matrix, ROC-AUC. Feature engineering și hyperparameter tuning.",
            "code": "# ML cu Scikit-learn\nfrom sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier()\nmodel.fit(X_train, y_train)\nprint(f'Acuratețe: {model.score(X_test, y_test):.2%}')",
            "real_world": "Când Netflix îți recomandă un film, când Google Maps prezice traficul, când banca detectează o tranzacție frauduloasă — Machine Learning e în spate.",
            "quiz": {"question": "Ce tip de ML folosește date etichetate?", "options": ["Supervised", "Unsupervised", "Reinforcement", "Manual"], "answer": "Supervised"},
            "related": ["deep learning", "neural network", "ai", "data science", "tensorflow"]
        },

        "firewall": {
            "beginner": "Un firewall e ca un bodyguard la intrarea într-un club. El verifică pe toți cei care vor să intre. Dacă ești pe listă, intri. Dacă nu, rămâi afară. Firewall-ul face același lucru cu datele.",
            "professional": "Un firewall monitorizează și filtrează traficul de rețea pe baza unor reguli de securitate predefinite. Poate fi hardware sau software și operează la nivel de rețea (Layer 3/4) sau aplicație (Layer 7).",
            "expert": "Next-Generation Firewall (NGFW) integrează IPS, DPI, SSL inspection și application awareness. Arhitecturi: perimeter firewall, distributed firewall, cloud firewall (AWS Security Groups, Azure NSG).",
            "code": "# Reguli firewall simplificate\nfirewall_rules = {\n    'allow': ['80', '443', '22'],\n    'deny': ['23', '21', '3389']\n}\ndef check_port(port):\n    return 'ALLOW' if port in firewall_rules['allow'] else 'DENY'",
            "real_world": "Routerul tău de acasă are un firewall încorporat. Windows are Windows Defender Firewall. Fiecare site web e protejat de un WAF (Web Application Firewall).",
            "quiz": {"question": "Ce face un firewall?", "options": ["Filtrează traficul", "Scrie cod", "Editează poze", "Trimite email-uri"], "answer": "Filtrează traficul"},
            "related": ["vpn", "ids", "ips", "encryption", "cybersecurity"]
        },

        "neural network": {
            "beginner": "O rețea neuronală e ca un creier artificial făcut din mulți 'neuroni' mici conectați între ei. Fiecare neuron primește informație, o procesează și o trimite mai departe. Împreună, rezolvă probleme complexe.",
            "professional": "O rețea neuronală artificială este inspirată de creierul uman, formată din straturi de neuroni interconectați. Fiecare conexiune are o pondere (weight) care se ajustează prin backpropagation.",
            "expert": "Arhitecturi: CNN (imagini), RNN/LSTM (secvențe), Transformer (NLP). Antrenare: forward pass, loss calculation, backward pass (gradient descent). Optimizare: Adam, SGD, learning rate scheduling.",
            "code": "# Rețea neuronală simplă cu Keras\nfrom tensorflow.keras.models import Sequential\nfrom tensorflow.keras.layers import Dense\nmodel = Sequential([\n    Dense(64, activation='relu'),\n    Dense(32, activation='relu'),\n    Dense(1, activation='sigmoid')\n])\nmodel.compile(optimizer='adam', loss='binary_crossentropy')",
            "real_world": "Când deblochezi telefonul cu fața, o rețea neuronală recunoaște fața ta. Când Google Translate traduce un text, o rețea neuronală face traducerea.",
            "quiz": {"question": "Ce algoritm ajustează ponderile într-o rețea neuronală?", "options": ["Backpropagation", "Quick Sort", "Binary Search", "Dijkstra"], "answer": "Backpropagation"},
            "related": ["deep learning", "machine learning", "cnn", "rnn", "transformer"]
        },

        "encryption": {
            "beginner": "Criptarea e ca un limbaj secret. Scrii un mesaj, îl transformi în ceva de necitit (criptezi), și doar persoana care are 'cheia' poate să-l citească (decripteze).",
            "professional": "Criptarea transformă datele într-un format codificat folosind algoritmi matematici. Tipuri: simetrică (AES — aceeași cheie) și asimetrică (RSA — cheie publică + privată).",
            "expert": "Standarde: AES-256 (guvernamental), RSA-4096, ECC. TLS 1.3 pentru web. Criptarea end-to-end (Signal Protocol). Hashing: SHA-256, bcrypt. Quantum-resistant cryptography în dezvoltare.",
            "code": "# Criptare simetrică cu Python\nfrom cryptography.fernet import Fernet\nkey = Fernet.generate_key()\ncipher = Fernet(key)\nencrypted = cipher.encrypt(b'Mesaj secret')\ndecrypted = cipher.decrypt(encrypted)",
            "real_world": "WhatsApp folosește criptare end-to-end. HTTPS (lacătul verde din browser) e criptare. Când plătești cu cardul online, datele sunt criptate.",
            "quiz": {"question": "Ce tip de criptare folosește două chei diferite?", "options": ["Asimetrică", "Simetrică", "Hashing", "Compresie"], "answer": "Asimetrică"},
            "related": ["decryption", "aes", "rsa", "ssl", "tls", "https"]
        },

        "kubernetes": {
            "beginner": "Kubernetes e ca un dirijor de orchestră. Ai multe containere (muzicieni) și Kubernetes se asigură că toate cântă la timp, că niciunul nu lipsește și că totul sună perfect.",
            "professional": "Kubernetes (K8s) este o platformă open-source pentru automatizarea deployment-ului, scalării și managementului containerelor. Componente: Pods, Nodes, Services, Deployments, ConfigMaps.",
            "expert": "Arhitectură: Control Plane (API Server, etcd, Scheduler) + Worker Nodes (kubelet, kube-proxy). Networking: CNI (Calico, Cilium). Service Mesh: Istio. GitOps: ArgoCD, Flux.",
            "code": "# Deployment Kubernetes (YAML)\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: aegis-app\nspec:\n  replicas: 3\n  selector:\n    matchLabels:\n      app: aegis\n  template:\n    spec:\n      containers:\n      - name: aegis\n        image: aegis:latest\n        ports:\n        - containerPort: 8501",
            "real_world": "Google, Netflix, Spotify — toate rulează pe Kubernetes. Când Netflix are milioane de utilizatori simultan, Kubernetes scalează automat serverele.",
            "quiz": {"question": "Ce e un Pod în Kubernetes?", "options": ["Cel mai mic obiect deployabil", "Un tip de bază de date", "Un limbaj de programare", "Un protocol de rețea"], "answer": "Cel mai mic obiect deployabil"},
            "related": ["docker", "docker compose", "helm", "istio", "devops", "microservices"]
        },

        "iot": {
            "beginner": "IoT (Internet of Things) e când obiectele din casa ta devin 'smart' și se conectează la internet. Frigiderul îți spune că ai rămas fără lapte, ceasul îți monitorizează somnul, becurile se aprind singure.",
            "professional": "IoT conectează dispozitive fizice (senzori, actuatori) la internet pentru colectare de date și control. Protocoale: MQTT, CoAP, Zigbee. Platforme: AWS IoT, Azure IoT Hub.",
            "expert": "Arhitecturi: Edge Computing (procesare locală), Fog Computing, Cloud IoT. Securitate: PKI pentru device-uri, OTA updates. Provocări: scalabilitate miliarde de device-uri, latență, interoperabilitate.",
            "code": "# Simulare senzor IoT\nimport random, time\nwhile True:\n    temp = random.uniform(20.0, 30.0)\n    print(f'Temperatură: {temp:.1f}°C')\n    time.sleep(5)",
            "real_world": "Galaxy Watch-ul tău e un dispozitiv IoT! La fel și Alexa, becurile Philips Hue, termostatele Nest, și mașinile Tesla conectate la internet.",
            "quiz": {"question": "Ce înseamnă IoT?", "options": ["Internet of Things", "Internet of Technology", "Input Output Transfer", "Internal Operating Tool"], "answer": "Internet of Things"},
            "related": ["arduino", "raspberry pi", "sensor", "cloud", "5g"]
        },

        "5g": {
            "beginner": "5G e a cincea generație de internet mobil. E ca și cum ai trece de la o șosea cu 2 benzi la o autostradă cu 100 de benzi. Totul e mai rapid, mai instant.",
            "professional": "5G este standardul de rețea mobilă cu viteze de până la 20 Gbps, latență sub 1ms și capacitate pentru 1 milion de device-uri pe km². Benzi: low-band, mid-band, mmWave.",
            "expert": "Arhitectură 5G: Network Slicing (rețele virtuale dedicate), MEC (Multi-access Edge Computing), beamforming. 3GPP Release 17/18. Aplicații critice: V2X (vehicule autonome), remote surgery, Industry 4.0.",
            "code": "# Verifică viteza internetului (conceptual)\nimport speedtest\nst = speedtest.Speedtest()\nprint(f'Download: {st.download()/1e6:.1f} Mbps')\nprint(f'Upload: {st.upload()/1e6:.1f} Mbps')\nprint(f'Ping: {st.results.ping} ms')",
            "real_world": "Telefonul tău Galaxy A56 suportă 5G! Când vezi '5G' în bara de sus, ești conectat la cea mai rapidă rețea mobilă din lume.",
            "quiz": {"question": "Ce viteză maximă teoretică are 5G?", "options": ["20 Gbps", "100 Mbps", "1 Gbps", "500 Mbps"], "answer": "20 Gbps"},
            "related": ["iot", "wifi 7", "bandwidth", "latency", "network"]
        },

        "wifi 7": {
            "beginner": "Wi-Fi 7 e cea mai nouă și mai rapidă tehnologie de internet wireless. E ca Wi-Fi-ul pe care îl știi, dar pe steroizi. Perfect pentru gaming, streaming 8K și realitate virtuală.",
            "professional": "Wi-Fi 7 (802.11be) oferă viteze de până la 46 Gbps, canale de 320 MHz, 4096-QAM, Multi-Link Operation (MLO) și latență ultra-scăzută.",
            "expert": "MLO permite conectarea simultană pe mai multe benzi (2.4, 5, 6 GHz). 16x16 MU-MIMO, OFDMA îmbunătățit. Compatibilitate cu Wi-Fi 6/6E. Aplicații enterprise: AR/VR fără fir, Industry 4.0.",
            "code": "# Verifică rețelele Wi-Fi disponibile (Windows)\n# import subprocess\n# result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], capture_output=True, text=True)\n# print(result.stdout)",
            "real_world": "Samsung Galaxy Book5 Pro 360 are Wi-Fi 7! Când îl vei avea, vei putea descărca un film 4K în câteva secunde.",
            "quiz": {"question": "Ce viteză maximă teoretică are Wi-Fi 7?", "options": ["46 Gbps", "10 Gbps", "1 Gbps", "100 Gbps"], "answer": "46 Gbps"},
            "related": ["5g", "bandwidth", "latency", "router", "network"]
        },

        "ssd": {
            "beginner": "SSD-ul e ca o bibliotecă ultra-rapidă pentru fișierele tale. Spre deosebire de HDD (care are piese care se învârt), SSD-ul nu are piese mișcătoare și e de 10 ori mai rapid.",
            "professional": "SSD (Solid State Drive) folosește memorie NAND flash pentru stocare persistentă. Interfețe: SATA III (până la 550 MB/s), NVMe PCIe 4.0/5.0 (până la 14 GB/s).",
            "expert": "Tehnologii: 3D NAND (straturi multiple), SLC/MLC/TLC/QLC caching, DRAM cache vs DRAM-less. NVMe 2.0, ZNS (Zoned Namespaces) pentru centre de date. Endurance: TBW (Total Bytes Written).",
            "code": "# Verifică viteza discului (conceptual)\nimport time, os\nsize = 1024*1024*100  # 100MB\nstart = time.time()\nwith open('test.bin', 'wb') as f:\n    f.write(os.urandom(size))\nend = time.time()\nprint(f'Viteză scriere: {size/(end-start)/1e6:.0f} MB/s')",
            "real_world": "Laptopul tău viitor (Book5 Pro 360) are SSD NVMe de 1TB. Se deschide în 5 secunde. Jocurile se încarcă instant. Aplicațiile pornesc fără delay.",
            "quiz": {"question": "Ce interfață e mai rapidă pentru SSD?", "options": ["NVMe PCIe", "SATA III", "USB 3.0", "FireWire"], "answer": "NVMe PCIe"},
            "related": ["hdd", "ram", "nvme", "storage", "motherboard"]
        },

        "html": {
            "beginner": "HTML e ca scheletul unei case. Fiecare pagină web e construită pe un schelet HTML — el ține totul în picioare: texte, poze, butoane.",
            "professional": "HTML (HyperText Markup Language) este limbajul standard pentru structurarea paginilor web, folosind elemente și tag-uri pentru a defini conținutul.",
            "expert": "HTML5 aduce semantic elements (article, section, nav), suport multimedia nativ (video, audio), canvas pentru grafică și API-uri moderne (localStorage, Web Workers).",
            "code": "<!DOCTYPE html>\n<html>\n<head><title>Pagina mea</title></head>\n<body>\n  <h1>Salut, Andrei!</h1>\n  <p>Acesta e AEGIS.</p>\n</body>\n</html>",
            "real_world": "Fiecare site pe care-l vizitezi — Google, YouTube, Instagram — e construit pe HTML. E prima limbă pe care o învață orice web developer.",
            "quiz": {"question": "Ce înseamnă HTML?", "options": ["HyperText Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "Home Tool Markup Language"], "answer": "HyperText Markup Language"},
            "related": ["css", "javascript", "dom", "frontend", "web development"]
        },

        "css": {
            "beginner": "Dacă HTML e scheletul casei, CSS e vopseaua, mobila și decorațiunile. CSS face site-urile să arate FRUMOS — culori, fonturi, layout-uri.",
            "professional": "CSS (Cascading Style Sheets) controlează prezentarea vizuală a paginilor web: layout, culori, fonturi, animații și responsive design.",
            "expert": "CSS modern include Flexbox și Grid pentru layout, custom properties (variabile), animații keyframe, media queries pentru responsive design și preprocesoare ca Sass.",
            "code": "/* CSS simplu */\nbody {\n  background-color: #0a0a0a;\n  color: white;\n  font-family: Arial, sans-serif;\n}\n\nh1 {\n  color: #00ffcc;\n  text-align: center;\n}",
            "real_world": "Când vezi un site frumos — cu culori, animații, butoane stilizate — totul e făcut cu CSS. Fără CSS, internetul ar fi alb-negru și urât.",
            "quiz": {"question": "Ce face CSS într-o pagină web?", "options": ["Stilizează conținutul", "Rulează pe server", "Gestionează baza de date", "Face calcule matematice"], "answer": "Stilizează conținutul"},
            "related": ["html", "javascript", "frontend", "responsive design", "bootstrap"]
        },

        "javascript": {
            "beginner": "JavaScript e magicianul paginii web. Face butoanele să reacționeze, animațiile să se miște și totul să fie INTERACTIV. E ca un creier pentru site-uri.",
            "professional": "JavaScript este un limbaj de scripting pentru web, permițând conținut dinamic, manipulare DOM și comunicare asincronă cu serverele.",
            "expert": "JS modern (ES2024+) suportă async/await, modules, arrow functions, destructuring, spread operators. Rulează pe server prin Node.js, Deno, Bun. Framework-uri: React, Vue, Angular.",
            "code": "// JavaScript simplu\ndocument.querySelector('button').addEventListener('click', () => {\n  alert('Salut, Andrei! AEGIS e cel mai tare!');\n});",
            "real_world": "Google Maps, YouTube, Facebook, Instagram — toate folosesc JavaScript. Orice site pe care dai click și se întâmplă ceva — acolo e JavaScript.",
            "quiz": {"question": "Unde rulează JavaScript?", "options": ["În browser și pe server (Node.js)", "Doar pe server", "Doar în browser", "Pe Marte"], "answer": "În browser și pe server (Node.js)"},
            "related": ["html", "css", "react", "node.js", "typescript"]
        },

        "sql": {
            "beginner": "SQL e ca un bibliotecar care găsește orice carte într-o bibliotecă imensă. Îi spui ce cauți, și el știe exact unde e. SQL face același lucru cu datele.",
            "professional": "SQL (Structured Query Language) gestionează și interoghează baze de date relaționale. Operații: SELECT, INSERT, UPDATE, DELETE, JOIN-uri între tabele.",
            "expert": "Optimizare SQL: indexing (B-tree, hash), query execution plans, normalization vs denormalization, stored procedures, triggers, window functions, CTE-uri.",
            "code": "-- SQL simplu\nSELECT nume, varsta\nFROM utilizatori\nWHERE oras = 'Ploiesti'\nORDER BY nume ASC;",
            "real_world": "Când faci login pe un site, SQL caută numele tău în baza de date. Când verifici soldul la bancă, SQL îți aduce tranzacțiile. E peste tot.",
            "quiz": {"question": "Ce comandă SQL extrage date?", "options": ["SELECT", "GET", "FETCH", "EXTRACT"], "answer": "SELECT"},
            "related": ["database", "mysql", "postgresql", "nosql", "orm"]
        },
    
        "react": {
            "beginner": "React e ca un set de piese LEGO pentru site-uri. Construiești bucăți mici (componente) și le îmbini într-o pagină web interactivă și rapidă.",
            "professional": "React este o bibliotecă JavaScript pentru construirea interfețelor utilizator, bazată pe componente reutilizabile și Virtual DOM pentru performanță.",
            "expert": "React avansat: hooks (useState, useEffect, useContext), state management (Redux, Zustand), server components, Next.js pentru SSR, React Native pentru mobile.",
            "code": "// Componentă React simplă\nfunction Salut({nume}) {\n  return <h1>Salut, {nume}! Bine ai venit la AEGIS!</h1>;\n}\n\nexport default function App() {\n  return <Salut nume='Andrei' />;\n}",
            "real_world": "Facebook, Instagram, Netflix, Airbnb — toate folosesc React. E una dintre cele mai populare tehnologii web din lume.",
            "quiz": {"question": "Cine a creat React?", "options": ["Facebook (Meta)", "Google", "Microsoft", "Amazon"], "answer": "Facebook (Meta)"},
            "related": ["javascript", "angular", "vue", "frontend", "next.js"]
        },

        "linux": {
            "beginner": "Linux e ca un motor invizibil care rulează lumea. Nu-l vezi, dar e în telefoane, servere, supercomputere și chiar în mașina Tesla. E gratuit și foarte puternic.",
            "professional": "Linux este un kernel open-source pentru sisteme de operare. Distribuții populare: Ubuntu, Fedora, Debian, Arch. Domină serverele, cloud-ul și dispozitivele embedded.",
            "expert": "Linux kernel: process scheduling (CFS), memory management, VFS, namespaces/cgroups pentru containere. Administrare: systemd, iptables/nftables, LVM, kernel tuning.",
            "code": "# Comenzi Linux esențiale\nls -la           # Listare fișiere\ncd /var/log      # Navigare\nsudo systemctl restart nginx   # Restart serviciu\ngrep 'error' app.log           # Căutare în fișiere\nchmod +x script.sh             # Permisiuni executare",
            "real_world": "Android rulează pe kernel Linux. Google, Facebook, NASA — toate folosesc Linux pe servere. 100% din supercomputerele lumii rulează Linux.",
            "quiz": {"question": "Cine a creat Linux?", "options": ["Linus Torvalds", "Bill Gates", "Steve Jobs", "Elon Musk"], "answer": "Linus Torvalds"},
            "related": ["ubuntu", "bash", "terminal", "kernel", "debian"]
        },

        "vpn": {
            "beginner": "Un VPN e ca un tunel secret între tine și internet. Nimeni nu poate vedea ce faci — nici hackerii, nici furnizorul de internet. E ca o pelerină de invizibilitate digitală.",
            "professional": "VPN (Virtual Private Network) criptează traficul de internet și îl direcționează printr-un server securizat, ascunzând adresa IP și protejând confidențialitatea.",
            "expert": "Protocoale VPN: WireGuard (modern, rapid), OpenVPN (flexibil), IKEv2/IPSec (mobil). Arhitecturi: site-to-site, remote access, split tunneling, kill switch.",
            "code": "# Configurare WireGuard (exemplu)\n[Interface]\nPrivateKey = <cheia-ta-privata>\nAddress = 10.0.0.2/24\nDNS = 1.1.1.1\n\n[Peer]\nPublicKey = <cheia-serverului>\nEndpoint = vpn.example.com:51820\nAllowedIPs = 0.0.0.0/0",
            "real_world": "Când te conectezi la Wi-Fi-ul unui hotel sau cafenea, un VPN te protejează de hackeri. Jurnaliștii și activiștii folosesc VPN-uri pentru siguranță.",
            "quiz": {"question": "Ce face un VPN?", "options": ["Criptează conexiunea și ascunde IP-ul", "Accelerează internetul", "Repară viruși", "Editează poze"], "answer": "Criptează conexiunea și ascunde IP-ul"},
            "related": ["encryption", "cybersecurity", "firewall", "privacy", "proxy"]
        },

        "android": {
            "beginner": "Android e ca un sistem de operare care face telefonul tău să fie SMART. E creat de Google și e folosit de miliarde de telefoane, tablete și ceasuri din toată lumea.",
            "professional": "Android este un sistem de operare open-source bazat pe kernel Linux, dezvoltat de Google. Domină piața mobilă cu peste 70% cotă globală.",
            "expert": "Arhitectura Android: kernel Linux, HAL, Android Runtime (ART), framework Java/Kotlin. Componente: Activities, Services, Broadcast Receivers, Content Providers. Jetpack Compose pentru UI modern.",
            "code": "// Kotlin — Activitate Android simplă\nclass MainActivity : ComponentActivity() {\n  override fun onCreate(savedInstanceState: Bundle?) {\n    super.onCreate(savedInstanceState)\n    setContent {\n      Text('Salut, Andrei! AEGIS rulează pe Android!')\n    }\n  }\n}",
            "real_world": "Telefonul tău Galaxy A56 rulează Android! Samsung, Xiaomi, OnePlus — toate folosesc Android. E cel mai folosit sistem de operare din lume.",
            "quiz": {"question": "Cine deține Android?", "options": ["Google", "Samsung", "Microsoft", "Apple"], "answer": "Google"},
            "related": ["ios", "kotlin", "flutter", "google play", "linux"]
        },

        "windows": {
            "beginner": "Windows e ca un birou digital pe care îl folosești zilnic. E sistemul de operare care pornește când deschizi laptopul — cu pictograme, ferestre și bara de start.",
            "professional": "Microsoft Windows este cel mai popular sistem de operare pentru PC-uri. Windows 11 oferă Copilot AI, suport pentru aplicații Android și securitate avansată.",
            "expert": "Windows 11 arhitectură: kernel NT, Hyper-V virtualization, WSL2 pentru Linux, DirectStorage pentru gaming, TPM 2.0 pentru securitate. PowerShell pentru administrare avansată.",
            "code": "# PowerShell — Comenzi utile\nGet-Process | Sort-Object CPU -Descending\nGet-Service | Where-Object Status -eq 'Running'\nwinget install Python.Python.3.12",
            "real_world": "Majoritatea laptopurilor din lume rulează Windows. Samsung Galaxy Book5 Pro 360 al tău va rula Windows 11 cu Copilot AI integrat.",
            "quiz": {"question": "Ce companie creează Windows?", "options": ["Microsoft", "Apple", "Google", "IBM"], "answer": "Microsoft"},
            "related": ["linux", "macos", "powershell", "kernel", "uefi"]
        },

        "github": {
            "beginner": "GitHub e ca o bibliotecă uriașă unde programatorii își pun codul. E și o rețea socială pentru developeri — poți colabora, învăța și arăta ce ai construit.",
            "professional": "GitHub este cea mai mare platformă de găzduire a codului sursă, folosind Git pentru versionare. Oferă CI/CD prin GitHub Actions, code review și project management.",
            "expert": "GitHub avansat: Actions workflows, Codespaces, Dependabot, code scanning cu CodeQL, branch protection rules, GitHub Pages, API REST și GraphQL.",
            "code": "# Comenzi Git + GitHub\ngit clone https://github.com/andrei28vieru-boop/AEGIS-AI.git\ngit add .\ngit commit -m 'Added new AEGIS LEVEL terms'\ngit push origin main",
            "real_world": "AEGIS e pe GitHub chiar acum! Toate companiile mari — Google, Microsoft, Facebook — au codul pe GitHub. E portofoliul tău de developer.",
            "quiz": {"question": "Ce sistem de versionare folosește GitHub?", "options": ["Git", "SVN", "Mercurial", "CVS"], "answer": "Git"},
            "related": ["git", "github actions", "devops", "ci/cd", "repository"]
        },

                "json": {
            "beginner": "JSON e ca un translator universal pentru computere. Orice limbaj de programare înțelege JSON — e modul în care aplicațiile vorbesc între ele pe internet.",
            "professional": "JSON (JavaScript Object Notation) este un format lightweight de schimb de date, ușor de citit pentru oameni și simplu de procesat pentru mașini. Folosește perechi cheie-valoare și array-uri.",
            "expert": "JSON suportă tipuri: string, number, boolean, null, object, array. Validare prin JSON Schema. Alternativă la XML, mai compact. JSON Lines pentru streaming. JSONB în PostgreSQL pentru interogări rapide.",
            "code": "{\n  \"nume\": \"Andrei\",\n  \"varsta\": 15,\n  \"proiect\": \"AEGIS\",\n  \"termeni\": 725,\n  \"obiectiv\": \"Billionaire\"\n}",
            "real_world": "Când verifici vremea pe telefon, aplicația primește datele în JSON. API-urile Google, Facebook, Instagram — toate returnează JSON. E limba universală a internetului.",
            "quiz": {"question": "Ce înseamnă JSON?", "options": ["JavaScript Object Notation", "Java System Online Network", "Just Simple Object Name", "JSON Standard Object Notation"], "answer": "JavaScript Object Notation"},
            "related": ["api", "xml", "api rest", "database", "mongodb"]
        },

        "bitcoin": {
            "beginner": "Bitcoin e ca aurul digital. Nu există fizic — e doar pe internet. Nimeni nu-l controlează: nici bănci, nici guverne. Oamenii îl trimit direct unul altuia, ca pe un email cu bani.",
            "professional": "Bitcoin (BTC) este prima criptomonedă descentralizată, creată în 2009 de Satoshi Nakamoto. Rulează pe tehnologia blockchain și folosește Proof of Work pentru securitate.",
            "expert": "Bitcoin: supply limitat la 21 milioane, mining cu SHA-256, halving la fiecare 210,000 blocuri, Lightning Network pentru Layer 2 scaling. UTXO model, non-Turing complete scripting.",
            "code": "# Verifică prețul Bitcoin în timp real\nimport requests\nresponse = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')\ndata = response.json()\nprint(f\"BTC: ${data['bpi']['USD']['rate']}\")",
            "real_world": "El Salvador a adoptat Bitcoin ca monedă națională. Companii ca Tesla și MicroStrategy dețin Bitcoin. Poți cumpăra Bitcoin pe Binance sau Coinbase.",
            "quiz": {"question": "Care e supply-ul maxim de Bitcoin?", "options": ["21 milioane", "100 milioane", "Nelimitat", "1 miliard"], "answer": "21 milioane"},
            "related": ["blockchain", "ethereum", "criptomonedă", "mining", "wallet"]
        },

        "gpu": {
            "beginner": "GPU-ul e ca un artist care pictează tot ce vezi pe ecran — jocuri, filmulețe, poze. Face asta de sute de ori pe secundă, mult mai rapid decât CPU-ul la grafică.",
            "professional": "GPU (Graphics Processing Unit) este un procesor specializat pentru calcule paralele masive, esențial pentru randare 3D, gaming, AI și mining crypto.",
            "expert": "GPU-urile moderne (NVIDIA CUDA, AMD ROCm) au mii de core-uri pentru parallel computing. Tensor Cores pentru AI, RT Cores pentru ray tracing. VRAM (GDDR6X, HBM3) oferă bandwidth masiv.",
            "code": "# Verifică GPU-ul disponibil pentru AI\nimport torch\nprint(f\"CUDA disponibil: {torch.cuda.is_available()}\")\nprint(f\"GPU: {torch.cuda.get_device_name(0)}\")\nprint(f\"Memorie: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB\")",
            "real_world": "NVIDIA face GPU-uri care antrenează AI-ul din spatele ChatGPT. GPU-ul tău integrat Intel Arc din viitorul Book5 Pro 360 poate rula jocuri și accelerare AI.",
            "quiz": {"question": "Ce companie domină piața de GPU-uri pentru AI?", "options": ["NVIDIA", "Intel", "AMD", "Apple"], "answer": "NVIDIA"},
            "related": ["cpu", "ram", "nvidia", "deep learning", "ssd"]
        },

        "ram": {
            "beginner": "RAM-ul e ca un birou imens. Cu cât ai mai mult birou, cu atât poți lucra la mai multe lucruri simultan fără să se aglomereze. Când închizi calculatorul, biroul se golește.",
            "professional": "RAM (Random Access Memory) este memoria volatilă care stochează date temporar pentru procesor. DDR5 oferă viteze de până la 6400 MT/s cu consum redus.",
            "expert": "RAM arhitectură: canale (single/dual/quad), timing-uri CAS, XMP/EXPO pentru overclocking. ECC RAM pentru servere corectează erori. LPDDR5X în laptopuri oferă până la 8533 MT/s.",
            "code": "# Verifică RAM disponibilă în Python\nimport psutil\nram = psutil.virtual_memory()\nprint(f\"Total: {ram.total / 1e9:.1f} GB\")\nprint(f\"Disponibil: {ram.available / 1e9:.1f} GB\")\nprint(f\"Utilizat: {ram.percent}%\")",
            "real_world": "Samsung Galaxy Book5 Pro 360 are 16GB DDR5 RAM — poți rula AEGIS, browser cu 50 de tab-uri, PyCharm și Netflix simultan fără lag.",
            "quiz": {"question": "Ce tip de RAM e în Book5 Pro 360?", "options": ["DDR5", "DDR4", "DDR3", "LPDDR4X"], "answer": "DDR5"},
            "related": ["cpu", "ssd", "gpu", "motherboard", "ddr5"]
        },

        "nvidia": {
            "beginner": "NVIDIA e ca un magician al graficii. Fac plăci video care transformă codul în lumi 3D incredibile și antrenează inteligența artificială. Sunt creierul din spatele ChatGPT și al jocurilor video.",
            "professional": "NVIDIA este liderul mondial în GPU-uri și AI computing. Seria GeForce pentru gaming, RTX cu ray tracing, și CUDA pentru calcul paralel în deep learning.",
            "expert": "NVIDIA arhitecturi: Hopper (H100 — datacenter AI), Ada Lovelace (RTX 40 — consumer), Blackwell (2024 — next-gen). CUDA API permite GPU computing. TensorRT pentru inferență optimizată.",
            "code": "# Verifică GPU NVIDIA cu CUDA\nimport torch\nif torch.cuda.is_available():\n    print(f\"GPU: {torch.cuda.get_device_name(0)}\")\n    print(f\"CUDA Cores: {torch.cuda.get_device_properties(0).multi_processor_count}\")\nelse:\n    print(\"Niciun GPU NVIDIA detectat\")",
            "real_world": "NVIDIA valorează peste 2 trilioane de dolari în 2024. GPU-urile lor antrenează ChatGPT, conduc mașini autonome și randează filmele Marvel.",
            "quiz": {"question": "Cum se numește platforma NVIDIA pentru AI?", "options": ["CUDA", "TensorFlow", "PyTorch", "OpenCL"], "answer": "CUDA"},
            "related": ["gpu", "ai", "deep learning", "intel", "amd"]
        },

        "intel": {
            "beginner": "Intel e ca un bucătar-șef care gătește procesoarele din majoritatea laptopurilor. E compania care a inventat microprocesorul și încă e una dintre cele mai mari din lume.",
            "professional": "Intel Corporation este cel mai mare producător de procesoare x86 pentru PC-uri și servere. Produce procesoare Core Ultra, Xeon și plăci grafice Arc.",
            "expert": "Intel arhitecturi: Lunar Lake (Core Ultra 200V — 3nm, AI NPU), Arrow Lake (desktop), Granite Rapids (Xeon server). Foundry services (Intel 18A). Gaudi acceleratoare AI.",
            "code": "# Verifică CPU-ul Intel\nimport platform\ncpu = platform.processor()\nprint(f\"CPU: {cpu}\")\nprint(f\"Arhitectură: {platform.architecture()[0]}\")",
            "real_world": "Samsung Galaxy Book5 Pro 360 rulează pe Intel Core Ultra 7 256V. Intel procesoare sunt în miliarde de dispozitive — de la laptopuri la servere NASA.",
            "quiz": {"question": "Ce serie de procesoare Intel e în Book5 Pro 360?", "options": ["Core Ultra 7", "Core i9", "Pentium", "Atom"], "answer": "Core Ultra 7"},
            "related": ["cpu", "amd", "nvidia", "gpu", "motherboard"]
        },

        "amd": {
            "beginner": "AMD e ca un underdog care a devenit campion. Era mereu pe locul 2 după Intel, dar acum face unele dintre cele mai rapide procesoare din lume. Și plăci video, și cipuri pentru console.",
            "professional": "AMD (Advanced Micro Devices) produce procesoare Ryzen (desktop/laptop), plăci grafice Radeon și cipuri pentru console (PlayStation 5, Xbox Series X).",
            "expert": "AMD arhitecturi: Zen 5 (Ryzen 9000), RDNA 3 (Radeon RX 7000), CDNA (instinct AI accelerators). Chiplet design pentru yield și costuri reduse. 3D V-Cache pentru gaming.",
            "code": "# Verifică CPU AMD Ryzen\nimport platform\ncpu = platform.processor()\nprint(f\"CPU: {cpu}\")",
            "real_world": "PlayStation 5 și Xbox Series X rulează pe cipuri AMD. Toate consolele next-gen sunt AMD. Ryzen domină piața de desktop pentru gameri și creatori.",
            "quiz": {"question": "Care e concurentul principal al AMD?", "options": ["Intel", "NVIDIA", "Apple", "Samsung"], "answer": "Intel"},
            "related": ["cpu", "intel", "nvidia", "gpu", "motherboard"]
        },

        "apple": {
            "beginner": "Apple e ca un designer de lux al tehnologiei. Fac iPhone, MacBook, iPad — toate scumpe, dar elegante și ușor de folosit. E ca Mercedes-ul din lumea tech.",
            "professional": "Apple Inc. este cea mai valoroasă companie din lume, cunoscută pentru iPhone, Mac, iPad și ecosistemul integrat de hardware și software.",
            "expert": "Apple Silicon: cipuri M-series (M4 — 3nm, Neural Engine). Arhitectură unificată memory. Ecosistem: iOS, macOS, watchOS, visionOS. App Store cu peste 2 milioane de aplicații.",
            "code": "// Swift — Limbajul Apple pentru iOS/macOS\nimport SwiftUI\nstruct ContentView: View {\n    var body: some View {\n        Text(\"Salut, Andrei!\")\n            .font(.largeTitle)\n            .foregroundColor(.blue)\n    }\n}",
            "real_world": "iPhone-ul e cel mai vândut smartphone. Apple Watch domină piața de smartwatch-uri. Apple Vision Pro a lansat era spatial computing.",
            "quiz": {"question": "Cum se numesc procesoarele Apple pentru Mac?", "options": ["M-series (M1, M2, M3, M4)", "A-series", "S-series", "X-series"], "answer": "M-series (M1, M2, M3, M4)"},
            "related": ["ios", "macos", "iphone 16 pro max", "samsung", "macbook pro 16"]
        },

        "tesla": {
            "beginner": "Tesla e ca un iPhone pe roți. Mașinile lor sunt electrice, rapide și pline de tehnologie. Se conduc singure pe autostradă și primesc update-uri ca un telefon.",
            "professional": "Tesla Inc. este lider în vehicule electrice și energie curată, fondată de Elon Musk. Produce Model S, 3, X, Y și Cybertruck cu tehnologie de conducere autonomă.",
            "expert": "Tesla Full Self-Driving (FSD) folosește computer vision și rețele neuronale antrenate pe miliarde de km. Dojo supercomputer pentru training AI. 4680 battery cells pentru eficiență.",
            "code": "# Simulare autonomie Tesla\nbattery_kwh = 75  # Model 3 Long Range\nefficiency_wh_km = 150  # Wh per km\nautonomie_km = (battery_kwh * 1000) / efficiency_wh_km\nprint(f\"Autonomie estimată: {autonomie_km:.0f} km\")",
            "real_world": "Tesla Model Y a fost cea mai vândută mașină din lume în 2023. Tesla produce și baterii Powerwall pentru case și panouri solare.",
            "quiz": {"question": "Cine e CEO-ul Tesla?", "options": ["Elon Musk", "Jeff Bezos", "Tim Cook", "Satya Nadella"], "answer": "Elon Musk"},
            "related": ["elon musk", "ev", "ai", "nvidia", "green tech"]
        },

        "spotify": {
            "beginner": "Spotify e ca un DJ personal care știe exact ce muzică îți place. Cauți orice melodie, asculți podcasturi, și descoperi artiști noi. E ca un radio infinit în buzunar.",
            "professional": "Spotify este cea mai mare platformă de streaming audio din lume cu peste 500 milioane de utilizatori. Oferă muzică, podcasturi și recomandări bazate pe AI.",
            "expert": "Spotify arhitectură: microservicii, Kafka pentru streaming de date, Cassandra pentru scalability, ML pentru Discover Weekly și algoritmi de recomandare. Codec Ogg Vorbis/AAC.",
            "code": "# Caută un artist pe Spotify API\nimport requests\nheaders = {'Authorization': 'Bearer YOUR_TOKEN'}\nresponse = requests.get(\n    'https://api.spotify.com/v1/search',\n    headers=headers,\n    params={'q': 'Depeche Mode', 'type': 'artist'}\n)\ndata = response.json()\nfor artist in data['artists']['items']:\n    print(f\"{artist['name']} — Popularitate: {artist['popularity']}\")",
            "real_world": "Spotify a schimbat industria muzicală. Artiștii sunt plătiți per stream. Playlist-uri ca Discover Weekly folosesc AI să-ți găsească muzică nouă în fiecare săptămână.",
            "quiz": {"question": "Câți utilizatori are Spotify?", "options": ["Peste 500 milioane", "100 milioane", "1 miliard", "50 milioane"], "answer": "Peste 500 milioane"},
            "related": ["streaming", "ai", "machine learning", "podcast", "apple"]
        },

        "database": {
            "beginner": "O bază de date e ca o bibliotecă digitală imensă. În loc de cărți, ține informații organizate — nume, numere, poze. Când cauți ceva, găsești instant.",
            "professional": "O bază de date este o colecție structurată de date stocate electronic. Tipuri: relaționale (SQL) cu tabele și relații, și non-relaționale (NoSQL) cu documente, grafuri sau cheie-valoare.",
            "expert": "Arhitecturi de baze de date: master-slave replication, sharding pentru scalare orizontală, ACID vs BASE, indexing (B-tree, hash, GiST), query optimization cu EXPLAIN, connection pooling.",
            "code": "-- Creează o bază de date și o tabelă\nCREATE DATABASE aegis_db;\nUSE aegis_db;\nCREATE TABLE users (\n    id INT PRIMARY KEY AUTO_INCREMENT,\n    name VARCHAR(100),\n    level VARCHAR(20)\n);\nINSERT INTO users (name, level) VALUES ('Andrei', 'Expert');",
            "real_world": "Când îți verifici soldul la bancă, datele tale sunt într-o bază de date. Facebook stochează miliarde de poze în baze de date. AEGIS însuși ar putea folosi o bază de date pentru termeni.",
            "quiz": {"question": "Care sunt cele două tipuri principale de baze de date?", "options": ["SQL și NoSQL", "HTML și CSS", "JSON și XML", "RAM și ROM"], "answer": "SQL și NoSQL"},
            "related": ["sql", "mysql", "postgresql", "mongodb", "nosql"]
        },

        "mysql": {
            "beginner": "MySQL e ca un bibliotecar foarte rapid care organizează datele în tabele. E folosit de Facebook, YouTube și milioane de site-uri. E gratuit și foarte popular.",
            "professional": "MySQL este un sistem de management al bazelor de date relaționale (RDBMS) open-source. Folosește SQL pentru interogări și este parte a stivei LAMP (Linux, Apache, MySQL, PHP).",
            "expert": "MySQL: engine-uri InnoDB (ACID, foreign keys) și MyISAM (rapid, fără FK). Replication (master-slave, group replication). Indexing: B-tree, full-text. Partitioning, stored procedures, triggers, views.",
            "code": "-- MySQL: Creează utilizator și acordă permisiuni\nCREATE USER 'andrei'@'localhost' IDENTIFIED BY 'parola_sigura';\nGRANT ALL PRIVILEGES ON aegis_db.* TO 'andrei'@'localhost';\nFLUSH PRIVILEGES;",
            "real_world": "WordPress rulează pe MySQL. Facebook a pornit cu MySQL. Platforme ca Uber și Airbnb îl folosesc pentru date critice. E peste tot pe web.",
            "quiz": {"question": "MySQL este un sistem de baze de date de tip...?", "options": ["Relațional (SQL)", "Document (NoSQL)", "Graph", "Key-Value"], "answer": "Relațional (SQL)"},
            "related": ["sql", "database", "postgresql", "mongodb", "orm"]
        },

        "mongodb": {
            "beginner": "MongoDB e ca un caiet de notițe flexibil. În loc de tabele rigide, poți scrie orice fel de notiță, în orice format, și o găsești rapid. E baza de date preferată pentru aplicații moderne.",
            "professional": "MongoDB este o bază de date NoSQL orientată pe documente, stocând datele în format BSON (similar JSON). Ideală pentru date nestructurate și scalare orizontală.",
            "expert": "MongoDB: sharding pentru scalare, replica sets pentru high availability, aggregation pipeline pentru analytics. Indexing: compound, text, geospatial, TTL. Schema validation opțională.",
            "code": "// MongoDB: Inserare și căutare documente\ndb.users.insertOne({\n  name: 'Andrei',\n  level: 'Expert',\n  projects: ['AEGIS', 'Coffee Business']\n});\ndb.users.find({ level: 'Expert' });",
            "real_world": "Forbes, eBay, și Adobe folosesc MongoDB. E alegerea preferată pentru startup-uri care au nevoie de flexibilitate și scalare rapidă.",
            "quiz": {"question": "Ce format folosește MongoDB pentru stocare?", "options": ["BSON (Binary JSON)", "CSV", "XML", "YAML"], "answer": "BSON (Binary JSON)"},
            "related": ["nosql", "database", "mysql", "json", "postgresql"]
        },

        "node.js": {
            "beginner": "Node.js e ca un motor care face JavaScript să ruleze pe server, nu doar în browser. Cu Node.js poți construi un site întreg — frontend și backend — folosind aceeași limbă.",
            "professional": "Node.js este un runtime JavaScript construit pe motorul V8 de la Chrome. Permite dezvoltarea de aplicații server-side cu JavaScript, folosind un model asincron non-blocant.",
            "expert": "Node.js: event loop pentru I/O non-blocant, libuv pentru operații asincrone, cluster module pentru multi-threading, streams pentru date mari. npm — cel mai mare ecosistem de pachete.",
            "code": "// Server Node.js simplu\nconst http = require('http');\nconst server = http.createServer((req, res) => {\n  res.writeHead(200, {'Content-Type': 'text/plain'});\n  res.end('Salut, Andrei! AEGIS rulează pe Node.js!');\n});\nserver.listen(3000, () => console.log('Server pornit pe portul 3000'));",
            "real_world": "Netflix, LinkedIn, și Uber folosesc Node.js. E backend-ul din spatele a milioane de aplicații web moderne.",
            "quiz": {"question": "Pe ce motor JavaScript rulează Node.js?", "options": ["V8 (Chrome)", "SpiderMonkey (Firefox)", "JavaScriptCore (Safari)", "Chakra (Edge)"], "answer": "V8 (Chrome)"},
            "related": ["javascript", "npm", "express", "backend", "react"]
        },

        "typescript": {
            "beginner": "TypeScript e ca JavaScript, dar cu super-puteri. Adaugă 'tipuri' — etichete care spun exact ce fel de date folosești. E ca și cum ai avea un corector care te avertizează înainte să greșești.",
            "professional": "TypeScript este un superset tipat al JavaScript, dezvoltat de Microsoft. Adaugă tipuri statice, interfețe, generice și compilare în JavaScript standard.",
            "expert": "TypeScript: type system avansat (union, intersection, conditional types), decorators, declaration files (.d.ts), strict mode, tsconfig pentru configurare. Integrare perfectă cu VS Code.",
            "code": "// TypeScript: Funcție cu tipuri\nfunction salut(nume: string, varsta: number): string {\n  return `Salut, ${nume}! Ai ${varsta} ani.`;\n}\nconsole.log(salut('Andrei', 15));",
            "real_world": "Angular, Deno, și VS Code sunt scrise în TypeScript. Majoritatea companiilor mari migrează de la JavaScript la TypeScript pentru proiecte complexe.",
            "quiz": {"question": "Cine a creat TypeScript?", "options": ["Microsoft", "Google", "Facebook", "Apple"], "answer": "Microsoft"},
            "related": ["javascript", "react", "angular", "node.js", "frontend"]
        },

        "next.js": {
            "beginner": "Next.js e ca un atelier magic pentru site-uri React. Face site-urile să se încarce instant și să fie găsite ușor de Google. E folosit de cele mai mari companii din lume.",
            "professional": "Next.js este un framework React pentru producție, oferind Server-Side Rendering (SSR), Static Site Generation (SSG) și routing bazat pe fișiere.",
            "expert": "Next.js 14+: App Router cu React Server Components, streaming cu Suspense, server actions pentru mutații, ISR (Incremental Static Regeneration), middleware pe edge. Optimizat pentru Vercel.",
            "code": "// Next.js: Pagină simplă\nexport default function Home() {\n  return (\n    <div>\n      <h1>Salut, Andrei!</h1>\n      <p>AEGIS construit cu Next.js</p>\n    </div>\n  );\n}",
            "real_world": "TikTok, Twitch, Hulu și Nike folosesc Next.js. E framework-ul React #1 pentru site-uri moderne, rapide și SEO-friendly.",
            "quiz": {"question": "Ce companie a creat Next.js?", "options": ["Vercel", "Google", "Meta", "Netflix"], "answer": "Vercel"},
            "related": ["react", "javascript", "typescript", "frontend", "ssr"]
        },

        "express": {
            "beginner": "Express e ca un schelet gata-făcut pentru servere web. În loc să construiești totul de la zero, Express îți dă piesele de bază și tu le aranjezi cum vrei. Simplu și rapid.",
            "professional": "Express.js este un framework minimalist pentru Node.js, oferind routing, middleware și suport pentru API-uri REST. Este cel mai popular framework Node.js.",
            "expert": "Express: middleware chain (req, res, next), error handling, route parameters, query strings. Combinat cu body-parser, cors, helmet pentru securitate. Alternativă modernă: Fastify.",
            "code": "// Express server simplu\nconst express = require('express');\nconst app = express();\napp.get('/', (req, res) => {\n  res.json({ message: 'Salut, Andrei!', project: 'AEGIS' });\n});\napp.listen(3000, () => console.log('Server Express pornit!'));",
            "real_world": "PayPal, Uber, și Twitter au folosit Express la început. Milioane de API-uri rulează pe Express. E fundamentul backend-ului JavaScript modern.",
            "quiz": {"question": "Express este un framework pentru...?", "options": ["Node.js", "Python", "Ruby", "PHP"], "answer": "Node.js"},
            "related": ["node.js", "javascript", "api rest", "backend", "fastapi"]
        },

        "npm": {
            "beginner": "npm e ca un magazin imens cu piese gratuite pentru proiectele tale de cod. Ai nevoie de ceva — cauți pe npm, instalezi și folosești. E cel mai mare magazin de cod din lume.",
            "professional": "npm (Node Package Manager) este managerul de pachete implicit pentru Node.js, oferind acces la peste 2 milioane de pachete pentru dezvoltare JavaScript.",
            "expert": "npm: package.json pentru dependențe, semantic versioning (semver), lock files (package-lock.json), scripts personalizate, npm audit pentru securitate, npx pentru executare one-time.",
            "code": "# Comenzi npm esențiale\nnpm init -y                    # Inițializează proiect\nnpm install express            # Instalează pachet\nnpm install -g create-react-app  # Instalare globală\nnpm run start                 # Rulează script\nnpm audit fix                 # Repară vulnerabilități",
            "real_world": "npm e folosit de peste 17 milioane de developeri. Orice proiect JavaScript modern începe cu npm install. Ecosistemul npm e cel mai mare din lume.",
            "quiz": {"question": "Ce fișier conține dependențele unui proiect Node.js?", "options": ["package.json", "app.js", "config.yml", "docker-compose.yml"], "answer": "package.json"},
            "related": ["node.js", "javascript", "pip", "pypi", "express"]
        },

        "rest api": {
            "beginner": "Un REST API e ca un meniu într-un restaurant. Tu alegi din meniu (faci o cerere), chelnerul o duce la bucătărie (server), și primești mâncarea (răspunsul). Simplu și standardizat.",
            "professional": "REST (Representational State Transfer) este un stil arhitectural pentru API-uri web, folosind metode HTTP (GET, POST, PUT, DELETE) și resurse identificate prin URL-uri.",
            "expert": "REST principles: statelessness, cacheability, uniform interface, resource-based URLs. HATEOAS pentru descoperire. Versionare (v1/, header). Paginare, filtrare, rate limiting. OpenAPI/Swagger pentru documentație.",
            "code": "# API REST cu Flask (Python)\nfrom flask import Flask, jsonify\napp = Flask(__name__)\n@app.route('/api/hello')\ndef hello():\n    return jsonify({'message': 'Salut, Andrei!', 'status': 'success'})\nif __name__ == '__main__':\n    app.run(port=5000)",
            "real_world": "API-urile Google Maps, Twitter, și GitHub sunt REST. Când o aplicație mobilă comunică cu un server, aproape sigur folosește un REST API.",
            "quiz": {"question": "Ce metodă HTTP folosești pentru a OBȚINE date?", "options": ["GET", "POST", "PUT", "DELETE"], "answer": "GET"},
            "related": ["api", "json", "http", "oauth", "express"]
        },

        "http": {
            "beginner": "HTTP e ca un poștaș al internetului. Când scrii un site în browser, HTTP duce cererea ta la server și aduce pagina înapoi. E fundamentul pe care rulează tot web-ul.",
            "professional": "HTTP (HyperText Transfer Protocol) este protocolul de comunicare la baza World Wide Web. Metode: GET, POST, PUT, DELETE. Status codes: 200 (OK), 404 (Not Found), 500 (Server Error).",
            "expert": "HTTP/2: multiplexing, header compression (HPACK), server push. HTTP/3: bazat pe QUIC (UDP), latență redusă. HTTPS = HTTP + TLS. Caching headers (ETag, Cache-Control), CORS, cookies.",
            "code": "# Cerere HTTP simplă cu Python\nimport requests\nresponse = requests.get('https://api.github.com')\nprint(f\"Status: {response.status_code}\")\nprint(f\"Headers: {dict(response.headers)}\")\nprint(f\"Body: {response.json()}\")",
            "real_world": "Fiecare pagină web pe care o vizitezi folosește HTTP sau HTTPS. Status 200 = totul e bine. Status 404 = pagina nu există. Status 500 = eroare pe server.",
            "quiz": {"question": "Ce înseamnă status code 404?", "options": ["Not Found (Pagină negăsită)", "OK (Totul bine)", "Server Error", "Redirect"], "answer": "Not Found (Pagină negăsită)"},
            "related": ["https", "api", "dns", "tcp", "rest api"]
        },

        "dns": {
            "beginner": "DNS e ca o agendă telefonică a internetului. În loc să ții minte numere (adrese IP), scrii numele site-ului (google.com) și DNS-ul îl traduce automat în adresa corectă.",
            "professional": "DNS (Domain Name System) este sistemul care traduce numele de domenii în adrese IP. Funcționează ca o bază de date distribuită global, cu servere recursive și authoritative.",
            "expert": "DNS: record types (A, AAAA, CNAME, MX, TXT, NS, SOA), DNSSEC pentru autentificare, TTL pentru caching, Anycast pentru reziliență. DNS over HTTPS (DoH) și DNS over TLS (DoT) pentru confidențialitate.",
            "code": "# Verifică înregistrări DNS cu Python\nimport socket\ndomain = 'google.com'\nip = socket.gethostbyname(domain)\nprint(f\"{domain} → {ip}\")",
            "real_world": "De fiecare dată când scrii un site în browser, DNS-ul lucrează în fundal. Fără DNS, ar trebui să ții minte numere IP pentru fiecare site.",
            "quiz": {"question": "Ce face DNS-ul?", "options": ["Traduce nume de domenii în IP-uri", "Criptează date", "Stochează fișiere", "Rulează aplicații"], "answer": "Traduce nume de domenii în IP-uri"},
            "related": ["ip", "http", "https", "domain", "network"]
        },

        "https": {
            "beginner": "HTTPS e ca un plic securizat pentru datele tale pe internet. Când vezi lacătul verde în browser, înseamnă că nimeni nu poate citi ce trimiți — parolele și cardul tău sunt în siguranță.",
            "professional": "HTTPS (HyperText Transfer Protocol Secure) combină HTTP cu TLS/SSL pentru criptare end-to-end, autentificare a serverului și integritatea datelor transmise.",
            "expert": "TLS 1.3: handshake redus la 1-RTT, forward secrecy obligatorie, ciphersuite-uri moderne (AES-GCM, ChaCha20-Poly1305). Certificate X.509, PKI, Certificate Transparency. HSTS pentru forțare HTTPS.",
            "code": "# Verifică certificatul SSL al unui site\nimport ssl\nimport socket\nctx = ssl.create_default_context()\nwith ctx.wrap_socket(socket.socket(), server_hostname='google.com') as s:\n    s.connect(('google.com', 443))\n    cert = s.getpeercert()\n    print(f\"Emis de: {cert['issuer']}\")\n    print(f\"Expiră: {cert['notAfter']}\")",
            "real_world": "Când faci cumpărături online sau intri pe internet banking, HTTPS îți protejează datele. Site-urile fără HTTPS sunt marcate ca 'Not Secure'.",
            "quiz": {"question": "Ce indică lacătul verde în browser?", "options": ["Conexiune securizată HTTPS", "Site-ul e rapid", "Site-ul are viruși", "E nevoie de parolă"], "answer": "Conexiune securizată HTTPS"},
            "related": ["http", "ssl", "tls", "encryption", "certificate"]
        },

        "tcp": {
            "beginner": "TCP e ca un poștaș foarte atent. Nu doar că duce pachetele la destinație, dar verifică să ajungă TOATE și în ordinea corectă. Dacă unul se pierde, îl retrimite.",
            "professional": "TCP (Transmission Control Protocol) oferă comunicare fiabilă, orientată pe conexiune. Garantează livrarea pachetelor în ordine, fără erori, prin three-way handshake și acknowledgment.",
            "expert": "TCP: congestion control (Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery), flow control cu sliding window, segmentare și reassembly. TCP vs UDP: fiabilitate vs viteză.",
            "code": "# Client TCP simplu în Python\nimport socket\nclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\nclient.connect(('example.com', 80))\nclient.send(b'GET / HTTP/1.1\\r\\nHost: example.com\\r\\n\\r\\n')\nresponse = client.recv(4096)\nprint(response.decode())\nclient.close()",
            "real_world": "Când descarci un fișier, trimiți un email, sau încarci o pagină web, TCP se asigură că fiecare bucățică de date ajunge corect și completă.",
            "quiz": {"question": "TCP garantează...?", "options": ["Livrare fiabilă în ordine", "Cea mai rapidă viteză", "Anonimitate", "Criptare automată"], "answer": "Livrare fiabilă în ordine"},
            "related": ["ip", "http", "dns", "udp", "network"]
        },

        "ip address": {
            "beginner": "O adresă IP e ca adresa casei tale, dar pe internet. Când trimiți un pachet de date, adresa IP spune exact unde trebuie să ajungă — ca un GPS pentru informație.",
            "professional": "IP (Internet Protocol) adrese identifică unic fiecare dispozitiv pe o rețea. IPv4: 32 biți (4 miliarde adrese). IPv6: 128 biți (adrese practic nelimitate).",
            "expert": "IPv6: adrese hexazecimale pe 8 grupuri, elimină nevoia de NAT, suportă autoconfigurare (SLAAC), IPsec nativ. Subnetting, CIDR notation, private vs public IP ranges (RFC 1918).",
            "code": "# Verifică adresa IP publică și locală\nimport requests\nimport socket\npublic_ip = requests.get('https://api.ipify.org').text\nprint(f\"IP Public: {public_ip}\")\nlocal_ip = socket.gethostbyname(socket.gethostname())\nprint(f\"IP Local: {local_ip}\")",
            "real_world": "Fiecare dispozitiv conectat la internet are o adresă IP — laptopul tău, telefonul, serverele AEGIS. Poliția folosește IP-uri pentru a găsi infractori online.",
            "quiz": {"question": "Câte adrese are IPv6?", "options": ["Practic nelimitate (2^128)", "4 miliarde", "1 milion", "65,000"], "answer": "Practic nelimitate (2^128)"},
            "related": ["dns", "tcp", "http", "router", "network"]
        },

        "router": {
            "beginner": "Router-ul e ca un polițist de trafic pentru internetul din casa ta. Dirijează datele între dispozitivele tale și internet, asigurându-se că fiecare pachet ajunge unde trebuie.",
            "professional": "Un router direcționează pachetele de date între rețele, folosind tabele de rutare și protocoale ca OSPF, BGP. Router-ul de acasă combină funcții de routing, switch și access point Wi-Fi.",
            "expert": "Routing: static vs dynamic (RIP, OSPF, BGP), NAT/PAT pentru partajare IP public, port forwarding, QoS pentru prioritizare trafic, firewall integrat. MESH networking pentru acoperire extinsă.",
            "code": "# Verifică ruta către o destinație (traceroute)\nimport subprocess\nresult = subprocess.run(['tracert', 'google.com'], capture_output=True, text=True)\nprint(result.stdout)",
            "real_world": "Router-ul tău de acasă conectează laptopul, telefonul și televizorul la internet simultan. Router-ele enterprise dirijează traficul pentru companii întregi.",
            "quiz": {"question": "Ce face un router?", "options": ["Direcționează traficul între rețele", "Stochează fișiere", "Rulează aplicații", "Editează documente"], "answer": "Direcționează traficul între rețele"},
            "related": ["ip", "dns", "tcp", "wifi 7", "network"]
        },

        "ethernet": {
            "beginner": "Ethernet e ca o șosea pentru date în interiorul casei tale. Conectează laptopul, PC-ul și router-ul prin cabluri, oferind internet stabil și rapid.",
            "professional": "Ethernet (IEEE 802.3) este tehnologia standard pentru rețele locale (LAN) prin cablu. Viteze: de la 10 Mbps (Ethernet) până la 400 Gbps (400 Gigabit Ethernet).",
            "expert": "Ethernet standards: 10GBASE-T (cupru), 100GBASE-LR4 (fibră), PoE pentru alimentare prin cablu. Frame structure: preamble, MAC dest/src, EtherType, payload, FCS. Switching vs routing la Layer 2.",
            "code": "# Verifică adresa MAC a interfeței de rețea\nimport uuid\nmac = uuid.getnode()\nmac_address = ':'.join(f'{(mac >> 8*i) & 0xff:02x}' for i in range(5, -1, -1))\nprint(f\"Adresa MAC: {mac_address}\")",
            "real_world": "Când conectezi laptopul la router prin cablu, folosești Ethernet. E mai rapid și mai stabil decât Wi-Fi-ul. Toate centrele de date folosesc Ethernet pentru servere.",
            "quiz": {"question": "Ethernet este o tehnologie pentru...?", "options": ["Rețele locale prin cablu", "Internet wireless", "Stocare de date", "Procesare AI"], "answer": "Rețele locale prin cablu"},
            "related": ["router", "ip", "wifi 7", "lan", "network"]
        },

        "lan": {
            "beginner": "LAN-ul e ca o petrecere privată pentru dispozitivele din casa ta. Laptopul, telefonul și imprimanta vorbesc între ele prin LAN, fără să iasă pe internetul mare.",
            "professional": "LAN (Local Area Network) conectează dispozitive într-o zonă restrânsă (casă, birou). Folosește Ethernet și Wi-Fi, cu switch-uri și access point-uri pentru conectivitate.",
            "expert": "LAN topologii: star, mesh, bus. VLAN-uri pentru segmentare logică. Subnetting pentru organizare IP. Protocoale: ARP pentru rezolvare MAC, STP pentru prevenire bucle. 802.1X pentru autentificare de port.",
            "code": "# Scanează dispozitivele din LAN\nimport os\nnetwork = '192.168.1.'\nfor i in range(1, 255):\n    ip = network + str(i)\n    response = os.system(f'ping -n 1 -w 100 {ip}')\n    if response == 0:\n        print(f\"Dispozitiv găsit: {ip}\")",
            "real_world": "LAN-ul tău de acasă conectează toate dispozitivele la același router. Când trimiți un fișier de pe laptop pe telefon prin Wi-Fi, folosești LAN-ul.",
            "quiz": {"question": "Ce înseamnă LAN?", "options": ["Local Area Network", "Large Access Node", "Limited Area Net", "Long-range Antenna Network"], "answer": "Local Area Network"},
            "related": ["wan", "ethernet", "wifi 7", "router", "network"]
        },

        "wan": {
            "beginner": "WAN-ul e ca o autostradă care leagă orașe întregi. În timp ce LAN-ul e casa ta, WAN-ul e internetul întreg — conectează milioane de LAN-uri din toată lumea.",
            "professional": "WAN (Wide Area Network) acoperă arii geografice extinse, conectând LAN-uri prin routere și link-uri de telecomunicații. Internetul este cel mai mare WAN.",
            "expert": "WAN technologies: MPLS, SD-WAN, VPN site-to-site, leased lines, satelit. Protocoale: BGP pentru rutare inter-domenii, MPLS pentru traffic engineering. SD-WAN optimizează traficul pe multiple link-uri.",
            "code": "# Verifică latența către un server extern\nimport subprocess\nresult = subprocess.run(['ping', '-n', '4', 'google.com'], capture_output=True, text=True)\nprint(result.stdout)",
            "real_world": "Când accesezi un site din America sau Asia, datele călătoresc prin WAN. Companiile cu birouri în mai multe țări folosesc WAN pentru a conecta echipele.",
            "quiz": {"question": "Internetul este un exemplu de...?", "options": ["WAN", "LAN", "PAN", "MAN"], "answer": "WAN"},
            "related": ["lan", "router", "ip", "dns", "network"]
        },

        "subnet mask": {
            "beginner": "Subnet mask e ca un separator care îți spune care parte din adresa IP e numele străzii și care e numărul casei. Ajută router-ul să știe unde să trimită datele.",
            "professional": "Subnet mask separă adresa IP în porțiunea de rețea și porțiunea de host. Notație: zecimală punctată (255.255.255.0) sau CIDR (/24).",
            "expert": "Subnetting: împărțirea unui spațiu IP în subrețele mai mici. VLSM (Variable Length Subnet Masking) pentru utilizare eficientă. Calcul: network address, broadcast address, usable hosts. Supernetting pentru agregare de rute.",
            "code": "# Calculează adresa de rețea dintr-un IP și subnet mask\nimport ipaddress\nip = ipaddress.IPv4Address('192.168.1.100')\nsubnet = ipaddress.IPv4Network('192.168.1.0/24', strict=False)\nprint(f\"Adresa IP: {ip}\")\nprint(f\"Rețea: {subnet.network_address}\")\nprint(f\"Broadcast: {subnet.broadcast_address}\")\nprint(f\"Host-uri utilizabile: {subnet.num_addresses - 2}\")",
            "real_world": "Administratorii de rețea folosesc subnet mask-uri pentru a organiza rețelele pe departamente. Acasă, router-ul tău folosește de obicei 255.255.255.0.",
            "quiz": {"question": "Ce înseamnă /24 în notație CIDR?", "options": ["255.255.255.0", "255.0.0.0", "255.255.0.0", "255.255.255.255"], "answer": "255.255.255.0"},
            "related": ["ip address", "router", "lan", "dns", "network"]
        },

        "mac address": {
            "beginner": "Adresa MAC e ca o amprentă digitală unică pentru fiecare dispozitiv. Niciun telefon, laptop sau imprimantă nu are aceeași adresă MAC — e înscrisă în hardware din fabrică.",
            "professional": "MAC (Media Access Control) address este un identificator unic de 48 de biți asignat interfeței de rețea. Format: șase perechi hexazecimale (00:1A:2B:3C:4D:5E).",
            "expert": "MAC: OUI (Organizationally Unique Identifier) — primii 24 biți identifică producătorul. MAC filtering pentru securitate, MAC spoofing pentru bypass. ARP (Address Resolution Protocol) leagă IP-ul de MAC.",
            "code": "# Obține adresa MAC a mașinii curente\nimport uuid\nmac = uuid.getnode()\nmac_address = ':'.join(f'{(mac >> 8*i) & 0xff:02x}' for i in range(5, -1, -1))\nprint(f\"Adresa MAC: {mac_address}\")",
            "real_world": "Când te conectezi la un Wi-Fi, router-ul îți înregistrează adresa MAC. Unele rețele folosesc MAC filtering pentru a permite doar dispozitivelor autorizate.",
            "quiz": {"question": "Adresa MAC are...?", "options": ["48 biți (6 perechi hexa)", "32 biți (4 perechi)", "64 biți (8 perechi)", "16 biți (2 perechi)"], "answer": "48 biți (6 perechi hexa)"},
            "related": ["ip address", "ethernet", "router", "lan", "network"]
        },

                "ssl": {
            "beginner": "SSL e ca un bodyguard care-ți păzește conversațiile pe internet. Când vezi lacătul în browser, SSL-ul lucrează să țină hackerii departe de datele tale.",
            "professional": "SSL (Secure Sockets Layer) și succesorul său TLS criptează comunicarea între browser și server. TLS 1.3 este standardul actual, oferind securitate pentru HTTPS.",
            "expert": "TLS 1.3: elimină algoritmi slabi (RC4, MD5), suportă doar forward secrecy, handshake redus la 1-RTT. Certificate X.509, PKI, chain of trust, certificate pinning, OCSP stapling.",
            "code": "# Verifică versiunea TLS a unui server\nimport ssl\nimport socket\nctx = ssl.create_default_context()\nwith ctx.wrap_socket(socket.socket(), server_hostname='google.com') as s:\n    s.connect(('google.com', 443))\n    print(f\"Versiune TLS: {s.version()}\")",
            "real_world": "Când faci cumpărături online, SSL/TLS îți criptează datele cardului. Orice site cu 'https://' și lacătul verde folosește această tehnologie.",
            "quiz": {"question": "Care este succesorul modern al SSL?", "options": ["TLS (Transport Layer Security)", "SSH", "FTP", "HTTP"], "answer": "TLS (Transport Layer Security)"},
            "related": ["https", "encryption", "certificate", "tls", "cybersecurity"]
        },

        "tls": {
            "beginner": "TLS e versiunea modernă a SSL-ului. E ca un scut invizibil care-ți protejează parolele, mesajele și plățile online de ochii curioșilor.",
            "professional": "TLS (Transport Layer Security) asigură confidențialitatea, integritatea și autentificarea în comunicațiile web. TLS 1.3 oferă securitate îmbunătățită față de versiunile anterioare.",
            "expert": "TLS 1.3: elimină suportul pentru ciphersuite-uri nesigure, impune Perfect Forward Secrecy, reduce latența handshake-ului. 0-RTT pentru reconectări rapide. Certificate Transparency pentru detectarea certificatelor malițioase.",
            "code": "# Testează suportul TLS al unui server\nimport subprocess\nresult = subprocess.run(['openssl', 's_client', '-connect', 'google.com:443', '-tls1_3'], capture_output=True, text=True)\nif 'CONNECTED' in result.stdout:\n    print(\"Serverul suportă TLS 1.3!\")\nelse:\n    print(\"Serverul nu suportă TLS 1.3\")",
            "real_world": "Băncile, magazinele online și rețelele sociale folosesc TLS să-ți protejeze datele. Fără TLS, oricine ar putea să-ți fure parolele pe Wi-Fi-ul public.",
            "quiz": {"question": "Ce oferă Perfect Forward Secrecy în TLS?", "options": ["Chei de sesiune unice, neafectate de compromiterea cheii private", "Criptare mai rapidă", "Compatibilitate cu dispozitive vechi", "Conexiune fără parolă"], "answer": "Chei de sesiune unice, neafectate de compromiterea cheii private"},
            "related": ["ssl", "https", "encryption", "certificate", "cybersecurity"]
        },

        "certificate": {
            "beginner": "Un certificat digital e ca un pașaport pentru site-uri web. Demonstrează că site-ul este cine pretinde că e, nu un fals. E eliberat de autorități de încredere.",
            "professional": "Certificatele SSL/TLS (X.509) autentifică identitatea unui website și permit criptarea conexiunilor. Sunt emise de Certificate Authorities (CA) precum Let's Encrypt, DigiCert, Sectigo.",
            "expert": "Certificate: Domain Validation (DV), Organization Validation (OV), Extended Validation (EV). Chain of trust: root CA → intermediate CA → leaf certificate. Wildcard (*.domain.com), SAN (multi-domain). ACME protocol pentru automatizare (Let's Encrypt).",
            "code": "# Generează certificat self-signed (test)\nimport subprocess\nsubprocess.run([\n    'openssl', 'req', '-x509', '-newkey', 'rsa:4096',\n    '-keyout', 'key.pem', '-out', 'cert.pem',\n    '-days', '365', '-nodes',\n    '-subj', '/CN=localhost'\n])\nprint(\"Certificat self-signed generat!\")",
            "real_world": "Let's Encrypt oferă certificate SSL GRATUITE pentru milioane de site-uri. Înainte, certificatele costau sute de dolari pe an. Acum orice site poate fi securizat gratuit.",
            "quiz": {"question": "Ce organizație oferă certificate SSL gratuite?", "options": ["Let's Encrypt", "Microsoft", "Google", "Amazon"], "answer": "Let's Encrypt"},
            "related": ["ssl", "tls", "https", "certificate authority", "encryption"]
        },

        "ssh": {
            "beginner": "SSH e ca o cheie magică ce-ți deschide ușa către servere de la distanță. Poți controla un computer din altă parte a lumii, în siguranță, prin criptare.",
            "professional": "SSH (Secure Shell) oferă acces terminal criptat la servere remote. Înlocuiește Telnet și FTP nesecurizate. Folosește autentificare prin parolă sau chei publice/private.",
            "expert": "SSH: key-based auth (RSA 4096, Ed25519), agent forwarding, port forwarding (local/remote/dynamic), SSH tunneling, config file (~/.ssh/config), multiplexing pentru conexiuni rapide, SSHFP DNS records.",
            "code": "# Conectare SSH cu Python\nimport paramiko\nclient = paramiko.SSHClient()\nclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())\nclient.connect('example.com', username='user', key_filename='/path/to/key')\nstdin, stdout, stderr = client.exec_command('ls -la')\nprint(stdout.read().decode())\nclient.close()",
            "real_world": "Administratorii de servere folosesc SSH zilnic. GitHub folosește SSH pentru push securizat de cod. Fără SSH, internetul ar fi mult mai nesigur.",
            "quiz": {"question": "SSH înlocuiește ce protocol nesecurizat?", "options": ["Telnet", "HTTPS", "FTP", "SMTP"], "answer": "Telnet"},
            "related": ["encryption", "linux", "terminal", "ssl", "cybersecurity"]
        },

        "flask": {
            "beginner": "Flask e ca un set de piese LEGO pentru site-uri web în Python. E atât de simplu încât poți face un site funcțional în doar 5 linii de cod.",
            "professional": "Flask este un micro-framework Python pentru aplicații web, oferind routing, template-uri Jinja2 și suport pentru extensii. Ideal pentru API-uri și aplicații mici până la medii.",
            "expert": "Flask: application factory pattern, blueprints pentru modularizare, context locals (request, session, g), before/after request hooks, error handlers. Extensii: Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-CORS.",
            "code": "from flask import Flask, jsonify\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return jsonify({'message': 'Salut, Andrei!', 'project': 'AEGIS'})\n\nif __name__ == '__main__':\n    app.run(debug=True, port=5000)",
            "real_world": "Pinterest, LinkedIn și Reddit au folosit Flask la început. E perfect pentru prototipuri rapide și API-uri. AEGIS ar putea avea un backend Flask!",
            "quiz": {"question": "Flask este un framework pentru...?", "options": ["Python", "JavaScript", "Ruby", "PHP"], "answer": "Python"},
            "related": ["python", "django", "api rest", "json", "fastapi"]
        },

        "django": {
            "beginner": "Django e ca un supermarket complet pentru site-uri web. Vine cu TOT inclus — autentificare, bază de date, panou admin. E framework-ul Python preferat pentru proiecte mari.",
            "professional": "Django este un framework Python full-stack, urmând principiul 'batteries included'. Oferă ORM, admin panel, autentificare, formulare și securitate încorporată.",
            "expert": "Django: MTV architecture (Model-Template-View), QuerySet lazy evaluation, middleware stack, class-based views, Django REST Framework pentru API-uri. Migrații automate de schemă. Suport pentru PostgreSQL, MySQL, SQLite.",
            "code": "# Django: views.py\nfrom django.http import JsonResponse\n\ndef home(request):\n    return JsonResponse({\n        'message': 'Salut, Andrei!',\n        'project': 'AEGIS',\n        'framework': 'Django'\n    })",
            "real_world": "Instagram, Spotify, YouTube și NASA folosesc Django. E alegerea #1 pentru startup-uri care vor să construiască rapid aplicații web complexe și sigure.",
            "quiz": {"question": "Django urmează principiul...?", "options": ["Batteries included (totul inclus)", "Micro-framework minimalist", "Doar frontend", "Doar pentru mobile"], "answer": "Batteries included (totul inclus)"},
            "related": ["python", "flask", "sql", "orm", "fastapi"]
        },

        "fastapi": {
            "beginner": "FastAPI e ca Flask, dar pe steroizi. E cel mai rapid framework Python pentru API-uri și vine cu documentație automată. Scrii codul și primești un site de testare GRATIS.",
            "professional": "FastAPI este un framework Python modern pentru API-uri, folosind type hints și async/await. Oferă validare automată, documentație OpenAPI și performanță comparabilă cu Node.js.",
            "expert": "FastAPI: Pydantic pentru validare, Starlette pentru performanță asincronă, dependency injection, background tasks, WebSocket support. Generare automată de OpenAPI/Swagger docs. Testare cu TestClient.",
            "code": "from fastapi import FastAPI\napp = FastAPI(title='AEGIS API', version='1.0')\n\n@app.get('/')\nasync def home():\n    return {'message': 'Salut, Andrei!', 'project': 'AEGIS'}\n\n@app.get('/terms/{term_id}')\nasync def get_term(term_id: str):\n    return {'term': term_id, 'definition': 'Coming soon...'}",
            "real_world": "Netflix, Uber și Microsoft folosesc FastAPI pentru API-uri rapide. E framework-ul Python cu cea mai rapidă creștere. Perfect pentru un API AEGIS în viitor!",
            "quiz": {"question": "FastAPI generează automat...?", "options": ["Documentație OpenAPI/Swagger", "Aplicații mobile", "Jocuri video", "Editoare de text"], "answer": "Documentație OpenAPI/Swagger"},
            "related": ["python", "flask", "django", "api rest", "json"]
        },

        "pandas": {
            "beginner": "Pandas e ca un Excel ultra-inteligent pentru programatori. Analizezi date, faci grafice, filtrezi informații — totul în câteva linii de cod Python.",
            "professional": "Pandas este o bibliotecă Python pentru manipularea și analiza datelor, oferind structuri DataFrame și Series pentru date tabulare și time series.",
            "expert": "Pandas: vectorized operations, groupby aggregation, merge/join/concat, pivot tables, handling missing data, multi-index, datetime operations. Integrare cu NumPy, Matplotlib, Scikit-learn. Performanță prin Cython backend.",
            "code": "import pandas as pd\n\ndata = {\n    'nume': ['Andrei', 'Ana', 'Maria'],\n    'varsta': [15, 17, 14],\n    'proiect': ['AEGIS', 'Design', 'Web']\n}\ndf = pd.DataFrame(data)\nprint(df.describe())\nprint(f\"Vârsta medie: {df['varsta'].mean():.1f} ani\")",
            "real_world": "Toate companiile mari — Google, Facebook, Goldman Sachs — folosesc Pandas pentru analiză de date. E folosit în știință, finanțe, marketing și sport.",
            "quiz": {"question": "Care e structura principală de date în Pandas?", "options": ["DataFrame", "Array", "List", "Dictionary"], "answer": "DataFrame"},
            "related": ["python", "numpy", "matplotlib", "data science", "machine learning"]
        },

        "numpy": {
            "beginner": "NumPy e ca un calculator științific ultra-rapid pentru Python. Face calcule matematice complexe în milisecunde — matrice, vectori, statistică.",
            "professional": "NumPy este fundamentul științei datelor în Python, oferind array-uri N-dimensionale și funcții matematice optimizate în C pentru performanță.",
            "expert": "NumPy: ndarray cu broadcasting, vectorization, slicing avansat, fancy indexing, universal functions (ufuncs), linear algebra (numpy.linalg), random sampling, FFT. Integrare cu C prin ctypes și Cython.",
            "code": "import numpy as np\n\narr = np.array([1, 2, 3, 4, 5])\nprint(f\"Medie: {np.mean(arr)}\")\nprint(f\"Deviație standard: {np.std(arr):.2f}\")\nprint(f\"Maxim: {np.max(arr)}, Minim: {np.min(arr)}\")\n\n# Operații pe matrice\nmatrix = np.array([[1, 2], [3, 4]])\nprint(f\"Determinant: {np.linalg.det(matrix):.0f}\")",
            "real_world": "NASA, CERN și toate companiile de AI folosesc NumPy. E biblioteca #1 pentru calcule științifice în Python. Toate framework-urile de ML (TensorFlow, PyTorch) se bazează pe concepte NumPy.",
            "quiz": {"question": "NumPy optimizează calculele prin...?", "options": ["Vectorizare și cod C", "JavaScript în browser", "CSS și HTML", "Machine learning"], "answer": "Vectorizare și cod C"},
            "related": ["python", "pandas", "matplotlib", "data science", "scikit-learn"]
        },

        "tensorflow": {
            "beginner": "TensorFlow e ca o fabrică de inteligență artificială creată de Google. Construiești modele AI care recunosc poze, traduc limbi și prezic viitorul — totul cu cod Python.",
            "professional": "TensorFlow este un framework open-source de la Google pentru machine learning și deep learning. Oferă Keras API pentru construirea rapidă de rețele neuronale.",
            "expert": "TensorFlow: static și dynamic graphs (Eager Execution), TensorBoard pentru vizualizare, TF Serving pentru deployment, TF Lite pentru mobile/IoT, distribuție pe GPU/TPU, mixed precision training.",
            "code": "import tensorflow as tf\nfrom tensorflow.keras.models import Sequential\nfrom tensorflow.keras.layers import Dense\n\nmodel = Sequential([\n    Dense(128, activation='relu', input_shape=(784,)),\n    Dense(64, activation='relu'),\n    Dense(10, activation='softmax')\n])\nmodel.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])\nprint(\"Model TensorFlow creat cu succes!\")",
            "real_world": "Google Translate, Google Photos și YouTube recomandări folosesc TensorFlow. E folosit de Airbnb, Uber, Twitter și mii de companii pentru AI.",
            "quiz": {"question": "Cine a creat TensorFlow?", "options": ["Google", "Facebook", "Microsoft", "Apple"], "answer": "Google"},
            "related": ["pytorch", "keras", "deep learning", "machine learning", "ai"]
        },

        "pytorch": {
            "beginner": "PyTorch e ca un atelier de construit inteligență artificială creat de Facebook. E mai flexibil decât TensorFlow și preferat de cercetători pentru experimente rapide.",
            "professional": "PyTorch este un framework open-source de machine learning dezvoltat de Meta (Facebook). Oferă dynamic computation graphs și este lider în cercetarea AI.",
            "expert": "PyTorch: autograd pentru diferențiere automată, TorchScript pentru producție, distributed training (DDP, FSDP), mixed precision cu torch.cuda.amp, ONNX export. Domină conferințele AI (NeurIPS, ICML).",
            "code": "import torch\nimport torch.nn as nn\n\nmodel = nn.Sequential(\n    nn.Linear(784, 128),\n    nn.ReLU(),\n    nn.Linear(128, 10),\n    nn.Softmax(dim=1)\n)\nprint(f\"Model PyTorch creat cu {sum(p.numel() for p in model.parameters())} parametri\")",
            "real_world": "Tesla folosește PyTorch pentru mașinile autonome. OpenAI a folosit PyTorch pentru a antrena modelele GPT. E framework-ul #1 în cercetarea AI.",
            "quiz": {"question": "Cine a creat PyTorch?", "options": ["Meta (Facebook)", "Google", "Microsoft", "Amazon"], "answer": "Meta (Facebook)"},
            "related": ["tensorflow", "deep learning", "machine learning", "ai", "python"]
        },

        "scikit-learn": {
            "beginner": "Scikit-learn e ca o cutie de instrumente gata-făcute pentru machine learning. Ai nevoie de un algoritm? E deja acolo. Importi, antrenezi, folosești — în 3 linii de cod.",
            "professional": "Scikit-learn este o bibliotecă Python pentru machine learning clasic, oferind algoritmi pentru clasificare, regresie, clustering și preprocessing.",
            "expert": "Scikit-learn: Pipeline API pentru workflows, cross-validation (KFold, Stratified), GridSearchCV/RandomizedSearchCV pentru hyperparameter tuning, feature engineering (OneHotEncoder, StandardScaler), metrics comprehensive.",
            "code": "from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\nmodel = RandomForestClassifier(n_estimators=100)\nmodel.fit(X_train, y_train)\nprint(f\"Acuratețe: {accuracy_score(y_test, model.predict(X_test)):.2%}\")",
            "real_world": "Spotify folosește Scikit-learn pentru recomandări muzicale. Băncile îl folosesc pentru detectarea fraudelor. E biblioteca #1 pentru ML clasic în Python.",
            "quiz": {"question": "Scikit-learn e folosit pentru...?", "options": ["Machine Learning clasic", "Deep Learning", "Web Development", "Mobile Apps"], "answer": "Machine Learning clasic"},
            "related": ["python", "pandas", "numpy", "machine learning", "tensorflow"]
        },

        "jupyter": {
            "beginner": "Jupyter e ca un caiet de laborator digital. Scrii cod, vezi rezultatele imediat, adaugi notițe și grafice — totul într-un singur loc. Perfect pentru experimente și învățare.",
            "professional": "Jupyter Notebook este o aplicație web interactivă pentru crearea și partajarea documentelor cu cod live, ecuații, vizualizări și text narativ.",
            "expert": "Jupyter: kernel-uri multiple (Python, R, Julia), magics (%timeit, %%bash), widget-uri interactive, JupyterLab ca IDE complet, nbconvert pentru export (PDF, HTML, slides). Voilà pentru dashboard-uri.",
            "code": "# Într-un notebook Jupyter:\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nx = np.linspace(0, 10, 100)\ny = np.sin(x)\nplt.plot(x, y)\nplt.title('Grafic creat în Jupyter')\nplt.show()",
            "real_world": "Data scientists la Google, Netflix și NASA folosesc Jupyter zilnic. E tool-ul standard pentru analiză de date, cercetare AI și tutoriale de programare.",
            "quiz": {"question": "Jupyter suportă doar Python?", "options": ["Nu — suportă R, Julia și altele", "Da, doar Python", "Doar JavaScript", "Doar Java"], "answer": "Nu — suportă R, Julia și altele"},
            "related": ["python", "pandas", "matplotlib", "data science", "anaconda"]
        },

        "matplotlib": {
            "beginner": "Matplotlib e ca un pictor pentru datele tale. Transformă numerele în grafice frumoase — linii, bare, puncte. E cel mai vechi și mai folosit tool de vizualizare din Python.",
            "professional": "Matplotlib este o bibliotecă Python pentru crearea de vizualizări statice, animate și interactive. Oferă control complet asupra fiecărui element al graficului.",
            "expert": "Matplotlib: Figure și Axes architecture, subplots, custom styling (rcParams), backends (Agg, TkAgg, interactive), animații (FuncAnimation), integrare cu Pandas și Seaborn.",
            "code": "import matplotlib.pyplot as plt\n\nluni = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai']\ntermeni_aegis = [51, 380, 785, 1010, 1430]\n\nplt.figure(figsize=(10, 6))\nplt.plot(luni, termeni_aegis, marker='o', color='#00ffcc', linewidth=2)\nplt.title('Creșterea AEGIS', fontsize=16)\nplt.xlabel('Luna')\nplt.ylabel('Număr de termeni')\nplt.grid(True, alpha=0.3)\nplt.show()",
            "real_world": "Toate publicațiile științifice folosesc Matplotlib pentru grafice. NASA îl folosește pentru vizualizarea datelor spațiale. E fundamentul vizualizării în Python.",
            "quiz": {"question": "Matplotlib este o bibliotecă pentru...?", "options": ["Vizualizare de date", "Machine Learning", "Web Development", "Baze de date"], "answer": "Vizualizare de date"},
            "related": ["python", "numpy", "pandas", "seaborn", "data science"]
        },

        "seaborn": {
            "beginner": "Seaborn e ca un designer de modă pentru grafice. Ia Matplotlib-ul de bază și îl face SUPERB — culori frumoase, stiluri elegante, totul automat.",
            "professional": "Seaborn este o bibliotecă Python de vizualizare statistică, construită peste Matplotlib. Oferă interfețe simplificate pentru grafice statistice complexe.",
            "expert": "Seaborn: heatmaps, pairplots, violin plots, swarm plots, facet grids pentru vizualizări multi-dimensionale. Integrare nativă cu Pandas DataFrames. Teme built-in (darkgrid, whitegrid, ticks).",
            "code": "import seaborn as sns\nimport pandas as pd\n\ndata = pd.DataFrame({\n    'nivel': ['Începător', 'Profesionist', 'Expert'] * 5,\n    'scor': [85, 72, 95, 78, 88, 92, 90, 85, 98, 82, 79, 91, 87, 93, 96]\n})\nsns.barplot(data=data, x='nivel', y='scor', palette='viridis')\nplt.title('Performanță AEGIS pe nivele')\nplt.show()",
            "real_world": "Cercetătorii în științe sociale și biologie folosesc Seaborn pentru analize statistice vizuale. E standardul pentru grafice științifice elegante.",
            "quiz": {"question": "Seaborn e construit peste...?", "options": ["Matplotlib", "NumPy", "Pandas", "Scikit-learn"], "answer": "Matplotlib"},
            "related": ["matplotlib", "pandas", "python", "data science", "numpy"]
        },

        "opencv": {
            "beginner": "OpenCV e ca un ochi magic pentru computer. Îl învață să vadă și să înțeleagă poze și video — recunoaște fețe, obiecte, mișcare.",
            "professional": "OpenCV (Open Source Computer Vision Library) este o bibliotecă open-source pentru computer vision și procesare de imagini, cu peste 2500 de algoritmi optimizați.",
            "expert": "OpenCV: image processing (filtre, morphing, thresholding), feature detection (SIFT, ORB, FAST), object detection (Haar cascades, DNN module), camera calibration, video analysis, integrare CUDA pentru GPU.",
            "code": "import cv2\nimport numpy as np\n\n# Citește o imagine și aplică detecție de margini\nimg = cv2.imread('poza.jpg')\nedges = cv2.Canny(img, 100, 200)\ncv2.imshow('Margini detectate', edges)\ncv2.waitKey(0)\ncv2.destroyAllWindows()",
            "real_world": "Tesla folosește OpenCV pentru mașini autonome. Instagram și Snapchat pentru filtre faciale. Sistemele de securitate pentru recunoaștere facială.",
            "quiz": {"question": "OpenCV e specializat în...?", "options": ["Computer Vision", "Web Development", "Baze de date", "Blockchain"], "answer": "Computer Vision"},
            "related": ["python", "deep learning", "ai", "computer vision", "tensorflow"]
        },

        "git": {
            "beginner": "Git e ca un jurnal magic pentru codul tău. Salvează fiecare schimbare și poți să te întorci oricând la o versiune anterioară. E ca un 'undo' infinit și puternic.",
            "professional": "Git este un sistem de versionare distribuit care urmărește modificările în codul sursă. Concepte fundamentale: commit, branch, merge, rebase, remote.",
            "expert": "Git avansat: interactive rebase, cherry-pick, bisect pentru debugging, hooks (pre-commit, post-receive), submodules, worktrees, reflog pentru recuperare. GitFlow și trunk-based development workflows.",
            "code": "# Git workflow zilnic\ngit status                    # Vezi ce ai modificat\ngit add .                     # Adaugă toate schimbările\ngit commit -m \"+420 termeni\"  # Salvează local\ngit push origin main          # Trimite pe GitHub\ngit log --oneline -5          # Vezi ultimele 5 commit-uri",
            "real_world": "AEGIS e pe Git chiar acum. Linux kernel-ul (cel mai mare proiect open-source) folosește Git. Toate companiile tech — Google, Microsoft, Apple — folosesc Git.",
            "quiz": {"question": "Ce comandă Git trimite codul pe server?", "options": ["git push", "git send", "git upload", "git deploy"], "answer": "git push"},
            "related": ["github", "github actions", "devops", "version control", "ci/cd"]
        },

        "github actions": {
            "beginner": "GitHub Actions e ca un robot-asistent care lucrează pentru tine. De fiecare dată când pui cod nou pe GitHub, robotul îl testează automat și îți spune dacă e totul bine.",
            "professional": "GitHub Actions este o platformă CI/CD integrată în GitHub pentru automatizarea workflow-urilor: testare, build, deployment direct din repository.",
            "expert": "GitHub Actions: YAML workflows, events triggers (push, pull_request, schedule), matrix builds pentru testare multiplatformă, secrets management, self-hosted runners, marketplace cu acțiuni comunitare.",
            "code": "# .github/workflows/test.yml\nname: Test AEGIS\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - uses: actions/setup-python@v4\n        with:\n          python-version: '3.11'\n      - run: pip install -r requirements.txt\n      - run: python -m pytest tests/",
            "real_world": "AEGIS poate folosi GitHub Actions pentru a testa automat codul la fiecare push. Facebook, Google și mii de proiecte open-source îl folosesc zilnic.",
            "quiz": {"question": "GitHub Actions este un tool de...?", "options": ["CI/CD — Integrare și Deployment Continuu", "Design grafic", "Editare video", "Baze de date"], "answer": "CI/CD — Integrare și Deployment Continuu"},
            "related": ["github", "git", "devops", "ci/cd", "docker"]
        },

        "ci/cd": {
            "beginner": "CI/CD e ca o bandă rulantă magică pentru cod. Scrii codul, iar banda îl testează automat și îl pune pe internet. Fără muncă manuală, fără stres, fără erori.",
            "professional": "CI/CD (Continuous Integration / Continuous Delivery) automatizează testarea și deployment-ul codului, permițând livrări rapide și sigure în producție.",
            "expert": "CI/CD pipeline: build → test → stage → deploy. Tools: GitHub Actions, Jenkins, GitLab CI, CircleCI. Strategii: blue-green deployment, canary releases, feature flags. Infrastructure as Code pentru medii consistente.",
            "code": "# Exemplu: Pipeline CI/CD simplu\n# 1. Developer push-uiește codul\n# 2. CI: Build + Test automat\n# 3. CD: Deploy pe staging\n# 4. Aprobare manuală (opțional)\n# 5. CD: Deploy pe producție\nprint(\"AEGIS deployed successfully!\")",
            "real_world": "Netflix deploy-ează de mii de ori pe zi folosind CI/CD. Amazon face deploy la fiecare secundă. CI/CD e standardul în industrie pentru livrare rapidă și sigură.",
            "quiz": {"question": "Ce înseamnă CD în CI/CD?", "options": ["Continuous Delivery/Deployment", "Code Development", "Computer Design", "Cloud Database"], "answer": "Continuous Delivery/Deployment"},
            "related": ["github actions", "devops", "git", "docker", "jenkins"]
        },

        "devops": {
            "beginner": "DevOps e ca o punte între programatori și administratorii de servere. În loc să se certe, lucrează împreună să livreze cod mai repede și mai sigur.",
            "professional": "DevOps este o cultură și set de practici care unifică development-ul (Dev) și operațiunile (Ops), automatizând întregul ciclu de viață al aplicațiilor.",
            "expert": "DevOps practices: CI/CD, Infrastructure as Code (Terraform, Ansible), monitoring (Prometheus, Grafana), logging (ELK stack), containerization (Docker, Kubernetes). CALMS framework: Culture, Automation, Lean, Measurement, Sharing.",
            "code": "# DevOps: Monitorizare simplă cu Prometheus\nfrom prometheus_client import start_http_server, Counter\n\nrequests_total = Counter('aegis_requests_total', 'Total requests to AEGIS')\nrequests_total.inc()\nstart_http_server(8000)\nprint(\"Metrics available at http://localhost:8000\")",
            "real_world": "Amazon, Netflix și Etsy au revoluționat DevOps. Companiile care adoptă DevOps deploy-ează de 200x mai frecvent și recuperează din incidente de 24x mai rapid.",
            "quiz": {"question": "DevOps unește...?", "options": ["Development și Operations", "Design și Operations", "Development și Optimization", "Database și Operations"], "answer": "Development și Operations"},
            "related": ["ci/cd", "docker", "kubernetes", "github actions", "terraform"]
        }

        
            "graphql": {
            "beginner": "GraphQL e ca un restaurant unde comanzi EXACT ce vrei, nici mai mult, nici mai puțin. În loc să primești un platou fix (ca la REST), tu scrii ce câmpuri vrei și le primești fix pe acelea.",
            "professional": "GraphQL este un limbaj de interogare pentru API-uri care permite clientului să solicite exact datele de care are nevoie. Folosește un singur endpoint și un sistem de tipuri puternic definit.",
            "expert": "GraphQL: schema definită cu tipuri, query-uri, mutații și subscription-uri. Resolvere, batching și caching cu DataLoader. Apollo Client/Server, Federation pentru microservicii. Persisted queries, security (depth limiting, rate limiting).",
            "code": "# Query GraphQL\nquery {\n  user(id: \"1\") {\n    name\n    email\n    posts {\n      title\n    }\n  }\n}",
            "real_world": "GitHub, Facebook, Shopify și multe altele folosesc GraphQL. În loc să faci 5 cereri REST, faci una singură și primești exact ce ai nevoie.",
            "quiz": {"question": "GraphQL este alternativă la...?", "options": ["REST API", "SOAP", "gRPC", "WebSockets"], "answer": "REST API"},
            "related": ["api rest", "apollo", "federation", "graphql client", "schema"]
        },

        "redis": {
            "beginner": "Redis e ca o memorie ultra-rapidă care ține minte date între sesiuni. Dacă un site e încet, Redis accelerează lucrurile stocând rezultatele în cache.",
            "professional": "Redis este un magazin de structuri de date în-memory, folosit ca cache, message broker și bază de date NoSQL. Suportă string-uri, hash-uri, liste, set-uri, hyperloglogs, stream-uri.",
            "expert": "Redis: persistare RDB/AOF, replicare master-slave, cluster, sentinel pentru HA. Operații atomice, Lua scripting, pub/sub. RedisJSON, RedisSearch, RedisTimeSeries ca module. Pipeline și tranzacții.",
            "code": "# Redis cu Python (redis-py)\nimport redis\nr = redis.Redis(host='localhost', port=6379, db=0)\nr.set('user:1', 'Andrei')\nprint(r.get('user:1'))",
            "real_world": "Twitter, GitHub, Stack Overflow folosesc Redis pentru cache. De asemenea, stochează sesiuni de utilizator, cozi de mesaje, și contoare în timp real.",
            "quiz": {"question": "Redis stochează date în...?", "options": ["memorie (RAM)", "disc dur", "bandă magnetică", "nor"], "answer": "memorie (RAM)"},
            "related": ["cache", "database", "message queue", "pub/sub", "memcached"]
        },

        "kafka": {
            "beginner": "Kafka e ca o bandă rulantă de mesaje între aplicații. O aplicație pune mesaje la un capăt, alta le ia de la celălalt. Poate gestiona milioane de mesaje pe secundă.",
            "professional": "Apache Kafka este o platformă distribuită de streaming de evenimente. Folosește topic-uri, producători, consumatori, brokeri. Oferă durabilitate, scalabilitate și ordonare.",
            "expert": "Kafka: partiționare, replicare, offset management, exactly-once semantics, Kafka Streams, ksqlDB, Connect pentru integrare. ZooKeeper sau KRaft pentru consens. Raft în noile versiuni.",
            "code": "# Producător Kafka simplu (Python)\nfrom kafka import KafkaProducer\nproducer = KafkaProducer(bootstrap_servers='localhost:9092')\nproducer.send('topic-test', b'Mesaj de la AEGIS')\nproducer.flush()",
            "real_world": "LinkedIn, Netflix, Uber folosesc Kafka pentru procesare în timp real. De exemplu, când livrezi mâncare, Kafka transmite comanda între sisteme.",
            "quiz": {"question": "Kafka este specializat în...?", "options": ["streaming de evenimente", "stocare de fișiere", "baze de date SQL", "machine learning"], "answer": "streaming de evenimente"},
            "related": ["message queue", "streaming", "zookeeper", "event sourcing", "pub/sub"]
        },

        "elasticsearch": {
            "beginner": "Elasticsearch e ca Google pentru datele tale. Cauți ceva în aplicație și găsești instant, chiar și în milioane de documente. E perfect pentru căutare și analiză rapidă.",
            "professional": "Elasticsearch este un motor de căutare și analiză distribuit, bazat pe Lucene. Suportă text complet, agregări, geo-search, și este parte din stack-ul ELK.",
            "expert": "Elasticsearch: cluster, noduri, shard-uri, replica-uri. Query DSL, bool queries, aggregations buckets/metrics, mapping, analizoare (stemming, tokenizare). Ingest pipelines, rollups, ILM. Securitate și audit.",
            "code": "# Căutare în Elasticsearch (Python)\nfrom elasticsearch import Elasticsearch\nes = Elasticsearch(['http://localhost:9200'])\nres = es.search(index='articole', body={'query': {'match': {'titlu': 'AEGIS'}}})\nprint(res['hits']['hits'])",
            "real_world": "Wikipedia, GitHub, eBay folosesc Elasticsearch pentru căutare. Este și baza pentru logging centralizat (ELK: Elasticsearch, Logstash, Kibana).",
            "quiz": {"question": "Elasticsearch este bazat pe...?", "options": ["Lucene", "MySQL", "MongoDB", "Redis"], "answer": "Lucene"},
            "related": ["kibana", "logstash", "elk", "search", "lucene"]
        },

        "prometheus": {
            "beginner": "Prometheus e ca un monitor care urmărește sănătatea aplicațiilor. Colectează metrici (câte cereri, cât timp, erori) și te alertează când ceva nu merge bine.",
            "professional": "Prometheus este un sistem open-source de monitorizare și alertare, cu model pull-based, metrici multi-dimensionale, și limbaj de interogare PromQL.",
            "expert": "Prometheus: exposition metrics (client libraries), exporters, service discovery, TSDB, recording rules, Alertmanager. Integrare cu Grafana. Federation. Pushgateway pentru job-uri scurte.",
            "code": "# Exporter simplu Python\nfrom prometheus_client import start_http_server, Counter\nc = Counter('requests_total', 'Total requests')\nc.inc()\nstart_http_server(8000)",
            "real_world": "Kubernetes folosește Prometheus implicit pentru monitorizare. Multe companii monitorizează microserviciile cu Prometheus + Grafana.",
            "quiz": {"question": "Prometheus folosește modelul...?", "options": ["pull (trage metrici)", "push (împinge metrici)", "batch", "real-time push"], "answer": "pull (trage metrici)"},
            "related": ["grafana", "alertmanager", "metrics", "monitoring", "kubernetes"]
        },

        "grafana": {
            "beginner": "Grafana e ca un tablou de bord superb pentru datele tale. Ia metrici din Prometheus, Elasticsearch și le arată în grafice colorate, ușor de citit.",
            "professional": "Grafana este o platformă open-source pentru vizualizare și analiză de metrici. Suportă multiple surse de date (Prometheus, Loki, Elasticsearch, InfluxDB, MySQL).",
            "expert": "Grafana: dashboard-uri, panel-uri, variabile, alertare, anotări, plugin-uri, provisionare (as code). Integrare cu Loki pentru loguri, Tempo pentru trace-uri. SSO și permisiuni RBAC.",
            "code": "# Configurare sursă de date în Grafana (JSON)\n{\n  \"name\": \"Prometheus\",\n  \"type\": \"prometheus\",\n  \"url\": \"http://prometheus:9090\",\n  \"access\": \"proxy\"\n}",
            "real_world": "Grafana este folosit de companii ca PayPal, Bloomberg, eBay pentru a monitoriza sănătatea sistemelor și a afișa KPI-uri executive.",
            "quiz": {"question": "Grafana este folosit pentru...?", "options": ["vizualizare metrici", "bază de date", "server web", "compilator"], "answer": "vizualizare metrici"},
            "related": ["prometheus", "loki", "dashboard", "monitoring", "timeseries"]
        },

        "terraform": {
            "beginner": "Terraform e ca un arhitect care desenează toată infrastructura IT ca pe un plan. Cu câteva linii de cod, creezi servere, baze de date, rețele — totul la comandă.",
            "professional": "Terraform este un tool Infrastructure as Code (IaC) de la HashiCorp, care folosește limbaj declarativ HCL pentru a provisiona resurse în cloud și on-premise.",
            "expert": "Terraform: state management (local/remote), modules, providers (AWS, Azure, GCP), workspaces, import. Terragrunt pentru orchestrare. Plan/apply/destroy. Sentinel pentru policy as code.",
            "code": "# Exemplu Terraform (AWS instance)\nresource \"aws_instance\" \"aegis\" {\n  ami           = \"ami-0c55b159cbfafe1f0\"\n  instance_type = \"t2.micro\"\n  tags = { Name = \"AEGIS-Server\" }\n}",
            "real_world": "Netflix, Airbnb, Uber își gestionează infrastructura cu Terraform. În loc să configurezi manual servere, scrii cod și Terraform le creează pe toate.",
            "quiz": {"question": "Terraform este un tool de...?", "options": ["Infrastructure as Code", "CI/CD", "Containerizare", "Machine Learning"], "answer": "Infrastructure as Code"},
            "related": ["aws", "hcl", "state", "pulumi", "openstack"]
        },

        "ansible": {
            "beginner": "Ansible e ca un robot care configurează automat servere. Vrei să instalezi același soft pe 100 de servere? Ansible face asta în câteva minute.",
            "professional": "Ansible este un automation engine agentless, folosind SSH pentru a rula playbook-uri scrise în YAML. Folosit pentru configurare, deploy, orchestră.",
            "expert": "Ansible: inventory, modules, playbooks, roles, ansible-vault pentru secrete, facts, handlers, tags. Tower/AWX pentru UI și orchestră avansată. Plugins de conexiune și inventar.",
            "code": "# Playbook Ansible pentru instalare nginx\n- hosts: webservers\n  tasks:\n    - name: Install nginx\n      apt:\n        name: nginx\n        state: present",
            "real_world": "Red Hat, NASA, Evernote folosesc Ansible. Este simplu și nu necesită agenți pe servere, doar SSH.",
            "quiz": {"question": "Ansible este un tool de...?", "options": ["automatizare configurare", "bază de date", "server web", "design grafic"], "answer": "automatizare configurare"},
            "related": ["devops", "automation", "ssh", "yaml", "terraform"]
        },

        "rust": {
            "beginner": "Rust e un limbaj de programare care e și rapid ca C++, și sigur ca Python. Nu se blochează, nu are erori de memorie, și e iubit de programatori.",
            "professional": "Rust este un limbaj de programare sistem care garantează siguranța memoriei fără garbage collector. Folosește ownership, borrowing, lifetimes. Performanță similară C++.",
            "expert": "Rust: cargo (build system), crates, pattern matching, trait-uri, async/await, FFI cu C, WebAssembly. Zero-cost abstractions, fearless concurrency. Folosit în sisteme critice.",
            "code": "fn main() {\n    let name = \"Andrei\";\n    println!(\"Salut, {}!\", name);\n}",
            "real_world": "Firefox, Dropbox, Cloudflare folosesc Rust. De asemenea, Deno (runtime JS) e scris în Rust. Este cel mai iubit limbaj în sondaje de 8 ani consecutiv.",
            "quiz": {"question": "Rust garantează...?", "options": ["siguranța memoriei", "viteză mică", "garbage collector", "interpretare"], "answer": "siguranța memoriei"},
            "related": ["cargo", "systems programming", "memory safety", "c++", "webassembly"]
        },

        "webassembly": {
            "beginner": "WebAssembly (WASM) e ca un super-putere pentru browser. Cod scris în C++, Rust, Go rulează aproape la fel de repede ca nativ în pagină web.",
            "professional": "WebAssembly este un format de instrucțiuni binare portabil, care rulează în browser la viteză aproape nativă. Permite utilizarea de cod scris în limbaje low-level în web.",
            "expert": "WASM: stack-based VM, liniară memorie, modul, import/export funcții. Compilare din C/C++ (Emscripten), Rust (wasm-pack), Go, AssemblyScript. WASI (System Interface) pentru outside browser.",
            "code": "// Exemplu WASM în Rust (export)\n#[no_mangle]\npub extern \"C\" fn add(a: i32, b: i32) -> i32 {\n    a + b\n}",
            "real_world": "Google Earth, Figma, Photoshop Web rulează WebAssembly pentru performanță mare în browser. De asemenea, jocuri și aplicații video.",
            "quiz": {"question": "WebAssembly rulează în...?", "options": ["browser", "server", "bază de date", "sistem de operare"], "answer": "browser"},
            "related": ["rust", "c++", "javascript", "wasm", "web performance"]
        },

        "grpc": {
            "beginner": "gRPC e ca un curier ultra-rapid între microservicii. Folosește Protocol Buffers (un format comprimat) și HTTP/2 pentru viteză și streaming.",
            "professional": "gRPC este un framework RPC open-source de la Google, bazat pe HTTP/2 și Protocol Buffers. Suportă streaming bidirecțional, autentificare, și generare de cod pentru mai multe limbaje.",
            "expert": "gRPC: service definition .proto, server streaming, client streaming, bidirectional streaming. Interceptors, deadline, load balancing. Integrare cu Envoy, Kubernetes. gRPC-Web pentru browser.",
            "code": "# .proto definitie\nservice AegisService {\n  rpc GetTerm (TermRequest) returns (TermResponse);\n}",
            "real_world": "Netflix, Dropbox, CoreOS folosesc gRPC pentru comunicații între microservicii. Este mai rapid decât REST JSON.",
            "quiz": {"question": "Ce format de serializare folosește gRPC?", "options": ["Protocol Buffers", "JSON", "XML", "YAML"], "answer": "Protocol Buffers"},
            "related": ["protobuf", "http2", "rpc", "microservices", "grpc gateway"]
        },

        "protobuf": {
            "beginner": "Protocol Buffers (protobuf) e ca o valiză super-eficientă pentru date. Împachetează informația mai mic și mai rapid decât JSON. E folosit de Google.",
            "professional": "Protocol Buffers este un limbaj neutru, extensibil pentru serializarea datelor structurate. Produce mesaje binare mici și rapide, cu scheme .proto și generare de cod.",
            "expert": "Protobuf: tipuri scalare, enum, mesaje nested, oneof, map. Compatibilitate înainte/înapoi cu câmpuri opționale. Well-known types (Timestamp, Any). gRPC folosește protobuf ca IDL.",
            "code": "syntax = \"proto3\";\nmessage Person {\n  string name = 1;\n  int32 age = 2;\n}",
            "real_world": "Google folosește protobuf intern pentru aproape toate serviciile. De asemenea, multe companii îl adoptă pentru performanță și compatibilitate.",
            "quiz": {"question": "Protobuf produce date în format...?", "options": ["binar", "text", "JSON", "CSV"], "answer": "binar"},
            "related": ["grpc", "serialization", "schema", "json", "messagepack"]
        }

                "hadoop": {
            "beginner": "Hadoop e ca un sistem de depozitare și procesare pentru cantități uriașe de date, răspândite pe mai multe calculatoare.",
            "professional": "Apache Hadoop este un framework open-source pentru stocarea și procesarea distribuită a big data, folosind HDFS și MapReduce.",
            "expert": "Hadoop: HDFS pentru stocare distribuită, YARN pentru gestionarea resurselor, MapReduce pentru procesare batch. Ecosistem: Hive, Pig, HBase, Spark.",
            "code": "# Exemplu simplu Hadoop MapReduce (Java)\npublic class WordCount {\n  public static void main(String[] args) throws Exception {\n    Job job = Job.getInstance();\n    job.setMapperClass(TokenizerMapper.class);\n    job.setReducerClass(IntSumReducer.class);\n    System.exit(job.waitForCompletion(true) ? 0 : 1);\n  }\n}",
            "real_world": "Companii precum Facebook, Twitter, eBay folosesc Hadoop pentru a procesa petabytes de date de utilizatori.",
            "quiz": {"question": "Ce înseamnă HDFS în Hadoop?", "options": ["Hadoop Distributed File System", "High Density File System", "Hadoop Data File System", "High Definition File System"], "answer": "Hadoop Distributed File System"},
            "related": ["spark", "hive", "big data", "mapreduce", "hdfs"]
        },
        "spark": {
            "beginner": "Spark e ca un motor ultra-rapid pentru prelucrarea datelor. Face calcule în memorie, de 100 de ori mai rapid decât Hadoop.",
            "professional": "Apache Spark este un motor unificat de procesare a datelor pentru big data, cu API-uri în Java, Scala, Python, R. Suportă SQL, streaming, ML, graph.",
            "expert": "Spark: RDD (Resilient Distributed Dataset), DataFrame, Dataset. Catalyst optimizer, Tungsten execution engine. Suportă procesare batch, streaming (Spark Streaming, Structured Streaming), MLlib, GraphX.",
            "code": "# Spark cu Python (PySpark)\nfrom pyspark.sql import SparkSession\nspark = SparkSession.builder.appName(\"AEGIS\").getOrCreate()\ndf = spark.read.csv(\"date.csv\", header=True)\ndf.show()",
            "real_world": "Netflix, Uber, Airbnb folosesc Spark pentru recomandări, analiză trafic, detectare fraudă.",
            "quiz": {"question": "Spark procesează date în...?", "options": ["memorie (RAM)", "disc dur", "bază de date", "cloud"], "answer": "memorie (RAM)"},
            "related": ["hadoop", "big data", "pyspark", "scala", "dataframe"]
        },
        "hive": {
            "beginner": "Hive e ca un translator care îți permite să scrii comenzi SQL pentru datele din Hadoop, fără să știi programare complexă.",
            "professional": "Apache Hive este un data warehouse construit peste Hadoop, care oferă un limbaj asemănător SQL (HiveQL) pentru interogarea datelor stocate în HDFS.",
            "expert": "Hive: HiveQL compilat în MapReduce, Tez sau Spark. Metastore pentru metadate (bazat pe RDBMS). Suportă partiționare, bucket, UDF-uri.",
            "code": "-- HiveQL\nCREATE TABLE users (id INT, name STRING)\nROW FORMAT DELIMITED FIELDS TERMINATED BY ',';\nLOAD DATA INPATH '/data/users.csv' INTO TABLE users;\nSELECT COUNT(*) FROM users;",
            "real_world": "Amazon, Netflix, LinkedIn folosesc Hive pentru analize de date și rapoarte pe big data.",
            "quiz": {"question": "Ce limbaj folosește Hive pentru interogări?", "options": ["HiveQL", "SQL", "MapReduce", "Java"], "answer": "HiveQL"},
            "related": ["hadoop", "spark", "hql", "big data", "data warehouse"]
        },
        "pig": {
            "beginner": "Pig e ca un script simplu pentru prelucrarea datelor mari. Scrii câteva comenzi, iar el le transformă în programe complexe.",
            "professional": "Apache Pig este o platformă de analiză a datelor mari care folosește un limbaj procedural numit Pig Latin, transformând scripturile în job-uri MapReduce, Tez sau Spark.",
            "expert": "Pig Latin: LOAD, FOREACH, FILTER, GROUP, JOIN, STORE. Permite UDF-uri în Java, Python, JavaScript. Suportă tipuri complexe (bag, tuple, map).",
            "code": "-- Pig Latin\nusers = LOAD '/data/users.csv' USING PigStorage(',') AS (id:int, name:chararray);\ngrouped = GROUP users BY id;",
            "real_world": "Yahoo, Twitter, LinkedIn au folosit Pig pentru a procesa fluxuri de date înaintea apariției Spark.",
            "quiz": {"question": "Care este limbajul lui Apache Pig?", "options": ["Pig Latin", "SQL", "Java", "Python"], "answer": "Pig Latin"},
            "related": ["hadoop", "hive", "big data", "mapreduce", "pig latin"]
        },
        "hbase": {
            "beginner": "HBase e ca o bază de date distribuită care permite citiri și scrieri în timp real pe miliarde de rânduri, ca un Google Bigtable.",
            "professional": "Apache HBase este o bază de date NoSQL distribuită, column-oriented, construită peste HDFS, care oferă acces în timp real la date mari.",
            "expert": "HBase: model tabelar cu rânduri și coloane, chei de rând sortate. Suportă versionare, compresie, filtre. Folosește ZooKeeper pentru coordonare.",
            "code": "# HBase shell\ncreate 'users', 'personal', 'professional'\nput 'users', 'row1', 'personal:name', 'Andrei'\nget 'users', 'row1'",
            "real_world": "Facebook folosește HBase pentru sistemul de mesagerie, iar Twitter pentru analytics.",
            "quiz": {"question": "HBase este o bază de date de tip...?", "options": ["column-oriented", "document", "key-value", "graph"], "answer": "column-oriented"},
            "related": ["hadoop", "hdfs", "big data", "nosql", "zookeeper"]
        },
        "zookeeper": {
            "beginner": "ZooKeeper e ca un organizator pentru sisteme distribuite. Ține evidența serverelor și ajută la coordonarea lor.",
            "professional": "Apache ZooKeeper este un serviciu centralizat pentru menținerea configurației, denumirii și sincronizării în sisteme distribuite.",
            "expert": "ZooKeeper: arhitectură master-slave, znode-uri (date), observatori, consens atomic. Folosit de Kafka, HBase, Hadoop, Solr.",
            "code": "# Conectare ZooKeeper cu Python (kazoo)\nfrom kazoo.client import KazooClient\nzk = KazooClient(hosts='127.0.0.1:2181')\nzk.start()\nzk.create('/aegis', b'some_data')",
            "real_world": "Apache Kafka, HBase și Solr folosesc ZooKeeper pentru a gestiona cluster-ele.",
            "quiz": {"question": "Ce rol are ZooKeeper în sisteme distribuite?", "options": ["coordonare", "stocare date", "procesare batch", "streaming"], "answer": "coordonare"},
            "related": ["kafka", "hbase", "distributed systems", "consensus", "apache"]
        },
        "airflow": {
            "beginner": "Airflow e ca un ceas inteligent care programează și monitorizează fluxuri de lucru (workflow-uri) în lumea datelor.",
            "professional": "Apache Airflow este o platformă open-source pentru crearea, programarea și monitorizarea workflow-urilor (DAG-uri) scrise în Python.",
            "expert": "Airflow: DAG (Directed Acyclic Graph), operatori, senzori, hook-uri. UI pentru monitorizare, backfill, variabile, conexiuni. Executori: Sequential, Local, Celery, Kubernetes.",
            "code": "# DAG simplu Airflow\nfrom airflow import DAG\nfrom airflow.operators.bash import BashOperator\nfrom datetime import datetime\nwith DAG('aegis_dag', start_date=datetime(2025,1,1)) as dag:\n    t1 = BashOperator(task_id='print_date', bash_command='date')",
            "real_world": "Airbnb (creatorul), Spotify, Walmart folosesc Airflow pentru a programa pipeline-uri de date.",
            "quiz": {"question": "Ce reprezintă DAG în Airflow?", "options": ["Directed Acyclic Graph", "Data Aggregation Graph", "Dynamic Algorithm Graph", "Distributed Access Gateway"], "answer": "Directed Acyclic Graph"},
            "related": ["etl", "workflow", "python", "big data", "scheduler"]
        },
        "dbt": {
            "beginner": "dbt e ca un instrument care te ajută să transformi datele din baze de date folosind doar SQL, ca un fel de control al versiunilor pentru date.",
            "professional": "dbt (data build tool) este un instrument de transformare a datelor în depozitele de date, folosind SELECT-uri SQL și concepte de modularizare, testare și documentare.",
            "expert": "dbt: modele (SQL), materializări (table, view, incremental, ephemeral), teste (unique, not null, relationships), documentație, lineage, CLI și Cloud.",
            "code": "-- dbt model (models/users.sql)\nSELECT id, name, email FROM {{ ref('raw_users') }} WHERE status = 'active'",
            "real_world": "GitLab, Snowflake, JetBlue folosesc dbt pentru analize de date și documentare.",
            "quiz": {"question": "Ce limbaj se folosește în dbt pentru definirea modelelor?", "options": ["SQL", "Python", "Java", "Scala"], "answer": "SQL"},
            "related": ["etl", "data warehouse", "snowflake", "bigquery", "analytics"]
        },
        "snowflake": {
            "beginner": "Snowflake e ca un depozit de date în nor, care separă stocarea de calcul, astfel încât să poți crește independent și să plătești doar pentru ce folosești.",
            "professional": "Snowflake este o platformă de date bazată pe cloud, cu arhitectură separată de stocare și calcul, suport pentru date semi-structurate și scalare aproape infinită.",
            "expert": "Snowflake: virtual warehouses, micro-partitioning, time travel, zero-copy cloning, suport pentru JSON, Avro, Parquet. Integrare cu dbt, Spark, Airflow.",
            "code": "-- SQL în Snowflake\nCREATE WAREHOUSE aegis_wh;\nCREATE DATABASE aegis_db;\nCREATE TABLE users (id INT, name STRING);\nSELECT * FROM users;",
            "real_world": "5000+ companii, inclusiv Adobe, DoorDash, Netflix, folosesc Snowflake ca data cloud.",
            "quiz": {"question": "Snowflake separă...?", "options": ["stocarea de calcul", "datele de metadate", "cloud de on-premise", "SQL de NoSQL"], "answer": "stocarea de calcul"},
            "related": ["cloud", "data warehouse", "bigquery", "redshift", "databricks"]
        },
        "bigquery": {
            "beginner": "BigQuery e ca un motor de căutare pentru date masive, în cloud-ul Google. Scrii SQL și el găsește răspunsuri rapid, chiar și în petabytes.",
            "professional": "Google BigQuery este un data warehouse serverless, scalabil, care permite interogarea rapidă a seturilor mari de date folosind SQL, cu securitate și integrare în ecosistemul Google Cloud.",
            "expert": "BigQuery: arhitectură coloane, clustering, partiționare, BI Engine, federated queries (Cloud Storage, Drive, Sheets), integrare cu Data Studio, Looker.",
            "code": "# Python client pentru BigQuery\nfrom google.cloud import bigquery\nclient = bigquery.Client()\nquery = \"SELECT name FROM `project.dataset.users` LIMIT 10\"\ndf = client.query(query).to_dataframe()",
            "real_world": "Twitter, Spotify, The New York Times folosesc BigQuery pentru analize de date în timp real.",
            "quiz": {"question": "BigQuery este produs de...?", "options": ["Google", "Amazon", "Microsoft", "Snowflake"], "answer": "Google"},
            "related": ["gcp", "data warehouse", "big data", "sql", "analytics"]
        },
        "databricks": {
            "beginner": "Databricks e ca un mediu de lucru unificat pentru ingineri de date și oameni de știință, construit în jurul Apache Spark.",
            "professional": "Databricks este o platformă unificată de analiză a datelor bazată pe cloud, care combină data engineering, data science și machine learning, creată de fondatorii Apache Spark.",
            "expert": "Databricks: Delta Lake pentru stocare fiabilă, MLflow pentru ciclul ML, colaborare în notebook-uri, auto-scaling, cluster management, Unity Catalog.",
            "code": "# PySpark în Databricks Notebook\ndf = spark.read.csv(\"/mnt/data.csv\", header=True)\ndf.createOrReplaceTempView(\"users\")\nresult = spark.sql(\"SELECT name FROM users\")",
            "real_world": "Shell, HP, Comcast, Bank of America folosesc Databricks pentru transformarea datelor și AI.",
            "quiz": {"question": "Databricks a fost fondat de creatorii...?", "options": ["Apache Spark", "Hadoop", "Kafka", "Airflow"], "answer": "Apache Spark"},
            "related": ["spark", "delta lake", "mlflow", "lakehouse", "big data"]
        },
        "delta lake": {
            "beginner": "Delta Lake e ca un strat de fiabilitate peste stocarea ta de date, asigurându-se că nu se corup și că poți face modificări în siguranță.",
            "professional": "Delta Lake este un strat de stocare open-source care aduce fiabilitatea ACID a bazelor de date la lacurile de date (data lakes), suportând citiri și scrieri concurente.",
            "expert": "Delta Lake: tranzacții ACID, time travel (versiuni), schema enforcement, schema evolution, merge (upsert/delete), streaming, integrare cu Spark.",
            "code": "# Delta Lake în PySpark\ndf.write.format(\"delta\").save(\"/mnt/delta/users\")\ndf2 = spark.read.format(\"delta\").load(\"/mnt/delta/users\")\ndf2.createOrReplaceTempView(\"users\")",
            "real_world": "Folosit intens de companii care construiesc data lakes fiabile, cum ar fi Apple, Samsung, Adobe.",
            "quiz": {"question": "Ce oferă Delta Lake lacurilor de date?", "options": ["tranzacții ACID", "numai citire", "procesare în memorie", "indexare"], "answer": "tranzacții ACID"},
            "related": ["spark", "databricks", "data lake", "iceberg", "hudi"]
        },
        "apache ice": {
            "beginner": "Apache Iceberg e ca un catalog inteligent pentru tabele mari, care face căutările și actualizările mult mai rapide și eficiente.",
            "professional": "Apache Iceberg este un format de tabel open-source pentru seturi de date uriașe, conceput pentru a îmbunătăți performanța și fiabilitatea în data lakes.",
            "expert": "Iceberg: partiționare ascunsă, evoluția schemei, time travel, compatibilitate cu multiple engine-uri (Spark, Flink, Trino).",
            "code": "-- Creare tabel Iceberg în Spark\nCREATE TABLE iceberg.default.users (id INT, name STRING) USING iceberg",
            "real_world": "Netflix, Apple, LinkedIn folosesc Iceberg pentru a gestiona petabytes de date în mod eficient.",
            "quiz": {"question": "Iceberg este un format de...?", "options": ["tabel", "fișier", "stream", "bază de date"], "answer": "tabel"},
            "related": ["data lake", "spark", "flink", "trino", "lakehouse"]
        },
        "flink": {
            "beginner": "Flink e ca un procesor de date în flux continuu (streaming), care reacționează la evenimente în timp real.",
            "professional": "Apache Flink este un framework de procesare a fluxurilor de date (stream processing) cu latență scăzută, toleranță la erori și capabilități de procesare batch.",
            "expert": "Flink: DataStream API, Table API, CEP (complex event processing), exactly-once semantics, checkpoints și savepoints, integrare cu Kafka, RabbitMQ.",
            "code": "# Flink DataStream în Java\nDataStream<String> stream = env.addSource(new FlinkKafkaConsumer<>(\"topic\", new SimpleStringSchema(), props));\nstream.map(s -> s.toUpperCase()).print();",
            "real_world": "Alibaba, Uber, Zalando folosesc Flink pentru sisteme de recomandare, monitorizare, fraude.",
            "quiz": {"question": "Flink este specializat în...?", "options": ["stream processing", "batch processing", "data warehouse", "machine learning"], "answer": "stream processing"},
            "related": ["kafka", "streaming", "spark streaming", "event driven", "real time"]
        },
        "kinesis": {
            "beginner": "Kinesis e ca o conductă de date în cloud-ul Amazon, care transportă milioane de mesaje în timp real între aplicații.",
            "professional": "Amazon Kinesis este o platformă de streaming de date în timp real, care permite colectarea, procesarea și analiza fluxurilor de date la scară largă pe AWS.",
            "expert": "Kinesis: Kinesis Data Streams (shard-uri), Kinesis Data Firehose (încărcare în S3, Redshift, Elasticsearch), Kinesis Data Analytics (SQL, Flink).",
            "code": "# Python boto3 pentru Kinesis\nimport boto3\nkinesis = boto3.client('kinesis')\nresponse = kinesis.put_record(StreamName='test', Data=b'data', PartitionKey='1')",
            "real_world": "Netflix, Pinterest, Airbnb folosesc Kinesis pentru înregistrarea activităților utilizatorilor și monitorizare.",
            "quiz": {"question": "Kinesis este serviciu de streaming de la...?", "options": ["Amazon AWS", "Google Cloud", "Microsoft Azure", "Apache"], "answer": "Amazon AWS"},
            "related": ["aws", "streaming", "kafka", "firehose", "real time"]
        },
        "pubsub": {
            "beginner": "Pub/Sub (Google) e ca un sistem de anunțuri între aplicații: una publică un mesaj, iar altele care sunt abonate îl primesc instant.",
            "professional": "Google Cloud Pub/Sub este un serviciu de mesagerie asincronă, scalabil, care permite transmiterea de mesaje între aplicații, cu suport pentru at-least-once și exactly-once.",
            "expert": "Pub/Sub: topic-uri, abonamente, pull/push, ordering, retry policies, dead-letter topics. Integrare cu Cloud Functions, Dataflow, GKE.",
            "code": "# Python client pentru Pub/Sub\nfrom google.cloud import pubsub_v1\npublisher = pubsub_v1.PublisherClient()\ntopic_path = publisher.topic_path('project', 'topic')\nfuture = publisher.publish(topic_path, b'data')",
            "real_world": "Spotify, Twitter, Google folosesc Pub/Sub pentru a decupla microserviciile și a construi sisteme event-driven.",
            "quiz": {"question": "Pub/Sub este un serviciu de...?", "options": ["mesagerie asincronă", "bază de date", "streaming video", "calcul serverless"], "answer": "mesagerie asincronă"},
            "related": ["gcp", "message queue", "kafka", "rabbitmq", "event driven"]
        },
        "rabbitmq": {
            "beginner": "RabbitMQ e ca un poștaș pentru mesaje între aplicații. Trimiți o scrisoare (mesaj), iar el se asigură că ajunge la destinația corectă.",
            "professional": "RabbitMQ este un message broker open-source, care implementează AMQP (Advanced Message Queuing Protocol), folosit pentru comunicare asincronă între servicii.",
            "expert": "RabbitMQ: exchange (direct, topic, fanout, headers), queue, binding, durable messages, confirm, prefetch, cluster, management UI.",
            "code": "# Python pika pentru RabbitMQ\nimport pika\nconnection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))\nchannel = connection.channel()\nchannel.queue_declare(queue='aegis')\nchannel.basic_publish(exchange='', routing_key='aegis', body='Hello')",
            "real_world": "Reddit, Instagram, Pinterest folosesc RabbitMQ pentru a gestiona cozi de sarcini și actualizări în timp real.",
            "quiz": {"question": "RabbitMQ implementează protocolul...?", "options": ["AMQP", "MQTT", "HTTP", "gRPC"], "answer": "AMQP"},
            "related": ["message queue", "broker", "amqp", "celery", "microservices"]
        },
        "activemq": {
            "beginner": "ActiveMQ e ca un alt poștaș pentru mesaje, asemănător cu RabbitMQ, dar mai vechi și folosit în aplicații enterprise Java.",
            "professional": "Apache ActiveMQ este un message broker open-source, bazat pe Java, care suportă multiple protocoale: AMQP, MQTT, STOMP, OpenWire.",
            "expert": "ActiveMQ: persistent messages, virtual topics, network of brokers, JMS (Java Message Service) compliant, integrare cu Spring.",
            "code": "// Java JMS cu ActiveMQ\nimport javax.jms.*;\nConnectionFactory factory = new ActiveMQConnectionFactory(\"tcp://localhost:61616\");\nConnection conn = factory.createConnection();\nSession session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);\nMessageProducer producer = session.createProducer(new ActiveMQQueue(\"aegis\"));",
            "real_world": "Folosit în multe aplicații enterprise Java, în special în sistemele bancare și de logistică.",
            "quiz": {"question": "ActiveMQ este scris în...?", "options": ["Java", "C++", "Python", "Go"], "answer": "Java"},
            "related": ["jms", "message queue", "broker", "activemq artemis", "stomp"]
        },

        # ============================================
        # 📚 EXPERT TERMS — Quick Definitions
        # ============================================
        
        # --- Cunoștințe Existente ---
        "variabilă": "O variabilă este ca o cutie în care poți păstra o valoare. În Python, o creezi simplu: `x = 5`.",
        "listă": "O listă este o colecție ordonată de elemente, care poate fi modificată. Se scrie între paranteze pătrate: `[1, 2, 3]`.",
        "dicționar": "Un dicționar este o colecție de perechi cheie-valoare. Se scrie între acolade: `{'nume': 'Andrei', 'vârstă': 15}`.",
        "funcție": "O funcție este un bloc de cod reutilizabil care face o anumită sarcină. Se definește cu `def`: `def salut(): print('Salut!')`.",
        "buclă": "O buclă (loop) este o instrucțiune care repetă o bucată de cod. `for` și `while` sunt cele mai comune în Python.",
        "clasă": "O clasă (class) este un șablon pentru crearea de obiecte. Este fundamentul Programării Orientate pe Obiecte (OOP).",
        "criptomonedă": "O monedă digitală descentralizată. Exemple: Bitcoin (BTC), Ethereum (ETH).",

        "mit": "MIT (Massachusetts Institute of Technology) este una dintre cele mai prestigioase universități din lume, lider în cercetare și inovație tehnologică.",
        "white hat": "White Hat Hacking este practica etică și legală de a testa securitatea sistemelor pentru a le proteja împotriva atacatorilor reali.",
        "vpn": "Un VPN (Virtual Private Network) creează o conexiune criptată și sigură între dispozitivul tău și internet.",
        "ransomware": "Ransomware este un tip de malware care criptează fișierele victimei și cere o răscumpărare pentru a le debloca.",
        "phishing": "Phishing-ul este o tentativă de fraudă prin care atacatorii se dau drept entități de încredere pentru a fura date personale.",
        "criptografie": "Criptografia este știința de a proteja informația prin transformarea ei într-un format care nu poate fi citit fără o cheie.",
        "hash": "Un hash este o amprentă digitală unică a unui set de date, obținută printr-o funcție matematică ireversibilă.",
        "parolă": "O parolă este o cheie secretă, formată dintr-un șir de caractere, folosită pentru autentificare și protecția conturilor.",
        "malware": "Malware (software malițios) este orice program creat pentru a dăuna unui sistem, a fura date sau a prelua controlul.",
        "antivirus": "Un antivirus este un program care detectează, blochează și elimină malware-ul de pe un dispozitiv.",

        "ddos": "Un atac DDoS (Distributed Denial of Service) încearcă să supraaglomereze un server cu trafic masiv pentru a-l face inaccesibil.",
        "aws": "AWS (Amazon Web Services) este cea mai mare platformă de cloud computing din lume, oferind peste 200 de servicii.",
        "azure": "Microsoft Azure este platforma de cloud computing a Microsoft, folosită pentru crearea, testarea și gestionarea aplicațiilor.",
        "google cloud": "Google Cloud Platform (GCP) este suita de servicii cloud oferită de Google.",
        "saas": "SaaS (Software as a Service) este un model de livrare software unde utilizatorii accesează aplicația prin internet, fără a o instala.",
        "ip": "O adresă IP este o etichetă numerică unică atribuită fiecărui dispozitiv conectat la o rețea.",
        "dns": "DNS (Domain Name System) este sistemul care traduce numele de domenii (ex: google.com) în adrese IP.",
        "tcp": "TCP (Transmission Control Protocol) este un protocol de comunicare sigur, care garantează livrarea pachetelor de date.",
        "http": "HTTP (HyperText Transfer Protocol) este protocolul folosit pentru a transfera pagini web între un server și un browser.",
        "router": "Un router este un dispozitiv care direcționează traficul de date între diferite rețele.",

        "javascript": "JavaScript is the programming language of the web. It makes websites interactive and works directly in your browser.",
        "java": "Java is a powerful, general-purpose programming language used for building Android apps, enterprise software, and large systems.",
        "c++": "C++ is a high-performance programming language used for game development, operating systems, and applications requiring speed.",
        "algoritm": "An algorithm is a step-by-step set of instructions to solve a specific problem, like a recipe for a computer.",
        "structură de date": "A data structure is a way of organizing and storing data so it can be accessed and modified efficiently, like lists or dictionaries.",
        "debugging": "Debugging is the process of finding and fixing errors (bugs) in your code.",

        "ide": "An IDE (Integrated Development Environment) is a software application that helps you write code, like PyCharm or VS Code.",
        "compilator": "A compiler is a program that translates your code into machine language that a computer can understand and run.",
        "linux": "Linux is a free, open-source operating system known for its stability and security. It's widely used on servers and by developers.",
        "windows": "Microsoft Windows is the most popular operating system for personal computers, known for its user-friendly interface.",
        "macos": "macOS is the operating system developed by Apple for its Mac computers, known for its elegant design and smooth performance.",
        "terminal": "The terminal is a text-based interface where you can type commands to interact with your computer directly.",
        "bash": "Bash is a popular command-line shell on Linux and macOS that lets you run commands and write scripts.",
        "powershell": "PowerShell is a powerful command-line tool from Microsoft for automating tasks on Windows.",

        "kernel": "The kernel is the heart of an operating system. It manages everything from your hardware to your software.",
        "driver": "A driver is a small piece of software that allows your operating system to talk to a piece of hardware, like a printer.",
        "guido van rossum": "Guido van Rossum is the Dutch programmer who created the Python programming language in the late 1980s.",
        "silicon valley": "Silicon Valley is a region in California, USA, that is famous for being the global center for technology and innovation.",
        "istoria internetului": "The internet began in the late 1960s as a US military project called ARPANET and became public in the 1990s.",
        "alan turing": "Alan Turing was a brilliant British mathematician who is considered the father of computer science and artificial intelligence.",
        "react": "React is a popular JavaScript library for building user interfaces, developed by Facebook.",

        "angular": "Angular is a TypeScript-based web application framework led by Google.",
        "vue": "Vue.js is a progressive JavaScript framework for building user interfaces.",
        "django": "Django is a high-level Python web framework that encourages rapid development.",
        "flask": "Flask is a micro web framework written in Python, known for its simplicity.",
        "sql": "SQL (Structured Query Language) is a language for managing and querying relational databases.",
        "github": "GitHub is a platform for hosting and collaborating on Git repositories.",
        "oop": "OOP (Object-Oriented Programming) is a paradigm based on objects containing data and code.",
        "recursivitate": "Recursion is a technique where a function calls itself to solve a problem.",
        "api rest": "A REST API is an API that follows the principles of Representational State Transfer.",
        "json": "JSON (JavaScript Object Notation) is a lightweight data-interchange format.",
        "xml": "XML (eXtensible Markup Language) is a markup language for storing and transporting data.",
        "agile": "Agile is a methodology for software development that emphasizes flexibility and collaboration.",
        "scrum": "Scrum is a framework within Agile for managing complex projects.",

        "devops": "DevOps is a set of practices that combines software development and IT operations.",
        "ci/cd": "CI/CD (Continuous Integration/Continuous Delivery) is a method to frequently deliver apps.",
        "typescript": "TypeScript is a typed superset of JavaScript that compiles to plain JavaScript.",
        "swift": "Swift is a powerful programming language for iOS, macOS, watchOS, and tvOS.",
        "kotlin": "Kotlin is a modern programming language used mainly for Android development.",
        "rust": "Rust is a language for performance and safety, especially safe concurrency.",
        "go": "Go is a statically typed, compiled language designed at Google.",
        "php": "PHP is a popular general-purpose scripting language especially suited to web development.",
        "ruby": "Ruby is a dynamic, open-source programming language with a focus on simplicity.",

        "scala": "Scala is a language that combines object-oriented and functional programming.",
        "perl": "Perl is a highly capable, feature-rich programming language with over 30 years of development.",
        "r programming": "R is a programming language and environment specifically designed for statistical analysis and data visualization.",
        "matlab": "MATLAB is a high-level language and interactive environment used by engineers and scientists for numerical computation.",
        "framework": "A framework is a pre-built set of tools and libraries that provides a foundation for developing software applications.",
        "library": "A library is a collection of pre-written code that developers can use to perform common tasks.",
        "sdk": "An SDK (Software Development Kit) is a collection of tools that allows developers to create applications for a specific platform.",
        "runtime": "A runtime is the environment in which a program is executed, providing necessary services.",
        "interpreter": "An interpreter is a program that directly executes instructions written in a programming language.",
        "syntax": "Syntax refers to the set of rules that define the structure of a programming language.",

        "semantics": "Semantics refers to the meaning of a program's instructions, separate from their syntax.",
        "variable scope": "Variable scope determines where a variable can be accessed within a program.",
        "global variable": "A global variable is declared outside any function and can be accessed from anywhere in the code.",
        "local variable": "A local variable is declared inside a function and can only be used within that function.",
        "constant": "A constant is a value that cannot be altered during the execution of a program.",
        "operator": "An operator is a symbol that tells the compiler to perform specific mathematical or logical manipulations.",
        "operand": "An operand is the object on which an operator performs an action.",
        "expression": "An expression is a combination of operators and operands that evaluates to a single value.",
        "statement": "A statement is a single instruction that performs a specific action.",
        "block": "A block is a group of statements that are treated as a single unit.",
        "comment": "A comment is a programmer-readable explanation in the source code, ignored by the compiler.",
        "whitespace": "Whitespace refers to characters like spaces and tabs, often used to format code.",

        "indentation": "Indentation is the space at the beginning of a code line, used in Python to define code blocks.",
        "exception": "An exception is an error that occurs during the execution of a program.",
        "try-except": "Try-except is a block used in Python to handle exceptions gracefully.",
        "finally": "The 'finally' block is executed after a try-except block, regardless of the outcome.",
        "raise": "The 'raise' keyword in Python is used to throw an exception manually.",
        "assert": "The 'assert' statement is used to verify if a condition is true, raising an error if it is not.",
        "debugger": "A debugger is a tool used to test and debug programs by running them line by line.",
        "profiler": "A profiler is a tool that measures the performance of a program, identifying bottlenecks.",
        "refactoring": "Refactoring is the process of restructuring existing code without changing its external behavior.",
        "code smell": "A code smell is any characteristic in source code that possibly indicates a deeper problem.",
        "technical debt": "Technical debt is the implied cost of additional rework caused by choosing an easy solution now.",
        "design pattern": "A design pattern is a general, reusable solution to a commonly occurring problem in software design.",
        "singleton": "Singleton is a design pattern that restricts a class to a single instance.",

        "factory": "Factory is a design pattern that creates objects without specifying the exact class.",
        "observer": "Observer is a design pattern where an object maintains a list of its dependents and notifies them of state changes.",
        "mvc": "MVC (Model-View-Controller) is an architectural pattern for building user interfaces.",
        "tdd": "TDD (Test-Driven Development) is a process where tests are written before the code itself.",
        "unit test": "A unit test is a way to test a small, isolated piece of code to ensure it works correctly.",
        "integration test": "Integration testing is a phase where individual units are combined and tested as a group.",
        "e2e test": "End-to-end testing is a methodology to test an application's flow from start to finish.",

        "regression test": "Regression testing ensures that recent code changes have not adversely affected existing features.",
        "performance test": "Performance testing evaluates the speed, responsiveness, and stability of a system under a workload.",
        "load test": "Load testing is putting demand on a system and measuring its response.",
        "stress test": "Stress testing evaluates system robustness and error handling under extremely heavy loads.",
        "cms": "A CMS (Content Management System) is software that helps users create, manage, and modify website content.",
        "wordpress": "WordPress is a popular open-source CMS written in PHP.",
        "bootstrap": "Bootstrap is a free and open-source CSS framework for responsive, mobile-first front-end development.",
        "jquery": "jQuery is a fast, small, and feature-rich JavaScript library.",
        "ajax": "AJAX (Asynchronous JavaScript and XML) is a technique for creating fast and dynamic web pages.",
        "dom": "DOM (Document Object Model) is a programming interface for web documents.",
        "regex": "Regex (Regular Expression) is a sequence of characters that define a search pattern.",

        "unicode": "Unicode is a universal character encoding standard.",
        "ascii": "ASCII (American Standard Code for Information Interchange) is a character encoding standard.",
        "bit": "A bit is the most basic unit of information in computing.",
        "byte": "A byte is a unit of digital information that most commonly consists of eight bits.",
        "binary": "Binary is a base-2 numeral system used by computers.",
        "hexadecimal": "Hexadecimal is a base-16 numeral system used in programming.",

        "octal": "Octal is a base-8 numeral system.",
        "c#": "C# (C-Sharp) is a modern, object-oriented programming language developed by Microsoft for the .NET framework.",
        "database": "A database is an organized collection of structured information, stored and accessed electronically.",
        "relational database": "A relational database organizes data into tables with rows and columns, connected by relationships. Example: MySQL, PostgreSQL.",
        "nosql": "NoSQL databases store data in a non-tabular format, like documents or graphs. Examples: MongoDB, Cassandra, Redis.",
        "mysql": "MySQL is a popular open-source relational database management system, widely used for web applications.",
        "postgresql": "PostgreSQL is an advanced, open-source relational database known for its reliability and feature set.",
        "mongodb": "MongoDB is a NoSQL database that stores data in flexible, JSON-like documents.",

        "redis": "Redis is an in-memory data structure store used as a database, cache, and message broker.",
        "sqlite": "SQLite is a lightweight, file-based SQL database engine often used in mobile apps and small projects.",
        "orm": "ORM (Object-Relational Mapping) is a technique that lets you interact with a database using objects instead of SQL queries.",
        "acid": "ACID (Atomicity, Consistency, Isolation, Durability) are properties that guarantee reliable database transactions.",
        "normalization": "Normalization is the process of organizing database columns and tables to reduce data redundancy.",
        "index": "A database index is a data structure that improves the speed of data retrieval operations.",
        "query": "A query is a request for data from a database, usually written in SQL.",

        "join": "A JOIN clause in SQL combines rows from two or more tables based on a related column.",
        "primary key": "A primary key is a unique identifier for each record in a database table.",
        "foreign key": "A foreign key is a column that creates a link between two tables by referencing the primary key of another table.",
        "view": "A view is a virtual table based on the result-set of an SQL query.",
        "stored procedure": "A stored procedure is a set of precompiled SQL statements that can be executed on demand.",
        "trigger": "A trigger is a stored procedure that automatically executes when a specific event occurs in a database.",
        "transaction": "A transaction is a sequence of database operations treated as a single unit of work.",
        "deep learning": "Deep Learning is a subset of ML using artificial neural networks with many layers to model complex patterns.",
        "supervised learning": "Supervised learning trains an AI model on labeled data, where the correct answer is provided.",
        "unsupervised learning": "Unsupervised learning finds hidden patterns in data without pre-existing labels.",

        "reinforcement learning": "Reinforcement learning trains an agent to make decisions by rewarding desired behaviors and punishing undesired ones.",
        "overfitting": "Overfitting occurs when a model learns the training data too well, including its noise, and performs poorly on new data.",
        "underfitting": "Underfitting happens when a model is too simple to capture the underlying pattern in the data.",
        "dataset": "A dataset is a collection of data used to train, validate, and test machine learning models.",
        "feature": "A feature is an individual measurable property or characteristic used as input for a machine learning model.",
        "label": "A label is the output or target variable that a machine learning model is trying to predict.",
        "training": "Training is the process of teaching a machine learning model by feeding it data and adjusting its parameters.",
        "inference": "Inference is the process of using a trained model to make predictions on new, unseen data.",
        "epoch": "An epoch is one complete pass through the entire training dataset during model training.",

        "batch": "A batch is a subset of the training data used to update the model's parameters in one iteration.",
        "loss function": "A loss function measures how far a model's predictions are from the actual values. Lower is better.",
        "gradient descent": "Gradient descent is an optimization algorithm that minimizes the loss function by iteratively adjusting parameters.",
        "backpropagation": "Backpropagation is the algorithm that calculates how much each neuron contributed to the error and adjusts weights accordingly.",
        "activation function": "An activation function decides whether a neuron should be activated, introducing non-linearity. Examples: ReLU, Sigmoid, Tanh.",
        "cnn": "CNN (Convolutional Neural Network) is a deep learning architecture specialized for processing grid-like data, especially images.",
        "rnn": "RNN (Recurrent Neural Network) is a neural network designed to recognize patterns in sequences of data, like text or time series.",
        "lstm": "LSTM (Long Short-Term Memory) is a type of RNN capable of learning long-term dependencies.",

        "transformer": "A Transformer is a deep learning model architecture that uses self-attention, forming the basis of models like GPT and BERT.",
        "nlp": "NLP (Natural Language Processing) is a field of AI focused on the interaction between computers and human language.",
        "computer vision": "Computer vision is a field of AI that trains computers to interpret and understand visual information from images and videos.",
        "gan": "GAN (Generative Adversarial Network) consists of two neural networks (generator and discriminator) competing to create realistic synthetic data.",
        "transfer learning": "Transfer learning is a technique where a model developed for one task is reused as the starting point for another task.",
        "fine-tuning": "Fine-tuning is the process of taking a pre-trained model and training it further on a specific dataset.",
        "tokenization": "Tokenization is the process of splitting text into smaller units (tokens) like words or subwords.",
        "embedding": "An embedding is a dense vector representation of data (like words) that captures semantic meaning.",

        "llm": "LLM (Large Language Model) is an AI model trained on massive text datasets. Examples: GPT, Claude, Gemini.",
        "rag": "RAG (Retrieval-Augmented Generation) combines an LLM with a retrieval system to fetch relevant external knowledge.",
        "hallucination": "AI hallucination occurs when a model generates text that sounds plausible but is factually incorrect.",
        "prompt": "A prompt is the input text given to an AI model to guide its response.",
        "prompt engineering": "Prompt engineering is the practice of designing effective prompts to get desired outputs from AI models.",
        "temperature": "Temperature is a parameter that controls randomness in AI model outputs. Lower = more focused, Higher = more creative.",
        "html": "HTML (HyperText Markup Language) is the standard language for creating web pages and web applications.",
        "css": "CSS (Cascading Style Sheets) is a stylesheet language used to describe the presentation of a document written in HTML.",
        "sass": "Sass is a CSS preprocessor that extends CSS with features like variables, nesting, and mixins.",

        "tailwind": "Tailwind CSS is a utility-first CSS framework for rapidly building custom user interfaces.",
        "responsive design": "Responsive design is an approach where a website adapts its layout to different screen sizes and devices.",
        "media query": "A media query is a CSS technique used to apply styles conditionally based on device characteristics like screen width.",
        "flexbox": "Flexbox is a CSS layout module that provides an efficient way to arrange items within a container.",
        "grid": "CSS Grid is a two-dimensional layout system for creating complex web layouts with rows and columns.",
        "frontend": "Frontend refers to the client-side part of a web application — what users see and interact with in their browser.",
        "backend": "Backend refers to the server-side part of a web application that handles logic, databases, and authentication.",
        "full stack": "Full Stack development involves working on both the frontend and backend of a web application.",

        "spa": "SPA (Single Page Application) is a web app that loads a single HTML page and dynamically updates content as the user interacts.",
        "pwa": "PWA (Progressive Web App) is a web application that uses modern capabilities to deliver an app-like experience.",
        "ssr": "SSR (Server-Side Rendering) is a technique where the server generates the full HTML for a page before sending it to the browser.",
        "csr": "CSR (Client-Side Rendering) renders web pages directly in the browser using JavaScript.",
        "node.js": "Node.js is a JavaScript runtime built on Chrome's V8 engine that allows JavaScript to run on the server.",
        "npm": "npm (Node Package Manager) is the default package manager for Node.js, used to install and manage dependencies.",
        "webpack": "Webpack is a module bundler for JavaScript applications, processing and bundling assets for the browser.",
        "vite": "Vite is a modern build tool that provides a fast development server and optimized build for web projects.",
        "cors": "CORS (Cross-Origin Resource Sharing) is a security mechanism that controls how web pages can request resources from another domain.",
        "decryption": "Decryption is the process of converting encrypted data back to its original, readable form.",
        "aes": "AES (Advanced Encryption Standard) is a symmetric encryption algorithm widely used worldwide.",

        "rsa": "RSA is an asymmetric encryption algorithm used for secure data transmission and digital signatures.",
        "ssl": "SSL (Secure Sockets Layer) is a protocol for encrypting data between a web server and a browser. Now replaced by TLS.",
        "tls": "TLS (Transport Layer Security) is the successor to SSL, providing encrypted communication over the internet.",
        "https": "HTTPS is the secure version of HTTP, using TLS/SSL to encrypt data between browser and server.",
        "certificate": "An SSL/TLS certificate is a digital file that authenticates a website's identity and enables encrypted connections.",
        "xss": "XSS (Cross-Site Scripting) is a security vulnerability that allows attackers to inject malicious scripts into web pages.",
        "csrf": "CSRF (Cross-Site Request Forgery) is an attack that tricks a user into performing unwanted actions on a web application.",
        "sql injection": "SQL Injection is a code injection technique that exploits vulnerabilities in database queries.",
        "buffer overflow": "A buffer overflow occurs when a program writes more data to a block of memory than it can hold, potentially executing malicious code.",
        "zero day": "A zero-day exploit is an attack that targets a previously unknown vulnerability, before a fix is available.",
        "penetration testing": "Penetration testing (pen test) is a simulated cyberattack to evaluate the security of a system.",
        "red team": "A Red Team is a group that simulates real-world attacks to test an organization's defenses.",

        "blue team": "A Blue Team is a group that defends an organization's systems against cyber threats.",
        "purple team": "A Purple Team combines Red and Blue teams to maximize collaboration and security effectiveness.",
        "siem": "SIEM (Security Information and Event Management) provides real-time analysis of security alerts.",
        "ids": "IDS (Intrusion Detection System) monitors network traffic for suspicious activity and alerts administrators.",
        "ips": "IPS (Intrusion Prevention System) is like an IDS but can also automatically block detected threats.",
        "mfa": "MFA (Multi-Factor Authentication) requires two or more verification factors to gain access to an account.",
        "oauth": "OAuth is an open standard for access delegation, allowing users to grant third-party access without sharing passwords.",
        "jwt": "JWT (JSON Web Token) is a compact, URL-safe way to represent claims between two parties.",
        "social engineering": "Social engineering is the psychological manipulation of people to trick them into revealing confidential information.",
        "certificate authority": "A Certificate Authority (CA) is a trusted entity that issues digital certificates.",
        "gpu": "GPU (Graphics Processing Unit) is a specialized processor designed to accelerate graphics rendering and parallel computations.",
        "ram": "RAM (Random Access Memory) is temporary memory that stores data actively being used by the computer.",
        "rom": "ROM (Read-Only Memory) is non-volatile memory that stores firmware and cannot be easily modified.",
        "hdd": "HDD (Hard Disk Drive) is a traditional storage device that uses spinning magnetic disks.",

        "motherboard": "The motherboard is the main circuit board that connects all components of a computer.",
        "bios": "BIOS (Basic Input/Output System) is firmware that initializes hardware during the boot process. Now largely replaced by UEFI.",
        "uefi": "UEFI (Unified Extensible Firmware Interface) is the modern replacement for BIOS, with more features and security.",
        "overclocking": "Overclocking is the process of increasing a component's clock rate to run faster than factory specifications.",
        "cache": "Cache is a small, high-speed memory that stores frequently accessed data for quick retrieval.",
        "bandwidth": "Bandwidth is the maximum rate of data transfer across a network path, measured in bits per second.",
        "latency": "Latency is the time delay between a request and its response in a network.",
        "arduino": "Arduino is an open-source electronics platform based on easy-to-use hardware and software.",
        "raspberry pi": "Raspberry Pi is a small, affordable single-board computer used for learning programming and building projects.",
        "firmware": "Firmware is software programmed into the read-only memory of a hardware device, providing low-level control.",
        "bios update": "A BIOS update is a process of upgrading the firmware that controls the motherboard to fix bugs or add features.",
        "bitcoin": "Bitcoin (BTC) is the first and most well-known cryptocurrency, created in 2009 by an anonymous entity called Satoshi Nakamoto.",
        "ethereum": "Ethereum is a decentralized blockchain platform that enables smart contracts and decentralized applications (dApps).",

        "smart contract": "A smart contract is a self-executing program stored on a blockchain that runs when predetermined conditions are met.",
        "nft": "NFT (Non-Fungible Token) is a unique digital asset verified using blockchain technology, representing ownership of a specific item.",
        "defi": "DeFi (Decentralized Finance) is a financial system built on blockchain that operates without traditional intermediaries like banks.",
        "dao": "DAO (Decentralized Autonomous Organization) is an organization represented by rules encoded as a computer program, controlled by members.",
        "web3": "Web3 is a vision for a decentralized internet built on blockchain technologies, emphasizing user ownership and control.",
        "metamask": "MetaMask is a popular cryptocurrency wallet and gateway to blockchain apps, available as a browser extension.",
        "solidity": "Solidity is a programming language designed for writing smart contracts on Ethereum and other blockchain platforms.",
        "mining": "Mining is the process of validating transactions and adding them to a blockchain, often rewarded with cryptocurrency.",
        "pos": "Proof of Stake (PoS) is a consensus mechanism where validators stake cryptocurrency to validate transactions.",
        "pow": "Proof of Work (PoW) is a consensus mechanism where miners solve complex puzzles to validate transactions (used by Bitcoin).",
        "gas fee": "A gas fee is a transaction fee paid to network validators on blockchain platforms like Ethereum.",
        "wallet": "A crypto wallet stores private keys and allows users to send, receive, and manage their digital assets.",
        "private key": "A private key is a secret alphanumeric code that allows cryptocurrency to be spent. It must never be shared.",
        "public key": "A public key is derived from a private key and serves as an address for receiving cryptocurrency.",

        "seed phrase": "A seed phrase is a series of words that can restore a cryptocurrency wallet. It must be kept secret and safe.",
        "exchange": "A crypto exchange is a platform where users can buy, sell, and trade cryptocurrencies. Examples: Binance, Coinbase.",
        "binance": "Binance is one of the world's largest cryptocurrency exchanges by trading volume.",
        "coinbase": "Coinbase is a major US-based cryptocurrency exchange known for its user-friendly interface.",
        "ledger": "Ledger is a hardware wallet company that provides secure cold storage for cryptocurrencies.",
        "altcoin": "An altcoin is any cryptocurrency other than Bitcoin. Examples: Ethereum, Solana, Cardano.",
        "stablecoin": "A stablecoin is a cryptocurrency designed to maintain a stable value, often pegged to a fiat currency like USD.",
        "tokenomics": "Tokenomics is the study of the economic model and incentives behind a cryptocurrency or token.",
        "dapp": "A dApp (Decentralized Application) runs on a blockchain network rather than a centralized server.",
        "ipfs": "IPFS (InterPlanetary File System) is a peer-to-peer protocol for storing and sharing files in a decentralized manner.",
        "consensus": "Consensus is the mechanism by which blockchain participants agree on the validity of transactions.",
        "android": "Android is a mobile operating system developed by Google, used by billions of devices worldwide.",
        "ios": "iOS is Apple's mobile operating system for iPhone and iPad, known for its security and smooth user experience.",
        "flutter": "Flutter is Google's open-source UI toolkit for building natively compiled applications for mobile, web, and desktop from a single codebase.",
        "react native": "React Native is a framework by Meta for building mobile apps using JavaScript and React.",

        "xcode": "Xcode is Apple's integrated development environment (IDE) for building apps for iOS, macOS, watchOS, and tvOS.",
        "android studio": "Android Studio is the official IDE for Android development, built on IntelliJ IDEA.",
        "apk": "APK (Android Package) is the file format used to distribute and install applications on Android.",
        "ipa": "IPA (iOS App Store Package) is the file format for distributing iOS applications.",
        "app store": "The App Store is Apple's digital marketplace for iOS applications.",
        "google play": "Google Play is the official app store for Android devices.",
        "emulator": "An emulator is software that mimics a mobile device on a computer, used for testing apps without physical hardware.",
        "simulator": "A simulator mimics the basic behavior of a device but doesn't replicate hardware exactly, unlike an emulator.",
        "ui/ux": "UI (User Interface) is the visual design, while UX (User Experience) is how a user feels when interacting with a product.",
        "wireframe": "A wireframe is a low-fidelity visual guide representing the skeletal framework of an app or website.",
        "prototype": "A prototype is an early sample or model of a product built to test concepts before full development.",
        "mvp": "MVP (Minimum Viable Product) is a product with just enough features to attract early users and validate an idea.",
        "app lifecycle": "The app lifecycle describes the series of states an app goes through from launch to termination.",

        "push notification": "A push notification is a message sent from a server to a user's device, appearing even when the app is closed.",
        "firebase": "Firebase is Google's platform for building mobile and web apps with features like databases, auth, and analytics.",
        "swiftui": "SwiftUI is Apple's modern framework for building user interfaces across all Apple platforms using declarative Swift code.",
        "jetpack compose": "Jetpack Compose is Android's modern toolkit for building native UI using declarative Kotlin code.",
        "terraform": "Terraform is an Infrastructure as Code (IaC) tool by HashiCorp for building and managing cloud infrastructure.",
        "ansible": "Ansible is an open-source automation tool for configuration management, application deployment, and task automation.",
        "jenkins": "Jenkins is an open-source automation server used for Continuous Integration and Continuous Delivery (CI/CD).",
        "github actions": "GitHub Actions is a CI/CD platform integrated with GitHub for automating software workflows.",
        "gitlab": "GitLab is a DevOps platform that provides source code management, CI/CD, and monitoring.",

        "prometheus": "Prometheus is an open-source monitoring and alerting toolkit designed for reliability and scalability.",
        "grafana": "Grafana is an open-source platform for data visualization and monitoring dashboards.",
        "elk stack": "The ELK Stack (Elasticsearch, Logstash, Kibana) is a set of tools for searching, analyzing, and visualizing log data.",
        "nginx": "Nginx is a high-performance web server that can also act as a reverse proxy, load balancer, and HTTP cache.",
        "apache": "Apache HTTP Server is a widely-used open-source web server software.",
        "load balancer": "A load balancer distributes incoming network traffic across multiple servers to ensure availability and reliability.",
        "reverse proxy": "A reverse proxy is a server that sits in front of web servers and forwards client requests, adding security and performance.",
        "microservices": "Microservices architecture breaks an application into small, independent services that communicate over a network.",
        "monolith": "A monolithic architecture builds an application as a single, unified unit, as opposed to microservices.",
        "serverless": "Serverless computing lets you run code without managing servers. The cloud provider dynamically allocates resources.",
        "api gateway": "An API Gateway manages, routes, and secures API requests between clients and backend services.",
        "message queue": "A message queue allows applications to communicate asynchronously by sending messages. Examples: RabbitMQ, Kafka.",
        "apache kafka": "Apache Kafka is a distributed event streaming platform for building real-time data pipelines.",
        "rabbitmq": "RabbitMQ is an open-source message broker that implements the Advanced Message Queuing Protocol (AMQP).",
        "docker compose": "Docker Compose is a tool for defining and running multi-container Docker applications using a YAML file.",
        "helm": "Helm is a package manager for Kubernetes that helps deploy and manage applications.",

        "istio": "Istio is an open-source service mesh for connecting, securing, and monitoring microservices.",
        "gitops": "GitOps is a framework that uses Git as the single source of truth for declarative infrastructure and applications.",
        "big o notation": "Big O Notation describes the performance or complexity of an algorithm, specifically its worst-case scenario.",
        "time complexity": "Time complexity measures how the runtime of an algorithm grows as the input size increases.",
        "space complexity": "Space complexity measures how much memory an algorithm uses relative to the input size.",
        "array": "An array is a data structure that stores elements of the same type in contiguous memory locations.",
        "linked list": "A linked list is a linear data structure where each element points to the next one.",
        "stack": "A stack is a data structure that follows LIFO (Last In, First Out). Think of a stack of plates.",
        "queue": "A queue is a data structure that follows FIFO (First In, First Out). Think of a line at a store.",
        "hash table": "A hash table is a data structure that maps keys to values using a hash function for fast lookups.",
        "tree": "A tree is a hierarchical data structure with a root node and child nodes connected by edges.",
        "binary tree": "A binary tree is a tree where each node has at most two children.",

        "graph": "A graph is a data structure consisting of nodes (vertices) connected by edges.",
        "sorting algorithm": "A sorting algorithm arranges elements in a specific order. Examples: Quick Sort, Merge Sort, Bubble Sort.",
        "bubble sort": "Bubble Sort is a simple sorting algorithm that repeatedly compares and swaps adjacent elements.",
        "merge sort": "Merge Sort is an efficient, divide-and-conquer sorting algorithm with O(n log n) time complexity.",
        "quick sort": "Quick Sort is a fast divide-and-conquer algorithm that selects a pivot and partitions the array.",
        "binary search": "Binary Search is an algorithm that finds an element in a sorted array by repeatedly dividing the search interval in half.",
        "dp": "Dynamic Programming (DP) solves complex problems by breaking them into simpler overlapping subproblems.",
        "greedy algorithm": "A greedy algorithm makes the locally optimal choice at each step, aiming for a global optimum.",

        "boolean": "Boolean is a data type with two possible values: true or false.",
        "logic gate": "A logic gate is an electronic component that performs a Boolean function. Examples: AND, OR, NOT, XOR.",
        "set theory": "Set theory is the mathematical study of collections of objects, foundational to databases and logic programming.",
        "graph theory": "Graph theory is the study of graphs — mathematical structures used to model pairwise relations between objects.",
        "apple": "Apple Inc. is a global technology company known for the iPhone, Mac, iPad, and innovative design.",
        "google": "Google is a technology company specializing in internet services like search, cloud computing, and AI.",
        "microsoft": "Microsoft is a leading tech corporation behind Windows, Azure, Office, and Xbox.",

        "meta": "Meta (formerly Facebook) is a social media and technology company focused on connecting people and building the metaverse.",
        "amazon": "Amazon is a multinational company known for e-commerce, AWS cloud, and AI assistant Alexa.",
        "netflix": "Netflix is a streaming service that uses advanced AI algorithms for content recommendation.",
        "tesla": "Tesla is an electric vehicle and clean energy company that heavily integrates AI and autonomous driving.",
        "openai": "OpenAI is an AI research organization behind models like GPT and DALL-E.",
        "nvidia": "NVIDIA is a company known for its GPUs that power gaming, AI, and data centers worldwide.",
        "intel": "Intel is a major semiconductor company known for microprocessors that power most personal computers.",
        "amd": "AMD (Advanced Micro Devices) is a semiconductor company producing CPUs and GPUs, a key competitor to Intel and NVIDIA.",
        "arm": "ARM designs processor architectures used in most smartphones and increasingly in laptops and servers.",

        "tsmc": "TSMC (Taiwan Semiconductor Manufacturing Company) is the world's largest contract chip manufacturer.",
        "elon musk": "Elon Musk is an entrepreneur involved in Tesla, SpaceX, and xAI, pushing boundaries in tech and space.",
        "tim berners-lee": "Tim Berners-Lee is the inventor of the World Wide Web and a key figure in internet history.",
        "linus torvalds": "Linus Torvalds created the Linux kernel and also developed Git, the version control system.",
        "steve jobs": "Steve Jobs was the co-founder of Apple, a visionary behind the Macintosh, iPod, iPhone, and iPad.",
        "bill gates": "Bill Gates co-founded Microsoft and played a key role in the personal computer revolution.",
        "satoshi nakamoto": "Satoshi Nakamoto is the pseudonymous creator of Bitcoin and the first blockchain.",
        "mark zuckerberg": "Mark Zuckerberg is the co-founder and CEO of Meta (formerly Facebook).",
        "sundar pichai": "Sundar Pichai is the CEO of Google and Alphabet Inc.",

        "satya nadella": "Satya Nadella is the CEO of Microsoft, credited with its successful pivot to cloud computing.",
        "samsung galaxy s24 ultra": "Samsung Galaxy S24 Ultra este smartphone-ul flagship Samsung din 2024, cu procesor Snapdragon 8 Gen 3, cameră 200MP, S Pen integrat și AI Galaxy.",
        "samsung galaxy s25 ultra": "Samsung Galaxy S25 Ultra este cel mai avansat smartphone Samsung, lansat în 2025, cu procesor Snapdragon 8 Elite, AI avansat și cameră îmbunătățită.",
        "samsung galaxy a56": "Samsung Galaxy A56 este telefonul tău, Andrei! Un mid-range excelent cu ecran Super AMOLED 120Hz, baterie 5000mAh și suport AI.",
        "iphone 16 pro max": "iPhone 16 Pro Max este flagship-ul Apple din 2024, cu procesor A18 Pro, cameră tetraprism 5x zoom și Apple Intelligence AI.",
        "iphone 17 pro max": "iPhone 17 Pro Max este cel mai nou iPhone, lansat în 2025, cu design ultra-subțire, Dynamic Island îmbunătățit și cameră revoluționară.",
        "google pixel 9 pro": "Google Pixel 9 Pro este telefonul Google flagship cu procesor Tensor G4, cameră AI avansată și Android curat.",
        "oneplus 13": "OnePlus 13 este un flagship killer cu procesor Snapdragon 8 Elite, încărcare 100W și ecran AMOLED 120Hz.",

        "xiaomi 15 ultra": "Xiaomi 15 Ultra este telefonul premium Xiaomi cu cameră Leica, procesor Snapdragon 8 Elite și ecran AMOLED superb.",
        "huawei pura 70 ultra": "Huawei Pura 70 Ultra (fost P Series) este flagship-ul Huawei cu cameră retractabilă și procesor Kirin.",
        "nothing phone 3": "Nothing Phone 3 este telefonul inovator cu design transparent, Glyph Interface LED și sistem Android curat.",
        "samsung galaxy watch": "Samsung Galaxy Watch este o serie de smartwatch-uri premium care rulează Wear OS, cu monitorizare avansată a sănătății (ECG, tensiune arterială, somn) și integrare perfectă cu ecosistemul Samsung Galaxy.",
        "samsung galaxy watch ultra": "Samsung Galaxy Watch Ultra este cel mai rezistent smartwatch Samsung, cu carcasă din titan, baterie 590mAh și certificare militară MIL-STD-810H.",
        "apple watch ultra 3": "Apple Watch Ultra 3 este smartwatch-ul premium Apple pentru sportivi extremi, cu carcasă din titan, GPS precis și rezistență la scufundări.",
        "huawei watch": "Huawei Watch este o serie de ceasuri inteligente care rulează HarmonyOS, cunoscute pentru designul elegant, bateria de lungă durată (până la 14 zile) și monitorizarea detaliată a somnului și sănătății.",
        "google pixel watch 3": "Google Pixel Watch 3 este smartwatch-ul Google cu Wear OS, integrare Fitbit și design rotund elegant.",

        "garmin fenix 8": "Garmin Fenix 8 este un smartwatch premium pentru atleți, cu baterie solară, GPS multi-band și hărți topografice.",
        "smartwatch": "Un smartwatch este un ceas de mână digital care oferă funcții precum notificări, monitorizarea sănătății, GPS și control muzical, conectat la smartphone prin Bluetooth.",
        "wear os": "Wear OS este sistemul de operare Google pentru smartwatch-uri, folosit de mărci precum Samsung, Google Pixel Watch și Fossil.",
        "ceas samsung": "Samsung Galaxy Watch este o serie de smartwatch-uri premium care rulează Wear OS, cu monitorizare avansată a sănătății (ECG, tensiune arterială, somn) și integrare perfectă cu ecosistemul Samsung Galaxy.",
        "ceas huawei": "Huawei Watch este o serie de ceasuri inteligente care rulează HarmonyOS, cunoscute pentru designul elegant, bateria de lungă durată (până la 14 zile) și monitorizarea detaliată a somnului și sănătății.",
        "galaxy watch": "Samsung Galaxy Watch este o serie de smartwatch-uri premium care rulează Wear OS, cu monitorizare avansată a sănătății și integrare perfectă cu ecosistemul Samsung.",
        "samsung galaxy book5 pro": "Samsung Galaxy Book5 Pro este varianta clasică (non-360) cu același hardware premium: AMOLED 2X, Intel Ultra 7, 16GB RAM, baterie 25 ore.",
        "samsung galaxy book4 pro 360": "Samsung Galaxy Book4 Pro 360 este generația anterioară (2024) cu Intel Core Ultra Series 1, ecran AMOLED 2X și design convertibil.",
        "macbook pro 16": "MacBook Pro 16 este laptopul profesional Apple cu cip M4 Pro/Max, ecran Liquid Retina XDR, baterie 22 ore și macOS Sequoia.",
        "macbook air 15": "MacBook Air 15 este laptopul subțire Apple cu cip M4, ecran Liquid Retina 15.3\", design fanless și baterie 18 ore.",

        "dell xps 16": "Dell XPS 16 este laptopul premium Windows cu design futurist, ecran OLED 4K, Intel Core Ultra și trackpad invizibil.",
        "lenovo yoga 9i": "Lenovo Yoga 9i este un laptop convertibil premium cu soundbar rotativ Bowers & Wilkins, ecran OLED 4K și stylus inclus.",
        "hp spectre x360": "HP Spectre x360 este un laptop convertibil de lux cu ecran OLED 3K2K, design din aluminiu și cameră 9MP.",
        "asus zenbook duo": "ASUS Zenbook Duo are două ecrane OLED 14\" și tastatură detașabilă, perfect pentru multitasking extrem.",

        "microsoft surface laptop 7": "Microsoft Surface Laptop 7 este primul laptop Surface cu procesor Snapdragon X Elite ARM, baterie 20 ore și AI Copilot+.",
        "samsung galaxy tab s10 ultra": "Samsung Galaxy Tab S10 Ultra este cea mai mare tabletă Samsung, cu ecran Dynamic AMOLED 2X 14.6\", S Pen, AI Galaxy și mod DeX pentru productivitate.",
        "ipad pro m4": "iPad Pro M4 este cea mai puternică tabletă Apple, cu ecran Ultra Retina XDR (OLED tandem), cip M4 și Apple Pencil Pro.",
        "ipad air m3": "iPad Air M3 este tableta versatilă Apple cu ecran Liquid Retina 11\" sau 13\", cip M3 și suport Apple Pencil.",
        "oneplus pad 2": "OnePlus Pad 2 este o tabletă Android premium cu ecran 12.1\" 144Hz, stylus și tastatură detașabilă.",
        "xiaomi pad 7 pro": "Xiaomi Pad 7 Pro este tableta Xiaomi cu ecran 144Hz, procesor Snapdragon 8 Gen 2 și HyperOS.",
        "android 15": "Android 15 este cea mai recentă versiune Android (2025), cu AI Gemini integrat, securitate îmbunătățită și Private Space.",
        "android 16": "Android 16 este următoarea versiune majoră Android, așteptată în 2026, cu AI și mai profund integrat.",
        "ios 19": "iOS 19 este cel mai nou sistem de operare Apple pentru iPhone (2025), cu Apple Intelligence, redesign și funcții AI avansate.",
        "macos sequoia": "macOS Sequoia este sistemul de operare Apple pentru Mac (2024-2025), cu iPhone Mirroring, Apple Intelligence și window tiling.",
        "windows 11": "Windows 11 este cel mai recent sistem de operare Microsoft, cu Copilot AI integrat, design modern și suport pentru aplicații Android.",

        "windows 12": "Windows 12 este următoarea versiune Windows (așteptată 2026-2027), promițând AI profund și design revoluționar.",
        "harmonyos next": "HarmonyOS NEXT este noul sistem de operare Huawei, complet independent de Android, cu AI nativ și ecosistem unificat.",
        "one ui 7": "One UI 7 este interfața Samsung peste Android, cu Galaxy AI, design simplificat și funcții exclusive pentru dispozitive Samsung.",
        "hyperos": "HyperOS este sistemul de operare Xiaomi care înlocuiește MIUI, unificând telefoane, tablete, smart home și mașini electrice.",
        "linux ubuntu": "Ubuntu este cea mai populară distribuție Linux pentru desktop, folosită de dezvoltatori și servere worldwide.",
        "linux fedora": "Fedora este o distribuție Linux de vârf cu software nou, sponsorizată de Red Hat.",
        "linux mint": "Linux Mint este o distribuție Linux prietenoasă pentru începători, bazată pe Ubuntu, cu interfață Cinnamon.",
        "debian": "Debian este o distribuție Linux stabilă și fundamentală, baza pentru Ubuntu și multe altele.",

        "chrome os": "Chrome OS este sistemul de operare Google bazat pe cloud, folosit pe Chromebook-uri, simplu și rapid.",
        "google gemini": "Google Gemini este asistentul AI Google, integrat în Android, Search și Workspace, rival cu ChatGPT.",
        "chatgpt": "ChatGPT este asistentul AI creat de OpenAI, bazat pe GPT-4 și GPT-5, capabil de conversații și generare de conținut.",
        "samsung bixby": "Bixby este asistentul vocal Samsung, integrat în dispozitive Galaxy, cu Galaxy AI și control smart home.",
        "siri": "Siri este asistentul vocal Apple, integrat în iPhone, Mac și HomePod, acum cu Apple Intelligence.",

        "alexa": "Alexa este asistentul vocal Amazon, folosit pe dispozitive Echo pentru control smart home și informații.",
        "copilot microsoft": "Microsoft Copilot este asistentul AI Microsoft integrat în Windows 11, Edge și Office 365.",
        "galaxy ai": "Galaxy AI este suita de funcții AI de la Samsung, inclusiv Circle to Search, Live Translate și Photo Assist.",
        "apple intelligence": "Apple Intelligence este suita AI Apple lansată în 2024-2025, integrată în iOS, macOS și aplicațiile Apple.",
        "samsung galaxy buds3 pro": "Samsung Galaxy Buds3 Pro sunt căști wireless premium cu ANC adaptiv, sunet 360 și integrare Galaxy AI pentru traducere.",
        "airpods pro 3": "AirPods Pro 3 sunt căștile wireless Apple cu ANC îmbunătățit, Adaptive Audio și integrare perfectă cu ecosistemul Apple.",
        "samsung galaxy ring": "Galaxy Ring este inelul inteligent Samsung pentru monitorizarea sănătății 24/7, cu senzori pentru somn, ritm cardiac și activitate.",
        "meta quest 3": "Meta Quest 3 este casca VR/MR de la Meta cu procesor Snapdragon XR2 Gen 2, mixed reality și bibliotecă vastă de jocuri.",
        "playstation 6": "PlayStation 6 este viitoarea consolă Sony (așteptată după 2027), succesoarea PS5 cu grafică revoluționară.",
        "xbox next": "Next Xbox este viitoarea consolă Microsoft, promițând putere masivă și integrare cu cloud gaming.",

        "nintendo switch 2": "Nintendo Switch 2 este noua consolă hibridă Nintendo, lansată în 2025, cu hardware îmbunătățit și joy-con-uri magnetice.",
        "steam deck 2": "Steam Deck 2 este următoarea consolă portabilă Valve pentru jocuri PC, cu hardware mai puternic și baterie îmbunătățită.",
        "robotics": "Robotics is the interdisciplinary field of engineering and science that designs, builds, and operates robots.",
        "robot": "A robot is a programmable machine capable of carrying out complex actions automatically.",
        "automation": "Automation is the technology by which a process or procedure is performed with minimal human assistance.",
        "rpa": "RPA (Robotic Process Automation) uses software robots to automate repetitive digital tasks normally done by humans.",
        "cobot": "A cobot (collaborative robot) is designed to work safely alongside humans in a shared workspace.",
        "ros": "ROS (Robot Operating System) is an open-source framework for writing robot software.",
        "lidar": "LiDAR (Light Detection and Ranging) uses laser pulses to measure distances and create 3D maps, used in autonomous vehicles.",
        "actuator": "An actuator is a component of a machine that moves or controls a mechanism, like a motor or hydraulic cylinder.",
        "sensor": "A sensor detects changes in the environment and sends the information to a computer or controller.",
        "computer vision robot": "Computer vision in robotics allows machines to interpret visual data from cameras to navigate and manipulate objects.",
        "agv": "AGV (Automated Guided Vehicle) is a portable robot that follows markers or wires on the floor for material handling.",
        "drone": "A drone is an unmanned aerial vehicle (UAV) that can fly autonomously or be remotely controlled.",

        "humanoid robot": "A humanoid robot is designed to resemble the human body, often used for research and human-robot interaction.",
        "asimo": "ASIMO was Honda's humanoid robot, famous for walking, running, and interacting with humans.",
        "boston dynamics": "Boston Dynamics is a robotics company known for advanced robots like Spot (dog robot) and Atlas (humanoid robot).",
        "tesla bot": "Tesla Bot (Optimus) is a humanoid robot under development by Tesla for general-purpose tasks.",
        "ros2": "ROS 2 is the next generation of the Robot Operating System with improved security and real-time capabilities.",
        "slam": "SLAM (Simultaneous Localization and Mapping) allows a robot to build a map of an unknown environment while tracking its location.",
        "gripper": "A gripper is an end-effector on a robot arm designed to grasp and hold objects.",
        "industrial robot": "An industrial robot is used in manufacturing for tasks like welding, painting, assembly, and packaging.",
        "vr": "VR (Virtual Reality) is a fully immersive digital environment that replaces the real world, experienced through headsets.",
        "ar": "AR (Augmented Reality) overlays digital information onto the real world, viewed through smartphones or AR glasses.",
        "mr": "MR (Mixed Reality) blends real and virtual worlds where physical and digital objects interact in real-time.",
        "oculus": "Oculus is Meta's VR headset brand, now called Meta Quest, popular for gaming and social experiences.",

        "apple vision pro": "Apple Vision Pro is Apple's mixed reality headset, blending AR and VR with advanced spatial computing.",
        "microsoft hololens": "Microsoft HoloLens is an AR headset used in enterprise, medicine, and engineering for holographic computing.",
        "metaverse": "The Metaverse is a network of 3D virtual worlds focused on social connection, using VR and AR technologies.",
        "haptic": "Haptic technology provides tactile feedback (vibrations or forces) to simulate the sense of touch in virtual environments.",
        "spatial computing": "Spatial computing uses 3D space to interact with digital content, as seen in Apple Vision Pro.",
        "360 video": "360-degree video captures every direction simultaneously, allowing viewers to look around in VR.",

        "game engine": "A game engine is software for building video games, providing rendering, physics, and scripting. Examples: Unity, Unreal Engine.",
        "unity": "Unity is a cross-platform game engine used for 2D, 3D, VR, and AR game development.",
        "unreal engine": "Unreal Engine is a powerful 3D game engine by Epic Games known for high-fidelity graphics.",
        "godot": "Godot is a free and open-source game engine for 2D and 3D game development.",
        "game design": "Game design is the art of creating the rules, mechanics, story, and world of a video game.",
        "npc": "NPC (Non-Player Character) is a character in a game not controlled by the player, often part of the story or environment.",
        "fps game": "FPS (Frames Per Second) measures how smoothly a game runs. 60 FPS is the standard for smooth gameplay.",
        "ray tracing": "Ray tracing is a rendering technique that simulates realistic lighting by tracing the path of light rays.",
        "open world": "An open world game allows players to explore a large, non-linear virtual world freely.",
        "indie game": "An indie game is created by independent developers without major publisher backing, often innovative and experimental.",
        "steam": "Steam is the largest digital distribution platform for PC games, developed by Valve.",
        "epic games store": "Epic Games Store is a digital game distribution platform competing with Steam.",
        "minecraft": "Minecraft is the best-selling video game of all time, a sandbox game about building and exploring block worlds.",
        "roblox": "Roblox is an online platform where users create and play games made by other users.",

        "fortnite": "Fortnite is a popular battle royale game by Epic Games, known for its building mechanics and live events.",
        "green tech": "Green technology uses science to create products and services that are environmentally friendly.",
        "solar panel": "A solar panel converts sunlight into electricity using photovoltaic cells.",
        "ev": "EV (Electric Vehicle) runs on electric motors instead of internal combustion engines. Examples: Tesla, Nissan Leaf.",
        "carbon footprint": "Carbon footprint is the total amount of greenhouse gases generated by human activities.",
        "recycling tech": "Recycling technology uses advanced processes to recover materials from waste for reuse.",
        "smart grid": "A smart grid is an electricity network that uses digital technology to monitor and manage energy flow efficiently.",
        "wind turbine": "A wind turbine converts kinetic energy from wind into electrical power.",
        "biodegradable": "Biodegradable materials can be broken down naturally by microorganisms without harming the environment.",
        "e-waste": "E-waste is discarded electronic devices and components, a growing global environmental problem.",
        "sustainable computing": "Sustainable computing aims to reduce the environmental impact of computers through energy-efficient design and recycling.",
        "url": "URL (Uniform Resource Locator) is the address used to access resources on the internet, like https://www.google.com.",
        "isp": "ISP (Internet Service Provider) is a company that provides internet access. Examples: RCS-RDS, Orange, Vodafone.",
        "lan": "LAN (Local Area Network) connects computers in a small area like a home, office, or school.",

        "wan": "WAN (Wide Area Network) spans a large geographic area, like the internet itself.",
        "vpn acronim": "VPN (Virtual Private Network) encrypts your internet connection and hides your IP address for privacy.",
        "gui": "GUI (Graphical User Interface) allows users to interact with computers using visual elements like windows and icons.",
        "cli": "CLI (Command Line Interface) is a text-based way to interact with a computer by typing commands.",
        "os": "OS (Operating System) manages hardware and software on a computer. Examples: Windows, Linux, macOS.",
        "foss": "FOSS (Free and Open Source Software) is software that anyone can use, modify, and distribute freely.",
        "drm": "DRM (Digital Rights Management) controls how digital content is used and distributed to prevent piracy.",
        "captcha": "CAPTCHA is a test used to determine if a user is human or a bot, often requiring image recognition.",
        "emoji": "Emoji are small digital icons used to express emotions or ideas in electronic messages.",
        "meme": "A meme is a humorous image, video, or text that spreads rapidly online, often modified by users.",
        "troll": "A troll is someone who posts inflammatory messages online to provoke others.",
        "streaming": "Streaming delivers audio or video content over the internet in real-time without downloading. Examples: Netflix, YouTube, Spotify.",
        "podcast": "A podcast is a digital audio program available for streaming or download, covering countless topics.",
        "influencer": "An influencer is a person who uses social media to affect the purchasing decisions of followers.",
        "viral": "Viral content spreads rapidly and widely across the internet through social sharing.",

        "dark web": "The dark web is a hidden part of the internet requiring special software to access, often associated with anonymity.",
        "deep web": "The deep web includes all web pages not indexed by search engines, like private databases and email inboxes.",
        "async": "Asynchronous programming allows a program to handle multiple tasks concurrently without waiting for each to finish.",
        "multithreading": "Multithreading runs multiple threads simultaneously within a single process to improve performance.",
        "lambda": "A lambda function is a small anonymous function in Python defined with `lambda` keyword, used for short operations.",
        "decorator": "A decorator in Python modifies or enhances a function without changing its code, using the `@` syntax.",
        "generator": "A generator is a function in Python that yields values one at a time using `yield`, saving memory.",
        "virtual environment": "A virtual environment in Python isolates project dependencies to avoid conflicts between packages.",
        "pip": "pip is the package installer for Python, used to install and manage libraries from PyPI.",

        "pypi": "PyPI (Python Package Index) is the official repository of Python packages, hosting thousands of libraries.",
        "pep 8": "PEP 8 is the official style guide for Python code, promoting readability and consistency.",
        "jupyter": "Jupyter Notebook is an interactive web-based environment for writing and running Python code, popular in data science.",
        "anaconda": "Anaconda is a distribution of Python and R for scientific computing and data science.",
        "pandas": "Pandas is a Python library for data manipulation and analysis, especially with tabular data.",
        "numpy": "NumPy is a Python library for numerical computing, supporting arrays and mathematical functions.",

        "matplotlib": "Matplotlib is a Python library for creating static, animated, and interactive visualizations.",
        "scikit-learn": "Scikit-learn is a Python machine learning library with tools for classification, regression, and clustering.",
        "tensorflow": "TensorFlow is an open-source ML framework by Google for building and deploying AI models.",
        "pytorch": "PyTorch is an open-source ML framework by Meta, popular in research for its flexibility.",
        "keras": "Keras is a high-level neural network API running on top of TensorFlow, designed for fast experimentation.",
        "opencv": "OpenCV (Open Source Computer Vision Library) is used for real-time image and video processing.",
        "flask python": "Flask is a lightweight Python web framework for building web applications and APIs quickly.",
        "fastapi": "FastAPI is a modern Python web framework for building APIs with automatic interactive documentation.",
        "streamlit library": "Streamlit is a Python library for building interactive data apps and AI dashboards quickly, used to create AEGIS.",
        "gradio": "Gradio is a Python library for creating simple web interfaces for machine learning models.",
        "tkinter": "Tkinter is Python's standard GUI library for creating desktop applications.",
        "pygame": "Pygame is a Python library for writing 2D video games with graphics and sound.",

        # --- 25. REȚELE AVANSATE ---
        "subnet mask": "Subnet mask separates the IP address into network and host portions, determining which part identifies the network and which identifies the device.",
        "gateway": "A gateway is a network node that connects two different networks, often serving as the access point to the internet for devices on a local network.",
        "nat": "NAT (Network Address Translation) allows multiple devices on a private network to share a single public IP address for internet access.",
        "dhcp": "DHCP (Dynamic Host Configuration Protocol) automatically assigns IP addresses to devices on a network.",
        "mac address": "MAC address is a unique hardware identifier assigned to a network interface card (NIC) for communication on a physical network.",
        "packet": "A packet is a small unit of data transmitted over a network, containing source/destination addresses and the actual data being sent.",
        "ethernet": "Ethernet is a wired networking technology used to connect devices in a LAN, offering reliable high-speed data transfer.",
        "fiber optic": "Fiber optic cables use light to transmit data at extremely high speeds over long distances with minimal signal loss.",
        "switch": "A network switch connects devices within a LAN and forwards data only to the specific device it's intended for.",
        "hub": "A hub is a basic networking device that broadcasts data to all connected devices, unlike a switch which sends data selectively.",
        "poe": "PoE (Power over Ethernet) delivers electrical power along with data over standard Ethernet cables to devices like cameras and access points.",
        "vlan": "VLAN (Virtual LAN) logically segments a physical network into separate broadcast domains for security and efficiency.",
        "ssid": "SSID (Service Set Identifier) is the name of a Wi-Fi network that users see when connecting their devices.",
        "wpa3": "WPA3 is the latest Wi-Fi security protocol, providing stronger encryption and protection against password guessing attacks.",
        "captive portal": "A captive portal is a web page that requires user interaction before granting internet access, commonly used in hotels and airports.",
        "qos": "QoS (Quality of Service) prioritizes certain types of network traffic to ensure performance for critical applications like voice and video.",
        "snmp": "SNMP (Simple Network Management Protocol) monitors and manages network devices like routers, switches, and servers.",
        "ftp": "FTP (File Transfer Protocol) transfers files between computers on a network. SFTP adds encryption for security.",
        "telnet": "Telnet is an old protocol for remote terminal access, now largely replaced by SSH due to lack of encryption.",
        "rdp": "RDP (Remote Desktop Protocol) allows users to remotely connect to and control a Windows computer over a network.",
        "smtp": "SMTP (Simple Mail Transfer Protocol) sends emails from a client to a server or between servers.",
        "pop3": "POP3 downloads emails from a server to a local device, typically deleting them from the server afterward.",
        "imap": "IMAP allows access to emails stored on a server, keeping them synchronized across multiple devices.",

        # --- 26. PROGRAMARE WEB AVANSATĂ ---
        "websocket": "WebSocket enables real-time, two-way communication between a browser and a server, used in chat apps and live notifications.",
        "graphql": "GraphQL is a query language for APIs that lets clients request exactly the data they need, nothing more, nothing less.",
        "rest": "REST (Representational State Transfer) is an architectural style for designing networked APIs using standard HTTP methods.",
        "soap": "SOAP is a protocol for exchanging structured data in web services, using XML and often more rigid than REST.",
        "cdn": "CDN (Content Delivery Network) distributes website content across global servers, improving load times and reducing bandwidth.",
        "seo": "SEO (Search Engine Optimization) improves a website's visibility in search engine results through keywords, links, and technical optimizations.",
        "caching": "Caching temporarily stores frequently accessed data for faster retrieval, reducing server load and improving response times.",
        "session": "A session maintains user state across multiple requests on a website, often tracked with cookies or tokens.",
        "cookie": "A cookie is a small piece of data stored in the browser by a website, used for sessions, preferences, and tracking.",
        "local storage": "Local Storage is a browser API that stores key-value data persistently, surviving browser restarts.",
        "xss attack": "XSS (Cross-Site Scripting) injects malicious scripts into web pages viewed by other users, stealing data or hijacking sessions.",
        "csrf token": "CSRF token is a unique secret value included in forms to prevent Cross-Site Request Forgery attacks.",
        "sql injection prevention": "Prepared statements and parameterized queries prevent SQL injection by separating SQL code from user input.",
        "content security policy": "CSP is a security header that controls which resources (scripts, styles) a browser is allowed to load.",
        "cors policy": "CORS (Cross-Origin Resource Sharing) controls how a web page can request resources from a different domain.",
        "authentication": "Authentication verifies a user's identity (who you are), typically through passwords, biometrics, or tokens.",
        "authorization": "Authorization determines what an authenticated user is allowed to do (what you can access).",
        "jwt token": "JWT (JSON Web Token) securely transmits information between parties as a compact, URL-safe token.",
        "openid connect": "OpenID Connect is an authentication layer built on OAuth 2.0, allowing single sign-on across websites.",
        "saml": "SAML (Security Assertion Markup Language) enables single sign-on between an identity provider and service providers.",

        # --- 27. DEZVOLTARE MOBILĂ AVANSATĂ ---
        "progressive web app": "PWA uses modern web capabilities to deliver an app-like experience, including offline mode and push notifications.",
        "native app": "A native app is built specifically for one platform (iOS or Android) using platform-specific languages like Swift or Kotlin.",
        "cross platform": "Cross-platform development creates apps for multiple platforms from a single codebase, using frameworks like Flutter or React Native.",
        "app bundle": "Android App Bundle (AAB) is the publishing format that includes all compiled code and resources, letting Google Play optimize delivery.",
        "testflight": "TestFlight is Apple's platform for beta testing iOS apps before releasing them on the App Store.",
        "gradle": "Gradle is a build automation tool used primarily for Android development, managing dependencies and compiling code.",
        "cocoapods": "CocoaPods is a dependency manager for Swift and Objective-C projects on iOS and macOS.",
        "hot reload": "Hot reload instantly updates a running app with code changes without losing state, speeding up development in Flutter and React Native.",
        "app permissions": "App permissions control what data and features an app can access on a device (camera, location, contacts).",
        "deep link": "Deep linking opens a specific screen or content within an app from a URL, improving user navigation and engagement.",

        # --- 28. BAZE DE DATE AVANSATE ---
        "sharding": "Sharding splits a large database into smaller, faster, more manageable pieces across multiple servers.",
        "replication": "Database replication copies data from one server to another for redundancy, backup, and improved read performance.",
        "cap theorem": "CAP Theorem states that a distributed system can provide only two of three guarantees: Consistency, Availability, Partition Tolerance.",
        "nosql types": "NoSQL database types include document (MongoDB), key-value (Redis), column-family (Cassandra), and graph (Neo4j).",
        "acid vs base": "ACID (Atomicity, Consistency, Isolation, Durability) vs BASE (Basically Available, Soft state, Eventually consistent) — two database consistency models.",
        "connection pool": "Connection pooling maintains a cache of database connections for reuse, reducing the overhead of establishing new connections.",
        "migration": "Database migration tracks and applies schema changes systematically, often using version control for database structure.",
        "seed data": "Seed data is initial data loaded into a database for testing or to provide default values for an application.",
        "backup": "Database backup creates copies of data for disaster recovery, available as full, incremental, or differential backups.",
        "sql vs nosql": "SQL databases are relational with structured schemas; NoSQL databases are non-relational with flexible data models.",

        # --- 29. CLOUD & DEVOPS AVANSAT ---
        "iaac": "IaC (Infrastructure as Code) manages infrastructure through configuration files instead of manual processes, using tools like Terraform.",
        "ci pipeline": "CI (Continuous Integration) pipeline automatically builds, tests, and validates code changes when pushed to a repository.",
        "cd pipeline": "CD (Continuous Delivery/Deployment) pipeline automatically releases validated code changes to staging or production environments.",
        "blue green deployment": "Blue-Green deployment runs two identical environments, switching traffic between them for zero-downtime releases.",
        "canary release": "Canary release gradually rolls out a new version to a small subset of users before full deployment.",
        "feature flag": "Feature flags toggle features on or off without deploying new code, enabling gradual rollouts and A/B testing.",
        "observability": "Observability measures how well a system's internal state can be understood from its external outputs: logs, metrics, and traces.",
        "incident response": "Incident response is the process of detecting, investigating, and resolving system outages or security breaches.",
        "runbook": "A runbook documents step-by-step procedures for handling recurring IT tasks or incidents.",
        "chaos engineering": "Chaos engineering intentionally introduces failures to test system resilience and identify weaknesses before they cause outages.",
        "finops": "FinOps is the practice of managing cloud costs through collaboration between finance, engineering, and operations teams.",
        "sla": "SLA (Service Level Agreement) defines the expected level of service, including uptime guarantees and response times.",
        "slo": "SLO (Service Level Objective) is a specific measurable target for service performance within an SLA.",
        "sli": "SLI (Service Level Indicator) is the actual measurement of a service's performance against its SLO.",
        "multicloud": "Multi-cloud uses services from multiple cloud providers (AWS, Azure, GCP) for flexibility and avoiding vendor lock-in.",
        "hybrid cloud": "Hybrid cloud combines on-premises infrastructure with public cloud services, sharing data and applications between them.",

        # --- 30. SECURITATE CIBERNETICĂ AVANSATĂ ---
        "zero trust": "Zero Trust is a security model where no user or device is trusted by default, even inside the network perimeter.",
        "edr": "EDR (Endpoint Detection and Response) monitors endpoints for threats and provides tools for investigation and remediation.",
        "soar": "SOAR (Security Orchestration, Automation, and Response) automates security tasks and coordinates responses across tools.",
        "threat hunting": "Threat hunting proactively searches for hidden threats in a network before they trigger automated alerts.",
        "forensics": "Digital forensics investigates cyber incidents by collecting and analyzing digital evidence from systems and networks.",
        "patching": "Patching updates software to fix security vulnerabilities, bugs, or performance issues.",
        "cve": "CVE (Common Vulnerabilities and Exposures) is a database of publicly known security vulnerabilities with unique identifiers.",
        "cvss": "CVSS (Common Vulnerability Scoring System) rates the severity of security vulnerabilities on a scale of 0-10.",
        "waf": "WAF (Web Application Firewall) protects web applications by filtering and monitoring HTTP traffic between the app and the internet.",
        "dlp": "DLP (Data Loss Prevention) prevents sensitive data from leaving an organization's network unauthorized.",
        "honeypot": "A honeypot is a decoy system designed to attract attackers and study their methods without risking real data.",
        "bastion host": "A bastion host is a hardened server placed at the network edge to withstand attacks and provide secure access.",
        "pki": "PKI (Public Key Infrastructure) manages digital certificates and encryption keys for secure communication.",
        "2fa": "2FA (Two-Factor Authentication) adds a second verification step (SMS code, authenticator app) to password login.",
        "biometric auth": "Biometric authentication uses unique physical traits (fingerprint, face, iris) to verify identity.",
        "fido2": "FIDO2 is a passwordless authentication standard using security keys or biometrics for secure login.",

        # --- 31. INTELIGENȚĂ ARTIFICIALĂ AVANSATĂ ---
        "generative ai": "Generative AI creates new content — text, images, code, music — based on patterns learned from training data.",
        "attention mechanism": "Attention mechanism lets AI models focus on relevant parts of input data, key to Transformer architectures.",
        "self-attention": "Self-attention relates different positions of a single sequence to compute a representation of the sequence.",
        "bert": "BERT (Bidirectional Encoder Representations from Transformers) is a Google AI model for natural language understanding.",
        "gpt": "GPT (Generative Pre-trained Transformer) is OpenAI's language model series powering ChatGPT and other AI applications.",
        "stable diffusion": "Stable Diffusion is an open-source AI model that generates images from text descriptions.",
        "midjourney": "Midjourney is an AI image generation tool known for creating artistic and photorealistic images from text prompts.",
        "vector database": "Vector databases store and search embeddings for AI applications like semantic search and recommendations.",
        "semantic search": "Semantic search understands the intent and meaning behind a query, not just matching keywords.",
        "reinforcement learning from human feedback": "RLHF trains AI models using human preferences to align outputs with human values and expectations.",

        # --- 32. HARDWARE AVANSAT ---
        "npu": "NPU (Neural Processing Unit) is a specialized processor designed to accelerate AI and machine learning tasks.",
        "tpu": "TPU (Tensor Processing Unit) is Google's custom AI accelerator chip for machine learning workloads.",
        "quantum processor": "Quantum processors use quantum bits (qubits) to perform calculations impossible for classical computers.",
        "ddr5": "DDR5 is the latest RAM standard, offering higher speeds and better power efficiency than DDR4.",
        "pcie 5": "PCIe 5.0 doubles the bandwidth of PCIe 4.0, enabling faster data transfer for GPUs and SSDs.",
        "thunderbolt 5": "Thunderbolt 5 offers up to 120 Gbps bandwidth, supporting multiple 8K displays and high-speed external storage.",
        "usb4": "USB4 unifies USB and Thunderbolt protocols, offering up to 40 Gbps transfer speeds and better compatibility.",
        "oled vs amoled": "OLED displays have organic pixels that emit light; AMOLED adds an active matrix for better touch response and refresh rates.",
        "mini led": "Mini LED uses thousands of tiny LEDs for backlighting LCD displays, offering better contrast and brightness control.",
        "microled": "MicroLED uses microscopic LEDs for each pixel, combining OLED's perfect blacks with LED's brightness and longevity.",

        # --- 33. TECH BUSINESS & STARTUP ---
        "unicorn": "A unicorn is a privately held startup valued at over 1 billion dollars. Examples: SpaceX, Stripe, ByteDance.",
        "pivot": "A pivot is a fundamental change in business strategy when the original plan isn't working.",
        "mrr": "MRR (Monthly Recurring Revenue) measures predictable subscription income a business earns each month.",
        "burn rate": "Burn rate is how quickly a company spends its cash reserves, usually calculated monthly.",
        "runway": "Runway is how many months a startup can operate before running out of cash, based on burn rate.",
        "equity": "Equity represents ownership shares in a company, often given to employees or investors instead of cash.",
        "vesting": "Vesting gradually grants ownership of equity over time, typically 4 years with a 1-year cliff.",
        "accelerator": "An accelerator provides mentorship, funding, and resources to early-stage startups. Examples: Y Combinator, Techstars.",
        "incubator": "An incubator supports very early-stage startups with workspace, mentorship, and resources for longer periods.",
        "angel investor": "An angel investor is a wealthy individual who provides capital to startups in exchange for equity or convertible debt.",
        "series a": "Series A is the first major round of venture capital funding for a startup, typically after initial traction.",
        "ipo": "IPO (Initial Public Offering) is when a private company first sells shares to the public on a stock exchange.",

        # --- 34. INTERNET CULTURE & TRENDING ---
        "hashtag": "A hashtag (#) categorizes social media content, making it discoverable to users following that topic.",
        "thread": "A thread is a series of connected social media posts on a single topic, popular on Twitter/X and Threads.",
        "algorithm feed": "Algorithmic feeds sort content by predicted user interest rather than chronological order, used by TikTok and Instagram.",
        "creator economy": "The creator economy allows individuals to earn money directly from content creation through platforms like YouTube, TikTok, and Patreon.",
        "nft art": "NFT art uses blockchain tokens to prove ownership and authenticity of digital artworks.",
        "dao governance": "DAO governance allows token holders to vote on organizational decisions without centralized leadership.",
        "web5": "Web5 is a decentralized web platform combining Web2 convenience with Web3 principles, proposed by Jack Dorsey's TBD.",
        "digital nomad": "A digital nomad works remotely while traveling, relying on technology and internet connectivity.",
        "gig economy": "The gig economy is based on temporary, flexible jobs, often facilitated by platforms like Uber, Fiverr, and Upwork.",
        "quiet quitting": "Quiet quitting means doing the minimum required at work without going above and beyond, prioritizing work-life balance.",

                # --- 35. COMPANII TECH ȘI PRODUSE (EXTRA) ---
        "spotify": "Spotify is a Swedish audio streaming platform with over 500 million users, known for personalized playlists and podcasts.",
        "adobe": "Adobe is a software company known for creative tools like Photoshop, Premiere Pro, and the PDF format.",
        "oracle": "Oracle is a major database software company, also offering cloud services and enterprise applications.",
        "sap": "SAP is a German software company specializing in enterprise resource planning (ERP) systems for businesses.",
        "ibm": "IBM is one of the oldest tech companies, known for mainframes, AI (Watson), and quantum computing research.",
        "cisco": "Cisco is the leading networking hardware company, producing routers, switches, and cybersecurity solutions.",
        "vmware": "VMware is a leader in virtualization and cloud infrastructure software, now part of Broadcom.",
        "salesforce": "Salesforce is the world's leading CRM (Customer Relationship Management) platform, delivered entirely via cloud.",

                # --- 36. DEZVOLTARE SOFTWARE ---
        "ide integrated": "An IDE (Integrated Development Environment) combines code editor, debugger, and build tools in one application. Examples: VS Code, PyCharm, IntelliJ.",
        "version control": "Version control tracks changes to code over time, allowing multiple developers to collaborate and revert to previous versions.",
        "code review": "Code review is the process of having other developers examine your code for bugs, style issues, and improvements before merging.",
        "pair programming": "Pair programming involves two developers working together at one computer — one writes code, the other reviews each line.",
        "standup": "A daily standup is a short team meeting where each member shares what they did yesterday, what they'll do today, and any blockers.",
        "sprint": "A sprint is a fixed time period (usually 1-4 weeks) in Agile development where a team completes a set of planned work items.",
        "backlog": "A backlog is a prioritized list of features, bugs, and tasks for a software project, maintained by the product owner.",
        "user story": "A user story describes a software feature from the end-user's perspective, typically following the format: 'As a [user], I want [feature] so that [benefit].'",
        "epic": "An epic is a large user story that spans multiple sprints and is broken down into smaller stories for implementation.",
        "kanban": "Kanban is a visual workflow management method using boards and cards to track work progress through stages like To Do, In Progress, and Done.",

        # --- 37. TESTING SOFTWARE ---
        "smoke test": "Smoke testing is a preliminary test to check if the basic functions of a software build work correctly before detailed testing.",
        "sanity test": "Sanity testing verifies that a specific feature or bug fix works as expected after changes, without testing the entire system.",
        "regression": "Regression testing ensures that new code changes haven't broken or negatively affected existing features.",
        "black box testing": "Black box testing evaluates software functionality without knowledge of internal code structure, focusing on inputs and outputs.",
        "white box testing": "White box testing examines internal code structure, logic, and paths to verify correctness at the source code level.",
        "mutation testing": "Mutation testing introduces small changes (mutations) to code to verify that tests can detect and reject them.",
        "test coverage": "Test coverage measures what percentage of code is executed during testing, helping identify untested areas.",
        "mock": "A mock is a simulated object that mimics the behavior of a real component in controlled ways during testing.",
        "stub": "A stub provides predetermined responses to calls during testing, simpler than mocks and used for basic dependency replacement.",
        "assertion": "An assertion is a statement that checks if a condition is true during testing, failing the test if the condition is false.",

        # --- 38. PROTOCOALE DE COMUNICARE ---
        "mqtt": "MQTT (Message Queuing Telemetry Transport) is a lightweight messaging protocol for IoT devices with limited bandwidth.",
        "coap": "CoAP (Constrained Application Protocol) is a specialized web transfer protocol for constrained nodes and networks in IoT.",
        "amqp": "AMQP (Advanced Message Queuing Protocol) is an open standard for message-oriented middleware, used by RabbitMQ.",
        "grpc": "gRPC is a high-performance RPC framework by Google using Protocol Buffers and HTTP/2 for efficient service communication.",
        "protobuf": "Protocol Buffers (protobuf) is a compact binary serialization format by Google for structured data, faster than JSON.",
        "websocket vs http": "WebSocket provides full-duplex, persistent connections ideal for real-time apps; HTTP is request-response and stateless.",
        "long polling": "Long polling keeps an HTTP connection open until the server has data to send, simulating real-time updates.",
        "server sent events": "SSE (Server-Sent Events) allows servers to push real-time updates to browsers over a single HTTP connection.",
        "udp": "UDP (User Datagram Protocol) is a connectionless protocol that sends data without guarantee of delivery, used for streaming and gaming.",
        "icmp": "ICMP (Internet Control Message Protocol) sends error messages and operational information for network diagnostics, like the 'ping' command.",

        # --- 39. FORMATURI DE DATE ---
        "yaml": "YAML (YAML Ain't Markup Language) is a human-readable data serialization format used for configuration files.",
        "csv": "CSV (Comma-Separated Values) stores tabular data in plain text, with each line representing a row and commas separating columns.",
        "toml": "TOML (Tom's Obvious Minimal Language) is a configuration file format designed to be easy to read and parse.",
        "ini": "INI files are simple configuration files with sections and key-value pairs, commonly used in Windows and legacy applications.",
        "parquet": "Parquet is a columnar storage file format optimized for big data processing, used with Apache Spark and Hadoop.",
        "avro": "Avro is a row-based data serialization framework with schema support, used in Apache Kafka and Hadoop ecosystems.",
        "bson": "BSON (Binary JSON) extends JSON with additional data types and binary encoding, used by MongoDB for document storage.",
        "markdown": "Markdown is a lightweight markup language with plain text formatting syntax, widely used for documentation and README files.",
        "base64": "Base64 encodes binary data as ASCII text using 64 characters, commonly used to embed images in HTML or transmit data in JSON.",
        "url encoding": "URL encoding converts special characters into a format safe for transmission in URLs, replacing spaces with %20 and symbols with %XX codes.",

        # --- 40. SISTEME DE OPERARE AVANSATE ---
        "sandbox": "A sandbox is an isolated environment where programs can run without affecting the rest of the system, used for security testing.",
        "hypervisor": "A hypervisor creates and runs virtual machines by abstracting hardware resources. Type 1 runs on bare metal (VMware ESXi); Type 2 runs on an OS (VirtualBox).",
        "dual boot": "Dual booting installs two operating systems on one computer, allowing the user to choose which to run at startup.",
        "live usb": "A live USB runs an operating system directly from a USB drive without installing it on the computer's hard disk.",
        "package manager": "A package manager automates installing, updating, and removing software. Examples: apt (Debian), brew (macOS), winget (Windows).",
        "systemd": "systemd is the init system and service manager for many Linux distributions, managing boot processes and system services.",
        "cron job": "A cron job schedules commands or scripts to run automatically at specific times or intervals on Unix-like systems.",
        "environment variable": "Environment variables store configuration values outside of code, like PATH, HOME, and API keys, accessible system-wide.",
        "shell": "A shell is a command-line interpreter that lets users interact with the operating system. Examples: Bash, Zsh, Fish, PowerShell.",
        "process": "A process is an instance of a running program, with its own memory space and system resources managed by the OS kernel.",

        # --- 41. FRAMEWORKS WEB ---
        "django rest framework": "Django REST Framework is a powerful toolkit for building Web APIs with Django, featuring serialization, authentication, and browsable APIs.",
        "spring boot": "Spring Boot is a Java framework that simplifies building production-ready applications with embedded servers and auto-configuration.",
        "laravel": "Laravel is a PHP web framework with elegant syntax, featuring Eloquent ORM, Blade templating, and Artisan CLI.",
        "ruby on rails": "Ruby on Rails is a full-stack web framework emphasizing convention over configuration, enabling rapid application development.",
        "asp.net": "ASP.NET is Microsoft's web framework for building dynamic web applications and APIs using C# and the .NET ecosystem.",
        "flask vs django": "Flask is a micro-framework for small, flexible apps; Django is a full-stack framework with built-in admin, ORM, and authentication.",
        "svelte": "Svelte is a radical frontend framework that compiles components to vanilla JavaScript at build time, eliminating the need for a virtual DOM.",
        "nuxt": "Nuxt.js is a Vue.js framework for building universal applications with SSR, SSG, and automatic code splitting.",
        "gatsby": "Gatsby is a React-based static site generator using GraphQL, optimized for speed and SEO.",
        "remix": "Remix is a full-stack React framework focused on web standards, progressive enhancement, and fast user experiences.",

        # --- 42. UNELTE DE DEZVOLTARE ---
        "postman": "Postman is a popular API testing tool that allows developers to send HTTP requests, inspect responses, and automate API workflows.",
        "swagger": "Swagger (now OpenAPI) is a specification for describing REST APIs, with tools for auto-generating documentation and client SDKs.",
        "eslint": "ESLint is a static analysis tool for JavaScript that finds and fixes code problems, enforcing consistent code style.",
        "prettier": "Prettier is an opinionated code formatter that automatically formats code to a consistent style across multiple languages.",
        "webpack vs vite": "Webpack is a mature, highly configurable bundler; Vite is a modern, faster alternative using native ES modules for development.",
        "babel": "Babel is a JavaScript compiler that converts modern JavaScript (ES6+) into backwards-compatible code for older browsers.",
        "figma": "Figma is a cloud-based design tool for UI/UX design, prototyping, and collaboration, widely used by designers and developers.",
        "storybook": "Storybook is a frontend workshop for building UI components in isolation, making development and testing easier.",
        "lighthouse": "Lighthouse is an open-source tool by Google for auditing web page performance, accessibility, SEO, and best practices.",
        "chrome devtools": "Chrome DevTools is a set of web developer tools built into Google Chrome for debugging, profiling, and inspecting web pages.",

        # --- 43. CONCEPTE DE PROGRAMARE ---
        "dry": "DRY (Don't Repeat Yourself) is a software principle that reduces duplication by abstracting common code into reusable functions or modules.",
        "kiss": "KISS (Keep It Simple, Stupid) advocates for simplicity in design, avoiding unnecessary complexity.",
        "solid": "SOLID is a set of five object-oriented design principles: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.",
        "dependency injection": "Dependency Injection provides objects with their dependencies from outside rather than creating them internally, improving testability and flexibility.",
        "convention over configuration": "A design paradigm where default conventions reduce the number of decisions developers need to make.",
        "immutable": "Immutable objects cannot be modified after creation; any change creates a new object, preventing unintended side effects.",
        "polymorphism": "Polymorphism allows objects of different types to respond to the same method call in their own way, a key OOP concept.",
        "inheritance": "Inheritance allows a class to inherit properties and methods from a parent class, promoting code reuse.",
        "encapsulation": "Encapsulation hides internal object state and requires all interaction to go through methods, protecting data integrity.",
        "abstraction": "Abstraction hides complex implementation details behind a simpler interface, letting developers work at a higher level.",

        # --- 44. SISTEME DE FIȘIERE ---
        "ntfs": "NTFS (New Technology File System) is Microsoft's file system for Windows, supporting large files, security permissions, and journaling.",
        "ext4": "ext4 (Fourth Extended File System) is the default Linux file system, offering journaling, large file support, and reliability.",
        "fat32": "FAT32 is an older file system compatible with most devices, limited to 4GB maximum file size.",
        "exfat": "exFAT extends FAT32 with support for large files and is optimized for flash drives and SD cards.",
        "hfs": "APFS (Apple File System) is Apple's modern file system for macOS, iOS, optimized for flash storage with snapshots and encryption.",
        "zfs": "ZFS is an advanced file system with data integrity verification, snapshots, compression, and massive storage capacity.",
        "raid": "RAID (Redundant Array of Independent Disks) combines multiple drives for performance (RAID 0), mirroring (RAID 1), or both (RAID 5, 10).",
        "journaling": "Journaling file systems keep a log of changes before writing them, preventing corruption from crashes or power failures.",
        "inode": "An inode is a data structure in Unix file systems that stores information about a file, like permissions, size, and location.",
        "mount": "Mounting makes a file system accessible by attaching it to a directory in the existing file hierarchy.",

        # --- 45. TEHNOLOGII EMERGENTE ---
        "webassembly": "WebAssembly (Wasm) runs high-performance code in browsers at near-native speed, enabling languages like C++ and Rust on the web.",
        "edge ai": "Edge AI runs artificial intelligence algorithms directly on devices like phones and sensors, without needing cloud connectivity.",
        "digital twin": "A digital twin is a virtual replica of a physical object or system, used for simulation, monitoring, and optimization.",
        "neuromorphic computing": "Neuromorphic computing designs chips that mimic the brain's neural structure for ultra-efficient AI processing.",
        "holographic storage": "Holographic storage uses light to store data in three dimensions, promising massive capacity increases over traditional methods.",
        "6g": "6G is the future mobile network beyond 5G, expected around 2030, with terabit speeds, microsecond latency, and AI-native architecture.",
        "brain computer interface": "BCI connects the human brain directly to computers, enabling thought-controlled devices and restoring sensory functions.",
        "smart dust": "Smart dust refers to tiny wireless sensors smaller than a grain of sand, used for distributed environmental monitoring.",
        "quantum internet": "Quantum internet uses entangled particles for ultra-secure communication that cannot be intercepted without detection.",
        "fusion energy": "Fusion energy replicates the sun's power on Earth, promising nearly unlimited clean energy if successfully commercialized.",

                # --- 46. STANDARDE ȘI CERTIFICĂRI IT ---
        "iso 27001": "ISO 27001 is the international standard for information security management systems (ISMS), providing a framework for protecting data assets.",
        "comptia a+": "CompTIA A+ is an entry-level IT certification covering hardware, software, networking, and troubleshooting fundamentals.",
        "comptia security+": "CompTIA Security+ is a globally recognized certification for foundational cybersecurity skills and knowledge.",
        "comptia network+": "CompTIA Network+ certifies knowledge of networking concepts, infrastructure, operations, and security.",
        "cisco ccna": "Cisco CCNA (Cisco Certified Network Associate) validates skills in network fundamentals, access, IP services, and security.",
        "aws certified": "AWS Certified Solutions Architect validates expertise in designing distributed systems on Amazon Web Services.",
        "google cloud certified": "Google Cloud Certified Professional Cloud Architect validates skills in designing and managing Google Cloud solutions.",
        "microsoft certified azure": "Microsoft Certified Azure Administrator validates skills in managing Azure subscriptions, resources, and services.",
        "pmp": "PMP (Project Management Professional) is a globally recognized project management certification by PMI.",
        "itil": "ITIL (Information Technology Infrastructure Library) is a framework for IT service management best practices.",

        # --- 47. TEHNOLOGII DE STOCARE ---
        "nvme": "NVMe (Non-Volatile Memory Express) is a high-performance protocol for SSDs using PCIe lanes, offering much faster speeds than SATA.",
        "sata": "SATA (Serial Advanced Technology Attachment) is an interface for connecting storage devices like HDDs and SSDs to a computer.",
        "sas": "SAS (Serial Attached SCSI) is a high-performance storage interface for enterprise hard drives, offering better reliability than SATA.",
        "iscsi": "iSCSI (Internet Small Computer System Interface) transports SCSI commands over IP networks for storage area networks.",
        "nas": "NAS (Network Attached Storage) is a dedicated file storage device connected to a network, allowing multiple users to access shared files.",
        "san": "SAN (Storage Area Network) is a high-speed network that provides block-level storage access to servers, used in data centers.",
        "raid 0": "RAID 0 stripes data across multiple drives for maximum performance, but offers no redundancy — if one drive fails, all data is lost.",
        "raid 1": "RAID 1 mirrors data across two drives, providing full redundancy — if one drive fails, data remains available on the other.",
        "raid 5": "RAID 5 stripes data with distributed parity across at least three drives, offering a balance of performance and fault tolerance.",
        "raid 10": "RAID 10 combines mirroring and striping, requiring at least four drives, offering both high performance and full redundancy.",

        # --- 48. COMUNICAȚII ȘI MESAGERIE ---
        "smtp server": "An SMTP server sends outgoing emails from a client to a recipient's mail server using the SMTP protocol on port 25, 465, or 587.",
        "exchange server": "Microsoft Exchange Server is a mail server and calendaring platform for businesses, integrating with Outlook.",
        "slack": "Slack is a cloud-based team communication platform with channels, direct messaging, and integrations with hundreds of tools.",
        "discord": "Discord is a communication platform originally for gamers, now used broadly for voice, video, and text chat in communities.",
        "teams": "Microsoft Teams is a collaboration platform integrating chat, video meetings, file storage, and Office 365 applications.",
        "zoom": "Zoom is a video conferencing platform known for its ease of use, supporting large meetings, webinars, and screen sharing.",
        "webhook": "A webhook is a way for an app to provide real-time information to another app by sending HTTP POST requests when events occur.",
        "pub sub": "Pub/Sub (Publish-Subscribe) is a messaging pattern where senders (publishers) send messages without knowing who receives them (subscribers).",
        "websocket vs socket": "WebSocket provides full-duplex communication over a single connection for web apps; raw sockets are lower-level network programming interfaces.",
        "webrtc": "WebRTC (Web Real-Time Communication) enables peer-to-peer audio, video, and data sharing in browsers without plugins.",

        # --- 49. DESIGN ȘI ARHITECTURĂ SOFTWARE ---
        "uml": "UML (Unified Modeling Language) is a standardized way to visualize the design of a software system using diagrams.",
        "class diagram": "A class diagram shows the structure of a system by displaying classes, attributes, methods, and relationships between objects.",
        "sequence diagram": "A sequence diagram shows how objects interact in a particular scenario, displaying the sequence of messages exchanged.",
        "entity relationship diagram": "An ERD (Entity Relationship Diagram) visualizes database structure, showing entities (tables), attributes (columns), and relationships.",
        "design system": "A design system is a collection of reusable UI components, patterns, and guidelines for building consistent user interfaces.",
        "responsive vs adaptive": "Responsive design fluidly adjusts to any screen size; adaptive design uses fixed layouts for specific screen sizes.",
        "accessibility": "Web accessibility (a11y) ensures websites are usable by people with disabilities, following standards like WCAG.",
        "i18n": "i18n (Internationalization) prepares software to support multiple languages and regional differences without code changes.",
        "l10n": "l10n (Localization) adapts software for a specific region or language by translating text and adjusting cultural conventions.",
        "micro frontend": "Micro frontends extend the microservices concept to the frontend, splitting a web app into independently deployable features.",

        # --- 50. DEZVOLTARE JOCURI ---
        "game loop": "A game loop is the core cycle of a video game that processes input, updates game state, and renders frames continuously.",
        "collision detection": "Collision detection determines when two objects in a game intersect, triggering events like damage, bouncing, or collecting items.",
        "sprite": "A sprite is a 2D image or animation integrated into a game scene, representing characters, objects, or effects.",
        "shader": "A shader is a program that runs on a GPU to calculate rendering effects like lighting, shadows, and textures.",
        "physics engine": "A physics engine simulates real-world physics in games, handling gravity, collisions, and object movement.",
        "asset pipeline": "The asset pipeline manages the creation, import, and optimization of game assets like textures, models, and sounds.",
        "level design": "Level design creates the stages, maps, and environments of a game, balancing challenge, exploration, and storytelling.",
        "procedural generation": "Procedural generation creates game content algorithmically rather than manually, used for maps, levels, and items.",
        "multiplayer netcode": "Netcode handles communication between players in online games, managing latency, synchronization, and lag compensation.",
        "game ai": "Game AI controls non-player character behavior, pathfinding (A* algorithm), and decision-making in video games.",

        # --- 51. SECURITATE PERSONALĂ ȘI PRIVACY ---
        "password manager": "A password manager securely stores and generates complex passwords, requiring only one master password to access all accounts.",
        "phishing detection": "Phishing detection identifies fraudulent attempts to steal personal information, often using email filtering and AI analysis.",
        "vpn vs proxy": "VPN encrypts all traffic and routes it through a server for privacy; a proxy only routes specific traffic without encryption.",
        "incognito mode": "Incognito mode prevents local browser history and cookies from being saved, but does not hide activity from ISPs or websites.",
        "end to end encryption": "End-to-end encryption ensures only the communicating users can read messages — not even the service provider has access.",
        "metadata": "Metadata is data about data — like who you called, when, and for how long — often more revealing than content itself.",
        "digital footprint": "A digital footprint is the trail of data you leave online through social media, browsing, and online activity.",
        "cookies tracking": "Tracking cookies follow your browsing across websites to build a profile for advertising and analytics purposes.",
        "gdpr": "GDPR (General Data Protection Regulation) is an EU law protecting personal data and privacy, with strict rules for companies handling data.",
        "ccpa": "CCPA (California Consumer Privacy Act) gives California residents rights over their personal data, including the right to know, delete, and opt-out.",

        # --- 52. PROGRAMARE FUNCȚIONALĂ ---
        "functional programming": "Functional programming treats computation as the evaluation of mathematical functions, avoiding side effects and mutable data.",
        "pure function": "A pure function always returns the same output for the same input and has no side effects, making it predictable and testable.",
        "immutable data": "Immutable data cannot be changed after creation. Instead of modifying, new copies are made, preventing unexpected bugs.",
        "higher order function": "A higher-order function takes other functions as arguments or returns them, enabling powerful abstractions like map, filter, and reduce.",
        "currying": "Currying transforms a function with multiple arguments into a sequence of functions, each taking a single argument.",
        "closure": "A closure is a function that remembers variables from its outer scope even after the outer function has finished executing.",
        "monad": "A monad is an abstraction that wraps values and chains operations, common in languages like Haskell and used in JavaScript Promises.",
        "tail recursion": "Tail recursion is a recursive function where the recursive call is the last operation, allowing compilers to optimize it into a loop.",
        "lazy evaluation": "Lazy evaluation delays computation until the result is needed, improving performance by avoiding unnecessary calculations.",
        "pattern matching": "Pattern matching checks a value against patterns and executes code based on which pattern fits, used extensively in functional languages.",

        # --- 53. BAZE DE DATE AVANSATE 2 ---
        "graph database": "Graph databases like Neo4j store data as nodes and edges, ideal for relationships like social networks and recommendations.",
        "time series database": "Time series databases like InfluxDB optimize storage and queries for time-stamped data like sensor readings and stock prices.",
        "columnar database": "Columnar databases like Cassandra store data by columns instead of rows, optimizing for analytical queries over large datasets.",
        "in memory database": "In-memory databases like Redis keep all data in RAM for sub-millisecond access, used for caching and real-time applications.",
        "bloom filter": "A Bloom filter is a space-efficient probabilistic data structure that tests if an element is in a set, with possible false positives.",
        "write ahead log": "WAL (Write-Ahead Log) records changes before they are written to the database, ensuring data integrity after crashes.",
        "two phase commit": "Two-phase commit is a protocol ensuring all participants in a distributed transaction agree to commit or abort.",
        "paxos": "Paxos is a consensus algorithm used in distributed systems to agree on a single value, forming the basis of many distributed databases.",
        "raft": "Raft is a consensus algorithm designed to be easier to understand than Paxos, used in etcd, CockroachDB, and other systems.",
        "eventual consistency": "Eventual consistency guarantees that if no new updates are made, all replicas will eventually converge to the same value.",

        # --- 54. LINUX ȘI ADMINISTRARE SISTEM ---
        "ssh": "SSH (Secure Shell) provides encrypted remote terminal access to servers, replacing insecure protocols like Telnet.",
        "scp": "SCP (Secure Copy Protocol) transfers files securely between hosts using SSH for encryption and authentication.",
        "rsync": "rsync efficiently synchronizes files between systems, transferring only changed parts of files for speed.",
        "iptables": "iptables is a Linux firewall tool that configures packet filtering rules in the kernel's netfilter framework.",
        "systemctl": "systemctl controls the systemd system and service manager, used to start, stop, and manage services on Linux.",
        "journalctl": "journalctl queries and displays logs from systemd's journal, offering powerful filtering by time, service, and priority.",
        "top": "top displays real-time Linux system information including running processes, CPU usage, and memory consumption.",
        "htop": "htop is an interactive process viewer for Linux with a better interface than top, supporting mouse controls and visual bars.",
        "netstat": "netstat shows network connections, routing tables, and interface statistics for monitoring network activity.",
        "lsof": "lsof (List Open Files) displays all open files and the processes using them — on Unix, everything is a file.",

        # --- 55. TEHNOLOGII VIITOARE ---
        "spintronics": "Spintronics uses electron spin instead of charge for data processing and storage, promising faster and more efficient devices.",
        "photonic computing": "Photonic computing uses light instead of electricity for computation, enabling ultra-fast data processing with minimal heat.",
        "biocomputing": "Biocomputing uses biological molecules like DNA for computation, offering massive parallelism for specific problem types.",
        "carbon nanotubes": "Carbon nanotubes are cylindrical molecules with extraordinary strength and electrical properties, promising faster transistors than silicon.",
        "room temperature superconductor": "Room temperature superconductors would transmit electricity with zero resistance without cooling, revolutionizing energy and computing.",
        "swarm robotics": "Swarm robotics coordinates large numbers of simple robots to accomplish complex tasks through decentralized control.",
        "autonomous vehicles": "Autonomous vehicles use AI, lidar, and cameras to navigate without human input, classified from Level 0 (no automation) to Level 5 (full automation).",
        "space internet": "Space internet uses satellite constellations like Starlink to provide global broadband coverage, even in remote areas.",
        "lab grown meat": "Lab-grown meat is cultured from animal cells without slaughtering animals, offering sustainable protein production.",
        "vertical farming": "Vertical farming grows crops in stacked layers indoors, using LED lighting and hydroponics for year-round food production.",

        # --- 56. INSTRUMENTE DE MONITORIZARE ---
        "nagios": "Nagios is an open-source monitoring system that watches hosts and services, alerting when problems occur.",
        "zabbix": "Zabbix is an enterprise monitoring platform for networks, servers, and applications with auto-discovery and visualization.",
        "datadog": "Datadog is a cloud monitoring and analytics platform providing infrastructure, application, and log monitoring.",
        "new relic": "New Relic is an observability platform for real-time application performance monitoring and analytics.",
        "splunk": "Splunk collects, indexes, and analyzes machine data for security, IT operations, and business analytics.",
        "elasticsearch": "Elasticsearch is a distributed search and analytics engine used for full-text search, logging, and data analysis.",
        "kibana": "Kibana is a visualization tool for Elasticsearch data, creating dashboards and charts for log and metrics analysis.",
        "logstash": "Logstash processes and transforms data before sending it to Elasticsearch, handling logs, metrics, and events.",
        "pagerduty": "PagerDuty is an incident management platform that alerts teams and coordinates responses to outages.",
        "uptime": "Uptime measures the percentage of time a system is operational, typically expressed as 99.9% ('three nines') availability.",

        # --- 57. CONTAINERE ȘI ORCHESTRARE ---
        "container vs vm": "Containers share the host OS kernel and isolate applications; VMs run full guest OS on hypervisor for stronger isolation.",
        "docker hub": "Docker Hub is a cloud registry for sharing and managing Docker container images, public and private.",
        "dockerfile": "A Dockerfile is a text file with instructions to build a Docker image, defining the environment and dependencies.",
        "docker network": "Docker network allows containers to communicate with each other, supporting bridge, host, overlay, and custom drivers.",
        "docker volume": "Docker volumes persist data independently of container lifecycle, used for databases and file storage.",
        "kubectl": "kubectl is the command-line tool for interacting with Kubernetes clusters, used to deploy and manage applications.",
        "kubeconfig": "kubeconfig is a configuration file used by kubectl to connect to Kubernetes clusters with authentication details.",
        "helm chart": "A Helm chart is a package of pre-configured Kubernetes resources, making application deployment repeatable and shareable.",
        "ingress": "Kubernetes Ingress manages external access to services, typically HTTP/HTTPS routing with load balancing and SSL termination.",
        "configmap": "A ConfigMap stores non-sensitive configuration data as key-value pairs, decoupling configuration from application code.",

        # --- 58. SISTEME DE OPERARE MOBILE ---
        "ios vs android": "iOS is Apple's closed mobile OS with strict control; Android is Google's open-source OS with broader device support.",
        "ipados": "iPadOS is Apple's tablet-optimized version of iOS with multitasking, Apple Pencil support, and desktop-class features.",
        "wear os vs watchos": "Wear OS is Google's smartwatch platform for multiple brands; watchOS is Apple's exclusive Watch operating system.",
        "huawei harmonyos": "HarmonyOS is Huawei's distributed operating system designed for phones, tablets, IoT, and smart home devices.",
        "samsung one ui": "One UI is Samsung's Android overlay with a clean design, one-handed usability, and Galaxy ecosystem features.",
        "xiaomi hyperos": "HyperOS is Xiaomi's unified operating system replacing MIUI, connecting phones, cars, and smart home products.",
        "google play vs app store": "Google Play serves Android apps with more openness; Apple App Store has stricter review and higher revenue per app.",
        "sideloading": "Sideloading installs apps from outside the official store, allowed on Android with warnings, restricted on iOS.",
        "mobile device management": "MDM allows organizations to manage, secure, and enforce policies on employee mobile devices remotely.",
        "huawei mobile services": "HMS is Huawei's alternative to Google Mobile Services, providing APIs, app store, and cloud for Huawei devices.",

        # --- 59. REALITATE VIRTUALĂ ȘI AUGMENTATĂ 2 ---
        "inside out tracking": "Inside-out tracking uses cameras on the headset to map surroundings and track movement, without external sensors.",
        "outside in tracking": "Outside-in tracking uses external sensors placed in the room to track headset and controller movements precisely.",
        "foveated rendering": "Foveated rendering renders only the area the user is looking at in high detail, saving GPU resources.",
        "passthrough": "Passthrough uses cameras on VR headsets to show the real world, enabling mixed reality experiences.",
        "haptic gloves": "Haptic gloves provide tactile feedback in VR, letting users feel virtual objects through vibrations and force.",
        "volumetric capture": "Volumetric capture records subjects in 3D space using multiple cameras, creating holographic video content.",
        "lightfield": "Lightfield technology captures both intensity and direction of light rays, enabling realistic 3D displays.",
        "eye tracking": "Eye tracking follows where a user is looking, enabling foveated rendering and more intuitive interfaces.",
        "full body tracking": "Full body tracking captures entire body movement for VR, enabling realistic avatars and motion in virtual spaces.",
        "omnidirectional treadmill": "Omnidirectional treadmills let users walk naturally in any direction in VR while staying in place.",

        # --- 60. ENERGIE ȘI SUSTENABILITATE ---
        "carbon neutral": "Carbon neutral means balancing emitted carbon with equivalent carbon removal or offsets, achieving net zero carbon footprint.",
        "net zero": "Net zero extends carbon neutrality by eliminating all avoidable emissions and offsetting remaining unavoidable ones.",
        "circular economy": "Circular economy designs products for reuse, repair, and recycling, minimizing waste and resource consumption.",
        "right to repair": "Right to repair gives consumers legal access to repair their own devices, opposing manufacturer restrictions.",
        "green data center": "Green data centers minimize environmental impact through renewable energy, efficient cooling, and sustainable design.",
        "e-waste recycling": "E-waste recycling recovers valuable materials like gold, copper, and lithium from discarded electronics.",
        "low power chip": "Low-power chips use energy-efficient architectures like ARM big.LITTLE and Intel E-cores to reduce consumption.",
        "solar efficiency": "Solar efficiency measures what percentage of sunlight a panel converts to electricity, with current records around 47%.",
        "battery recycling": "Battery recycling extracts lithium, cobalt, and nickel from used batteries for reuse in new battery production.",
        "smart home energy": "Smart home energy systems optimize electricity use through smart thermostats, automated lights, and real-time monitoring.",

        # --- 61. ROBOTICĂ ȘI AUTOMATIZARE 2 ---
        "ros topics": "ROS topics are named buses over which nodes exchange messages in a publish-subscribe pattern.",
        "ros services": "ROS services allow synchronous request-reply communication between ROS nodes for specific tasks.",
        "ros actions": "ROS actions provide asynchronous goal-oriented communication with feedback, suitable for long-running tasks.",
        "gazebo": "Gazebo is a 3D robot simulation environment with physics engine, used with ROS for testing algorithms.",
        "rviz": "RViz is a 3D visualization tool for ROS, displaying robot models, sensor data, and maps in real-time.",
        "slam algorithm": "SLAM (Simultaneous Localization and Mapping) builds maps while tracking robot position, using lidar or cameras.",
        "inverse kinematics": "Inverse kinematics calculates joint angles needed to position a robot's end-effector at a desired point.",
        "forward kinematics": "Forward kinematics calculates the position of a robot's end-effector given specific joint angles.",
        "pid controller": "PID (Proportional-Integral-Derivative) controller adjusts robot motors by calculating error correction for smooth movement.",
        "ros bag": "ROS bag files record and play back ROS message data, used for debugging and testing robotic systems.",

        # --- 62. CERCETARE ȘI ACADEMIC ---
        "peer review": "Peer review is the evaluation of scientific work by others in the same field before publication.",
        "arxiv": "arXiv is a free online repository of scientific papers, widely used in physics, computer science, and mathematics.",
        "impact factor": "Impact factor measures the frequency a journal's articles are cited, indicating its influence in the field.",
        "open access": "Open access makes research freely available to everyone without paywalls, increasing knowledge accessibility.",
        "h index": "h-index measures a researcher's productivity and citation impact — an h-index of 10 means 10 papers with at least 10 citations each.",
        "moore's law": "Moore's Law observed that transistor density doubles about every two years, though it's slowing in recent years.",
        "turing test": "The Turing Test evaluates if a machine can exhibit intelligent behavior indistinguishable from a human.",
        "singularity": "The technological singularity hypothesizes AI surpassing human intelligence, causing runaway technological growth.",
        "bell's theorem": "Bell's theorem proves quantum mechanics cannot be explained by local hidden variables, confirming quantum entanglement.",
        "p vs np": "P vs NP asks if every problem whose solution can be verified quickly can also be solved quickly — one of the greatest unsolved problems in computer science.",

        # --- 63. BUSINESS ȘI MANAGEMENT ---
        "agile vs waterfall": "Agile iterates in small cycles with continuous feedback; Waterfall follows sequential phases with upfront planning.",
        "scrum master": "Scrum Master facilitates Agile Scrum processes, removing obstacles and ensuring team productivity.",
        "product owner": "Product Owner represents stakeholders' interests, managing the product backlog and prioritizing features.",
        "mvp product": "MVP (Minimum Viable Product) is the simplest version of a product that can be released to test market demand.",
        "okr": "OKR (Objectives and Key Results) is a goal-setting framework aligning company, team, and individual goals.",
        "kpi": "KPI (Key Performance Indicator) measures progress toward specific business objectives, like revenue, retention, and uptime.",
        "swot": "SWOT analysis evaluates Strengths, Weaknesses, Opportunities, and Threats for strategic business planning.",
        "lean startup": "Lean Startup methodology emphasizes rapid experimentation, customer feedback, and iterative product releases.",
        "venture capital": "Venture capital firms invest in high-growth startups in exchange for equity, often after Series A rounds.",
        "private equity": "Private equity invests in mature companies, often restructuring or improving them before selling for profit.",

        # --- 64. DEZVOLTARE API ---
        "openapi": "OpenAPI (formerly Swagger) is a specification for describing REST APIs, enabling auto-generated docs and client SDKs.",
        "postman collection": "Postman Collections group API requests for testing, documentation, and automation workflows.",
        "rate limiting": "Rate limiting restricts how many API requests a client can make in a time period, preventing abuse and overload.",
        "api versioning": "API versioning manages changes to APIs over time, using URL paths (/v1/, /v2/) or request headers.",
        "bearer token": "Bearer token is an access token sent in the Authorization header of HTTP requests for API authentication.",
        "api monetization": "API monetization charges for API access through subscription tiers, pay-per-call, or freemium models.",
        "api gateway vs load balancer": "API Gateway routes requests and handles auth; Load Balancer distributes traffic across servers for availability.",
        "sdk vs api": "SDK is a full development kit with tools and libraries; API is just the interface for service communication.",
        "idempotent": "An idempotent operation produces the same result whether called once or multiple times, important for API safety.",
        "throttling": "Throttling slows down API requests exceeding limits rather than rejecting them immediately.",

        # --- 65. ETICĂ ȘI LEGAL ÎN TECH ---
        "algorithmic bias": "Algorithmic bias occurs when AI systems produce unfair outcomes due to biased training data or flawed design.",
        "explainable ai": "XAI (Explainable AI) makes AI decisions transparent and understandable to humans, critical for trust and compliance.",
        "facial recognition ethics": "Facial recognition ethics debates the balance between security benefits and privacy rights in public surveillance.",
        "data sovereignty": "Data sovereignty requires data to follow the laws of the country where it's collected and stored.",
        "digital divide": "The digital divide is the gap between those with internet/tech access and those without, affecting education and opportunity.",
        "net neutrality": "Net neutrality requires ISPs to treat all internet traffic equally, without blocking or prioritizing paid content.",
        "right to be forgotten": "The right to be forgotten allows individuals to request removal of personal data from search engines under GDPR.",
        "open source license": "Open source licenses like MIT, GPL, and Apache grant permission to use, modify, and share code with varying conditions.",
        "patent troll": "A patent troll acquires patents solely to sue companies for infringement, without producing any products.",
        "whistleblower": "A whistleblower exposes unethical or illegal activities within an organization, often protected by law from retaliation.",

                # --- 66. TEHNOLOGII WEB AVANSATE ---
        "webpack vs vite": "Webpack is a mature, highly configurable bundler; Vite is a modern, faster alternative using native ES modules for development.",
        "babel vs swc": "Babel compiles modern JavaScript to backwards-compatible code; SWC is a faster Rust-based alternative used by Next.js.",
        "tailwind vs bootstrap": "Tailwind is utility-first CSS for custom designs; Bootstrap is component-based with pre-built UI elements.",
        "svelte vs react": "Svelte compiles components at build time for smaller bundles; React uses a virtual DOM for runtime updates.",
        "astro": "Astro is a static site builder that ships zero JavaScript by default, ideal for content-focused websites.",
        "qwik": "Qwik is a framework delivering instant-loading apps by resumability instead of hydration, created by the inventor of Angular.",
        "solidjs": "SolidJS is a reactive JavaScript framework with no virtual DOM, offering React-like syntax with Svelte-like performance.",
        "htmx": "HTMX extends HTML with AJAX, CSS transitions, and WebSockets directly in markup, reducing JavaScript complexity.",
        "alpinejs": "Alpine.js is a lightweight JavaScript framework for adding interactivity with minimal code, ideal for server-rendered pages.",
        "jquery modern": "jQuery simplified DOM manipulation for older browsers; modern vanilla JavaScript can do most tasks natively without jQuery.",

        # --- 67. BAZE DE DATE ÎN PRACTICĂ ---
        "orm vs raw sql": "ORM simplifies database operations with objects but can hide complexity; raw SQL offers full control and optimization.",
        "database indexing types": "B-tree for range queries, hash for equality, GiST for geometric data, GIN for full-text search.",
        "connection string": "A connection string contains database location, credentials, and parameters for establishing database connections.",
        "odbc": "ODBC (Open Database Connectivity) is a standard API for accessing different database management systems.",
        "jdbc": "JDBC (Java Database Connectivity) enables Java applications to interact with databases through standard SQL queries.",
        "query optimizer": "A query optimizer determines the most efficient way to execute an SQL query based on statistics and indexes.",
        "database view vs table": "A view is a saved query result that acts like a virtual table; a table stores actual data physically.",
        "materialized view": "A materialized view stores query results physically for faster access, refreshed periodically or on demand.",
        "database trigger example": "A trigger automatically logs changes to an audit table when INSERT, UPDATE, or DELETE occurs on a main table.",
        "cte sql": "CTE (Common Table Expression) creates temporary named result sets, making complex queries more readable and recursive queries possible.",

        # --- 68. SISTEME DE OPERARE SERVER ---
        "ubuntu server vs desktop": "Ubuntu Server is headless with no GUI, optimized for services; Desktop includes GNOME and user applications.",
        "centos vs rocky": "CentOS was the free Red Hat clone; Rocky Linux is its spiritual successor after CentOS was discontinued.",
        "rhel": "RHEL (Red Hat Enterprise Linux) is a commercial Linux distribution with enterprise support and certification ecosystem.",
        "suse": "SUSE Linux Enterprise Server is a commercial distribution popular in Europe for SAP and mainframe workloads.",
        "arch linux": "Arch Linux is a rolling-release distribution for advanced users, offering bleeding-edge software and full customization.",
        "gentoo": "Gentoo is a source-based Linux distribution where packages are compiled locally for optimal performance.",
        "alpine linux": "Alpine Linux is a lightweight distribution using musl and BusyBox, popular for Docker containers due to small size.",
        "freebsd": "FreeBSD is a Unix-like operating system known for networking performance, ZFS support, and the ports collection.",
        "openbsd": "OpenBSD emphasizes security, correctness, and portability, with integrated cryptography and a clean codebase.",
        "netbsd": "NetBSD runs on more platforms than any other OS, from embedded devices to mainframes, with a focus on portability.",

        # --- 69. AUTENTIFICARE ȘI AUTORIZARE ---
        "oauth vs jwt": "OAuth 2.0 is an authorization framework for delegated access; JWT is a token format used within OAuth flows.",
        "openid vs oauth": "OpenID Connect adds authentication (identity) on top of OAuth 2.0 authorization framework.",
        "sso": "SSO (Single Sign-On) lets users access multiple applications with one set of credentials, using protocols like SAML or OIDC.",
        "ldap": "LDAP (Lightweight Directory Access Protocol) is a protocol for accessing directory services like Microsoft Active Directory.",
        "active directory": "Active Directory is Microsoft's identity and access management service for Windows domain networks.",
        "kerberos": "Kerberos is a network authentication protocol using tickets to allow secure communication over non-secure networks.",
        "rbac": "RBAC (Role-Based Access Control) assigns permissions to roles rather than individual users, simplifying access management.",
        "abac": "ABAC (Attribute-Based Access Control) evaluates attributes (user, resource, environment) to make access decisions dynamically.",
        "password hashing": "Password hashing uses algorithms like bcrypt, Argon2 to securely store passwords — never store plain text passwords.",
        "session vs token": "Sessions store state on the server with cookies; tokens store state client-side and are validated cryptographically.",

        # --- 70. PERFORMANȚĂ ȘI OPTIMIZARE ---
        "lazy loading": "Lazy loading defers loading of non-critical resources until needed, improving initial page load speed.",
        "code splitting": "Code splitting divides JavaScript bundles into smaller chunks loaded on demand, reducing initial download size.",
        "tree shaking": "Tree shaking removes unused code from final bundles during build, reducing file size for production.",
        "debounce": "Debouncing limits function execution rate by waiting after the last call, useful for search inputs and resize events.",
        "throttle": "Throttling ensures a function executes at most once per interval, useful for scroll handlers and API rate limits.",
        "memoization": "Memoization caches function results based on input parameters, avoiding expensive recalculations.",
        "cors vs cors preflight": "Simple CORS requests are sent directly; complex requests trigger a preflight OPTIONS request for server approval.",
        "gzip compression": "Gzip compresses web assets before transmission, reducing transfer size by 60-80% for text-based files.",
        "brotli": "Brotli is a modern compression algorithm by Google, achieving better ratios than gzip with similar speed.",
        "http caching headers": "Cache-Control (max-age, public/private), ETag, and Last-Modified headers control how browsers cache responses.",

        # --- 71. DEZVOLTARE CROSS-PLATFORM ---
        "electron": "Electron builds desktop apps using web technologies (HTML, CSS, JS) with Chromium and Node.js. Used by VS Code, Discord, Slack.",
        "tauri": "Tauri is a lightweight alternative to Electron using Rust backend, producing smaller and faster desktop applications.",
        "react native vs flutter": "React Native uses JavaScript with native components; Flutter uses Dart with its own rendering engine.",
        "xamarin": "Xamarin is Microsoft's cross-platform framework using C# for iOS, Android, and Windows apps with shared code.",
        "capacitor": "Capacitor is a cross-platform runtime that turns web apps into native mobile apps with access to device APIs.",
        "cordova": "Apache Cordova wraps web apps in native containers with plugin access to device features like camera and GPS.",
        "ionic": "Ionic is a UI toolkit for building cross-platform mobile apps using web technologies, integrated with Angular, React, or Vue.",
        "kotlin multiplatform": "KMP shares business logic across platforms while keeping native UI per platform, as an alternative to Flutter.",
        "flutter vs dart": "Flutter is the framework; Dart is the language it uses, also used independently for server and CLI applications.",
        "native vs hybrid": "Native apps have full platform access and best performance; hybrid apps share code across platforms but may lag in complex UIs.",

        # --- 72. TESTING AVANSAT ---
        "integration vs unit test": "Unit tests verify isolated functions; integration tests verify that modules work together correctly.",
        "e2e testing tools": "Cypress, Playwright, and Selenium automate browser testing, simulating real user interactions.",
        "snapshot testing": "Snapshot tests capture component output and compare against saved snapshots to detect unexpected changes.",
        "mocking vs stubbing": "Mocks verify behavior (expectations on calls); stubs provide predetermined data responses.",
        "test driven development cycle": "TDD cycle: Write a failing test (Red) → Write minimal code to pass (Green) → Refactor cleanly (Refactor).",
        "behavior driven development": "BDD describes behavior in natural language (Gherkin: Given-When-Then), bridging technical and business teams.",
        "code coverage tools": "Istanbul (nyc), Coverage.py measure what percentage of code is exercised by tests, identifying gaps.",
        "property based testing": "Property-based testing generates random inputs to verify properties hold true for all possible values.",
        "fuzz testing": "Fuzzing feeds random or malformed inputs to find crashes, memory leaks, and security vulnerabilities.",
        "regression testing automation": "Automated regression tests run after each change to catch new bugs breaking previously working features.",

        # --- 73. SECURITATE ÎN PRACTICĂ ---
        "owasp top 10": "OWASP Top 10 lists the most critical web security risks: injection, broken auth, XSS, insecure design, and more.",
        "csrf prevention": "CSRF tokens, SameSite cookies, and Origin header validation prevent cross-site request forgery attacks.",
        "xss prevention": "Output encoding, Content Security Policy headers, and input sanitization prevent cross-site scripting attacks.",
        "clickjacking": "Clickjacking tricks users into clicking invisible elements; prevented with X-Frame-Options and CSP frame-ancestors.",
        "ssl pinning": "SSL pinning binds a specific certificate to an app, preventing man-in-the-middle attacks with fake certificates.",
        "dns poisoning": "DNS cache poisoning corrupts DNS records, redirecting users to malicious sites; DNSSEC prevents this.",
        "arp spoofing": "ARP spoofing associates the attacker's MAC address with a legitimate IP, intercepting network traffic.",
        "port scanning": "Port scanning discovers open ports and services on a target system, used by both admins and attackers.",
        "vulnerability scanning": "Automated tools like Nessus, OpenVAS scan systems for known vulnerabilities and misconfigurations.",
        "bug bounty": "Bug bounty programs reward security researchers for finding and responsibly disclosing vulnerabilities.",

        # --- 74. MANAGEMENTUL PROIECTELOR IT ---
        "jira": "Jira is an issue tracking and project management tool by Atlassian, widely used in Agile software development.",
        "confluence": "Confluence is a team workspace for documentation and knowledge sharing, integrated with Jira.",
        "trello": "Trello is a visual project management tool using Kanban boards, cards, and lists for task organization.",
        "asana": "Asana is a work management platform helping teams organize, track, and manage projects and tasks.",
        "notion": "Notion is an all-in-one workspace combining notes, databases, wikis, and project management in one tool.",
        "gantt chart": "Gantt charts visualize project schedules with bars showing tasks, durations, and dependencies over time.",
        "burndown chart": "A burndown chart tracks remaining work in a sprint, showing if the team is on track to complete the sprint goal.",
        "velocity agile": "Velocity measures how many story points a team completes per sprint, used for sprint planning and forecasting.",
        "retrospective": "A sprint retrospective is a meeting where teams discuss what went well, what to improve, and action items.",
        "definition of done": "DoD is a checklist ensuring all quality criteria are met before a task is considered complete.",

        # --- 75. CLOUD COMPUTING AVANSAT ---
        "aws lambda": "AWS Lambda runs code without provisioning servers, executing functions in response to events and scaling automatically.",
        "aws s3": "Amazon S3 (Simple Storage Service) is object storage with industry-leading scalability, availability, and durability.",
        "aws ec2": "Amazon EC2 provides resizable virtual servers in the cloud, with full control over computing resources.",
        "aws rds": "Amazon RDS manages relational databases (MySQL, PostgreSQL, Oracle) with automated backups and scaling.",
        "aws dynamodb": "DynamoDB is a fully managed NoSQL key-value database with single-digit millisecond performance.",
        "aws cloudfront": "CloudFront is a CDN service that delivers content globally with low latency through edge locations.",
        "aws route 53": "Route 53 is a scalable DNS service that routes users to AWS services and external endpoints.",
        "aws iam": "IAM (Identity and Access Management) controls who can access AWS resources and what they can do.",
        "aws vpc": "VPC (Virtual Private Cloud) provides an isolated network section of AWS where resources can be launched securely.",
        "aws sagemaker": "SageMaker is a fully managed service to build, train, and deploy machine learning models at scale.",

        # --- 76. AZURE CLOUD ---
        "azure functions": "Azure Functions is a serverless compute service running code on-demand without managing infrastructure.",
        "azure blob storage": "Azure Blob Storage stores massive amounts of unstructured data like images, videos, and backups.",
        "azure devops": "Azure DevOps provides CI/CD pipelines, Git repos, Kanban boards, and testing tools for development teams.",
        "azure active directory": "Azure AD is Microsoft's cloud identity service for authentication to Microsoft 365, Azure, and apps.",
        "azure kubernetes service": "AKS is a managed Kubernetes service simplifying cluster deployment and management on Azure.",
        "azure cosmos db": "Cosmos DB is a globally distributed NoSQL database with multi-model support and guaranteed SLAs.",
        "azure sql": "Azure SQL is a managed relational database service built on SQL Server engine with cloud capabilities.",
        "azure cognitive services": "Azure Cognitive Services offers pre-built AI APIs for vision, speech, language, and decision-making.",
        "azure virtual machines": "Azure VMs provide scalable computing resources in the cloud with full OS control.",
        "azure load balancer": "Azure Load Balancer distributes traffic across VMs for high availability and fault tolerance.",

        # --- 77. GOOGLE CLOUD ---
        "gcp compute engine": "Google Compute Engine offers virtual machines running in Google's data centers with flexible configurations.",
        "gcp cloud storage": "Google Cloud Storage is unified object storage with multiple classes for different access patterns.",
        "gcp cloud functions": "Google Cloud Functions is a lightweight serverless platform for event-driven microservices.",
        "gcp cloud run": "Cloud Run runs containerized applications serverlessly on Google's infrastructure with auto-scaling.",
        "gcp bigquery": "BigQuery is a serverless data warehouse for analytics with built-in machine learning capabilities.",
        "gcp cloud sql": "Cloud SQL is a fully managed relational database service for MySQL, PostgreSQL, and SQL Server.",
        "gcp firestore": "Firestore is a flexible NoSQL document database for mobile and web apps with real-time sync.",
        "gcp pubsub": "Pub/Sub is a messaging service for asynchronous communication between applications and services.",
        "gcp cloud spanner": "Spanner is a globally distributed relational database combining SQL with horizontal scalability.",
        "gcp vertex ai": "Vertex AI is Google's unified ML platform for building, deploying, and scaling AI models.",

        # --- 78. PROGRAMARE FUNCȚIONALĂ AVANSATĂ ---
        "functor": "A functor is a type that can be mapped over, like arrays with .map() — transforming values inside a container.",
        "applicative": "An applicative functor applies functions wrapped in a context to values wrapped in a context.",
        "monad vs promise": "JavaScript Promises behave like monads with .then() chaining, but aren't pure monads in the strict sense.",
        "either monad": "Either represents a value of one of two types: Right (success) or Left (error), avoiding exceptions.",
        "maybe monad": "Maybe (or Optional) handles nullable values safely, eliminating null reference errors.",
        "io monad": "IO monad encapsulates side effects (reading files, HTTP calls) and defers execution until explicitly run.",
        "function composition": "Function composition applies one function to the result of another: compose(f, g)(x) = f(g(x)).",
        "point free style": "Point-free (tacit) programming defines functions without naming their arguments, using composition.",
        "algebraic data types": "ADTs combine types: product types (AND — tuples, records) and sum types (OR — discriminated unions).",
        "pattern matching functional": "Pattern matching destructures data and branches execution based on structure and values.",

        # --- 79. SISTEME DISTRIBUITE ---
        "distributed consensus": "Consensus algorithms (Paxos, Raft) ensure agreement among nodes in distributed systems despite failures.",
        "distributed hash table": "DHT distributes key-value storage across nodes, used in BitTorrent, IPFS, and distributed databases.",
        "gossip protocol": "Gossip protocols spread information through peer-to-peer communication, like epidemics, used in Cassandra.",
        "leader election": "Leader election selects a node to coordinate tasks in a distributed system when leaders fail.",
        "vector clock": "Vector clocks track causality of events in distributed systems without relying on synchronized clocks.",
        "distributed lock": "Distributed locks prevent concurrent access to shared resources across multiple processes or nodes.",
        "quorum": "Quorum ensures a minimum number of nodes agree on an operation before it's considered successful.",
        "split brain": "Split brain occurs when a cluster divides into separate groups, each thinking it's the active cluster.",
        "event sourcing": "Event sourcing stores state changes as events, allowing full audit trails and temporal queries.",
        "cqrs": "CQRS (Command Query Responsibility Segregation) separates read and write operations for performance and scalability.",

        # --- 80. INTERNET OF THINGS (IoT) AVANSAT ---
        "esp32": "ESP32 is a low-cost microcontroller with Wi-Fi and Bluetooth, widely used in IoT and maker projects.",
        "esp8266": "ESP8266 is an earlier Wi-Fi chip enabling low-cost IoT devices with basic processing capabilities.",
        "zigbee vs zwave": "Zigbee and Z-Wave are wireless protocols for smart home devices; Zigbee is more open with mesh networking.",
        "lora": "LoRa (Long Range) enables low-power wide-area communication for IoT devices across kilometers.",
        "lorawan": "LoRaWAN defines the network protocol on top of LoRa for connecting IoT devices to gateways and servers.",
        "nb iot": "NB-IoT (Narrowband IoT) uses cellular networks for low-bandwidth, deep-coverage IoT communication.",
        "bluetooth le": "Bluetooth Low Energy provides short-range wireless with minimal power consumption for wearables and sensors.",
        "rfid": "RFID uses radio waves to identify and track objects through tags and readers, common in inventory systems.",
        "nfc": "NFC enables short-range communication between devices for payments, pairing, and data exchange.",
        "mqtt vs coap": "MQTT uses TCP publish-subscribe for reliable messaging; CoAP uses UDP request-response for constrained devices.",

        # --- 81. CRIPTOMONEDE ȘI BLOCKCHAIN ---
        "proof of stake vs work": "PoS selects validators by staked coins (energy efficient); PoW requires solving puzzles (energy intensive).",
        "defi lending": "DeFi lending platforms like Aave allow users to lend and borrow crypto without intermediaries.",
        "stablecoin types": "Stablecoins: fiat-collateralized (USDC), crypto-collateralized (DAI), algorithmic (UST — risky).",
        "dao example": "DAOs like Uniswap govern protocols through token-holder voting on proposals and treasury management.",
        "nft minting": "NFT minting creates a unique token on a blockchain representing ownership of digital art, music, or collectibles.",
        "gas optimization": "Gas optimization reduces transaction costs on Ethereum through efficient contract code and batch operations.",
        "smart contract audit": "Smart contract audits review code for security vulnerabilities, logic errors, and gas inefficiencies.",
        "layer 2 scaling": "Layer 2 solutions like Polygon, Arbitrum process transactions off-chain for faster and cheaper operations.",
        "zero knowledge proof": "ZK-proofs prove knowledge of a value without revealing it, used for privacy and scaling.",
        "metamask vs trust wallet": "MetaMask is a browser extension wallet; Trust Wallet is mobile-first with multi-chain support.",

        # --- 82. ȘTIINȚA DATELOR ---
        "data pipeline": "A data pipeline moves data from sources through processing stages to destinations like warehouses.",
        "etl vs elt": "ETL transforms before loading into warehouse; ELT loads raw data first then transforms inside warehouse.",
        "data lake": "A data lake stores raw, unstructured data at scale, using object storage with schema-on-read.",
        "data warehouse": "A data warehouse stores structured, processed data optimized for querying and business intelligence.",
        "data mesh": "Data mesh decentralizes data ownership by business domain, treating data as a product with self-serve access.",
        "feature store": "A feature store manages ML features for training and serving, ensuring consistency across environments.",
        "model drift": "Model drift occurs when ML model performance degrades as real-world data patterns change over time.",
        "data cleaning": "Data cleaning handles missing values, duplicates, outliers, and inconsistencies before analysis.",
        "exploratory data analysis": "EDA uses statistics and visualization to understand data patterns, relationships, and anomalies.",
        "ab testing statistics": "A/B testing compares two versions statistically to determine which performs better with significance.",

        # --- 83. DESIGN PATTERNS ---
        "strategy pattern": "Strategy pattern defines interchangeable algorithms and lets the client choose which to use at runtime.",
        "adapter pattern": "Adapter converts an interface into another expected by clients, enabling incompatible interfaces to work together.",
        "decorator pattern": "Decorator adds behavior to objects dynamically without modifying their structure or subclassing.",
        "facade pattern": "Facade provides a simplified interface to a complex subsystem, reducing dependencies for clients.",
        "builder pattern": "Builder separates object construction from representation, creating complex objects step by step.",
        "prototype pattern": "Prototype creates new objects by cloning existing ones, avoiding expensive construction.",
        "chain of responsibility": "Chain passes requests through handlers until one processes it, decoupling sender and receiver.",
        "state pattern": "State pattern allows objects to change behavior when internal state changes, like a finite state machine.",
        "command pattern": "Command encapsulates requests as objects, enabling parameterization, queuing, and undo operations.",
        "mediator pattern": "Mediator centralizes communication between objects, reducing direct dependencies and coupling.",

        # --- 84. MICROSERVICES ȘI ARHITECTURĂ ---
        "api gateway pattern": "API Gateway is a single entry point routing requests to appropriate microservices with cross-cutting concerns.",
        "service discovery": "Service discovery automatically detects services in a network, enabling dynamic scaling and failover.",
        "circuit breaker": "Circuit breaker prevents cascading failures by stopping calls to failing services and allowing recovery.",
        "saga pattern": "Saga manages distributed transactions across microservices through a sequence of local transactions.",
        "event driven architecture": "Event-driven architecture uses events to trigger communication between decoupled services.",
        "cors microservices": "CORS in microservices manages cross-origin access between services on different domains.",
        "bulkhead pattern": "Bulkhead isolates resources so a failure in one component doesn't exhaust all system resources.",
        "sidecar pattern": "Sidecar deploys helper components alongside services, used by service meshes like Istio for networking.",
        "strangler fig": "Strangler Fig pattern gradually migrates from a monolithic system by replacing parts incrementally.",
        "backends for frontends": "BFF creates separate backend APIs tailored to each frontend type (mobile, web, desktop).",

                # --- 85. DEZVOLTARE MOBILĂ AVANSATĂ 2 ---
        "swift ui vs uikit": "SwiftUI is Apple's modern declarative framework; UIKit is the older imperative framework still widely used.",
        "kotlin coroutines": "Kotlin coroutines simplify async programming with sequential code style, replacing callbacks and RxJava.",
        "jetpack vs compose": "Jetpack is Android's suite of libraries; Compose is the modern declarative UI toolkit within Jetpack.",
        "flutter widgets": "In Flutter, everything is a widget — stateful for dynamic content, stateless for static content.",
        "react native bridge": "React Native bridge communicates between JavaScript and native modules asynchronously for performance.",
        "xcode instruments": "Instruments in Xcode profile iOS apps for performance, memory leaks, and energy usage.",
        "android profiler": "Android Studio Profiler monitors CPU, memory, network, and battery usage in real-time during development.",
        "app thinning": "App thinning delivers only the assets needed for a specific device, reducing app size for iOS and Android.",
        "play store console": "Google Play Console manages app publishing, updates, reviews, and analytics for Android developers.",
        "app store connect": "App Store Connect manages iOS app submissions, TestFlight beta testing, and sales analytics.",

        # --- 86. REALITATE EXTINSĂ (XR) ---
        "augmented reality vs virtual": "AR overlays digital on real world (phone camera); VR immerses in fully digital environment (headset).",
        "mixed reality headsets": "MR headsets like HoloLens blend real and virtual, allowing digital objects to interact with physical space.",
        "apple vision pro development": "Vision Pro development uses SwiftUI, RealityKit, and ARKit for spatial computing experiences.",
        "meta quest development": "Meta Quest development uses Unity or Unreal Engine with Oculus SDK for VR applications.",
        "webxr": "WebXR enables VR and AR experiences directly in browsers without installing apps.",
        "spatial mapping": "Spatial mapping creates 3D meshes of real environments, enabling realistic AR object placement.",
        "hand tracking": "Hand tracking uses cameras to detect finger and hand movements as input without controllers.",
        "haptics in xr": "Haptic feedback in XR provides touch sensations (vibrations, forces) for immersive interactions.",
        "volumetric video": "Volumetric video captures 3D performances viewable from any angle, used in immersive entertainment.",
        "digital twin industry": "Digital twins in industry create virtual replicas of factories for simulation and optimization.",

        # --- 87. AUTOMATIZARE ȘI SCRIPTING ---
        "bash scripting": "Bash scripts automate command-line tasks on Linux/macOS with variables, loops, and conditionals.",
        "python scripting": "Python scripts automate file operations, API calls, data processing, and system administration.",
        "cron vs systemd timer": "Cron schedules jobs by time; systemd timers offer more features like randomized delays and dependencies.",
        "makefile": "Makefile defines rules for building and automating tasks, traditionally for compiling code but used broadly.",
        "shell vs bash": "Shell is any command interpreter; Bash (Bourne Again Shell) is the most common Unix shell.",
        "powershell vs cmd": "PowerShell is Microsoft's advanced shell with object-based scripting; CMD is the legacy command prompt.",
        "sed": "sed (stream editor) filters and transforms text in pipelines, useful for find-and-replace in scripts.",
        "awk": "awk processes and analyzes text files, extracting columns and performing calculations on structured data.",
        "jq": "jq is a lightweight command-line JSON processor for parsing, filtering, and transforming JSON data.",
        "ansible playbook": "Ansible playbooks define automation tasks in YAML for configuration management and deployment.",

        # --- 88. ARHITECTURI DE SISTEM ---
        "monolith vs microservices": "Monolith is a single deployable unit; microservices split into independent services communicating via APIs.",
        "serverless architecture": "Serverless runs code in response to events without managing servers, auto-scaling to zero when idle.",
        "event sourcing architecture": "Event sourcing records all state changes as events, enabling full rebuild and audit of system state.",
        "hexagonal architecture": "Hexagonal (ports & adapters) isolates core business logic from external dependencies through interfaces.",
        "clean architecture": "Clean Architecture organizes code in concentric circles with dependencies pointing inward to domain entities.",
        "onion architecture": "Onion Architecture builds on layers with domain at center, resisting coupling to infrastructure.",
        "space-based architecture": "Space-based architecture distributes processing and data across nodes to handle high concurrency.",
        "microkernel architecture": "Microkernel has a minimal core with plug-in modules, used in IDEs like Eclipse and VS Code.",
        "event bus": "An event bus decouples publishers and subscribers, enabling asynchronous communication in systems.",
        "api composition": "API composition aggregates data from multiple services into a single response for client convenience.",

        # --- 89. DEVOPS PRACTICES ---
        "infrastructure as code tools": "Terraform, Pulumi, CloudFormation manage cloud resources through declarative configuration files.",
        "gitops principles": "GitOps uses Git as single source of truth, with operators ensuring deployed state matches repository.",
        "canary deployment": "Canary deployment gradually shifts traffic to new version, monitoring for errors before full rollout.",
        "feature toggle tools": "LaunchDarkly, Flagsmith enable runtime feature control without deployment, enabling dark launches and A/B tests.",
        "chaos engineering tools": "Gremlin, LitmusChaos inject failures to test system resilience and identify weaknesses.",
        "site reliability engineering": "SRE applies software engineering to operations, balancing reliability with feature velocity through SLIs and SLOs.",
        "error budgets": "Error budget is the acceptable downtime derived from SLO (e.g., 99.9% = 8.76 hours/year allowed downtime).",
        "blameless postmortems": "Blameless postmortems analyze incidents focusing on systemic causes, not individual blame.",
        "mean time to recovery": "MTTR measures average time to restore service after an incident, a key reliability metric.",
        "change management": "Change management controls modifications to production systems with approval, testing, and rollback plans.",

        # --- 90. COMPUTER NETWORKING AVANSAT ---
        "bgp protocol": "BGP (Border Gateway Protocol) routes traffic between autonomous systems, forming the internet backbone.",
        "ospf vs bgp": "OSPF routes within a network (interior); BGP routes between networks (exterior) on the internet.",
        "mpls": "MPLS directs data through paths via labels instead of network addresses, improving speed and traffic engineering.",
        "vpn types": "VPN types: remote access (client to network), site-to-site (network to network), SSL VPN (browser-based).",
        "proxy vs reverse proxy": "Forward proxy serves clients accessing internet; reverse proxy serves applications to clients.",
        "load balancer algorithms": "Round-robin, least connections, IP hash, and weighted distribution balance traffic across servers.",
        "anycast": "Anycast routes traffic to the nearest server sharing the same IP, improving latency and resilience.",
        "network address translation types": "NAT types: static (1:1), dynamic (pool), PAT (many:1 with ports), enabling multiple devices on one IP.",
        "ipv6 transition": "IPv6 transition uses dual-stack (both v4/v6), tunneling, and translation to coexist during migration.",
        "software defined networking": "SDN separates network control from hardware, enabling programmable, centralized network management.",

        # --- 91. BAZE DE DATE PERFORMANȚĂ ---
        "query execution plan": "EXPLAIN shows how a database executes a query, revealing table scans, index usage, and join strategies.",
        "database partitioning": "Partitioning splits large tables into smaller pieces by range, list, or hash for performance.",
        "connection pooling tools": "PgBouncer, HikariCP maintain reusable database connections, reducing overhead of establishing new ones.",
        "caching strategies database": "Read-through, write-through, write-behind caching strategies balance performance and data consistency.",
        "full text search engines": "Elasticsearch, Solr, Meilisearch provide advanced search capabilities beyond basic SQL LIKE queries.",
        "acid compliance test": "ACID transactions ensure atomicity (all or nothing), consistency, isolation, and durability in databases.",
        "database replication lag": "Replication lag is delay between primary write and replica availability, affecting read-after-write consistency.",
        "hot vs cold data": "Hot data is frequently accessed (SSD, cache); cold data is rarely accessed (HDD, archive storage).",
        "schema migration tools": "Flyway, Liquibase version-control database schemas, enabling repeatable and trackable changes.",
        "database monitoring": "Monitoring tools like Prometheus + Grafana track query performance, connections, and resource usage.",

        # --- 92. CYBERSECURITY OPERATIONS ---
        "soc": "SOC (Security Operations Center) monitors and defends against cybersecurity threats 24/7 using SIEM tools.",
        "incident response phases": "IR phases: Preparation → Identification → Containment → Eradication → Recovery → Lessons Learned.",
        "threat intelligence": "Threat intelligence collects and analyzes data about current and emerging threats for proactive defense.",
        "mitre att&ck": "MITRE ATT&CK maps adversary tactics, techniques, and procedures (TTPs) for threat modeling.",
        "security information and event management": "SIEM tools like Splunk, QRadar aggregate and correlate security events for detection.",
        "user behavior analytics": "UBA/UBA detects anomalies in user activity that may indicate compromised accounts or insider threats.",
        "endpoint protection platforms": "EPP combines antivirus, firewall, and intrusion prevention on endpoints for defense-in-depth.",
        "network traffic analysis": "NTA monitors network flows to detect suspicious patterns, C2 communication, and exfiltration.",
        "deception technology": "Honeypots and decoys create traps for attackers, detecting and analyzing intrusion techniques.",
        "purple teaming": "Purple team combines red (attack) and blue (defense) teams to improve security through collaboration.",

                # --- 93. ASISTENȚI VOCALI ȘI CHATBOTS ---
        "alexa skills": "Alexa Skills are voice-driven capabilities adding functionality to Amazon Echo devices.",
        "google assistant actions": "Google Assistant Actions extend functionality through conversational voice commands.",
        "siri shortcuts": "Siri Shortcuts automate multi-step tasks on Apple devices with custom voice commands.",
        "chatbot frameworks": "Dialogflow, Rasa, Microsoft Bot Framework build conversational AI for messaging platforms.",
        "nlp in chatbots": "NLP enables chatbots to understand intent, extract entities, and manage dialogue context.",
        "rasa vs dialogflow": "Rasa is open-source with full control; Dialogflow is Google's managed service with easy integration.",
        "voice user interface": "VUI design creates intuitive voice interactions without visual screens, focusing on conversation flow.",
        "text to speech engines": "TTS engines like Amazon Polly, Google WaveNet convert text to natural-sounding speech.",
        "speech to text engines": "STT engines like Whisper, Google Speech-to-Text convert spoken audio into written text.",
        "sentiment analysis": "Sentiment analysis detects emotions (positive, negative, neutral) in text using machine learning.",

        # --- 94. ANALIZĂ DE DATE ---
        "power bi": "Power BI is Microsoft's business analytics tool for interactive dashboards and data visualization.",
        "tableau": "Tableau is a visual analytics platform turning data into interactive, shareable dashboards.",
        "looker": "Looker is a data platform with modeling language (LookML) for defining business metrics centrally.",
        "google data studio": "Looker Studio (formerly Data Studio) creates free interactive reports from various data sources.",
        "dbt": "dbt (data build tool) transforms data in warehouses through modular SQL, version-controlled analytics code.",
        "apache spark": "Apache Spark is a distributed computing engine for big data processing, ML, and streaming analytics.",
        "apache hadoop": "Hadoop processes massive datasets across clusters using MapReduce and distributed file system (HDFS).",
        "apache kafka streams": "Kafka Streams processes data in real-time within Kafka, enabling stream processing applications.",
        "apache flink": "Flink is a stream processing framework for real-time analytics with low latency and high throughput.",
        "snowflake": "Snowflake is a cloud data platform separating storage and compute with multi-cluster scaling.",

        # --- 95. SISTEME DE CONTROL AL VERSIUNILOR ---
        "git vs svn": "Git is distributed — every user has full repository; SVN is centralized — single server stores all history.",
        "git flow vs trunk": "Git Flow uses develop/main branches with feature releases; trunk-based development uses short-lived branches.",
        "git merge vs rebase": "Merge preserves history with a merge commit; rebase creates linear history by replaying commits.",
        "git stash": "git stash temporarily saves uncommitted changes, allowing clean working directory for other tasks.",
        "git cherry pick": "git cherry-pick applies specific commits from one branch to another without merging entire branch.",
        "git revert vs reset": "Revert creates a new commit undoing changes safely; reset moves branch pointer, potentially losing history.",
        "git tag": "Git tags mark specific commits as important (releases, versions) — lightweight or annotated with metadata.",
        "git hooks": "Git hooks run scripts automatically on events (pre-commit, post-receive) for linting, testing, notifications.",
        "git submodules": "Submodules include other Git repositories inside a parent repository for dependency management.",
        "git worktree": "Git worktrees allow multiple working directories from one repository, enabling parallel work on different branches.",

        # --- 96. STANDARDE WEB ---
        "w3c": "W3C (World Wide Web Consortium) develops web standards for HTML, CSS, accessibility, and APIs.",
        "whatwg": "WHATWG maintains the HTML Living Standard, the continuously updated specification for HTML.",
        "ecmascript": "ECMAScript is the specification standardizing JavaScript, with ES6 (2015) being a major modern update.",
        "tc39": "TC39 is the committee evolving ECMAScript through proposals with stages from 0 (idea) to 4 (finished).",
        "web components": "Web Components encapsulate HTML, CSS, and JS into reusable custom elements with Shadow DOM.",
        "shadow dom": "Shadow DOM isolates component styles and markup from the main document, preventing conflicts.",
        "custom elements": "Custom Elements define new HTML tags with custom behavior and lifecycle callbacks.",
        "html templates": "HTML templates define inert markup fragments cloned and activated by JavaScript at runtime.",
        "web workers": "Web Workers run scripts in background threads, enabling parallel processing without blocking UI.",
        "service workers": "Service Workers act as proxy between browser and network, enabling offline support and push notifications.",

        # --- 97. UNELTE DE PRODUCTIVITATE ---
        "docker desktop": "Docker Desktop provides GUI and CLI for container development on Windows and macOS.",
        "postman environments": "Postman environments store variables for different setups (dev, staging, prod) in API testing.",
        "insomnia": "Insomnia is a REST and GraphQL client for API debugging and testing with environment support.",
        "ngrok": "ngrok creates secure tunnels to localhost, exposing local servers to the internet for testing.",
        "wireshark filters": "Wireshark filters (ip.addr, tcp.port, http.request) isolate specific traffic in packet analysis.",
        "fiddler": "Fiddler is a web debugging proxy capturing HTTP/HTTPS traffic between computer and internet.",
        "charles proxy": "Charles is an HTTP proxy for viewing and manipulating web traffic during development.",
        "tmux": "tmux is a terminal multiplexer enabling multiple terminal sessions, panes, and persistent remote work.",
        "oh my zsh": "Oh My Zsh enhances Zsh shell with plugins, themes, and productivity features for developers.",
        "raycast": "Raycast is a macOS launcher replacing Spotlight with extensions, scripts, and productivity tools.",

        # --- 98. MACHINE LEARNING OPERATIONS (MLOps) ---
        "mlflow": "MLflow tracks experiments, packages models, and manages the ML lifecycle from training to deployment.",
        "kubeflow": "Kubeflow runs ML workflows on Kubernetes, orchestrating training and serving of models.",
        "weights and biases": "Weights & Biases tracks experiments, visualizes metrics, and manages model artifacts.",
        "model registry": "Model registry catalogs trained models with versions, metadata, and deployment status.",
        "feature engineering automation": "Automated feature engineering creates and selects optimal features from raw data.",
        "model serving": "Model serving (TensorFlow Serving, TorchServe) deploys trained models for real-time inference.",
        "batch inference": "Batch inference processes large datasets offline through pre-trained models for bulk predictions.",
        "data versioning": "Data versioning tools like DVC track datasets alongside code, enabling reproducible ML pipelines.",
        "pipeline orchestration": "Orchestration tools (Airflow, Prefect) schedule and coordinate ML workflow dependencies.",
        "model monitoring production": "Production model monitoring tracks prediction drift, data quality, and performance degradation over time.",

        # --- 99. PROGRAMARE CONCURENTĂ ---
        "thread vs process": "Threads share memory within a process; processes have separate memory and are more isolated.",
        "race condition": "Race conditions occur when multiple threads access shared data without synchronization, causing unpredictable results.",
        "deadlock": "Deadlock happens when threads wait for each other's resources indefinitely, freezing execution.",
        "mutex vs semaphore": "Mutex allows one thread at a time; semaphore allows a set number of concurrent accesses to resources.",
        "async await python": "async/await in Python enables non-blocking concurrent code execution without explicit thread management.",
        "goroutines": "Goroutines are lightweight threads in Go, multiplexed onto OS threads for efficient concurrency.",
        "actor model": "Actor model treats actors as concurrent units communicating through messages, avoiding shared state.",
        "futures and promises": "Futures/Promises represent values that will be available later, enabling asynchronous composition.",
        "thread pool": "Thread pools reuse threads for tasks, avoiding overhead of creating threads repeatedly.",
        "concurrent vs parallel": "Concurrent tasks overlap in time; parallel tasks run simultaneously on multiple processors.",

        # --- 100. TEHNOLOGII EMERGENTE ȘI VIITOR ---
        "crispr technology": "CRISPR gene editing precisely modifies DNA sequences, revolutionizing medicine and biotechnology.",
        "brain computer interface current": "Current BCIs like Neuralink aim to connect brains to computers for medical and enhancement purposes.",
        "solid state batteries": "Solid-state batteries replace liquid electrolyte with solid, offering higher density and safety.",
        "hydrogen fuel cells": "Hydrogen fuel cells generate electricity from hydrogen, emitting only water as byproduct.",
        "hyperloop": "Hyperloop concept transports pods through low-pressure tubes at near-supersonic speeds.",
        "autonomous drone delivery": "Drone delivery services (Wing, Amazon Prime Air) transport packages autonomously.",
        "lab grown diamonds": "Lab-grown diamonds have identical properties to mined ones but are more sustainable and affordable.",
        "3d printing construction": "3D printing builds houses layer by layer, reducing costs and construction time significantly.",
        "digital twins in healthcare": "Digital twins of human organs enable personalized medicine and surgical planning.",
        "space manufacturing": "Manufacturing in microgravity (space) enables production of materials impossible on Earth.",

         # --- 101. SECURITATE CLOUD NATIVĂ ---
        "cloud security posture management": "CSPM continuously monitors cloud environments for misconfigurations and compliance violations.",
        "cloud workload protection platform": "CWPP protects cloud workloads (VMs, containers, serverless) from threats and vulnerabilities.",
        "cloud infrastructure entitlement management": "CIEM manages cloud permissions and identities to reduce excessive privileges and risk.",
        "cloud native application protection platform": "CNAPP unifies CSPM, CWPP, and CIEM into a single cloud security platform.",
        "service mesh security": "Service mesh security includes mTLS encryption, authorization policies, and zero-trust between microservices.",
        "container security scanning": "Container scanning checks images for known vulnerabilities in OS packages and application libraries.",
        "kubernetes security context": "Security context defines privilege and access control settings for pods and containers in Kubernetes.",
        "admission controller security": "Admission controllers intercept API requests to enforce security policies before resources are created.",
        "opa gatekeeper": "Open Policy Agent Gatekeeper enforces custom security policies on Kubernetes clusters using rego language.",
        "kyverno": "Kyverno is a Kubernetes policy engine that validates, mutates, and generates configurations using YAML policies.",
        "falco": "Falco detects abnormal behavior and security threats in Kubernetes containers and hosts at runtime.",
        "tetragon": "Tetragon provides runtime security enforcement and observability using eBPF for deep kernel monitoring.",
        "kube-bench": "Kube-bench checks Kubernetes clusters against CIS benchmarks for security best practices.",
        "kube-hunter": "Kube-hunter hunts for security weaknesses in Kubernetes clusters from a penetration tester's perspective.",
        "trivy": "Trivy scans container images, file systems, and Git repositories for vulnerabilities and misconfigurations.",
        "clair": "Clair is an open-source container vulnerability scanner that analyzes image layers for known CVEs.",
        "docker bench security": "Docker Bench Security checks Docker hosts against CIS benchmarks for configuration hardening.",
        "notary": "Notary ensures supply chain security by signing and verifying container images using TUF framework.",
        "cosign": "Cosign is a tool for signing and verifying container images in OCI registries with Sigstore.",
        "slsa": "SLSA (Supply-chain Levels for Software Artifacts) is a framework for verifying artifact integrity and provenance.",

        # --- 102. OBSERVABILITATE AVANSATĂ ---
        "opentelemetry": "OpenTelemetry provides APIs and SDKs for collecting traces, metrics, and logs from applications.",
        "jaeger": "Jaeger is a distributed tracing system for monitoring and troubleshooting microservices-based systems.",
        "zipkin": "Zipkin is a distributed tracing system that helps gather timing data for latency troubleshooting.",
        "tempo": "Grafana Tempo is a high-scale distributed tracing backend that indexes traces by ID.",
        "loki": "Grafana Loki is a horizontally scalable log aggregation system designed for cost-effectiveness.",
        "thanos": "Thanos provides global query, metrics compactions, and long-term storage for Prometheus metrics.",
        "cortex": "Cortex is a horizontally scalable Prometheus-as-a-Service solution for metrics in multi-tenant environments.",
        "mimir": "Grafana Mimir is a highly scalable, durable Prometheus backend for long-term metrics storage.",
        "victoriametrics": "VictoriaMetrics is a fast, cost-effective monitoring solution and time-series database for Prometheus metrics.",
        "signoz": "SigNoz is an open-source observability platform for logs, metrics, and traces in one unified interface.",
        "honeycomb": "Honeycomb is a cloud-based observability platform for debugging complex, distributed systems.",
        "datadog observability": "Datadog integrates metrics, traces, and logs into a single platform for full-stack observability.",
        "new relic observability": "New Relic provides full-stack observability with APM, infrastructure monitoring, and log management.",
        "dynatrace": "Dynatrace uses AI-powered observability to automatically detect performance anomalies in applications.",
        "elastic apm": "Elastic APM collects performance metrics and traces from applications and stores them in Elasticsearch.",
        "appdynamics": "AppDynamics is an application performance monitoring tool that correlates business transactions to code.",
        "instana": "Instana provides automated application monitoring with one-second granularity for microservices.",
        "lightstep": "Lightstep is a cloud-native observability platform focused on distributed tracing and service health.",
        "splunk observability": "Splunk Observability Cloud combines metrics, traces, and logs with AI-driven analytics.",
        "checkmk": "Checkmk is an open-source monitoring solution for IT infrastructure, applications, and cloud services.",

        # --- 103. GESTIONAREA IDENTITĂȚII ȘI ACCESULUI (IAM) ---
        "oauth2.0": "OAuth 2.0 is an authorization framework that allows third-party applications to access user data without passwords.",
        "oidc": "OpenID Connect (OIDC) is an identity layer on top of OAuth 2.0 for user authentication and single sign-on.",
        "saml2": "SAML 2.0 enables single sign-on between identity providers and service providers using XML assertions.",
        "ldap vs active directory": "LDAP is a protocol for accessing directory services; Active Directory is Microsoft's implementation of LDAP.",
        "federated identity": "Federated identity allows users to access multiple domains or organizations with a single credential.",
        "zero trust network access": "ZTNA replaces VPNs by providing identity-based, least-privilege access to private applications.",
        "beyondcorp": "BeyondCorp is Google's zero-trust security model that removes network perimeter trust for employees.",
        "pam": "Privileged Access Management (PAM) controls and monitors privileged accounts to prevent credential abuse.",
        "secret management": "Secret management securely stores and rotates API keys, passwords, certificates, and tokens.",
        "hashicorp vault": "Vault manages secrets, encrypts data, and provides identity-based access control for systems.",
        "aws secrets manager": "AWS Secrets Manager rotates and retrieves database credentials and API keys securely.",
        "azure key vault": "Azure Key Vault safeguards cryptographic keys, certificates, and connection strings in the cloud.",
        "gcp secret manager": "GCP Secret Manager stores API keys, passwords, and certificates with fine-grained access control.",
        "keeper security": "Keeper Security is a zero-knowledge password and secrets management platform for enterprise.",
        "bitwarden": "Bitwarden is an open-source password manager for individuals, teams, and organizations.",
        "1password": "1Password is a password manager with secret automation and enterprise SSO integrations.",
        "cyberark": "CyberArk is a privileged access security solution that protects credentials and sessions.",
        "okta": "Okta is a cloud-based identity management service for single sign-on, MFA, and lifecycle management.",
        "auth0": "Auth0 is an authentication and authorization platform for applications with customizable login flows.",
        "azure ad b2c": "Azure AD B2C provides customer identity and access management for consumer-facing applications.",

        # --- 104. DEVOPS AVANSAT ȘI SRE ---
        "error budget": "Error budget is the amount of unreliability allowed within an SLO before improvements are required.",
        "toil": "Toil is manual, repetitive, automatable work that scales linearly with service growth, to be minimized by SREs.",
        "sli vs slo vs sla": "SLI measures performance, SLO sets a target, and SLA defines consequences for missing the target.",
        "postmortem culture": "Postmortem culture involves blameless analysis of incidents to improve system resilience.",
        "chaos engineering principles": "Chaos engineering experiments proactively test system tolerance to failures in production.",
        "game days": "Game days are organized chaos experiments where teams simulate failures to practice incident response.",
        "capacity planning": "Capacity planning forecasts resource needs to ensure performance and avoid outages under load.",
        "performance testing pyramid": "The pyramid includes unit performance tests, integration tests, and end-to-end load tests.",
        "distributed tracing in production": "Distributed tracing samples requests to analyze latency and failures in production services.",
        "canary analysis": "Canary analysis automatically compares metrics of new version against baseline to decide rollback.",
        "feature flag platforms": "LaunchDarkly, Flagsmith, Split.io enable gradual rollouts and experiments without code redeploys.",
        "continuous verification": "Continuous verification monitors deployments in real-time and auto-rolls back on anomalies.",
        "deployment strategies comparison": "Rolling, blue-green, canary, and recreate strategies balance risk, speed, and complexity.",
        "kong api gateway": "Kong is a cloud-native API gateway with plugins for authentication, rate limiting, and observability.",
        "traefik": "Traefik is a modern reverse proxy and load balancer designed for microservices and Kubernetes.",
        "envoy proxy": "Envoy is a high-performance proxy for service meshes, edge gateways, and observability.",
        "haproxy": "HAProxy is a reliable, high-performance TCP/HTTP load balancer for high-traffic websites.",
        "consul": "Consul is a service mesh providing service discovery, configuration, and segmentation capabilities.",
        "nomad": "Nomad is a flexible scheduler and orchestrator for containers, VMs, and standalone applications.",
        "vault": "Vault manages secrets, encrypts data, and provides identity-based access control for systems.",

        # --- 105. ANALIZA LOGURILOR AVANSATĂ ---
        "structured logging": "Structured logging outputs logs as JSON or key-value pairs for easier parsing and querying.",
        "centralized logging": "Centralized logging aggregates logs from multiple servers into a single searchable system.",
        "log indexing": "Log indexing creates inverted indexes over log fields for fast full-text search and filtering.",
        "log parsing": "Log parsing extracts structured fields from raw log lines using rules or regular expressions.",
        "log filtering": "Log filtering discards noisy or low-value log entries before ingestion to reduce costs.",
        "log sampling": "Log sampling retains only a fraction of high-volume logs while preserving representative data.",
        "log aggregation tools": "Fluentd, Logstash, Vector collect, process, and forward logs to storage systems.",
        "fluentd": "Fluentd is a unified logging layer that collects and processes logs from various sources.",
        "fluentbit": "Fluent Bit is a lightweight log processor and forwarder for embedded and edge environments.",
        "vector logging": "Vector is a high-performance observability data router for logs, metrics, and events.",
        "logstash pipelines": "Logstash pipelines define inputs, filters, and outputs for processing log data.",
        "graylog": "Graylog is an open-source log management platform with search, alerting, and dashboards.",
        "humio": "Humio (now CrowdStrike LogScale) provides real-time streaming log analysis with live queries.",
        "mezmo": "Mezmo (formerly LogDNA) offers cloud-based log management with instant search and alerts.",
        "papertrail": "Papertrail is a cloud-hosted log management service with fast search and live tailing.",
        "sematext": "Sematext provides log management, infrastructure monitoring, and real-time alerts.",
        "logz.io": "Logz.io offers open-source observability platform with ELK, Prometheus, and Jaeger as a service.",
        "scalyr": "Scalyr (acquired by SentinelOne) provides high-speed log analysis with fast search and alerts.",
        "quickwit": "Quickwit is a cloud-native log management engine designed for distributed object storage.",
        "parca": "Parca is a continuous profiling tool for Kubernetes infrastructure powered by eBPF.",

        # --- 106. SECURITATE OFENSIVĂ (ETHICAL HACKING) ---
        "reconnaissance": "Reconnaissance is the first phase of ethical hacking, gathering information about a target system or network.",
        "footprinting": "Footprinting collects public information about a target using OSINT techniques without direct interaction.",
        "scanning": "Scanning identifies live hosts, open ports, and running services on a target network using tools like Nmap.",
        "enumeration": "Enumeration extracts detailed information about network resources, users, shares, and services from a target.",
        "vulnerability assessment": "Vulnerability assessment systematically identifies and prioritizes security weaknesses in systems.",
        "exploit development": "Exploit development involves creating code that leverages a specific vulnerability to gain unauthorized access.",
        "reverse engineering malware": "Reverse engineering malware analyzes malicious code to understand its behavior and origin.",
        "binary exploitation": "Binary exploitation uses memory corruption bugs (buffer overflow, use-after-free) to execute arbitrary code.",
        "web application pentesting": "Web app pentesting tests for OWASP Top 10 vulnerabilities like SQLi, XSS, CSRF, and broken authentication.",
        "mobile app pentesting": "Mobile app pentesting analyzes iOS and Android apps for insecure data storage, weak cryptography, and logic flaws.",
        "api pentesting": "API pentesting checks REST, GraphQL, SOAP endpoints for broken object level authorization (BOLA), rate limiting, and injection.",
        "cloud pentesting": "Cloud pentesting tests misconfigured storage buckets, IAM roles, and vulnerable serverless functions in AWS, Azure, GCP.",
        "wireless pentesting": "Wireless pentesting cracks WPA2/WPA3, Evil Twin attacks, and rogue access points to compromise Wi-Fi networks.",
        "social engineering": "Social engineering manipulates people into revealing credentials or performing actions against security policies.",
        "phishing simulation": "Phishing simulation sends realistic fake emails to train employees and measure susceptibility to phishing attacks.",
        "red team vs blue team": "Red team attacks, blue team defends, and purple team collaborates to improve overall security posture.",
        "purple teaming": "Purple teaming combines red and blue teams to maximize detection and response capabilities through collaboration.",
        "breach and attack simulation": "BAS tools continuously emulate attack techniques to validate security controls and find gaps.",
        "adversary emulation": "Adversary emulation mimics known threat actor tactics, techniques, and procedures (TTPs) to test defenses.",
        "threat modeling": "Threat modeling identifies potential threats and mitigation strategies during application design (STRIDE, DREAD, PASTA).",

        # --- 107. FORENZICĂ DIGITALĂ ---
        "disk forensics": "Disk forensics analyzes hard drives and SSDs to recover deleted files, partitions, and hidden data.",
        "memory forensics": "Memory forensics examines RAM dumps to find malware, encryption keys, and processes that don't write to disk.",
        "network forensics": "Network forensics captures and analyzes packets to reconstruct attacks and data exfiltration routes.",
        "mobile forensics": "Mobile forensics extracts data from smartphones, including call logs, messages, locations, and app artifacts.",
        "malware analysis sandbox": "Sandbox executes malware in isolated environments to observe behavior without risking real systems.",
        "volatility framework": "Volatility is an open-source memory forensics framework for analyzing RAM dumps from Windows, Linux, Mac.",
        "autopsy": "Autopsy is a digital forensics platform for hard drive investigation, file recovery, and timeline analysis.",
        "sleuth kit": "The Sleuth Kit is a collection of command-line tools for file system forensics on NTFS, FAT, EXT, and HFS.",
        "wireshark forensics": "Wireshark can reconstruct files, extract credentials, and identify malicious traffic from packet captures.",
        "tshark": "tshark is the command-line version of Wireshark for scripting packet captures and analyzing pcap files.",
        "tcpdump": "tcpdump captures raw network packets from the command line, compatible with libpcap format.",
        "foremost": "Foremost recovers files based on their headers, footers, and internal data structures from disk images.",
        "scalpel": "Scalpel is a high-performance file carving tool that extracts files without filesystem metadata.",
        "photorec": "PhotoRec recovers lost files including videos, documents, and archives from hard disks and memory cards.",
        "testdisk": "TestDisk repairs partition tables, recovers deleted partitions, and rebuilds boot sectors.",
        "forensic hashing": "Forensic hashing (MD5, SHA256) ensures evidence integrity and verifies files haven't been altered.",
        "write blocker": "Write blocker prevents accidental modification of evidence drives during forensic acquisition.",
        "efs": "Encrypting File System (EFS) is Windows feature for encrypting files with user certificates.",
        "luks": "LUKS (Linux Unified Key Setup) is disk encryption standard for Linux systems.",
        "bitlocker forensics": "BitLocker forensics requires recovery key or memory dump to decrypt and analyze encrypted Windows drives.",

        # --- 108. BLUE TEAM ȘI SECURITY OPERATIONS ---
        "security orchestration automation response": "SOAR platforms automate incident response workflows, case management, and threat intelligence.",
        "user and entity behavior analytics": "UEBA detects insider threats and compromised accounts using machine learning on behavioral patterns.",
        "endpoint detection and response": "EDR continuously monitors endpoints for suspicious activity and enables remote threat hunting.",
        "network detection and response": "NDR analyzes network traffic to detect lateral movement, C2 communication, and data exfiltration.",
        "managed detection and response": "MDR outsources 24/7 threat detection and response to a third-party security team.",
        "extended detection and response": "XDR correlates alerts across endpoints, networks, and cloud to provide unified detection.",
        "security information and event management": "SIEM aggregates logs, normalizes data, and correlates events to detect security incidents.",
        "security analytics": "Security analytics applies big data and ML to security data for advanced threat detection.",
        "threat hunting": "Threat hunting proactively searches for hidden threats that evaded automated detection tools.",
        "intrusion detection system": "IDS monitors network or system activities for malicious actions or policy violations.",
        "intrusion prevention system": "IPS detects and blocks threats in real-time by dropping malicious packets.",
        "host intrusion detection system": "HIDS monitors system logs, file integrity, and registry changes on individual hosts.",
        "network intrusion detection system": "NIDS analyzes network traffic patterns and signatures to detect attacks.",
        "snort": "Snort is an open-source NIDS with rule-based detection and packet logging capabilities.",
        "suricata": "Suricata is a high-performance NIDS/NIPS that uses multi-threading and GPU acceleration.",
        "zeek": "Zeek (formerly Bro) is a network security monitor for analyzing traffic and generating logs.",
        "osquery": "osquery exposes operating systems as high-performance relational databases for security monitoring.",
        "wazuh": "Wazuh is an open-source SIEM and XDR platform for threat detection and compliance monitoring.",
        "elastic security": "Elastic Security provides SIEM, endpoint security, and cloud monitoring on the ELK stack.",
        "splunk security": "Splunk Enterprise Security is a premium SIEM for threat detection and compliance reporting.",

        # --- 109. CLOUD NATIVE SECURITY AVANSAT ---
        "cloud security posture management": "CSPM detects misconfigurations and compliance violations across AWS, Azure, GCP.",
        "cloud workload protection platform": "CWPP protects VMs, containers, and serverless workloads from runtime threats.",
        "cloud infrastructure entitlement management": "CIEM identifies over-privileged identities and enforces least privilege.",
        "cloud native application protection platform": "CNAPP unifies CSPM, CWPP, CIEM, and container security in single platform.",
        "k8s pod security standards": "Pod Security Standards define privileged, baseline, and restricted security profiles for pods.",
        "k8s network policies": "Network policies control pod-to-pod communication using labels and selectors in Kubernetes.",
        "k8s pod security admission": "Pod Security Admission replaces PSPs and enforces pod security standards at namespace level.",
        "k8s opa gatekeeper": "Gatekeeper enforces custom policies on Kubernetes clusters using Open Policy Agent.",
        "k8s admission webhook": "Admission webhooks intercept and modify requests to the Kubernetes API server.",
        "k8s runtime security with falco": "Falco detects runtime threats like privilege escalation, shell execution, and file writes.",
        "k8s image scanning": "Image scanning in CI/CD finds vulnerabilities in container images before deployment.",
        "k8s secrets encryption": "Encrypt Kubernetes secrets at rest using KMS providers or aescbc provider.",
        "k8s audit logging": "Audit logs record all API requests to the Kubernetes control plane for compliance.",
        "k8s cis benchmarks": "CIS Kubernetes Benchmark provides security configuration recommendations for clusters.",
        "k8s pod security context": "Security context defines runAsNonRoot, readOnlyRootFilesystem, and privilege escalation for pods.",
        "k8s apparmor": "AppArmor profiles limit container capabilities and system call access at the kernel level.",
        "k8s seccomp": "Seccomp filters system calls to reduce attack surface of containers in Kubernetes.",
        "aws security hub": "AWS Security Hub aggregates security findings from GuardDuty, Inspector, and Macie.",
        "azure security center": "Azure Security Center provides unified security management and advanced threat protection.",
        "gcp security command center": "SCC helps security teams find threats and misconfigurations across GCP resources.",

        # --- 110. DEVOPS SECURITY (DEV SEC OPS) ---
        "shift left security": "Shift left security integrates security testing early in the development lifecycle.",
        "software supply chain security": "Supply chain security verifies the integrity of dependencies, build tools, and artifacts.",
        "software bill of materials": "SBOM is a formal inventory of all components and dependencies in a software product.",
        "sbom formats (spdx, cyclonedx, swid)": "SPDX, CycloneDX, and SWID are standard formats for exchanging SBOM data.",
        "dependency scanning": "Dependency scanning finds known vulnerabilities in open-source libraries used by the application.",
        "static application security testing": "SAST analyzes source code for security flaws without executing the program.",
        "dynamic application security testing": "DAST tests running applications for vulnerabilities by sending malicious payloads.",
        "interactive application security testing": "IAST combines SAST and DAST by instrumenting the runtime to detect vulnerabilities.",
        "software composition analysis": "SCA identifies open-source components and licenses, and detects known vulnerabilities.",
        "container image scanning in cicd": "Integrate image scanning in CI/CD pipelines (Trivy, Clair, Grype) before deployment.",
        "infrastructure as code scanning": "IaC scanning (Checkov, tfsec, kics) finds misconfigurations in Terraform, CloudFormation, K8s YAML.",
        "secret scanning": "Secret scanning detects API keys, passwords, tokens committed to source code repositories.",
        "git hooks for security": "Git pre-commit hooks run linters, secret scanners, and SAST before code is committed.",
        "pre-commit framework": "pre-commit is a framework for managing and maintaining multi-language pre-commit hooks.",
        "github secret scanning": "GitHub scans repositories for known secret formats and alerts when secrets are exposed.",
        "gitlab secret detection": "GitLab detects secrets in commits and prevents them from being pushed to the repository.",
        "secret detection patterns": "Patterns include AWS keys, GitHub tokens, Stripe keys, and generic high-entropy strings.",
        "secrets rotation automation": "Automate secret rotation using HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault.",
        "audit logging for infrastructure": "Log all changes to infrastructure (Terraform plan/apply) for compliance and forensics.",
        "compliance as code": "Compliance as code uses policy engines (OPA, Cloud Custodian) to enforce regulatory standards.",

        # --- 111. INFRASTRUCTURĂ CA COD (IaC) AVANSAT ---
        "terraform modules": "Terraform modules encapsulate groups of resources for reuse, standardization, and versioning.",
        "terraform state backend": "Remote state backends (S3, GCS, Azure Storage, Terraform Cloud) enable team collaboration and state locking.",
        "terraform workspaces": "Workspaces manage multiple environments (dev, staging, prod) within the same Terraform configuration.",
        "terraform variables precedence": "Variable precedence from lowest to highest: defaults, tfvars files, environment variables, command-line flags.",
        "terraform functions": "Built-in functions like concat, merge, lookup, file, yamlencode, and templatefile manipulate values dynamically.",
        "terraform data sources": "Data sources fetch information from providers (e.g., current AWS region, AMI IDs) for use in configurations.",
        "terraform provisioners": "Provisioners (file, local-exec, remote-exec) run scripts on resources after creation — use as last resort.",
        "terraform import": "`terraform import` brings existing infrastructure under Terraform management without destroying it.",
        "terraform taint and untaiunt": "`taint` forces resource recreation on next apply; `untaint` removes the tainted state.",
        "terraform refresh": "`refresh` updates state file with real-world resource attributes without modifying infrastructure.",
        "pulumi vs terraform": "Pulumi uses general-purpose languages (TypeScript, Python, Go, C#) while Terraform uses HCL.",
        "pulumi automation api": "Automation API allows programmatic orchestration of Pulumi deployments from applications.",
        "pulumi state backends": "Pulumi supports self-managed (AWS S3, Azure Storage) or managed (Pulumi Cloud) state backends.",
        "pulumi stack references": "Stack references export and import outputs between different Pulumi stacks.",
        "cdk (aws cdk)": "AWS CDK defines cloud infrastructure using familiar programming languages, synthesizing to CloudFormation.",
        "cdk constructs": "Constructs are the basic building blocks of CDK apps: L1 (low-level), L2 (curated), and L3 (patterns).",
        "cdk aspects": "Aspects apply operations (like adding tags or security checks) to all constructs in a scope.",
        "cdk pipelines": "CDK Pipelines is a CDK construct for deploying CDK apps with CI/CD (CodePipeline, GitHub Actions, GitLab).",
        "cdk assertions": "Assertions module validates synthesized CloudFormation templates in unit tests.",
        "cdk migrate": "`cdk migrate` imports existing CloudFormation stacks into CDK applications.",        

        # --- 112. AUTOMATIZARE AVANSATĂ CU ANSIBLE ---
        "ansible dynamic inventory": "Dynamic inventory scripts pull host information from cloud providers, CMDB, or databases in real-time.",
        "ansible vault encryption": "Ansible Vault encrypts sensitive variables and files using AES-256 with a single password.",
        "ansible vault id": "Vault IDs allow using different passwords for different environments or files.",
        "ansible galaxy": "Ansible Galaxy is a repository for sharing and downloading community roles and collections.",
        "ansible collections": "Collections package modules, plugins, roles, and playbooks for distributing content.",
        "ansible facts caching": "Fact caching stores gathered facts in Redis, memcached, or files to speed up subsequent playbook runs.",
        "ansible pull mode": "Ansible-pull runs playbooks on nodes periodically from a Git repository without a central control machine.",
        "ansible tower/awx": "AWX provides a web UI, REST API, and job scheduling for Ansible execution in enterprise environments.",
        "ansible callback plugins": "Callback plugins alter playbook output, send notifications, or log results to external systems.",
        "ansible filter plugins": "Filter plugins extend Jinja2 filters for custom data manipulation in templates.",
        "ansible lookup plugins": "Lookup plugins retrieve data from external sources (files, environment variables, databases) during playbook runs.",
        "ansible connection plugins": "Connection plugins define how Ansible communicates with hosts (ssh, winrm, local, docker).",
        "ansible inventory plugins": "Inventory plugins parse sources (YAML, TOML, AWS EC2, GCP) to build host inventories.",
        "ansible strategy plugins": "Strategy plugins control execution flow: linear (default), free (unordered), or custom.",
        "ansible action plugins": "Action plugins run on the control node before modules execute on target hosts.",
        "ansible cache plugins": "Cache plugins store facts and data in Redis, memcached, MongoDB, or file systems.",
        "ansible vars plugins": "Variables plugins dynamically inject variables from external sources at runtime.",
        "ansible module development": "Custom modules can be written in Python, PowerShell, or any language returning JSON.",
        "ansible module documentation": "Module documentation includes DOCUMENTATION, EXAMPLES, and RETURN sections in YAML/JSON.",
        "ansible testing with molecule": "Molecule is a testing framework for Ansible roles, supporting multiple instances and verifiers.",

        # --- 113. MONITORIZARE AVANSATĂ ȘI ALERTARE ---
        "prometheus service discovery": "Prometheus discovers scrape targets via file_sd, dns_sd, consul_sd, ec2_sd, and kubernetes_sd.",
        "prometheus relabel config": "Relabel_configs drop, add, or modify labels before and after service discovery.",
        "prometheus metric relabel": "Metric_relabel_configs modify metric names and labels before ingestion.",
        "prometheus recording rules": "Recording rules precompute frequently used or computationally expensive expressions into new metrics.",
        "prometheus alerting rules": "Alerting rules define conditions that trigger alerts to Alertmanager.",
        "prometheus blackbox exporter": "Blackbox exporter probes endpoints (HTTP, HTTPS, DNS, TCP, ICMP) for availability and performance.",
        "prometheus snmp exporter": "SNMP exporter collects metrics from network devices (routers, switches, firewalls).",
        "prometheus pushgateway": "Pushgateway collects metrics from short-lived jobs that cannot be scraped directly.",
        "prometheus query functions": "Functions include rate, irate, increase, avg_over_time, predict_linear, and histogram_quantile.",
        "prometheus binary operators": "Operators include arithmetic (+, -), comparison, logical (and, or), and vector matching.",
        "alertmanager routing tree": "Routing tree routes alerts based on labels (severity, service) to different receivers.",
        "alertmanager inhibition rules": "Inhibition rules suppress notifications for non-critical alerts when critical alert fires.",
        "alertmanager silence": "Silences temporarily mute alerts matching labels for maintenance periods.",
        "alertmanager receiver integrations": "Receivers include Slack, PagerDuty, OpsGenie, WeChat, Email, and generic webhooks.",
        "grafana annotations": "Annotations mark events (deploys, incidents, changes) directly on Grafana graphs.",
        "grafana alerting": "Grafana Alerting evaluates rules against any datasource and supports multi-dimensional alerts.",
        "grafana reporting": "Reporting generates PDF reports of dashboards for scheduled delivery via email.",
        "grafana folders and permissions": "Folders organize dashboards; permissions grant view/edit/admin access at folder or dashboard level.",
        "grafana provisioning": "Provision dashboards and datasources declaratively using YAML files for automation.",
        "grafana variables": "Template variables (query, interval, custom) make dashboards interactive and reusable.",

        # --- 114. BAZE DE DATE ȘI MESAGERIE ---
        "redis persistence": "RDB (snapshots) and AOF (append-only file) persistence methods trade off performance vs durability.",
        "redis replication": "Replica of master can be synchronous or asynchronous, providing high availability and read scalability.",
        "redis sentinel": "Sentinel provides high availability, monitoring, notifications, and automatic failover for Redis.",
        "redis cluster": "Redis Cluster shards data across 16384 hash slots, supporting horizontal scaling and partitioning.",
        "redis stream": "Streams are append-only logs that implement consumer groups for reliable message processing.",
        "redis pubsub": "Pub/Sub messaging pattern with channels, supports wildcard subscriptions but no persistence.",
        "redis lua scripting": "Lua scripts run atomically on the server, reducing network round trips and ensuring consistency.",
        "postgresql replication": "Physical (streaming) and logical (by table) replication for high availability and reporting.",
        "postgresql pgpool": "Pgpool-II provides connection pooling, load balancing, and automatic failover for PostgreSQL.",
        "postgresql partitioning": "Table partitioning by range, list, or hash improves query performance and data management.",
        "postgresql vacuum": "VACUUM reclaims storage occupied by dead rows and updates transaction ID wraparound.",
        "postgresql indexes": "Index types: B-tree, Hash, GiST, SP-GiST, GIN, BRIN — each optimized for different query patterns.",
        "postgresql jsonb": "JSONB stores JSON data in binary format, supporting indexing and efficient query operations.",
        "postgresql full text search": "Full-text search uses tsvector and tsquery with dictionaries and ranking functions.",
        "postgresql explain analyze": "EXPLAIN ANALYZE shows actual execution plan and row counts for query tuning.",
        "kafka topic compaction": "Topic compaction retains only the latest value for each key, useful for changelogs.",
        "kafka partition rebalance": "Rebalance redistributes partitions among consumer group members after membership changes.",
        "kafka idempotent producer": "Idempotent producers prevent duplicate messages by using producer ID and sequence numbers.",
        "kafka exactly once semantics": "EOS ensures messages are processed exactly once across producers, brokers, and consumers.",
        "kafka rbac authorization": "Kafka ACLs (resource-based access control) manage permissions for topics, consumer groups, and clusters.",

        # --- 115. DEZVOLTARE SOFTWARE AVANSAT ---
        "git worktree vs submodule": "Worktrees allow multiple branches checked out simultaneously; submodules link external repositories.",
        "git bisect": "Bisect performs binary search through commit history to find which commit introduced a bug.",
        "git reflog": "Reflog records all branch, HEAD, and reference updates; recovers lost commits.",
        "git filter branch": "Filter-branch rewrites history (removes files, changes emails) but can be slow on large repos.",
        "git replace": "Replace objects with alternate versions without rewriting history, useful for grafts.",
        "git notes": "Notes attach additional metadata to commits without changing commit SHA.",
        "git maintain": "Maintenance tasks (gc, prune, repack) optimize repository performance and size.",
        "pre-commit hooks types": "Hook types include pre-commit, pre-push, commit-msg, post-checkout, pre-rebase, and post-merge.",
        "semantic versioning rules": "MAJOR.MINOR.PATCH: MAJOR for breaking changes, MINOR for features, PATCH for bug fixes.",
        "conventional commits": "Conventional Commits format: type(scope): description (feat, fix, docs, style, refactor, test, chore).",
        "gitlab ci stages": "Stages define execution order (build, test, deploy) in GitLab CI pipelines.",
        "gitlab ci cache": "Cache dependencies and build artifacts across pipeline runs to speed up execution.",
        "gitlab ci artifacts": "Artifacts are files generated by jobs that are stored and passed to subsequent jobs.",
        "gitlab ci needs": "`needs` keyword defines job dependencies to speed up pipelines with DAG execution.",
        "github actions cache": "`actions/cache` restores and saves cache (dependencies, build outputs) across workflow runs.",
        "github actions matrix strategy": "Matrix strategy runs a job with multiple versions of language, OS, or environment variables.",
        "github actions reusable workflows": "Reusable workflows are called by other workflows, reducing duplication.",
        "github actions composite actions": "Composite actions combine multiple steps into a single action without container overhead.",
        "github actions self-hosted runners": "Self-hosted runners run workflows on your own infrastructure for custom hardware or security.",


        # --- 116. PERFORMANȚĂ APLICAȚII AVANSATĂ ---
        "profiling tools": "Profilers (cProfile, py-spy, perf, valgrind) measure execution time and memory usage to find bottlenecks.",
        "flame graphs": "Flame graphs visualize stack traces over time, identifying where applications spend most of their time.",
        "apdex score": "Apdex (Application Performance Index) measures user satisfaction based on response time thresholds (tolerating, satisfied, frustrated).",
        "distributed tracing standards": "W3C Trace Context, OpenTracing, OpenTelemetry standards propagate trace IDs across services.",
        "sampling strategies": "Head-based (random, probabilistic) and tail-based (latency, error) sampling balance observability cost.",
        "continuous profiling": "Continuous profiling captures application performance data in production for ongoing optimization.",
        "pyroscope": "Pyroscope is a continuous profiling platform for finding performance issues in code.",
        "parca profiling": "Parca is a continuous profiling tool for Kubernetes infrastructure powered by eBPF.",
        "serverless cold start optimization": "Reduce cold starts with provisioned concurrency, smaller deployment packages, and faster runtimes.",
        "database query tuning": "Indexing, query rewriting, denormalization, and partitioning optimize database response times.",
        "connection pooling sizing": "Pool size formula: (max connections per core) * (number of cores) to avoid connection storms.",
        "async patterns for performance": "Non-blocking I/O, event loops, coroutines, and async/await reduce thread pool usage.",
        "cpu bound vs io bound": "CPU-bound needs faster processors; IO-bound benefits from concurrency and caching.",
        "memory leak detection": "Heap profiling, GC logs, and object retention analysis identify memory leaks in applications.",
        "garbage collection tuning": "Adjust GC strategy, heap size, and thresholds to minimize pause times in managed runtimes.",
        "jvm tuning": "Tune heap sizes, garbage collectors (G1GC, ZGC), JIT compiler, and thread stacks for performance.",
        "v8 engine optimization": "Hidden classes, inline caching, and JIT compilation optimize JavaScript execution in Node.js.",
        "pypy vs cpython": "PyPy uses JIT compilation, often faster for long-running numeric workloads; CPython is default.",
        "numba": "Numba translates Python functions to machine code using LLVM for numerical performance.",
        "c profiling": "Tools like gprof, perf, Valgrind, and Intel VTune analyze C/C++ application performance.",

        # --- 117. REȚELE ȘI PROTOCOALE AVANSATE ---
        "http/2 server push": "Server push sends resources to the client before they are requested, reducing round trips.",
        "http/2 stream prioritization": "Streams have priorities and dependencies to optimize resource delivery order.",
        "http/3 quic": "QUIC replaces TCP+TLS with UDP, reducing connection establishment latency and improving loss recovery.",
        "websocket compression": "permessage-deflate compresses WebSocket messages, reducing bandwidth at cost of CPU.",
        "websocket subprotocols": "Subprotocols (like MQTT over WebSockets) negotiate application-level message formats.",
        "grpc status codes": "gRPC uses standard codes (OK, CANCELLED, UNKNOWN, INVALID_ARGUMENT, DEADLINE_EXCEEDED, NOT_FOUND, etc.)",
        "grpc compression": "gRPC supports gzip, snappy, and zstd compression for request and response messages.",
        "grpc load balancing": "Client-side (pick_first, round_robin) and proxy-side (envoy, nginx) load balancing strategies.",
        "protocol buffers encoding": "Varint, zigzag, length-delimited, and bit-packed encoding formats for protocol buffers.",
        "protocol buffers oneof": "Oneof fields allow at most one member to be set, saving memory and simplifying messages.",
        "protocol buffers maps": "Map fields are key-value pairs optimized for iteration order and serialization.",
        "mqtt qos levels": "QoS 0 (at most once), QoS 1 (at least once), QoS 2 (exactly once) guarantee message delivery.",
        "mqtt retained messages": "Retained messages are stored by the broker and sent to new subscribers immediately.",
        "mqtt last will testament": "LWT message is sent by the broker when a client disconnects unexpectedly.",
        "coap observe": "CoAP Observe allows clients to register for resource changes, similar to MQTT subscriptions.",
        "coap blockwise transfer": "Blockwise transfer splits large payloads into multiple CoAP messages for constrained networks.",
        "dns over tls": "DoT encrypts DNS queries over TLS on port 853 for privacy and integrity.",
        "dns over https": "DoH encrypts DNS queries inside HTTP POST requests over HTTPS on port 443.",
        "dnssec": "DNSSEC adds cryptographic signatures to DNS records to prevent spoofing and cache poisoning.",
        "mpls l3vpn": "Layer 3 VPN using MPLS labels routes customer traffic across provider networks.",

        # --- 118. ARHITECTURI SOFTWARE ȘI DESIGN PATTERNS AVANSAT ---
        "eventual consistency patterns": "Patterns include conflict-free replicated data types (CRDTs), gossip protocols, and idempotent operations.",
        "strong consistency patterns": "Two-phase commit (2PC), Paxos, Raft, and read-after-write achieve strong consistency.",
        "circuit breaker states": "Closed (normal), Open (failing), Half-Open (probing recovery) states in circuit breaker pattern.",
        "retry patterns": "Exponential backoff, jitter, and retry budget prevent cascading failures during retries.",
        "bulkhead isolation strategies": "Thread pools, connection limits, and semaphores isolate resources per tenant or service.",
        "compensating transactions": "Compensating actions revert failed operations in distributed sagas without distributed ACID.",
        "cqs vs cqrs": "CQS separates commands (writes) from queries (reads) at method level; CQRS at architecture level.",
        "event sourcing with snapshots": "Snapshots capture aggregate state periodically to reduce event replay time.",
        "outbox pattern": "Outbox pattern ensures database updates and message publishing occur atomically.",
        "inbox pattern": "Inbox pattern deduplicates messages to handle idempotent processing in distributed systems.",
        "polling publisher": "Polling publisher periodically queries a database or API to detect new events.",
        "change data capture": "CDC captures database changes (INSERT, UPDATE, DELETE) and streams them to downstream systems.",
        "leader election algorithms": "Bully algorithm, Ring algorithm, ZooKeeper, etcd, and Raft elect cluster leaders.",
        "lease mechanism": "Lease grants exclusive access for a time window, with renewal to handle failures.",
        "distributed scheduler patterns": "FIFO, fair, priority, capacity, and gang schedulers allocate resources across nodes.",
        "sharding key selection": "Partition keys influence data distribution, cross-shard queries, and hotspot avoidance.",
        "consistent hashing": "Consistent hashing minimizes key redistribution when adding/removing nodes in distributed caches.",
        "bloom filters in distributed systems": "Bloom filters reduce disk reads for missing keys in key-value stores.",
        "merkle trees": "Merkle trees efficiently compare data replicas for consistency in distributed databases.",
        "gossip membership protocols": "SWIM and Lifeguard protocols disseminate membership changes with low overhead.",

        # --- 119. CLOUD NATIVE ȘI SERVERLESS AVANSAT ---
        "serverless cold start mitigation": "Provisioned concurrency, keep-warm plugins, and smaller function sizes reduce cold starts.",
        "serverless timeout strategies": "Break long-running tasks into steps, use async workflows, or orchestrate with Step Functions.",
        "serverless vpc connectivity": "VPC connector or NAT gateway enables functions to access private resources.",
        "serverless environment variables encryption": "Encrypt sensitive environment variables with KMS for functions.",
        "serverless secret rotation": "Automate rotation of secrets used by serverless functions with Secrets Manager.",
        "serverless log sampling": "Sample logs from serverless functions to reduce storage and observability costs.",
        "serverless function chaining": "Orchestrate functions using queues, event bridge, or Step Functions to form workflows.",
        "lambda layers": "Layers package common dependencies (libraries, runtimes) for reuse across multiple functions.",
        "lambda container images": "Package and deploy Lambda functions as container images up to 10GB.",
        "lambda snapstart": "SnapStart reduces cold start latency for Java functions by restoring from snapshots.",
        "lambda response streaming": "Stream responses chunk by chunk to clients, reducing time to first byte (TTFB).",
        "lambda extensions": "Extensions run alongside functions to integrate monitoring, security, and observability tools.",
        "fargate spot": "Fargate Spot offers up to 70% discount for interruption-tolerant ECS/EKS tasks.",
        "eks fargate profiles": "Fargate profiles select which EKS pods run on serverless compute capacity.",
        "gcp cloud run cpu boost": "Cloud Run allows CPU boost during cold starts to improve startup time.",
        "azure container apps revisions": "Revisions manage version history and traffic splitting for container apps.",
        "knative serving": "Knative provides Kubernetes-based serverless platform with automatic scaling and revision management.",
        "openfaas": "OpenFaaS is a serverless framework for Kubernetes with container-native workflows.",
        "fission": "Fission is a fast serverless framework for Kubernetes with short cold start times.",
        "fn project": "Fn Project is an event-driven, container-native serverless platform.",

        # --- 120. BUG BOUNTY ȘI SECURITATE OFENSIVĂ (AVANSAT) ---
        "bug bounty disclosure policy": "Safe Harbor policy protects researchers from legal action when following program rules.",
        "bug bounty triage": "Triage validates, reproduces, and prioritizes bug reports before developer assignment.",
        "bug bounty reward structure": "Rewards based on severity (P1-P5), impact, exploit complexity, and asset criticality.",
        "responsible disclosure process": "Standard 90-day disclosure timeline before public release of vulnerability details.",
        "vulnerability severity ratings": "CVSS v3 metrics (attack vector, complexity, privileges, user interaction, scope, impact).",
        "zero-day exploit pricing": "Zero-day exploits market ranges from $50,000 (web) to $2.5M+ (mobile/OS) for exclusive rights.",
        "ghidra": "Ghidra is NSA's reverse engineering framework for analyzing malware and binaries.",
        "idapro": "IDA Pro is a commercial disassembler and debugger for binary analysis.",
        "binary ninja": "Binary Ninja is an intermediate-level reverse engineering platform with intuitive UI.",
        "radare2": "Radare2 is an open-source reverse engineering framework with scripting capabilities.",
        "x64dbg": "x64dbg is an open-source x64/x32 debugger for Windows with plugin support.",
        "gdb peda": "PEDA (Python Exploit Development Assistance) enhances GDB for exploit development.",
        "pwntools": "pwntools is a CTF framework and exploit development library for Python.",
        "ropper": "Ropper searches for ROP gadgets and assembly instructions in binaries.",
        "qemu user mode emulation": "QEMU user mode emulation runs foreign architecture binaries on host for debugging.",
        "frida instrumentation": "Frida dynamically instruments running processes for analysis and bypassing security.",
        "burp suite extension development": "Burp extensions (Python, Java, Ruby) automate custom attack scanning and testing.",
        "zap scripting": "ZAP scripts (Groovy, JavaScript, Python) automate security testing flows.",
        "intercepting proxies": "Tools like mitmproxy, Charles Proxy, and Fiddler intercept and modify HTTP/HTTPS traffic.",
        "web cache deception": "Cache deception exploits misconfigured caches to expose sensitive user data.",
    }
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


# -----------------------------
# GESTIUNEA SESIUNII
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
# AUTENTIFICARE
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


# -----------------------------
# INTERFAȚA PRINCIPALĂ
# -----------------------------
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
