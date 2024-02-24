from django.urls import path
from .views import UserRegistrationView, UserLoginView, ConfirmEmailView, user_logout_view, PassChangeView, UserProfileView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', ConfirmEmailView.as_view(), name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('profile/pass_change/', PassChangeView.as_view(), name='pass_change'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]




