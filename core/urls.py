from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('assess-risk/', views.assess_risk, name='assess_risk'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blogs/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_id>/vote/<str:vote_type>/', views.vote_comment, name='vote_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    path('hospital-finder/', views.hospital_finder_view, name='hospital_finder'),
    path('resources/', views.educational_resources_view, name='educational_resources'),
]
