from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

def split_text_to_paragraphs(text):
    paragraphs = text.split('\n\n')
    return paragraphs

pdf_path = "kankyouhakusyo.pdf"
text = extract_text_from_pdf(pdf_path)
paragraphs = split_text_to_paragraphs(text)
print(len(paragraphs))