
import cv2
import numpy as np
from django.conf import settings
import os
import tensorflow as tf

image_path = "E:\\work\\python-projects\\eye-detection\\myimg.jpg"


def render_font(input_type, boolean=False, default=False):
    my_message = ""

    # Face visibility msgs
    face_success_message = "Face posture is correct as recommended!"
    face_failure_message = "Face is not visible clearly, please try again with correct posture!"

    # Glasses visibility msgs
    obstacle_success_message = "No sunglasses found as per recommendation. Perfect!"
    obstacle_failure_message = "Sunglasses found! You look handsome but its against the rules. Please try again"

    my_class = "success" if boolean else "danger"
    my_title = "Face clarity" if input_type == "face" else "Obstacle"

    if (input_type == "glasses") and (not boolean) and (default):
        my_message = "To check the obstacle or glasses, clarity of face is necessary!"
    else:
        if input_type == "face":
            my_message = face_success_message if boolean else face_failure_message
        else:
            my_message = obstacle_success_message if boolean else obstacle_failure_message

    return {
        "title": my_title,
        "class": my_class,
        "is_success": boolean,
        "message": my_message
    }


def is_obstacle_exist(path, is_face_clarity_required=False):
    static_classifier_folder = os.path.join(
        settings.BASE_DIR, "static", "classifiers")

    face_cascade_location = os.path.join(
        static_classifier_folder, "haarcascade_frontalface_default.xml")
    eye_cascade_location = os.path.join(
        static_classifier_folder, "haarcascade_eye_tree_eyeglasses.xml")

    output = {}
    face_cascade = cv2.CascadeClassifier(face_cascade_location)
    eye_cascade = cv2.CascadeClassifier(eye_cascade_location)
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    dimension = (300, 300)
    image = cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    boolean_value_for_face = len(faces) > 0

    # Check for face clarity if required
    if is_face_clarity_required:
        output["face_clarity"] = render_font("face", boolean_value_for_face)

    output["obstacle_checking"] = render_font(
        "glasses",
        boolean_value_for_face,
        not boolean_value_for_face
    )

    # Check for glasses

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        output["obstacle_checking"] = render_font(
            "glasses",
            len(eyes) > 0,
            False
        )
        if len(eyes) > 0:
            break

    return output


# def is_mask_exists(path):

def is_mask_exists(filename):
    face_mask_classifier = os.path.join(
        settings.BASE_DIR, "static", "classifiers")

    face_mask_classifier_path = os.path.join(
        face_mask_classifier, 'mask_detector.h5')

    model = tf.keras.models.load_model(face_mask_classifier_path)
    img = tf.io.read_file(filename)
    # Decode the read file into a tensor
    img = tf.image.decode_image(img)
    # Reshape an image
    img = tf.image.resize(img, [200, 200])

    class_names = ['true', 'false']

    pred = model.predict(tf.expand_dims(img, axis=0))

    if len(pred[0]) > 0:
        pred_class = class_names[tf.argmax(pred[0])]
    else:
        pred_class = class_names[int(tf.round(pred))]

    if pred_class == 'true':
        output = {
            "title": "Face-mask",
            "class": "danger",
            "is_success": False,
            "message": "Facemask found, Please remove the mask and try again."
        }
    else:
        output = {
            "title": "Face-mask",
            "class": "success",
            "is_success": True,
            "message": "Facemask is not found as per recommendation!"
        }

    return output


def is_background_correct(path):
    image = cv2.imread(path)
    image2 = cv2.resize(image, (600, 600))

    rows, cols, _ = image2.shape
    cropped_img = image2[0:100, 0:100]

    hsv_frame = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
    # Blue color
    low_blue = np.array([80, 150, 120])
    high_blue = np.array([130, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(cropped_img, cropped_img, mask=blue_mask)

    flag = 0
    b, g, r = cv2.split(cropped_img)
    b1, g1, r1 = cv2.split(blue)

    if b.all() == b1.all():
        flag = 1
    else:
        flag = 0

    rows, cols, _ = image2.shape
    cut_img = image2[0:100, 500:-1]

    hsv_frame = cv2.cvtColor(cut_img, cv2.COLOR_BGR2HSV)
    # Blue color
    low_blue = np.array([80, 150, 120])
    high_blue = np.array([130, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(cut_img, cut_img, mask=blue_mask)

    flag1 = 0
    b1, g1, r1 = cv2.split(blue)
    b2, g2, r2 = cv2.split(cut_img)

    if b2.all() == b1.all():
        flag1 = 1
    else:
        flag1 = 0

    if flag == 1 and flag1 == 1:
        output = {
            "title": "Background",
            "class": "success",
            "is_success": True,
            "message": " Photo background is correct as per recommendation!"
        }

    else:
        output = {
            "title": "Background",
            "class": "danger",
            "is_success": False,
            "message": "Incorrect background against the rules, it should be blue. Please try again!"
        }

    return output


def is_face_clear(path):
    output = {
        "title": "Face clarity",
        "class": "success",
        "is_success": True,
        "message": "Face posture is correct as recommend"
    }
    return output


# def is_obstacle_exist(path):
#     output = {
#         "title": "Obstacle",
#         "class": "danger",
#         "is_success": False,
#         "message": "Hat and sun glassess are highly inappropriate in front of picture!"
#     }
#     return output
