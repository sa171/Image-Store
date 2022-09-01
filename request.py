import requests

url = 'http://127.0.0.1:5000/im_size'
my_img = {'image': open('test.png', 'rb')}
r = requests.post(url, files=my_img)
