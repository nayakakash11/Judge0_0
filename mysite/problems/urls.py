from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),                    
    path('register/', views.register_view, name='register'),     
    path('logout/', views.logout_view, name='logout'),          
    path('problems/', views.problem_list, name='problem_list'),  
    path('problems/<int:pk>/', views.problem_detail, name='problem_detail'),
]
