import base64
import io
import json
import keras
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, Response
from numpyencoder import NumpyEncoder

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/image/store", methods=["POST"])
def process_image():
    file_data = base64.b64decode(request.json['image'])
    file = Image.open(io.BytesIO(file_data))
    # Read the image via file.stream and save it in directory
    try:
        img = file
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
        # return jsonify({'msg': 'success', 'size': [28, 28], 'cat': str(cate)});
        return jsonify({'msg': 'success', 'confidence_score': json.dumps(y_pred,cls=NumpyEncoder)})
    except:
        return Response(
            "some issue with the server",
            status=500,
        )

if __name__ == "__main__":
    app.run(host='192.168.0.214', port=5000)
