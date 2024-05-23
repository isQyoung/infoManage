import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# 生成随机验证码  宽  高 数量 字体大小
def check_code(width=120, height=35, char_length=5, font_size=34):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(204, 229, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rnd_char():
        """生成随机字母"""
        return chr(random.randint(65, 90))

    def rnd_color():
        """生成随机颜色 """
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 字体文件路径
    path = os.path.dirname(__file__)
    font_file = os.path.join(path, '..', 'static/infoManage/fonts/Pencil.otf')
    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rnd_char()
        code.append(char)
        h = random.randint(-3, 3)
        draw.text([i * width / char_length, h], char, font=font, fill=rnd_color())

    # 写干扰点
    for i in range(20):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rnd_color())

    # 写干扰圆圈
    for i in range(20):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rnd_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rnd_color())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rnd_color())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)
