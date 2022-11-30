from flask import Flask, request, jsonify, Response
from PIL import Image, ImageOps
import keras
import uuid, os
import numpy as np
import cv2
import tensorflow as tf
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/image/store", methods=["POST"])
def process_image():
    file = request.files['image']
    # Read the image via file.stream and save it in directory

    try:
        img = Image.open(file.stream)
        img.save('InputImage/test.png')
        img = cv2.imread('InputImage/test.png')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (threshold, bwImage) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        img = cv2.resize(bwImage, (28, 28), interpolation=cv2.INTER_AREA)
        img = 1 - img
        # predict number
        # E:\Courses\Mobile computing\mnist_nn model location
        #print(tf.config.list_physical_devices('GPU'))
        model = keras.models.load_model('mnist_nn')
    #    img = ImageOps.invert(img)
        X_test = np.asarray(img)
        print(X_test.shape)
        X_test = X_test.reshape(1,784)
        print(X_test)
        X_test = np.where(X_test < 120,0,X_test)
        print(X_test)
        y_pred = model.predict(X_test)
        print("y_pred = ", y_pred)
        cate = y_pred.argmax()
        print("cate = ",cate)
        filename = str(uuid.uuid4())
        filepath = os.path.join(os.getcwd(), str(cate))
        if (os.path.exists(filepath)):
            filepath = os.path.join(filepath, filename) + ".jpg"
            cv2.imwrite(filepath,img)
        else:
            os.mkdir(filepath)
            filepath = os.path.join(filepath, filename) + ".jpg"
            cv2.imwrite(filepath,img)
        return jsonify({'msg': 'success', 'category_score': y_pred})
    except:
        return Response(
            "some issue with the server",
            status=500,
        )

if __name__ == "__main__":
    app.run(host='192.168.0.214', port=5000)
