from django.urls import path, include
from . import views

app_name = 'consultation'

urlpatterns = [
    path('', views.home, name='home'),
    path('request-form/', views.consultation, name='index'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('consultation-requests/', views.requests_list, name='requests'),
    path('requests-history/', views.requests_history, name='requests_history'),
    path('answer/<int:id>/', views.consultation_page, name='consultation_page'),
    path('response/', views.consultation_response, name='response'),
    path('reject/<int:id>/', views.consultation_reject_page, name='reject_page'),
    path('reject/', views.consultation_reject, name='reject_save'),
    path('response/details/<int:id>/', views.consultation_response_details, name='response_details'),
    path('test-email/', views.test_email, name="test_email")
]
