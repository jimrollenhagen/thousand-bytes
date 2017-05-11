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


@app.route('/ascii', methods=['POST'])
def convert():
    f = request.files['file']
    height = request.form.get('height', 50)
    try:
        height = int(height)
    except ValueError:
        response = jsonify({'error': '"height" parameter must be an integer'})
        response.status_code = 400
        return response

    img = convert_image(f, height)
    response = make_response(img)
    response.mimetype = 'text/plain'
    return response
