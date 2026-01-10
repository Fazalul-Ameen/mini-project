import easyocr

reader = easyocr.Reader(['en'])

def extract_text(path):
    result = reader.readtext(path)
    text = " ".join([res[1] for res in result])
    return text
