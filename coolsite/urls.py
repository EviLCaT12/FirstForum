from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import *
from .forms import*
urlpatterns = [
    path('',Index.as_view(), name='home-page'),
    path('register/', RegisterView.as_view(), name='reg-page'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('profile/', profile, name='users-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('post/<slug:slug>/', ShowPost.as_view(), name='show-post'),
    path('friends/',friends,name='friends')

]