from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/',views.loginuser,name='login'),
    path('logout',views.logoutuser,name='logout'),
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('nidan-data-table/<str:nidan_id>',views.nidan_ticket_data,name='nidan_data_table'),
    path('edit-profile/',views.userSettings,name='settings'),
    path('all-tickets/', views.allTicket, name='all_tickets'),
    path('create-ticket/', views.createTicket, name='create_ticket'),
    path('update-ticket/<str:pk>/', views.updateTicket, name='update_ticket'),
    path('api-nidan/', views.api_nidan, name='api_nidan'),
]
