from PIL import Image
import pytesseract


def read(src):
    return pytesseract.image_to_data(Image.open('test.png'), output_type=pytesseract.Output.DICT, nice=0)


if __name__ == '__main__':
    print(read('s'))