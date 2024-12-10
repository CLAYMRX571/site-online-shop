from django.urls import path
from .views import (
    UpdatePasswordView,
    UserRegisterView,
    LoginView,
    LogoutView,
    UpdateUserView,
    PasswordResetView,
    CheckVeryfyCodeView,
    OrderProfileView,
    ResetNewPasswordView,
)

app_name = 'accounts'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-info/', UpdateUserView.as_view(), name='update-user-info'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('check-verify-email/<uuid:uuid>/', CheckVeryfyCodeView.as_view(), name='check-verify-code'),
    path('orders/', OrderProfileView.as_view(), name='orders'),
    path('reset-new-password/<uuid:uuid>/', ResetNewPasswordView.as_view(), name='reset-new-password'),
]
