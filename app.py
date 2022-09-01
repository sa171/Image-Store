from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/image/store", methods=["POST"])
def process_image():
    file = request.files['image']
    cate = request.form['category']
    print(request.data)
    # Read the image via file.stream
    img = Image.open(file.stream)
    img.save("api_image.jpg")

    return jsonify({'msg': 'success', 'size': [img.width, img.height],'cat': cate})

if __name__ == "__main__":
  app.run()