"""
Views for the user API
"""
from rest_framework import generics,authentication,permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer,AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer #Usamos este serializer porque modificamos al usuario y la forma de autenticacion es correo y contraseña
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES #para hacer la renderizacion por defecto


#Clase que va a permitir la actualizacion del usuario
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrive and return the authenticated user"""
        return self.request.user