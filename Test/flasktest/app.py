from flask import Flask, request, render_template

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
        # get_flower_name(image_bytes=image)
        # tensor = get_tensor(image_bytes=image)
        # print(get_tensor(image_bytes=image))
        # return render_template('result.html', flower=flower_name, category=category)
        return render_template('result.html', flower=resultClass)

if __name__ == '__main__':
    app.run(debug=True)