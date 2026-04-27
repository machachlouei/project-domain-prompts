#=== version 1 ===========================

import os
import re
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd

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


#=== version 2 =============================

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

#==  version 3 =======================
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd

def extract_paragraphs_with_styles(path):
    """
    Extracts paragraphs and associated styles from a .docx file using raw XML.
    Returns a list of (text, style) tuples.
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

def extract_structure_from_styles(path):
    """
    Extracts section and subsection structure using Heading1 and Heading2 styles from a .docx file.

    Parameters:
        path (str): Path to the input .docx file.

    Returns:
        pd.DataFrame: Structured DataFrame with section/subsection metadata and associated text.
    """
    paragraphs = extract_paragraphs_with_styles(path)
    data = []

    current_section_name = ""
    current_subsection_name = ""
    current_text = []

    for text, style in paragraphs:
        if style == "Heading1":
            # Save previous subsection before starting new section
            if current_subsection_name and current_text:
                data.append({
                    "Section_number": "",
                    "Section_name": current_section_name,
                    "Subsection_number": "",
                    "Subsection_name": current_subsection_name,
                    "Subsection_text": " ".join(current_text).strip()
                })
            current_section_name = text
            current_subsection_name = ""
            current_text = []

        elif style == "Heading2":
            if current_subsection_name and current_text:
                data.append({
                    "Section_number": "",
                    "Section_name": current_section_name,
                    "Subsection_number": "",
                    "Subsection_name": current_subsection_name,
                    "Subsection_text": " ".join(current_text).strip()
                })
            current_subsection_name = text
            current_text = []

        else:
            current_text.append(text)

    # Append the final subsection
    if current_subsection_name and current_text:
        data.append({
            "Section_number": "",
            "Section_name": current_section_name,
            "Subsection_number": "",
            "Subsection_name": current_subsection_name,
            "Subsection_text": " ".join(current_text).strip()
        })

    return pd.DataFrame(data)
    
    
file_path = "your_file.docx"
df = extract_structure_from_styles(file_path)

print(df.head())
df.to_csv("structured_output.csv", index=False)

#====== Extract small units of instructions 

Prompt template:
You are given a paragraph of technical documentation or guidance text from a model validation document. 

Your task is to extract all **distinct guideline instructions** from the text. Each instruction should:
- Start with an action verb (e.g., "Review", "Assess", "Describe", "Document").
- Be self-contained and actionable.
- Be concise, no longer than 1–2 sentences each.

Format your output as a bullet list of instructions.

Text:
"""
{Insert Subsection_text here}
"""

#=== Version 4 ================

import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
import openai
import time

openai.api_key = os.environ["OPENAI_API_KEY"]

def extract_paragraphs_with_styles(path):
    """
    Extracts paragraphs and associated styles from a .docx file.
    Returns a list of (text, style) tuples.
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

def extract_guideline_instructions(text):
    """
    Uses GPT to extract atomic guideline instructions from a long paragraph.
    """
    prompt = f"""
You are given a paragraph of technical documentation from a model validation document.

Your task is to extract all distinct guideline instructions from the text. Each instruction should:
- Start with an action verb (e.g., "Review", "Assess", "Describe", "Document").
- Be self-contained and actionable.
- Be concise, no longer than 1–2 sentences each.

Format your output as a bullet list of instructions.

Text:
\"\"\"
{text}
\"\"\"
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts guideline instructions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=600
        )
        output = response["choices"][0]["message"]["content"]
        # Extract bullet points
        instructions = [line.strip("-• ").strip() for line in output.splitlines() if line.strip().startswith(("-", "•"))]
        return instructions
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return []

def extract_structure_from_styles(path):
    """
    Extracts structured content from a .docx file using style-based heading parsing,
    then extracts individual guideline instructions using GPT from each subsection text.

    Returns:
    pd.DataFrame with columns:
    - Section_name
    - Section_number
    - Subsection_name
    - Subsection_number
    - Guideline_instruction
    """
    paragraphs = extract_paragraphs_with_styles(path)
    data = []

    current_section_name = ""
    current_subsection_name = ""
    current_text = []

    for text, style in paragraphs:
        if style == "Heading1":
            # If ending a subsection, extract its instructions
            if current_subsection_name and current_text:
                instructions = extract_guideline_instructions(" ".join(current_text).strip())
                for instr in instructions:
                    data.append({
                        "Section_name": current_section_name,
                        "Section_number": "",
                        "Subsection_name": current_subsection_name,
                        "Subsection_number": "",
                        "Guideline_instruction": instr
                    })
            current_section_name = text
            current_subsection_name = ""
            current_text = []

        elif style == "Heading2":
            # Flush previous subsection
            if current_subsection_name and current_text:
                instructions = extract_guideline_instructions(" ".join(current_text).strip())
                for instr in instructions:
                    data.append({
                        "Section_name": current_section_name,
                        "Section_number": "",
                        "Subsection_name": current_subsection_name,
                        "Subsection_number": "",
                        "Guideline_instruction": instr
                    })
            current_subsection_name = text
            current_text = []

        else:
            current_text.append(text)

    # Final flush
    if current_subsection_name and current_text:
        instructions = extract_guideline_instructions(" ".join(current_text).strip())
        for instr in instructions:
            data.append({
                "Section_name": current_section_name,
                "Section_number": "",
                "Subsection_name": current_subsection_name,
                "Subsection_number": "",
                "Guideline_instruction": instr
            })

    return pd.DataFrame(data)


