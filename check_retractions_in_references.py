# Check for retracted papers in the reference list - extracts a reference list from a PDF file and compares the DOIs of these papers with the Retraction Watch database (https://gitlab.com/crossref/retraction-watch-data/)

import re
import csv
from PyPDF2 import PdfReader

def normalize_doi(doi):
    return re.sub(r'\s+', '', doi.strip().lower()) if doi else None

def extract_doi_from_pdf(file_path):
    """Витягуємо DOIs зі списку літератури у PDF-файлі."""
    references = set()
    try:
        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text()
        
        # Виділення DOI
        doi_matches = re.findall(r'(10\.\d{4,9}/[\w.\-]+)', full_text, re.IGNORECASE)
        for doi in doi_matches:
            normalized_doi = normalize_doi(doi)
            if normalized_doi:
                references.add(normalized_doi)
    except Exception as e:
        print(f"Помилка під час читання PDF: {e}")
    return references

def load_retraction_watch(file_path):
    """Завантаження списку DOIs з бази Retraction Watch."""
    retractions = set()
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            original_doi = normalize_doi(row.get('OriginalPaperDOI', ''))
            if original_doi:
                retractions.add(original_doi)
    return retractions

def find_retractions(references, retractions):
    """Порівнюємо DOIs зі списку літератури з базою Retraction Watch."""
    return references.intersection(retractions)

def main():
    pdf_file = "paper1.pdf"  # Шлях до PDF-файлу
    retractions_file = "retraction_watch.csv"  # Шлях до файлу Retraction Watch

    # Витягування DOI зі списку літератури в PDF
    print("Витягування DOIs зі списку літератури в PDF...")
    references = extract_doi_from_pdf(pdf_file)

    # Завантаження файлу Retraction Watch
    print("Завантаження бази Retraction Watch...")
    retractions = load_retraction_watch(retractions_file)

    # Пошук ретракцій
    print("Пошук ретракцій...")
    found_retractions = find_retractions(references, retractions)

    # Результати
    if found_retractions:
        print(f"Знайдено {len(found_retractions)} ретракцій:")
        for doi in found_retractions:
            print(f"Відкликана стаття: {doi}")
    else:
        print("Ретракцій не знайдено у списку літератури.")

if __name__ == "__main__":
    main()


# In[ ]:




