from asciimatics.renderers import ImageFile
from flask import Flask
from flask import request


app = Flask(__name__)


def convert_image(fp):
    imgf = ImageFile(fp)
    img = [i for i in imgf.images][0]
    img = '\n'.join(line for line in img)
    return img


@app.route('/ascii', methods=['POST'])
def convert():
    f = request.files['file']
    img = convert_image(f)
    return img
