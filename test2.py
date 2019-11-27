import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, send_from_directory
import cv2
from PIL import Image
import numpy as np
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import torch
densenet121 = models.densenet121(pretrained=True)


transform = transforms.Compose([            #[1]
transforms.Resize(256),                    #[2]
transforms.CenterCrop(224),                #[3]
transforms.ToTensor(),                     #[4]
transforms.Normalize(                      #[5]
mean=[0.485, 0.456, 0.406],                #[6]
std=[0.229, 0.224, 0.225]                  #[7]
)])

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("website.html")
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
        name = "images/"+upload.filename
        # X_test = cv2.imread(name)
        # img = Image.fromarray(np.uint8(X_test/255))
        x  = Image.open(name)
        img_t = transform(x)
        batch_t = torch.unsqueeze(img_t, 0)

        densenet121.eval()

        output = densenet121(batch_t)
        print(output.shape)


        with open('classnames.txt') as f:
            classes = [line.strip() for line in f.readlines()]

        labels = {int((x.split(':')[0]).replace('"',"").replace("'","")):x.split(':')[1].replace('"',"").replace("'","") for x in classes}

        _, idx = torch.max(output,1)

        print(labels[int(idx)])

        print(torch.sum(output))

        
    return render_template("report.html", image_name=filename)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(port=4555, debug=True)
