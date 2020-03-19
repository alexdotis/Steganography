import os
from PIL import Image
import textwrap


class MessageNotFound(Exception):
    pass


class MessageTooLong(Exception):
    pass


def to_bits(data):
    """
    If message is "secret"
    :param data: len("secret") : "secret"
    :return: ['01110011', '01100101', '01100011', '01110010', '01100101', '01110100']
    """
    return [bin(ord(c))[2:].zfill(8) for c in data]


def component(pixel, bit):
    """
    :param pixel: pixel
    :param bit: Bit
    :return: pixel
    """
    return pixel & ~1 | int(bit)


def message_hide(image, message):
    """
    Hiding Message on Image
    :param image: Image
    :param message: Message
    :return:
    """
    msg = str(len(message)) + ":" + message
    bit_msg = "".join(to_bits(msg))
    img = Image.open(image)
    if len(bit_msg) > img.width * img.height:
        raise MessageTooLong("Message is too long")
    new_image = Image.new("RGB", (img.width, img.height))
    index = 0
    for h in range(img.height):
        for w in range(img.width):
            r, g, b = img.getpixel((w, h))
            if index + 1 <= len(bit_msg):
                R = component(r, bit_msg[index])
                new_image.putpixel((w, h), (R, g, b))
                index += 1
            else:
                new_image.putpixel((w, h), (r, g, b))
    name_image = os.path.splitext(image)[0]
    new_image.save(f"{name_image}-secret.png")


def rcmp(pixel):
    """

    :param pixel: pixel
    :return: Binary
    """
    result = pixel & 1
    return result


def reveal(image):
    assert image.endswith(".png")
    img = Image.open(image)
    byte = []
    for h in range(img.height):
        for w in range(img.width):
            r, g, b = img.getpixel((w, h))
            bit = rcmp(r)
            byte.append(bit)
    w = "".join(str(i) for i in byte)
    wrap = textwrap.wrap(w, 8)
    table_wrap = [chr(int(i, 2)) for i in wrap]

    if table_wrap.__contains__(":"):
        index = table_wrap.index(":")
        length_words = "".join(table_wrap[:index])
        tab = table_wrap[index + 1:]
        return "".join(tab[i] for i in range(int(length_words)))
    else:
        raise MessageNotFound("Message not Found")
