from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserRegisterView, LoginView, LogoutView, ShowUsersView,DeleteUserView, UpdateMemberView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', UserRegisterView.as_view()),
    path('members/', ShowUsersView.as_view()),
    path('deletemember/', DeleteUserView.as_view()),
    path('updatemember/', UpdateMemberView.as_view(), name='update-members')
]