import tkinter as tk
import cv2
from PIL import Image, ImageTk
from keras.applications.inception_v3 import InceptionV3, decode_predictions, preprocess_input
from keras.preprocessing import image
import numpy as np

width, height = 1244, 700

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = tk.Tk()

widgets = [root]

model = InceptionV3(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000)
target_size = (224, 224)


def update_feed():

    _, frame = cam.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)

    img = img.resize((1500, 750))

    imgtk = ImageTk.PhotoImage(image=img)

    video_feed.imgtk = imgtk
    video_feed.configure(image=imgtk)
    video_feed.after(10, update_feed)


def key_binding(event):
    if event.char == " ":
        predict()
    elif event.char == "q":
        root.destroy()


def predict():
    _, input_img = cam.read()
    input_img = Image.fromarray(input_img)

    if input_img.size != target_size:
        input_img = input_img.resize(target_size)

    x = image.img_to_array(input_img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    plist = (decode_predictions(preds, top=5)[0])
    make_text(plist)


def make_text(pred_list):
    a = []
    for index, value in enumerate(pred_list, start=1):
        a.append("%i. %s - %i%%" % (index, value[1], int(round(value[2]*100))))

    preds.set(a[0])
    preds2.set("\n".join(a[1:]))
    root.update_idletasks()

title = tk.Label(root, text="Google image recognition", font="Verdana 20 bold")
title.pack(side=tk.TOP, fill=tk.X)
widgets.append(title)

video_frame = tk.Frame(root)
video_frame.pack(side=tk.TOP)
widgets.append(video_frame)

text_frame_main = tk.Frame(root)
text_frame_main.pack(side=tk.TOP)
widgets.append(text_frame_main)

photo_button = tk.Button(text_frame_main, text="Run detection", command=predict, height=4, width=20, font="Verdana 15 bold")#, borderwidth=0)
photo_button.grid(column=0, row=0, padx=10, pady=20)
widgets.append(photo_button)

preds = tk.StringVar()
preds.set("")
prediction_text = tk.Label(text_frame_main, textvariable=preds, font="Verdana 25 bold")
prediction_text.grid(column=1, row=0, padx=10, pady=20)
widgets.append(prediction_text)

preds2 = tk.StringVar()
preds2.set("")
prediction_text_small = tk.Label(text_frame_main,textvariable=preds2, font="Verdana 14")
prediction_text_small.grid(column=2, row=0, padx=10, pady=20)
widgets.append(prediction_text_small)

video_feed = tk.Label(video_frame)
video_feed.pack()
widgets.append(video_feed)

root.bind("<Key>", key_binding)

text_colour = "white"

primary_colour = "#212121"
dark_colour = "#000000"
light_colour = "#484848"

for widget in widgets:
    try:
        widget.configure(bg=primary_colour, fg=text_colour)
    except:
        widget.configure(bg=primary_colour)

title.configure(bg=dark_colour)
photo_button.configure(bg=light_colour)


update_feed()
root.attributes("-fullscreen", True)
root.mainloop()