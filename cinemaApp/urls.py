from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sessions/', views.all_sessions, name='list-sessions'),
    path('add_session', views.add_session, name='add-session'),
    path('my_tickets', views.my_tickets, name='my-tickets'),
    path('session/<session_id>', views.show_session, name='show-session'),
    path('ajax/load-halls/', views.load_halls,
         name='ajax_load_halls'),
]
