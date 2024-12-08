from django.urls import path
from apps.users.views import LoginView, SignupView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name="auth-login"),
    path('signup/', SignupView.as_view(), name="auth-signup"),
    path('logout/', LogoutView.as_view(), name="auth-logout"),
]