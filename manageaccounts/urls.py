from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path("register/", views.register, name="register"),
    #path("register/", UserRegistration.as_view(), name="register"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(from_email="psc.official.bu@gmail.com", template_name='manageaccounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='manageaccounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='manageaccounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='manageaccounts/password_reset_complete.html'), name='password_reset_complete'),

    path("profile/changePassword", views.changePassword, name="changePassword"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/posts", views.userFeed, name="userFeed"),
    path("profile/<str:username>/favorites", views.bookmark, name="bookmark"),
    path("profile/<str:username>/editProfile/", views.editProfile, name="editProfile"),
    path("profile/<str:username>/deleteProfile/", views.deleteUser, name="deleteUser"),



]

