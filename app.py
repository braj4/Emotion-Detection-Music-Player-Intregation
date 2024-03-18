import base64
import io
import os
import tensorflow
import random
from flask import Flask, request, render_template
from PIL import Image
from keras.models import load_model
import numpy as np
import cv2

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save_image', methods=['POST'])
def save_image():
    # Decode the base64-encoded image data
    image_data = base64.b64decode(request.json['image'])

    # Load the image data into a PIL Image object
    image = Image.open(io.BytesIO(image_data))

    # Convert the PIL Image object to a numpy array
    image_array = np.array(image)

    # Load the face detection model
    face_cascade = cv2.CascadeClassifier('static/haarcascades/haarcascade_frontalface_default.xml')

    # Convert the image to grayscale for face detection
    gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # Crop the image to the first detected face
        face = faces[0]
        cropped_image_array = image_array[face[1]:face[1] + face[3], face[0]:face[0] + face[2]]

        # Convert the cropped image array back to a PIL Image object
        cropped_image = Image.fromarray(cropped_image_array)

        # Save the cropped image to disk
        count = len(os.listdir('static/images'))
        filename = 'static/images/{}.jpg'.format(count)
        cropped_image.save(filename)

        return 'Image saved as {}'.format(filename)
    else:
        return 'No faces detected'



@app.route('/music')
def music():
    return render_template('music.html')


@app.route('/new_page')
def new_page():
    count= len(os.listdir('static/images'))
    count= count-1
    emotion_labels = ['angry', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']

    filename = '{}.jpg'.format(count)
    image_path = os.path.join('static', 'images', filename)
    image = cv2.imread(image_path, 0)
    image = cv2.resize(image, (48, 48))

    image = np.reshape(image, (1, 48, 48, 1))
    #Pass the preprocessed image through the model to get predictions

    predictions = load_model('3rd_model (2).h5').predict(image)
    la = np.argmax(predictions)
    if la == 7:
            la=random_number = random.randint(0, la)
    emotion_label = emotion_labels[la]

    folder_path = os.path.join(app.static_folder, 'songs', emotion_label)
    songs_list = os.listdir(folder_path)
    return render_template('new_page.html', songList=songs_list, mood=emotion_label, count=str(count))


if __name__ == '__main__':
    app.run(debug=True)




#
#
#
#
#
#
#
#
#
#
# app = Flask(__name__)
#
#
# app = Flask(__name__, static_url_path='/static', static_folder='static')
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# def get_image_count():
#     image_dir = os.path.join(app.static_folder, 'images')
#     if not os.path.exists(image_dir):
#         os.makedirs(image_dir)
#     return len(os.listdir(image_dir))
#
#
#


#
# @app.route('/play_music_button', methods=['POST'])
# def play_music_button():
#     mood = request.form['mood']
#     folder_path = os.path.join(app.static_folder, 'songs', mood)
#     songs_list = os.listdir(folder_path)
#     return render_template('new_page.html', songs=songs_list, mood=mood)
#
#
#
# @app.route('/play_music_file', methods=['POST'])
# def play_music_file():
#     count  = get_image_count()
#     count += 1
#     img = request.files['file']
#
#     img.save('static/images/{}.jpg'.format(count))
#     emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
#     image = cv2.imread('static/images/{}.jpg'.format(count), 0)
#     image = cv2.resize(image, (48, 48))
#     image = np.reshape(image, (1, 48, 48, 1))
#     # Pass the preprocessed image through the model to get prediction
#     predictions = load_model('1st_model.h5').predict(image)
#     # Convert the predictions to an emotion labe
#     emotion_label = emotion_labels[np.argmax(predictions)]
#     mood = emotion_label
#
#     folder_path = os.path.join(app.static_folder, 'songs', mood)
#     songs_list = os.listdir(folder_path)
#     return render_template('new_page.html', songs=songs_list, mood=mood)
#
#
# @app.route('/favicon.ico')
# def favicon():
#     return app.send_static_file('favicon.ico')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)