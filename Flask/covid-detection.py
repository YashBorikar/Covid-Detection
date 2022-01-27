from flask import Flask, render_template, request

import cv2
import numpy as np
import tensorflow as tf

app = Flask(__name__, template_folder='./templates')

# Load trained model
model = tf.keras.models.load_model('../Model/covid_detection.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def tasks():
    if request.method == 'POST':
        file = request.files['xray_image'].read()
        npimg = np.frombuffer(file, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        resize_image = cv2.resize(img, (224,224))
        img_pixels = resize_image.reshape(224,224,3)
        img_pixels = np.expand_dims(img_pixels, axis=0)
        classes = model.predict(img_pixels)
        New_pred = np.argmax(classes, axis=1)
        if New_pred==[1]:
            prediction = 'Normal'
        else:
            prediction = 'Covid Infection'
        return render_template('index.html', result=prediction)

    return render_template('index.html', result='')

if __name__ == '__main__':
    app.run()

cv2.destroyAllWindows()