"""
Views for the recipe APIs
"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
from recipe import serializers


class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # Es lo que se va a usar para unicamente obtener las recetas del usuario
        """Retrive recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(
            self):  # lo que hacemos es que como vamos a usar mucho el detail ponemos por defecto el DetailSerializer, en caso de
        # usar list simplemente regresamos ese serealizador
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer  # no ncesita los parentesis, si los pongemos va a regrear una instancia de la clase

        return self.serializer_class

    def perform_create(self, serializer):  # para la creacion de objetos
        """Create a new recipe"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Mange tags in database"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Mange ingredients database"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
