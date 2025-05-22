import docx
import csv
import re

def extract_guidelines_from_docx(docx_path, csv_path):
    """
    Extracts guideline instructions from a DOCX file and saves them into a CSV file.
    
    Assumes that:
    - Chapters and sections use heading styles or numbered format (e.g., "1.", "1.1", etc.)
    - Guidelines are written as bullet points or plain paragraphs under those headings
    """

    doc = docx.Document(docx_path)
    data = []

    current_chapter = ""
    current_section = ""

    for para in doc.paragraphs:
        text = para.text.strip()
        style = para.style.name.lower()

        # Detect Chapter (Heading 1 or "1.", "2.", etc.)
        if re.match(r'^\d+\.\s', text) or 'heading 1' in style:
            current_chapter = text
            current_section = ""  # Reset section when chapter updates

        # Detect Section (Heading 2 or "1.1", "2.3", etc.)
        elif re.match(r'^\d+\.\d+\s', text) or 'heading 2' in style:
            current_section = text

        # Assume any other paragraph might be a guideline
        elif text:
            data.append({
                "Chapter": current_chapter,
                "Section": current_section,
                "Instruction": text
            })

    # Write to CSV
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Chapter", "Section", "Instruction"])
        writer.writeheader()
        writer.writerows(data)

    print(f"Extracted {len(data)} guideline instructions to {csv_path}")

# Example usage:
docx_file = "model_validation_template.docx"
csv_file = "validation_guidelines.csv"
extract_guidelines_from_docx(docx_file, csv_file)