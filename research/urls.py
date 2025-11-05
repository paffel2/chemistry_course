from django.urls import path

from research.views import LoginView, LogoutView, IndexView

app_name = "research"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", IndexView.as_view(), name="index"),
]
