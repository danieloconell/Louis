from keras.applications.inception_v3 import InceptionV3, decode_predictions, preprocess_input
from keras.utils import plot_model
from keras.preprocessing import image
import cv2
import numpy as np
from PIL import Image


model = InceptionV3(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000)
target_size = (224, 224)


def predict(img):

    img = Image.fromarray(img)

    if img.size != target_size:
        img = img.resize(target_size)

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    return decode_predictions(preds, top=5)[0]


def clean_list(list):
    a = 1
    for i in list:
        info = "%i. %s - %f" % (a, i[1], (round(i[2] * 1000)/10))
        print(info)
        a += 1


cam = cv2.VideoCapture(0)

while(True):
    ret, img = cam.read()
    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        print(chr(27) + "[2J")
        prediction = predict(img)
        # print(prediction)

        clean_list(prediction)
        
        # first = prediction[0]
        # cv2.putText(img, str(first[1]), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()

