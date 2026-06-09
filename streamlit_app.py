import streamlit as st
import random, string, hashlib
from deep_translator import GoogleTranslator
from googlesearch import search

st.set_page_config(page_title="AEGIS AI - The IT Expert", page_icon="⚡")
st.title("AEGIS AI")
st.caption("The IT Expert - Your Personal Guide to Technology")

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

# ---------- INTERFAȚA DE LIMBĂ ----------
if not st.session_state.get("logged_in", False):
    selected_lang = st.selectbox("🌐 Choose your language / Alege limba", list(lang_map.keys()))
    st.session_state.lang = selected_lang

# ---------- DESPRE AEGIS (TRADUS) ----------
about_text_ro = """
**Despre AEGIS**
AEGIS a fost creat de un tânăr programator român, Andrei Vieru, cu pasiunea de a construi un scut digital pentru lumea modernă.
Este un expert AI dedicat exclusiv domeniilor IT și Inteligență Artificială.
**📞 Contact:** Pentru colaborări, scrie-ne pe WhatsApp (doar mesaje): **0722 911 793**
"""
st.markdown(translate_text(about_text_ro, lang_map[st.session_state.lang]))

# ---------- BAZA DE CUNOȘTINȚE (EXPERTUL TECH) ----------
if "knowledge" not in st.session_state:
    st.session_state.knowledge = {
        # --- Cunoștințe Existente ---
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
        
        # --- 1. SECURITATE CIBERNETICĂ ---
        "firewall": "Un firewall este un sistem de securitate care monitorizează și controlează traficul de rețea, permițând sau blocând accesul.",
        "vpn": "Un VPN (Virtual Private Network) creează o conexiune criptată și sigură între dispozitivul tău și internet.",
        "ransomware": "Ransomware este un tip de malware care criptează fișierele victimei și cere o răscumpărare pentru a le debloca.",
        "phishing": "Phishing-ul este o tentativă de fraudă prin care atacatorii se dau drept entități de încredere pentru a fura date personale.",
        "criptografie": "Criptografia este știința de a proteja informația prin transformarea ei într-un format care nu poate fi citit fără o cheie.",
        "hash": "Un hash este o amprentă digitală unică a unui set de date, obținută printr-o funcție matematică ireversibilă.",
        "parolă": "O parolă este o cheie secretă, formată dintr-un șir de caractere, folosită pentru autentificare și protecția conturilor.",
        "malware": "Malware (software malițios) este orice program creat pentru a dăuna unui sistem, a fura date sau a prelua controlul.",
        "antivirus": "Un antivirus este un program care detectează, blochează și elimină malware-ul de pe un dispozitiv.",
        "ddos": "Un atac DDoS (Distributed Denial of Service) încearcă să supraaglomereze un server cu trafic masiv pentru a-l face inaccesibil.",
        
        # --- 2. CLOUD COMPUTING ---
        "cloud": "Cloud computing-ul este livrarea de servicii de calcul (servere, stocare, baze de date) prin internet.",
        "aws": "AWS (Amazon Web Services) este cea mai mare platformă de cloud computing din lume, oferind peste 200 de servicii.",
        "azure": "Microsoft Azure este platforma de cloud computing a Microsoft, folosită pentru crearea, testarea și gestionarea aplicațiilor.",
        "google cloud": "Google Cloud Platform (GCP) este suita de servicii cloud oferită de Google.",
        "saas": "SaaS (Software as a Service) este un model de livrare software unde utilizatorii accesează aplicația prin internet, fără a o instala.",
        
        # --- 3. REȚELISTICĂ (NETWORKING) ---
        "ip": "O adresă IP este o etichetă numerică unică atribuită fiecărui dispozitiv conectat la o rețea.",
        "dns": "DNS (Domain Name System) este sistemul care traduce numele de domenii (ex: google.com) în adrese IP.",
        "tcp": "TCP (Transmission Control Protocol) este un protocol de comunicare sigur, care garantează livrarea pachetelor de date.",
        "http": "HTTP (HyperText Transfer Protocol) este protocolul folosit pentru a transfera pagini web între un server și un browser.",
        "router": "Un router este un dispozitiv care direcționează traficul de date între diferite rețele.",
        
        # --- 4. PROGRAMARE (Limbaje & Unelte) ---
        "javascript": "JavaScript is the programming language of the web. It makes websites interactive and works directly in your browser.",
        "java": "Java is a powerful, general-purpose programming language used for building Android apps, enterprise software, and large systems.",
        "c++": "C++ is a high-performance programming language used for game development, operating systems, and applications requiring speed.",
        "algoritm": "An algorithm is a step-by-step set of instructions to solve a specific problem, like a recipe for a computer.",
        "structură de date": "A data structure is a way of organizing and storing data so it can be accessed and modified efficiently, like lists or dictionaries.",
        "debugging": "Debugging is the process of finding and fixing errors (bugs) in your code.",
        "ide": "An IDE (Integrated Development Environment) is a software application that helps you write code, like PyCharm or VS Code.",
        "compilator": "A compiler is a program that translates your code into machine language that a computer can understand and run.",
        
        # --- 5. SISTEME DE OPERARE ---
        "linux": "Linux is a free, open-source operating system known for its stability and security. It's widely used on servers and by developers.",
        "windows": "Microsoft Windows is the most popular operating system for personal computers, known for its user-friendly interface.",
        "macos": "macOS is the operating system developed by Apple for its Mac computers, known for its elegant design and smooth performance.",
        "terminal": "The terminal is a text-based interface where you can type commands to interact with your computer directly.",
        "bash": "Bash is a popular command-line shell on Linux and macOS that lets you run commands and write scripts.",
        "powershell": "PowerShell is a powerful command-line tool from Microsoft for automating tasks on Windows.",
        "kernel": "The kernel is the heart of an operating system. It manages everything from your hardware to your software.",
        "driver": "A driver is a small piece of software that allows your operating system to talk to a piece of hardware, like a printer.",
        
        # --- 6. ISTORIE ȘI CURIOSITĂȚI TECH ---
        "guido van rossum": "Guido van Rossum is the Dutch programmer who created the Python programming language in the late 1980s.",
        "silicon valley": "Silicon Valley is a region in California, USA, that is famous for being the global center for technology and innovation.",
        "istoria internetului": "The internet began in the late 1960s as a US military project called ARPANET and became public in the 1990s.",
        "alan turing": "Alan Turing was a brilliant British mathematician who is considered the father of computer science and artificial intelligence.",
        
        # --- 7. PROGRAMARE AVANSATĂ ȘI FRAMEWORKS ---
        "react": "React is a popular JavaScript library for building user interfaces, developed by Facebook.",
        "angular": "Angular is a TypeScript-based web application framework led by Google.",
        "vue": "Vue.js is a progressive JavaScript framework for building user interfaces.",
        "django": "Django is a high-level Python web framework that encourages rapid development.",
        "flask": "Flask is a micro web framework written in Python, known for its simplicity.",
        "sql": "SQL (Structured Query Language) is a language for managing and querying relational databases.",
        "git": "Git is a distributed version control system for tracking changes in source code.",
        "github": "GitHub is a platform for hosting and collaborating on Git repositories.",
        "oop": "OOP (Object-Oriented Programming) is a paradigm based on objects containing data and code.",
        "recursivitate": "Recursion is a technique where a function calls itself to solve a problem.",
        "api rest": "A REST API is an API that follows the principles of Representational State Transfer.",
        "json": "JSON (JavaScript Object Notation) is a lightweight data-interchange format.",
        "xml": "XML (eXtensible Markup Language) is a markup language for storing and transporting data.",
        "docker": "Docker is a platform for developing, shipping, and running applications in containers.",
        "kubernetes": "Kubernetes is an open-source system for automating deployment of containerized applications.",
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
        "r": "R is a language and environment for statistical computing and graphics.",
        "matlab": "MATLAB is a high-level language and interactive environment for numerical computation.",
        "framework": "A framework is a pre-built set of tools and libraries that provides a foundation for developing software applications.",
        "library": "A library is a collection of pre-written code that developers can use to perform common tasks.",
        "sdk": "An SDK (Software Development Kit) is a collection of tools that allows developers to create applications for a specific platform.",
        "runtime": "A runtime is the environment in which a program is executed, providing necessary services.",
        "interpreter": "An interpreter is a program that directly executes instructions written in a programming language.",
        "compiler": "A compiler translates source code into machine code before execution.",
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
        "c": "C is a powerful general-purpose programming language. It is fast, portable, and the foundation of many modern languages like Python.",
        "c#": "C# (C-Sharp) is a modern, object-oriented programming language developed by Microsoft for the .NET framework.",
        "r programming": "R is a programming language and environment specifically designed for statistical analysis and data visualization.",
        "matlab": "MATLAB is a high-level language and interactive environment used by engineers and scientists for numerical computation.",
        "perl": "Perl is a versatile scripting language known for its powerful text-processing capabilities. It was widely used for CGI scripting.",

        # --- 8. BAZE DE DATE (DATABASES) ---
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

        # --- 9. INTELIGENȚĂ ARTIFICIALĂ ȘI MACHINE LEARNING ---
        "machine learning": "Machine Learning (ML) is a subset of AI where systems learn from data without being explicitly programmed.",
        "deep learning": "Deep Learning is a subset of ML using artificial neural networks with many layers to model complex patterns.",
        "neural network": "A neural network is a computing system inspired by the human brain, composed of interconnected nodes (neurons).",
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

        # --- 10. DEZVOLTARE WEB (WEB DEVELOPMENT) ---
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

        # --- 11. SECURITATE AVANSATĂ ȘI ETHICAL HACKING ---
        "encryption": "Encryption is the process of converting data into a coded form to prevent unauthorized access.",
        "decryption": "Decryption is the process of converting encrypted data back to its original, readable form.",
        "aes": "AES (Advanced Encryption Standard) is a symmetric encryption algorithm widely used worldwide.",
        "rsa": "RSA is an asymmetric encryption algorithm used for secure data transmission and digital signatures.",
        "ssl": "SSL (Secure Sockets Layer) is a protocol for encrypting data between a web server and a browser. Now replaced by TLS.",
        "tls": "TLS (Transport Layer Security) is the successor to SSL, providing encrypted communication over the internet.",
        "https": "HTTPS is the secure version of HTTP, using TLS/SSL to encrypt data between browser and server.",
        "certificate": "An SSL/TLS certificate is a digital file that authenticates a website's identity and enables encrypted connections.",
        "ca": "A Certificate Authority (CA) is a trusted entity that issues digital certificates.",
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

        # --- 12. HARDWARE ȘI ELECTRONICĂ ---
        "cpu": "CPU (Central Processing Unit) is the primary component of a computer that executes instructions. Often called the brain of the computer.",
        "gpu": "GPU (Graphics Processing Unit) is a specialized processor designed to accelerate graphics rendering and parallel computations.",
        "ram": "RAM (Random Access Memory) is temporary memory that stores data actively being used by the computer.",
        "rom": "ROM (Read-Only Memory) is non-volatile memory that stores firmware and cannot be easily modified.",
        "ssd": "SSD (Solid State Drive) is a fast storage device using flash memory, with no moving parts.",
        "hdd": "HDD (Hard Disk Drive) is a traditional storage device that uses spinning magnetic disks.",
        "motherboard": "The motherboard is the main circuit board that connects all components of a computer.",
        "bios": "BIOS (Basic Input/Output System) is firmware that initializes hardware during the boot process. Now largely replaced by UEFI.",
        "uefi": "UEFI (Unified Extensible Firmware Interface) is the modern replacement for BIOS, with more features and security.",
        "overclocking": "Overclocking is the process of increasing a component's clock rate to run faster than factory specifications.",
        "cache": "Cache is a small, high-speed memory that stores frequently accessed data for quick retrieval.",
        "bandwidth": "Bandwidth is the maximum rate of data transfer across a network path, measured in bits per second.",
        "latency": "Latency is the time delay between a request and its response in a network.",
        "iot": "IoT (Internet of Things) refers to the network of physical objects embedded with sensors and software to connect and exchange data.",
        "arduino": "Arduino is an open-source electronics platform based on easy-to-use hardware and software.",
        "raspberry pi": "Raspberry Pi is a small, affordable single-board computer used for learning programming and building projects.",
        "firmware": "Firmware is software programmed into the read-only memory of a hardware device, providing low-level control.",
        "bios update": "A BIOS update is a process of upgrading the firmware that controls the motherboard to fix bugs or add features.",
    }

# ---------- GESTIUNEA SESIUNII ----------
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_db" not in st.session_state: st.session_state.user_db = {}
if "messages" not in st.session_state: st.session_state.messages = []
if "chat_history" not in st.session_state: st.session_state.chat_history = {}

def hash_data(data): return hashlib.sha256(data.encode()).hexdigest()

# ============================================
# 🗡️ KOSANDRA SWORD OF TRUTH
# ============================================
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
                if user in st.session_state.chat_history: st.session_state.messages = st.session_state.chat_history[user]
                else: st.session_state.messages = []
                st.success(translate_text(f"Bun venit, {user}!", lang_map[st.session_state.lang]))
                st.rerun()
            else: st.error(translate_text("Autentificare eșuată.", lang_map[st.session_state.lang]))
    else:
        new_user = st.text_input(translate_text("👤 Alege un nume de utilizator", lang_map[st.session_state.lang]))
        new_pin = st.text_input(translate_text("🔑 Alege o parolă", lang_map[st.session_state.lang]), type="password")
        if st.button(translate_text("Creează Cont", lang_map[st.session_state.lang])):
            if new_user in st.session_state.user_db: st.error(translate_text("Acest nume de utilizator există deja.", lang_map[st.session_state.lang]))
            elif len(new_pin) < 4: st.error(translate_text("Parola trebuie să aibă minim 4 caractere.", lang_map[st.session_state.lang]))
            else:
                st.session_state.user_db[new_user] = hash_data(new_pin)
                st.success(translate_text("Cont creat! Acum te poți autentifica.", lang_map[st.session_state.lang]))
                st.info(translate_text("Selectează 'Autentificare' și folosește datele tale.", lang_map[st.session_state.lang]))

# ---------- INTERFAȚA PRINCIPALĂ ----------
else:
    greet_msg = translate_text("Salut, {user}! Cu ce te pot ajuta?", lang_map[st.session_state.lang])
    new_chat_btn = translate_text("➕ Chat Nou", lang_map[st.session_state.lang])
    chat_input_msg = translate_text("Scrie un mesaj...", lang_map[st.session_state.lang])
    thinking_msg = translate_text("AEGIS se gândește...", lang_map[st.session_state.lang])
    not_found_msg = translate_text("Nu am această informație încă. Poți căuta pe Google sau Wikipedia pentru mai multe detalii.", lang_map[st.session_state.lang])

    st.success(greet_msg.format(user=st.session_state.user))
    if st.button(new_chat_btn): st.session_state.messages = []; st.rerun()
    
    for msg in st.session_state.messages:
        if msg["role"] == "user": st.chat_message("user").write(msg["content"])
        else: st.chat_message("assistant").write(msg["content"])
    
    if prompt := st.chat_input(chat_input_msg):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner(thinking_msg):
                prompt_ro = translate_text(prompt, "ro")
                found = False
                response_ro = ""
                for key in st.session_state.knowledge:
                    if key in prompt_ro.lower():
                        response_ro = st.session_state.knowledge[key]
                        found = True
                        break
                
                if not found:
                    web_result = kosandra_blade(prompt_ro)
                    if web_result: response_ro = f"Am căutat în universul digital și am găsit acest răspuns: {web_result}"
                    else: response_ro = not_found_msg
                
                final_response = translate_text(response_ro, lang_map[st.session_state.lang])
                st.write(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
        
        st.session_state.chat_history[st.session_state.user] = st.session_state.messages
