import re

import cv2
import pytesseract
from pytesseract import Output
from src.image_transforms import opening, canny, get_grayscale


class Box:
    def __init__(self, left, top, width, height):
        self.height = height
        self.width = width
        self.top = top
        self.left = left
        self.margin = 0

    def mark(self, img_, color=(0, 255, 0)):
        (x, y, w, h) = self.get_box_sizes()
        cv2.rectangle(img_, (x, y), (x + w, y + h), color, 2)

    def get_box_sizes(self):
        return [max(0, n) for n in (self.left - self.margin,
                                    self.top - self.margin,
                                    self.width + self.margin*2,
                                    self.height + self.margin*2)]

    def set_margin(self, margin):
        self.margin = margin


class ReceiptContent:
    def __init__(self, content, box):
        self.content = content
        self.box = box

    def __repr__(self):
        return self.content


img = cv2.imread('test.jpg')
ret, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

# img = get_grayscale(image)
# img = opening(img)
cv2.imshow('img_raw', img)

custom_config = r'-l pol --psm 6'

d = pytesseract.image_to_data(img, output_type=Output.DICT, config=custom_config)
print(d.keys())
print(d['text'])

prices = []
contents = []

n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        box = Box(d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        content = d['text'][i]
        receipt_content = ReceiptContent(content, box)

        if re.match(r'\d+,\d+', content):
            prices.append(receipt_content)
        elif content:
            contents.append(receipt_content)

for price in prices:
    price.box.mark(img)

for content in contents:
    content.box.mark(img, (255, 0, 0))

main_price = max(prices, key=lambda x: x.box.height + x.box.width)
main_price.box.mark(img, (0, 0, 255))
print(main_price)

shop_name = max(filter(lambda x: len(x.content) > 2, contents), key=lambda x: [-x.box.top])
shop_name.box.mark(img, (100, 100, 100))
print(shop_name.content)

receipt_area = Box(0, shop_name.box.top, 500, (main_price.box.top - shop_name.box.top + main_price.box.height))
receipt_area.set_margin(30)
receipt_area.mark(img, (0, 0, 0))

# cv2.imshow('img', img)
(x, y, w, h) = receipt_area.get_box_sizes()
crop_img = img[y:y+h, x:x+w]
cv2.imshow('cropped', crop_img)

cv2.waitKey(0)
