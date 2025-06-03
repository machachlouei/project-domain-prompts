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




