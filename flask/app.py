from flask import Flask, request, render_template, redirect, url_for
import os
from PIL import Image
import io
import torchvision.transforms as transforms

photos_folder = os.path.join('static', 'photos')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = photos_folder

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

        # Save, resize, and resave image
        file.save("static/photos/original.jpg")
        image = Image.open('static/photos/original.jpg')
        my_transforms = transforms.Compose([
        transforms.Resize(256)])
        image = my_transforms(image)
        image.save("static/photos/original.jpg")

        # Run image through classification function
        resultClass = classify(image)
        # Run image through Segmentation function
        resultSeg = segment(image)

        # Save Segmented image
        full_filename = os.path.join("/", app.config['UPLOAD_FOLDER'], 'file.jpg')
        resultSeg.convert('RGB').save("static/photos/segmention.jpg")

        # Redirect to result page with required information
        return redirect(url_for('getResult', resultClass=resultClass, resultSeg='segmention.jpg', original='original.jpg'))

@app.route('/result/<resultClass>/<resultSeg>/<original>', methods=['GET', 'POST'])
def getResult(resultClass='beans', resultSeg='donnie.jpg', original='original.jpg'):
    # get page
    if request.method == 'GET':
        segFile = os.path.join('/', app.config['UPLOAD_FOLDER'], resultSeg)
        originalFile = os.path.join('/', app.config['UPLOAD_FOLDER'], original)
        return render_template('result.html', flower=resultClass, seg=segFile, original=originalFile)

    # Redirect back to Homepage
    if request.method == 'POST':
        return redirect(url_for('hello_world'))


if __name__ == '__main__':
    app.run(host= '0.0.0.0')