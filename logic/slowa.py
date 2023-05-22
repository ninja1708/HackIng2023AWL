import cv2
import os
from pytesseract import pytesseract

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def save(txt, path):
    f = open(path, "w", encoding="UTF-8")
    f.write(txt)

def get_words(path, new_path):
    img = cv2.imread(path)
    txt = pytesseract.image_to_string(img)
    save(txt, new_path)
    return txt
