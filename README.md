# 🛡️ CyberDemandIQ

### AI-Powered Cybersecurity Detection, Risk Intelligence & Security Analytics

<p align="center">

<img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/XGBoost-ML-FF6600?logo=xgboost&logoColor=white"/>
<img src="https://img.shields.io/badge/Scikit--Learn-ML-F7931E?logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/PyTorch-DL-EE4C2C?logo=pytorch&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-Data%20Science-150458?logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/NumPy-Data%20Science-013243?logo=numpy&logoColor=white"/>

<br/>

<img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/SQL-Analytics-4479A1?logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly&logoColor=white"/>

<br/>

<img src="https://img.shields.io/badge/Matplotlib-Visualization-11557C?logo=matplotlib&logoColor=white"/>
<img src="https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git&logoColor=white"/>
<img src="https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white"/>
<img src="https://img.shields.io/badge/REST%20API-FastAPI-009688"/>
<img src="https://img.shields.io/badge/Machine%20Learning-AI-blueviolet"/>
<img src="https://img.shields.io/badge/Cybersecurity-Threat%20Intelligence-red"/>

</p>

---

<img width="1672" height="941" alt="cyderdemandiq" src="https://github.com/user-attachments/assets/ccf083c8-4b9a-49b2-bb23-019f8ed5941c" />

**CyberDemandIQ** is an end-to-end cybersecurity intelligence platform that combines **Machine Learning, network-flow analytics, PostgreSQL, FastAPI and Streamlit** to detect attacks, investigate network activity, assess security risk and visualize threat intelligence.

The platform transforms large-scale network-flow data into an interactive security analytics workflow.

---

## 🧠 Core Capabilities

- 🤖 **AI Attack Detection** — XGBoost-based network attack classification
- 🔎 **Network Investigation** — Inspect and analyze network-flow records
- 🚨 **Threat Intelligence** — Analyze observed security events
- ⚠️ **Risk Analytics** — Security exposure and risk assessment
- 📊 **Security Analytics** — Interactive traffic and threat visualization
- 🧠 **Response Intelligence** — Security-response analysis
- 📈 **Security Demand Forecasting** — LSTM, GRU and XGBoost forecasting
- 🗄️ **Database Explorer** — PostgreSQL-powered security dataset exploration
- 🧪 **Model Monitoring** — ML model and feature analysis

---

## 🤖 AI Detection Pipeline

```text
Network Flow Data
       ↓
Data Cleaning
       ↓
Feature Engineering
       ↓
Train / Test Split
       ↓
XGBoost Classifier
       ↓
Attack Probability
       ↓
BENIGN / ATTACK
       ↓
Risk Interpretation
````

### 🔬 Engineered Security Features

The model uses network-flow features including:

* Packet length statistics
* Average packet size
* Forward / backward packet statistics
* Flow duration
* Packet and byte rates
* Flow inter-arrival time
* TCP flag activity
* Active / idle statistics
* Traffic asymmetry
* Window-size features
* Packet variability

---

## 📊 Model

**Algorithm:** XGBoost Binary Classifier

```text
Estimators       : 300
Max Depth        : 8
Learning Rate    : 0.08
Subsample        : 0.85
Column Sampling  : 0.85
Objective        : binary:logistic
Random State     : 42
```

Model artifact:

```text
models/cyberdemandiq_xgboost.json
```

Feature importance:

```text
models/feature_importance.csv
```

---

## 🏗️ Architecture

```text
                 ┌──────────────────────┐
                 │   Network Flow Data  │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ Data Processing & ML │
                 └───────┬───────┬──────┘
                         ↓       ↓
                ┌──────────┐  ┌──────────┐
                │PostgreSQL│  │ XGBoost  │
                └─────┬────┘  └────┬─────┘
                      │             ↓
                      │      Attack Detection
                      │             │
                      └──────┬──────┘
                             ↓
                       ┌───────────┐
                       │  FastAPI  │
                       └─────┬─────┘
                             ↓
                      ┌─────────────┐
                      │  Streamlit  │
                      │  Dashboard  │
                      └─────────────┘
```

---

## 🗄️ Database

**PostgreSQL** is used as the primary data layer.

```text
Schema : cybersecurity
Table  : network_flows
```

The database supports:

* Network-flow storage
* Attack statistics
* Traffic investigation
* Label distribution
* Security analytics

---

## ⚡ Backend API

Built with **FastAPI**.

### Main endpoints

```text
GET /
GET /api/database-stats
GET /api/attack-statistics
GET /api/network-flows
```

---

## 📊 Dashboard

Built with **Streamlit + Plotly**.

### Modules

```text
📊 Overview
🚨 Threat Intelligence
🤖 AI Detection
🔎 Network Investigation
⚠️ Risk Analytics
📈 Security Demand
🧠 Response Intelligence
🧪 Model Monitoring
🗄️ Database Explorer
```

---

## 🛠️ Tech Stack & Skills

### 💻 Programming & Data

🐍 Python • 🗃️ SQL • 🐼 Pandas • 🔢 NumPy

### 🤖 AI / Machine Learning

🤖 Machine Learning • 🌳 XGBoost • 📚 Scikit-learn • 🔥 PyTorch
🧠 Deep Learning • 📈 LSTM • 🔄 GRU • 🔬 Feature Engineering

### 🛡️ Cybersecurity

🔐 Network Security • 🚨 Attack Detection • 🔎 Threat Intelligence
⚠️ Risk Analytics • 📡 Network Traffic Analysis • 🧠 Security Intelligence

### 🗄️ Database & Backend

🐘 PostgreSQL • ⚡ FastAPI • 🔗 REST APIs • 🐍 Psycopg2

### 📊 Visualization

📊 Streamlit • 📈 Plotly • 📉 Matplotlib • 📊 Data Visualization

### 🧰 Development

💻 VS Code • 🔀 Git • 🐙 GitHub • 🧪 Model Evaluation
🔐 Environment Variables • 📦 Virtual Environments

---

## 📁 Project Structure

```text
CyberDemandIQ/
│
├── api/
├── config/
├── dashboard/
│   └── modules/
├── models/
├── reports/
├── src/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Run Locally

### 1️⃣ Clone

```bash
git clone https://github.com/shubhechchha-23/CyberDemandIQ.git
cd CyberDemandIQ
```

### 2️⃣ Create environment

```bash
python -m venv .venv
```

### 3️⃣ Activate

**Windows:**

```bash
.venv\Scripts\activate
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Configure environment

Create `.env` from `.env.example` and add your **local PostgreSQL credentials**.

> 🔐 Never commit `.env` or real database credentials to GitHub.

### 6️⃣ Start API

```bash
uvicorn api.main:app --reload --port 8000
```

### 7️⃣ Start Dashboard

Open another terminal:

```bash
streamlit run dashboard/dashboard.py
```

---

## 🎯 Project Focus

CyberDemandIQ brings together:

```text
🧠 Artificial Intelligence
🤖 Machine Learning
📊 Data Science
🛡️ Cybersecurity
🗄️ Database Engineering
⚡ Backend Development
📈 Data Visualization
🔮 Predictive Analytics
```

into a unified cybersecurity intelligence platform.

---

## 🔮 Future Scope

* 🔄 Real-time network-flow ingestion
* 🤖 AI security agents
* 📚 RAG-based threat intelligence
* 🚨 Automated alert prioritization
* 📡 Streaming detection
* 🐳 Docker deployment
* ☁️ Cloud deployment
* 📊 Advanced ML monitoring
* 🔐 Authentication & RBAC

---

## 👩‍💻 Author

### Shubhechchha Hazra

**B.Tech | NIT Raipur**

Interested in:

🤖 AI/ML • 📊 Data Science • 🛡️ Cybersecurity • 🧠 Decision Science • ⚡ Backend Development

---

<p align="center">

### 🛡️ CyberDemandIQ

**Detect • Investigate • Analyze • Predict**

</p>
