!sudo apt-get install tesseract-ocr-* #Downloads packages for all the languages supported by tesseract.
!pip install pytesseract

import pytesseract
import cv2

img = cv2.imread('Yout_Image_Adress_Here')
text = pytesseract.image_to_string(img, lang='ori') #Language codes here - https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
print(text)
