SecurePDF – Automated PII Redaction in PDFs
SecurePDF is an AI-powered web application that automatically detects and redacts Personally Identifiable Information (PII) from PDF documents. It ensures privacy protection by leveraging Natural Language Processing (NLP) to intelligently identify sensitive information and securely remove it.

🚩 Problem Statement
Organizations often share documents containing sensitive data such as:
- Names
- Email addresses
- Phone numbers
- Aadhaar / PAN numbers
- Physical addresses
Manual redaction is:
- ⏳ Time-consuming
- ⚠️ Error-prone
- 🔒 Risky
SecurePDF automates this process, ensuring fast, reliable, and secure redaction.

🧠 Features
- ✅ Automatic PII detection using spaCy NLP
- ✅ Intelligent redaction of sensitive information
- ✅ Upload & download interface for PDFs
- ✅ FastAPI backend for efficient API handling
- ✅ Clean React.js frontend for user interaction
- ✅ Secure document processing pipeline

🛠 Tech Stack
Backend
- Python
- FastAPI
- spaCy (NLP)
- PyMuPDF (fitz)
Frontend
- React.js
- Axios
- HTML, CSS

⚙️ How It Works
- User uploads a PDF.
- Text is extracted using PyMuPDF.
- spaCy NLP model detects PII entities.
- Detected entities are automatically redacted.
- A secure, redacted PDF is generated and returned to the user.

🚀 Future Enhancements
- Support for additional file formats (Word, Excel)
- Customizable redaction rules
- Role-based access control for enterprise use
- Integration with cloud storage (Google Drive, OneDrive)
