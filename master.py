import base64
import json
import os
import uuid

import cv2
import numpy as np
import requests
from PIL import Image
from flask import Flask, request, jsonify, Response

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
        (threshold,bwImage) = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        img = cv2.resize(bwImage,(28,28),interpolation = cv2.INTER_AREA)
        img = 1-img
        cv2.imwrite('InputImage/test.jpg',img)
        # Divide images
        h, w = (28,28)
        half = w // 2
        half2 = h // 2
        top_left = img[:half2, :half]
        top_right = img[:half2, half:]
        bottom_left = img[half2:, :half]
        bottom_right = img[half2:, half:]
        # Make API calls to servers for computations
        cv2.imwrite('InputImage/top_left.jpg', top_left)
        cv2.imwrite('InputImage/top_right.jpg', top_right)
        cv2.imwrite('InputImage/bottom_left.jpg', bottom_left)
        cv2.imwrite('InputImage/bottom_right.jpg', bottom_right)
        host_lst = ['http://192.168.0.169:5000/image/store','http://192.168.0.214:5000/image/store', 'http://192.168.0.97:5000/image/store','http://192.168.0.126:5000/image/store']
        image_parts = ["top_left.jpg","bottom_left.jpg","bottom_right.jpg","top_right.jpg"]
        score_lst = []
        for i,img_name in enumerate(image_parts):
            # Reference https://betatim.github.io/posts/python-create-multipart-formdata/
            with open("InputImage/"+image_parts[i], "rb") as f:
                im_bytes = f.read()
            encoded_string = base64.b64encode(im_bytes).decode('utf-8')
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            payload = {"image":encoded_string}
            payload = json.dumps(payload)
            response = requests.post(host_lst[i], data=payload,headers=headers)
            res = response.json()
            score_lst.append(res['confidence_score'])
        # predict number - Take Majority
        majority = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
        for val in score_lst:
            majority[np.argmax(json.loads(val))] += 1
        cate = max(majority,key=majority.get)
        # E:\Courses\Mobile computing\mnist_nn model location
        print("cate = ",cate)
        filename = str(uuid.uuid4())
        filepath = os.path.join(os.getcwd(), str(cate))
        if (os.path.exists(filepath)):
            filepath = os.path.join(filepath, filename) + ".jpg"
            cv2.imwrite(filepath,img)
        else:
            os.mkdir(filepath)
            filepath = os.path.join(filepath, filename) + ".jpg"
            cv2.imwrite(filepath, img)
        return jsonify({'msg': 'success', 'size': [28, 28], 'cat': str(cate)});
    except:
        return Response(
            "some issue with the server",
            status=500,
        )

if __name__ == "__main__":
    app.run(host='192.168.0.225', port=5000)