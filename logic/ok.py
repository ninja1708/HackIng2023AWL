from pytesseract import pytesseract
pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

from PIL import Image
img = "3.tiff"
osd = pytesseract.image_to_osd(img)
angle = osd.split("\n")[2].split(" ")[1]
print("angle: ", angle)
rotate_degrees = -(int(angle))
img = Image.open(img)
img2 = img.rotate(rotate_degrees, expand=True)
img2.save("new.jpg")
img.close()
