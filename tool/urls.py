from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.loginuser,name='login'),
    path('resgister/',views.registeruser,name='register'),
    path('logout/',views.logoutuser,name='logout'),
    path('password-change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password-change-done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password-reset-form/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('password-reset-done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('api-nidan/nidan-solved-api/<str:dcnum>/',views.nidanSolvedDetail,name='nidan_solved_api'),
    path('api-nidan/nidan-solved-list-api/',views.nidanSolvedList,name='nidan_solved_list_api'),
    path('api-nidan/', views.api_nidan, name='api_nidan'),
    path('api-nidan/nidan-pending-data/',views.nidan_pending_data,name='nidan_pending_data'),
    path('api-nidan/nidan-sovled-data/',views. nidan_solved_data,name='nidan_solved_data'),
    path('nidan-ticket-data/<int:pk>/',views.nidanTicketData,name='nidan_ticket_data'),
    path('edit-profile/',views.userSettings,name='settings'),
    path('all-tickets/', views.allTicket, name='all_tickets'),
    path('open-tickets/',views.openticketslist,name='open_tickets'),
    path('reopen-tickets/',views.reopenticketslist,name='reopen_tickets'),
    path('resolved-tickets/',views.resolvedticketslist,name='resolved_tickets'),
    path('close-tickets/',views.closeticketslist,name='close_tickets'),
    path('create-ticket/', views.createTicket, name='create_ticket'),
    path('update-ticket/<str:pk>/', views.updateTicket, name='update_ticket'),
]