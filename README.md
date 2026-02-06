## SecurePDF – Automated PII Redaction in PDFs
SecurePDF is an AI-powered web application that automatically detects and redacts Personally Identifiable Information (PII) from PDF documents. It ensures privacy protection by intelligently identifying sensitive information using Natural Language Processing (NLP).

-->Problem Statement
Organizations frequently share documents containing sensitive information such as:
Names
Email addresses
Phone numbers
Aadhaar / PAN numbers
Addresses
Manual redaction is:
Time-consuming
Error-prone
Risky

SecurePDF automates this process using AI to ensure fast and reliable redaction.
🧠 Features
✅ Automatic PII detection using NLP (spaCy)
✅ Redaction of detected sensitive information
✅ Upload and download PDF interface
✅ FastAPI backend for efficient API handling
✅ Clean React frontend for user interaction
✅ Secure document processing

**Tech Stack
🔹 Backend
Python
FastAPI
spaCy (NLP)
PyMuPDF (fitz)
🔹 Frontend
React.js
Axios
HTML, CSS


📂 Project Structure
SecurePDF/
│
├── backend/
│   ├── main.py
│   ├── utils.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   └── package.json
│
└── README.md

⚙️ How It Works
User uploads a PDF.
Text is extracted using PyMuPDF.
spaCy NLP model detects PII entities.
Detected entities are automatically redacted.
The redacted PDF is generated and returned to the user.
