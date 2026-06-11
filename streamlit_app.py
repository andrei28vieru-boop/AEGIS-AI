import streamlit as st
import random, string, hashlib, re
from deep_translator import GoogleTranslator
from googlesearch import search

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

# ---------- BAZA DE CUNOȘTINȚE HYBRID ----------
if "knowledge" not in st.session_state:
    st.session_state.knowledge = {
        
        # ============================================
        # 💎 AEGIS LEVEL — Interactive Mentor (20 terms)
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
        
        # ============================================
        # 💎 AEGIS LEVEL — Interactive Mentor (continued)
        # ============================================

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

        "git": {
            "beginner": "Git e ca un jurnal al codului tău. De fiecare dată când faci o schimbare, Git o salvează. Dacă strici ceva, poți să te întorci la o versiune anterioară. E ca un 'undo' infinit!",
            "professional": "Git este un sistem de versionare distribuit care urmărește modificările în codul sursă. Concepte: commit, branch, merge, rebase, pull request. Platforme: GitHub, GitLab, Bitbucket.",
            "expert": "Git flow avansat: GitFlow, trunk-based development, semantic versioning, conventional commits. CI/CD integrat prin GitHub Actions/GitLab CI.",
            "code": "# Comenzi Git\ngit init\ngit add .\ngit commit -m 'mesaj'\ngit push origin main\ngit pull\ngit branch nou\ngit checkout nou\ngit merge nou",
            "real_world": "AEGIS e pe GitHub chiar acum! Toate companiile mari — Google, Microsoft, Facebook — folosesc Git pentru codul lor.",
            "quiz": {"question": "Ce comandă Git salvează schimbările local?", "options": ["git push", "git commit", "git pull", "git merge"], "answer": "git commit"},
            "related": ["github", "github actions", "gitlab", "devops", "ci/cd"]
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
    }

# ---------- GESTIUNEA SESIUNII ----------
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_db" not in st.session_state: st.session_state.user_db = {}
if "messages" not in st.session_state: st.session_state.messages = []
if "chat_history" not in st.session_state: st.session_state.chat_history = {}
if "user_level" not in st.session_state: st.session_state.user_level = "beginner"

def hash_data(data): return hashlib.sha256(data.encode()).hexdigest()

def kosandra_blade(query, num_results=1):
    try:
        results = list(search(query, num_results=num_results, lang="en"))
        return results[0] if results else None
    except:
        return None

# ---------- AUTENTIFICARE ----------
if not st.session_state.logged_in:
    auth_choice_label = translate_text("Autentificare sau Înregistrare", lang_map[st.session_state.lang])
    st.subheader(auth_choice_label)
    auth_option_1 = translate_text("Autentificare", lang_map[st.session_state.lang])
    auth_option_2 = translate_text("Creează Cont Nou", lang_map[st.session_state.lang])
    auth_choice = st.radio(translate_text("Alege o opțiune:", lang_map[st.session_state.lang]), [auth_option_1, auth_option_2])
    
    if auth_choice == auth_option_1:
        user = st.text_input(translate_text("👤 Utilizator", lang_map[st.session_state.lang]))
        pin = st.text_input(translate_text("🔑 Parolă", lang_map[st.session_state.lang]), type="password")
        if st.button(translate_text("Autentificare", lang_map[st.session_state.lang])):
            if user in st.session_state.user_db and st.session_state.user_db[user] == hash_data(pin):
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.messages = st.session_state.chat_history.get(user, [])
                st.success(translate_text(f"Bun venit, {user}!", lang_map[st.session_state.lang]))
                st.rerun()
            else: st.error(translate_text("Autentificare eșuată.", lang_map[st.session_state.lang]))
    else:
        new_user = st.text_input(translate_text("👤 Alege un nume de utilizator", lang_map[st.session_state.lang]))
        new_pin = st.text_input(translate_text("🔑 Alege o parolă", lang_map[st.session_state.lang]), type="password")
        if st.button(translate_text("Creează Cont", lang_map[st.session_state.lang])):
            if new_user in st.session_state.user_db: st.error(translate_text("Utilizator existent.", lang_map[st.session_state.lang]))
            elif len(new_pin) < 4: st.error(translate_text("Parola minim 4 caractere.", lang_map[st.session_state.lang]))
            else:
                st.session_state.user_db[new_user] = hash_data(new_pin)
                st.success(translate_text("Cont creat!", lang_map[st.session_state.lang]))

# ---------- INTERFAȚA PRINCIPALĂ ----------
else:
    level_map = {"beginner": "🟢 Începător", "professional": "🟡 Profesionist", "expert": "🔴 Expert"}
    st.session_state.user_level = st.selectbox("📊 Nivelul tău:", ["beginner", "professional", "expert"], format_func=lambda x: level_map[x])
    
    st.success(translate_text(f"Salut, {st.session_state.user}!", lang_map[st.session_state.lang]))
    if st.button(translate_text("➕ Chat Nou", lang_map[st.session_state.lang])): st.session_state.messages = []; st.rerun()
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    
    if prompt := st.chat_input(translate_text("Scrie un mesaj...", lang_map[st.session_state.lang])):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
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
                            if "code" in term_data: parts.append(f"\n**💻 Cod:**\n```python\n{term_data['code']}\n```")
                            if "real_world" in term_data: parts.append(f"\n**🌍 În viața reală:**\n{term_data['real_world']}")
                            if "quiz" in term_data:
                                q = term_data['quiz']
                                parts.append(f"\n**🧠 Quiz:**\n{q['question']}")
                                for opt in q['options']: parts.append(f"  {'✅' if opt == q['answer'] else '⬜'} {opt}")
                            if "related" in term_data: parts.append(f"\n**🔗 Vezi și:** {', '.join(term_data['related'])}")
                            response_ro = "\n".join(parts)
                        else:
                            response_ro = term_data
                        
                        found = True
                        break
                
                if not found:
                    web_result = kosandra_blade(prompt_ro)
                    response_ro = f"Am căutat în universul digital și am găsit: {web_result}" if web_result else translate_text("Nu am această informație încă.", lang_map[st.session_state.lang])
                
                final_response = translate_text(response_ro, lang_map[st.session_state.lang])
                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
        
        st.session_state.chat_history[st.session_state.user] = st.session_state.messages
