from asciimatics.renderers import ImageFile
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request


app = Flask(__name__)


def convert_image(fp, height):
    imgf = ImageFile(fp, height=height)
    img = [i for i in imgf.images][0]
    img = '\n'.join(line for line in img if line)
    return img


def _error(msg):
    response = jsonify({'error': msg})
    response.status_code = 400
    return response


@app.route('/ascii', methods=['POST'])
def convert():
    f = request.files.get('image')
    if f is None:
        return _error('must provide image to convert')

    height = request.form.get('height', 50)
    try:
        height = int(height)
        if height <= 0:
            raise ValueError
    except ValueError:
        return _error('"height" parameter must be a positive integer')

    img = convert_image(f, height)
    response = make_response(img)
    response.mimetype = 'text/plain'
    return response
