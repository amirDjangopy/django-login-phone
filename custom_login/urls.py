from django.urls import path
from .views import register_view, verify, dashboard

app_name="custom_login"

urlpatterns = [
    path('', register_view, name='register_view'),
    path('verify/', verify, name='verify'),
    # path('login/', views.mobile_login, name='mobile_login'),
    path('dashboard/', dashboard, name='dashboard'),
]
