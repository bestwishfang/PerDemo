import pytesseract
from PIL import Image


if __name__ == '__main__':
    # 读取图片
    # image = Image.open('demo_ocr.png')
    image = Image.open('ce_demo.PNG')
    # 识别图片
    ret = pytesseract.image_to_string(image)
    print(ret)
