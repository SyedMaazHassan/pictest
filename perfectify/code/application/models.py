from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
# Create your models here.

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


class image(models.Model):
    source = models.ImageField(upload_to="all_images")
    is_background_success = models.BooleanField(default=False)
    is_facemask_success = models.BooleanField(default=False)
    is_obstacle_success = models.BooleanField(default=False)
    is_face_clarity_success = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
