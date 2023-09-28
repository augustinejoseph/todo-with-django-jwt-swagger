from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoTaskViewSet, RegisterUser, LoginView

router = DefaultRouter()
router.register(r"tasks", TodoTaskViewSet, basename="task-list")


urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register_user"),
    path("login/", LoginView.as_view(), name="login_user"),
    path("", include(router.urls)),
]
