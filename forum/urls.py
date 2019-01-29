from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeReDir, name='firstPage'),
    path('submitPost/', views.submitPost, name = 'submitPost'),
    path('submitPostLanding/', views.submitPostLanding, name = 'submitPostLanding'),
    path('submitComment/<int:post_pk>/', views.submitComment, name = 'submitComment'),
    path('submitCommentLanding/<int:post_pk>/', views.submitCommentLanding, name = 'submitCommentLanding'),
    path('<int:page_number>/', views.home, name='home'),
    path('post/<int:post_pk>/<int:page_number>/', views.postView, name='post'),
    path('user/<int:user_pk>/', views.userView, name = 'user'),
    path('login/', views.loginView, name = 'login'),
    path('loginLanding/', views.loginLanding, name = 'loginLanding'),
    path('signup/', views.signup, name = 'signup'),
    path('signupLanding/', views.signupLanding, name = 'signupLanding'),
    path('logout/', views.logoutView, name = 'logout'),
]
