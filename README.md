# 🌾 KrishiLekha

**KrishiLekha** is a secure, user-friendly digital record-keeping platform that transforms traditional agricultural logs into an intelligent, searchable, and interactive system. It empowers farmers and stakeholders by digitizing physical records, enabling advanced data insights, and ensuring secure access through cutting-edge AI and cloud-native infrastructure.

---

## 🚀 Problem Statement

Traditional record-keeping in agriculture is prone to errors, physical damage, and poor accessibility. **KrishiLekha** addresses these issues by:

* Digitizing handwritten or scanned agricultural documents.
* Structuring and storing data securely with encryption and RBAC.
* Enabling intelligent search using Agentic Retrieval-Augmented Generation (RAG) with vector databases and Azure OpenAI.
* Supporting multi-language interaction (Hindi and English) for accessibility.

---

## 🧠 Key Features

* **OCR-based PDF Ingestion**: Extracts handwritten or printed content from agricultural documents.
* **Vector Database Integration**: Efficient semantic search using Qdrant.
* **Secure Data Handling**: All PII is encrypted and access-controlled via RBAC.
* **Natural Language Querying**: Ask questions in plain language and receive contextual answers powered by generative AI.
* **Role-Based Access Control**: Ensures different stakeholders access only their permitted data.
* **Localized UI**: Supports Hindi and easily extendable to other regional languages.

---

## 👨‍🌾 Impact

By digitizing records and making them queryable through natural language, KrishiLekha:

* Reduces data loss and manual errors.
* Enhances decision-making with real-time insights.
* Improves access to subsidies, credit, and agricultural services.
* Accelerates digital transformation in rural and agricultural sectors.

---

## 🧑‍💻 Team

* **Sourav Sahu**
* **Laalini B**

---

## 🌐 Live Demo

**[KrishiLekha Demo](https://krishilekha.azurewebsites.net)**

---

## ⚙️ Local Setup Instructions

Follow the steps below to run KrishiLekha locally:

1. **Clone the repository**

```bash
git clone https://github.com/souravsahums/krishilekha.git
cd krishilekha
```

2. **Create a virtual environment (Python 3.11 recommended)**

```bash
# Using conda
conda create -n krishilekha python=3.11
conda activate krishilekha

# OR using venv
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root directory. Use `.env.template` as a reference. Required configurations include:

* Azure OpenAI API keys
* Qdrant connection info
* Other API credentials as needed

5. **Run the Streamlit app**

```bash
streamlit run app.py
```

---

## 📁 Tech Stack

* Python 3.11
* Streamlit (Frontend)
* Azure OpenAI (LLM APIs)
* Qdrant (Vector Store)
* LangChain & LangGraph (Agentic workflows)
* OCR tools (for PDF parsing)
* Role-Based Access Control (RBAC)
* Multilingual support
