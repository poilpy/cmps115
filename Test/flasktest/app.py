from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# from commons import get_tensor
from inference import classify

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
            return
        file = request.files['file']
        image = file.read()

        resultClass = classify(image)
        return redirect(url_for('getResult', resultClass=resultClass))
        # return redirect(url_for('getResult'))

@app.route('/result/<resultClass>', methods=['GET', 'POST'])
def getResult(resultClass='beans'):
    # get page
    if request.method == 'GET':
        return render_template('result.html', flower=resultClass)
    if request.method == 'POST':
        return redirect(url_for('hello_world'))

# @app.route('/results', methods=['POST'])
# def coolbeans():

#     # send image
#     if request.method == 'POST':
#         return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)