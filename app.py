from flask import Flask, request, jsonify, Response
from PIL import Image, ImageOps
import keras
import uuid, os
import numpy as np
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
        img = ImageOps.grayscale(img)
        img = img.resize((28, 28), Image.ANTIALIAS)
        print(img.width)
        print(img.height)

            # img_inverted = Image.open('mnist_4.png')
            # img_inverted = img_inverted.convert('L')
            # img_inverted = img_inverted.resize((28, 28), Image.ANTIALIAS)
            # img_inverted = ImageOps.invert(img)

        # predict number
        # E:\Courses\Mobile computing\mnist_nn model location
        print(tf.config.list_physical_devices('GPU'))
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
            img.save(filepath)
        else:
            os.mkdir(filepath)
            filepath = os.path.join(filepath, filename) + ".jpg"
            img.save(filepath)
        return jsonify({'msg': 'success', 'size': [img.width, img.height], 'cat': str(cate)})
    except:
        return Response(
            "some issue with the server",
            status=500,
        )

if __name__ == "__main__":
    app.run(host='192.168.0.214', port=5000)
