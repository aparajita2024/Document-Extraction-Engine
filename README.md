# ✨ Aurum Extract
## Intelligent Document Extraction Engine

| Category | Details |
|---|---|
| Project Name | Aurum Extract |
| Project Type | AI-Powered Document Extraction Engine |
| Objective | Convert unstructured documents into structured JSON |
| Backend | FastAPI |
| Frontend | Streamlit |
| AI Model | Gemini 2.5 Flash |
| Database | SQLite |
| Supported Files | PDF, DOCX, TXT, PNG, JPG |

---

# 🎥 Project Demo

| Demo | Link |
|---|---|
| Assessment Demo | https://drive.google.com/file/d/1Z9XjeWCDnVi8Vu5X6KBt2IuTTrC6LTRC/view?usp=sharing

---

# 📌 Project Overview

| Topic | Description |
|---|---|
| Purpose | Automate document data extraction |
| Main Function | Extract structured information from documents |
| Processing Method | OCR + Prompt Engineering + Validation |
| Output Format | Structured JSON |
| Target Documents | Invoices, Resumes, Contracts, Reports |

---

# 🚀 Key Features

| Feature | Description |
|---|---|
| 📄 Multi-Format Support | Supports PDF, DOCX, TXT, PNG, JPG |
| 🤖 AI Extraction | AI-powered structured extraction |
| ✅ Validation | Pydantic schema validation |
| 📊 Confidence Scoring | High / Medium / Low confidence |
| 🗄️ Database Storage | Stores results in SQLite |
| 📁 Export Support | CSV & Excel export |
| ⚡ Batch Processing | Multiple file uploads supported |
| 🔄 Correction System | Inline correction support |

---

# 🧠 Supported Document Types

| Document Type | Extracted Fields |
|---|---|
| 🧾 Invoice | Vendor, total, tax, invoice number |
| 👤 Resume | Skills, education, experience |
| 📋 Contract | Parties, terms, clauses |
| 📊 Report | Findings, recommendations, summary |

---

# ⚙️ Tech Stack

## 🔹 Backend

| Technology | Purpose |
|---|---|
| FastAPI | API development |
| Python | Core programming |
| Pydantic | Schema validation |

---

## 🔹 Frontend

| Technology | Purpose |
|---|---|
| Streamlit | User interface |

---

## 🔹 AI & OCR

| Technology | Purpose |
|---|---|
| Gemini 2.5 Flash | AI extraction |
| pdfplumber | PDF extraction |
| pytesseract | OCR processing |
| python-docx | DOCX reading |

---

## 🔹 Database

| Technology | Purpose |
|---|---|
| SQLite | Data storage |

---

# 🏗️ System Workflow

| Step | Process |
|---|---|
| 1️⃣ Upload | User uploads document |
| 2️⃣ Extraction | OCR/Text extraction performed |
| 3️⃣ Prompt Injection | Text inserted into prompt template |
| 4️⃣ AI Processing | Gemini generates structured output |
| 5️⃣ JSON Cleaning | Regex cleanup + parsing |
| 6️⃣ Validation | Pydantic schema validation |
| 7️⃣ Storage | Output stored in SQLite |

---

# 📂 Supported File Formats

| File Type | Supported |
|---|---|
| PDF | ✅ |
| DOCX | ✅ |
| TXT | ✅ |
| PNG/JPG | ✅ |

---

# 📊 Confidence Scoring

| Confidence | Meaning |
|---|---|
| 🟢 High | Reliable extraction |
| 🟡 Medium | Moderate certainty |
| ⚪ Low | Ambiguous extraction |

---

# 🔐 Validation & Error Handling

| Error Type | HTTP Code | Description |
|---|---|
| Unsupported file | 415 | Invalid file type |
| Invalid JSON | 422 | Parsing failure |
| Schema mismatch | 422 | Validation failed |
| API failure | 502 | Gemini API issue |
| Empty scanned PDF | 422 | No readable text |

---

# 📁 Project Structure

```text
Aurum-Extract/
│
├── backend/
│   ├── main.py
│   ├── extractor.py
│   ├── schemas.py
│   └── database.py
│
├── frontend/
│   └── app.py
│
├── uploads/
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🛠️ Installation Guide

| Step | Command |
|---|---|
| Clone Repository | `git clone https://github.com/aparajita2024/Document-Extraction-Engine.git` |
| Create venv | `python -m venv venv` |
| Activate venv | `venv\\Scripts\\activate` |
| Install Dependencies | `pip install -r requirements.txt` |
| Run Backend | `uvicorn main:app --reload` |
| Run Frontend | `streamlit run app.py` |


# 📚 Learning Outcomes

| Skill Learned | Description |
|---|---|
| FastAPI | Backend API development |
| OCR Integration | Text extraction techniques |
| Prompt Engineering | Structured AI prompting |
| Pydantic | Schema validation |
| Streamlit | Frontend development |
| Git & GitHub | Version control |

---

# 🏁 Conclusion

| Topic | Summary |
|---|---|
| Project Goal | Automate document extraction |
| Core Strength | AI + OCR + Validation |
| Result | Clean structured JSON output |
| Real-World Use | Business document automation |

---

# 👩‍💻 Author

| Name | Aparajita Sah |
|---|---|
| Department | Artificial Intelligence & Data Science |
| GitHub | https://github.com/aparajita2024 |

---
