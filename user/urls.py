from django.urls import path

from user.views import CreateUserView, LoginUserView, ManageUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="me")
]

app_name = "user"
