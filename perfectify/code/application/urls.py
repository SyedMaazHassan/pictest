from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('result', views.check_image, name="result")
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
