from PIL import Image
import pytesseract

img = Image.open('../assets/default.jpg')

pytesseract.pytesseract.tesseract_cmd = r"C:\users\hp\appdata\local\programs\python\python38-32\lib\site-packages\pytesseract.exe"
print(pytesseract.image_to_string(img))