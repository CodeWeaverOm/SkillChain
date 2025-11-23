from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile_page, name='profile'),
    path('profile/save/', views.save_profile, name='save_profile'),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    path('user/<int:profile_id>/', views.view_user_profile, name='view_user_profile'),
    path('profile/tab/<str:tab>/', views.load_profile_tab, name='load_profile_tab'),

    path('profile/upload-video/', views.profile_upload_video, name='profile_upload_video'),
    path('profile/upload-certificate/', views.upload_certificate, name='profile_upload_certificate'),

    path('rate_video/<int:video_id>/', views.rate_video, name='rate_video'),
    path("add-peer/<int:profile_id>/", views.add_peer, name="add_peer"),
    path("user/<int:profile_id>/", views.view_user_profile, name="user_profile"),

    # _----------------------------- Expert Urls ------------------------------------------
    path("expert-login/", views.expert_login, name="expert_login"),
    path("expert/home/", views.expert_home, name="expert_home"),
    path("expert/competition/create/", views.create_competition, name="create_competition"),
]
