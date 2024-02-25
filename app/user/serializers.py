"""
Serializers for the users API VIEW
user/serializers
"""
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """Serializers for the user object"""

    class Meta:
        model = get_user_model()  # modelo que vamos a usar
        fields = ['email', 'password', 'name']  # los campos que vamos a recibir
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}  # argumentos extra para comprobaciones
        # el write only quiere decir que no se va a retornar el valor solo se va a escribir

    def create(self, validated_data):  # crea un objeto con los valores que se pasan
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)


    def update(self, instance, validated_data): #creamos un metodo para hacer la actualizacion, usamos
    #el serializador para encriptar la contraseña tambien
    #instance es la instancia que se actualiza
    #validated data es la informacion que ya se valido a traves del serializador
        """Update and return user"""
        password = validated_data.pop('password',None) #recupera la contraseña y luego la elimina, como es opcional colocamos el None
        user = super().update(instance,validated_data) #realiza todos los pasoss para actualizar el objeto

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authtentica the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate( #Va a hacer la validacion del usuario, sino es correcto regresa un objeto vacio
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authtenticated with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user #La informacion que le vamos a pasar a la vista
        return attrs
