import pytesseract
import cv2

img = cv2.imread('test.jpg')

ret,img = cv2.threshold(img,125,1000,cv2.THRESH_BINARY)
cv2.imshow('gray', img)
d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang='pol')
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

print(d['text'])
cv2.imshow('img', img)
cv2.waitKey(0)