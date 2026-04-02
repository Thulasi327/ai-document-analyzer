import pytesseract
from PIL import Image

def extract_text_image(file_path):
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text