from django.shortcuts import render, redirect, resolve_url
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from .supporting_func import *
from django.conf import settings
import cv2
import os
import json
import tensorflow

# main page function


def index(request):
    return render(request, 'index.html')


def check_image(request):
    root = settings.BASE_DIR
    context = {}
    if request.method == "POST":
        context = {"result": True}
        target_file = request.FILES['targetfile']

        new_image = image(source=target_file)
        new_image.save()
        context['image'] = new_image.source

        # GET image path and check if obstacle exists
        new_image_path = os.path.join(root, "media", str(new_image.source))
        face_clarity_and_glassses = is_obstacle_exist(new_image_path, True)

        # Mask checking
        mask_check = is_mask_exists(new_image_path)

        # Background check
        background_check = is_background_correct(new_image_path)

        # Update the status
        new_image.is_background_success = background_check['is_success']
        # to be chaned
        new_image.is_facemask_success = mask_check['is_success']
        new_image.is_obstacle_success = face_clarity_and_glassses["obstacle_checking"]['is_success']
        new_image.is_face_clarity_success = face_clarity_and_glassses["face_clarity"]['is_success']
        new_image.save()

        # Store responses
        results = [
            mask_check,
            background_check,
            face_clarity_and_glassses["face_clarity"],
            face_clarity_and_glassses["obstacle_checking"]
        ]

        context['all_status'] = results
        context["foot"] = {
            "heading": "Facing difficulty in capturing a valid picture?",
            "tagline": "Download our Ai powered camera app"
        }

        # Success msg if all test is passed
        if results[0]["is_success"] and results[1]["is_success"] and results[2]["is_success"] and results[3]["is_success"]:
            context["head"] = {
                "heading": "Image is virtually acceptable!",
                "tagline": "Upload another image to see its credibility using this amazing service!."
            }
        else:
            context["head"] = {
                "heading": "Image is not virtually acceptable!",
                "tagline": "<a style='color: #ff7777'>Read guidlines</a> here and upload your updated image."
            }

        # return redirect("index")

    return render(request, "index.html", context)


# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name": name,
            "l_name": l_name,
            "email": email,
            "pass1": pass1,
            "pass2": pass2,
        }
        if pass1 == pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email"
                return render(request, "signup.html", context)

            user = User.objects.create_user(
                username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()

            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)

    return render(request, "signup.html")


# function for login

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")
