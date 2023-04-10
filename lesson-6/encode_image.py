import base64

with open('image.webp', 'rb') as f:
    img = open('image.raw', 'wb')
    img.write(base64.b64encode(f.read()))
    img.close()


if __name__ == '__main__':
    pass