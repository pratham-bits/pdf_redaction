import spacy
import fitz  # PyMuPDF
import re
import json
import logging
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import pytesseract
from typing import List, Tuple
import os
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# Ensure necessary SpaCy models are downloaded
models = ["en_core_web_lg", "xx_ent_wiki_sm"]
for model in models:
    try:
        subprocess.run(["python", "-m", "spacy", "download", model], check=True)
        logging.info(f"SpaCy model '{model}' downloaded successfully.")
    except subprocess.CalledProcessError:
        logging.error(f"Failed to download SpaCy model: {model}")

# Load SpaCy models
try:
    nlp_en = spacy.load("en_core_web_lg")
    nlp_hi = spacy.load("xx_ent_wiki_sm")
except Exception as e:
    logging.error(f"Failed to load SpaCy models: {e}")
    exit(1)

# Custom regex-based redaction rules
custom_rules = [
    {"rule_id": "phone_redact", "pattern": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b",
     "replacement": "[PHONE]"},
    {"rule_id": "email_redact", "pattern": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,20}\b",
     "replacement": "[EMAIL]"},
    {"rule_id": "gov_id_redact", "pattern": r"\b[A-Z]{5}\d{4}[A-Z]{1}\b|\b\d{9,12}\b", "replacement": "[GOV_ID]"},
    {"rule_id": "date_extended", "pattern": r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b",
     "replacement": "[DATE]"}
]


# Function to apply redaction rules
def apply_redaction(text: str, rules) -> str:
    for rule in rules:
        text = re.sub(rule["pattern"], rule["replacement"], text)
    return text


# Detect PII entities
def detect_pii(text: str) -> List[Tuple[str, int, int, str]]:
    pii_entities = []

    for nlp_model, lang in [(nlp_en, "English"), (nlp_hi, "Hindi")]:
        doc = nlp_model(text)
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "GPE", "ORG", "DATE", "CARDINAL"]:
                pii_entities.append((ent.text, ent.start_char, ent.end_char, ent.label_))

    for rule in custom_rules:
        pattern = re.compile(rule["pattern"])
        for match in pattern.finditer(text):
            pii_entities.append((match.group(), match.start(), match.end(), rule["rule_id"]))

    return sorted(pii_entities, key=lambda x: x[1])


# PDF redaction function
def redact_pdf(input_pdf: str, output_pdf: str, redaction_color=(0, 0, 0)) -> bool:
    try:
        doc = fitz.open(input_pdf)

        for page_num, page in enumerate(doc):
            text = page.get_text("text")

            if not text:
                logging.warning(f"No text found on page {page_num + 1}. Skipping.")
                continue

            pii_entities = detect_pii(text)

            for entity_text, _, _, label in pii_entities:
                areas = page.search_for(entity_text)

                for area in areas:
                    page.draw_rect(area, color=redaction_color, fill=redaction_color)

            page.clean_contents()

        doc.save(output_pdf)
        logging.info(f"Redacted PDF saved to {output_pdf}")
        return True

    except Exception as e:
        logging.error(f"Error during PDF redaction: {str(e)}")
        return False


# OCR extraction with image preprocessing
def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    full_text = ""

    for page_number, image in enumerate(pages):
        image = ImageEnhance.Contrast(image).enhance(2)
        text = pytesseract.image_to_string(image)
        full_text += f"\n--- Page {page_number + 1} ---\n{text}"

    return full_text


# Main execution
if __name__ == "__main__":
    input_pdf = "input.pdf"
    output_pdf = "redacted_output.pdf"

    if not os.path.exists(input_pdf):
        logging.error(f"Input PDF '{input_pdf}' not found.")
    else:
        if redact_pdf(input_pdf, output_pdf):
            logging.info("Redaction completed successfully.")
        else:
            logging.error("Redaction failed.")