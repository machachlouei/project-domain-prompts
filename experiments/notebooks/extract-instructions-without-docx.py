import zipfile
import xml.etree.ElementTree as ET

def extract_paragraphs_from_docx(path):
    """
    Parses the Word document (.docx) as XML and extracts paragraphs and heading levels.
    
    Returns:
        List of (text, style) tuples.
    """
    paragraphs = []
    with zipfile.ZipFile(path) as docx:
        xml_content = docx.read('word/document.xml')
        tree = ET.XML(xml_content)

        for elem in tree.iter():
            if elem.tag.endswith('}p'):
                text = ''
                style = 'Normal'
                for child in elem.iter():
                    if child.tag.endswith('}t'):
                        text += child.text or ''
                    if child.tag.endswith('}pStyle'):
                        style = child.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', 'Normal')
                if text.strip():
                    paragraphs.append((text.strip(), style))
    return paragraphs
    
def extract_headings_and_text_manual(docx_file):
    """
    Manually extracts headings and text from a .docx using zipfile + xml.
    
    Returns:
        List of [heading, paragraph_text]
    """
    paragraphs = extract_paragraphs_from_docx(docx_file)
    result, current_heading, current_text = [], None, []

    for text, style in paragraphs:
        if 'Heading' in style:
            if current_heading:
                result.append([current_heading, ' '.join(current_text)])
            current_heading = text
            current_text = []
        else:
            current_text.append(text)

    if current_heading:
        result.append([current_heading, ' '.join(current_text)])

    return result
    
    
text_data = extract_headings_and_text_manual(file_path)


df = pd.DataFrame(text_data, columns=["Heading", "Content"])

# Display first few rows
print(df.head())

# Optional: Save to Excel or CSV
df.to_csv("output_sections.csv", index=False)
# or
df.to_excel("output_sections.xlsx", index=False)


#================================

def extract_hierarchical_structure(path):
    """
    Extracts structured section and subsection data from a .docx file and returns a DataFrame.

    The function reads a Word document, identifies numbered headings (e.g., '1', '2.1'), and organizes them
    into a structured format with associated text. It assumes that headings follow a numeric pattern and 
    that content for each subsection follows the heading until the next numbered heading appears.

    Parameters:
    -----------
    path : str
        Path to the input .docx file.

    Returns:
    --------
    pd.DataFrame
        A DataFrame with the following columns:
        - Section_number (e.g., '2')
        - Section_name (e.g., 'Methodology')
        - Subsection_number (e.g., '2.1')
        - Subsection_name (e.g., 'Data Collection')
        - Subsection_text (combined paragraph text under that subsection)
    
    Notes:
    ------
    - This function does not require `python-docx`; it uses `zipfile` and `ElementTree` to parse XML.
    - Only sections and subsections with numeric headings are captured.
    - Paragraphs not preceded by a numeric heading are ignored.
    """
    paragraphs = extract_paragraphs_from_docx(path)
    data = []

    current_section_number = ""
    current_section_name = ""

    for i in range(len(paragraphs)):
        text, style = paragraphs[i]
        match = re.match(r"^(\d+(\.\d+)*)\s+(.*)", text)

        if match:
            number = match.group(1)
            name = match.group(3)

            levels = number.split(".")
            if len(levels) == 1:
                # New section
                current_section_number = number
                current_section_name = name
            elif len(levels) >= 2:
                # Subsection
                subsection_number = number
                subsection_name = name

                # Capture text under this subsection
                content = []
                for j in range(i + 1, len(paragraphs)):
                    next_text, next_style = paragraphs[j]
                    if re.match(r"^(\d+(\.\d+)*)\s+.*", next_text):
                        break
                    content.append(next_text)

                data.append({
                    "Section_number": current_section_number,
                    "Section_name": current_section_name,
                    "Subsection_number": subsection_number,
                    "Subsection_name": subsection_name,
                    "Subsection_text": " ".join(content).strip()
                })

    df = pd.DataFrame(data)
    return df
    
    
# Replace this path with your actual file
file_path = "path_to_your_docx_file.docx"
df = extract_hierarchical_structure(file_path)

# View or export
print(df.head())
df.to_csv("structured_sections.csv", index=False)


