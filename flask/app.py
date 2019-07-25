from flask import Flask, request, render_template, redirect, url_for
import os
from PIL import Image
import io
import torchvision.transforms as transforms

photos_folder = os.path.join('static', 'photos')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = photos_folder

# from commons import get_tensor
from inference import classify, segment


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# Upload image page, Get and Post
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # get page
    if request.method == 'GET':
        return render_template('index.html', value='hi')

    # send image
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            print('file not uploaded')
            return redirect(url_for('hello_world'))
        file = request.files['file']


        file.save("static/photos/original.jpg")
        # image = file.read()
        # image = Image.open(io.BytesIO('static/photos/original.jpg'))
        image = Image.open('static/photos/original.jpg')
        my_transforms = transforms.Compose([
        transforms.Resize(256)])
        image = my_transforms(image)
        image.save("static/photos/original.jpg")


        resultClass = classify(image)
        # resultClass = 'hello'
        resultSeg = segment(image)
        print(resultSeg)
        # resultSeg = os.path.join("img.jpg")
        # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'shovon.jpg')
        full_filename = os.path.join("/", app.config['UPLOAD_FOLDER'], 'file.jpg')
        # print(full_filename)
        # resultSeg.convert('RGB').save(full_filename)
        resultSeg.convert('RGB').save("static/photos/segmention.jpg")
        # image.convert('RGB').save("static/photos/original.jpg")
        # resultSeg.save(full_filename)

        return redirect(url_for('getResult', resultClass=resultClass, resultSeg='segmention.jpg', original='original.jpg'))

@app.route('/result/<resultClass>/<resultSeg>/<original>', methods=['GET', 'POST'])
def getResult(resultClass='beans', resultSeg='donnie.jpg', original='original.jpg'):
    # get page
    if request.method == 'GET':
        segFile = os.path.join('/', app.config['UPLOAD_FOLDER'], resultSeg)
        originalFile = os.path.join('/', app.config['UPLOAD_FOLDER'], original)
        # full_filename = resultSeg
        return render_template('result.html', flower=resultClass, seg=segFile, original=originalFile)
    if request.method == 'POST':
        return redirect(url_for('hello_world'))

# @app.route('/results', methods=['POST'])
# def coolbeans():

#     # send image
#     if request.method == 'POST':
#         return render_template('index.html')

if __name__ == '__main__':
    app.run(host= '0.0.0.0')