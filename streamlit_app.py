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
