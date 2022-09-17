from flask import Flask, request, jsonify
from PIL import Image
import uuid,os

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/image/store", methods=["POST"])
def process_image():
    file = request.files['image']
    cate = request.form['category']
    # Read the image via file.stream and save it in directory
    img = Image.open(file.stream)
    filename = str(uuid.uuid4())
    filepath = os.path.join(os.getcwd(),cate)
    if(os.path.exists(filepath)):
        filepath = os.path.join(filepath,filename)+".jpg"
        img.save(filepath)
    else:
        os.mkdir(filepath)
        filepath = os.path.join(filepath,filename)+".jpg"
        img.save(filepath)

    return jsonify({'msg': 'success', 'size': [img.width, img.height],'cat': cate})

if __name__ == "__main__":
  app.run()