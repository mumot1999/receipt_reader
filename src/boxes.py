import re

import cv2
import pytesseract
from pytesseract import Output


class Price:
    def __init__(self, price, box):
        self.price = price
        self.box = box


img = cv2.imread('test.png')

custom_config = r'-l pol --psm 6'

d = pytesseract.image_to_data(img, output_type=Output.DICT, config=custom_config)
print(d.keys())


prices = []

n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        if re.match(r'^\d+,\d+$', d['text'][i]):
            prices.append(Price(d['text'][i], (d['left'][i], d['top'][i], d['width'][i], d['height'][i])))


def mark_price(img, price, color=(0, 255, 0)):
    (x, y, w, h) = price.box
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

for price in prices:
    mark_price(img, price)

main_price = max(prices, key=lambda x: x.box[3]+x.box[2])
mark_price(img, main_price, (0, 0, 255))

cv2.imshow('img', img)
cv2.waitKey(0)