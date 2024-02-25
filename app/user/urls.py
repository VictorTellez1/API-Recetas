"""
URL mappings for the users API
"""
from django.urls import path
from user import views

app_name = 'user'  # esto lo usamos para que haga match con el test
# CREATE_USER_URL = reverse('user:create')  # el endpoint va a ser el de crear

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me')
]
