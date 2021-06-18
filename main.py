import os
import json
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import ST7789 as ST7789


app = Flask(__name__)

app.config.from_file("config.json", load=json.load)

ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
ROTATION = int(app.config['ROTATION'])

# Create ST7789 LCD display class.
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000,
    offset_left=0
)

WIDTH = disp.width
HEIGHT = disp.height

disp.begin()

def show_image(filename):
    try:
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = image.resize((WIDTH, HEIGHT))
        if ROTATION > 0:
            image = image.rotate(ROTATION)
        disp.display(image)
        return True
    except FileNotFoundError:
        return False

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def can_handle_html():
    return "text/html" in request.headers.get('Accept')

try:
    last_file_saved=open("last_file.json")
    last_file = last_file_saved.read()
    last_file_saved.close()
    show_image(last_file)
except FileNotFoundError:
    pass

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            if can_handle_html():
                return '"file" not uploaded'
            else:
                return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            last_file_saved=open("last_file.json", "w")
            last_file_saved.write(filename)
            last_file_saved.close()
            if last_file != filename:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], last_file))
            if not show_image(filename):
                return json.dumps({'success':False}), 500, {'ContentType':'application/json'}

    if can_handle_html():
        return '''
        <!doctype html>
        <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
        '''
    else:
        return json.dumps({'success':True}), 204, {'ContentType':'application/json'}

