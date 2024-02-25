"""
Urls mappings for the recipe app
"""
from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter  # crear las rutas para las apis
from recipe import views

router = DefaultRouter()  # creamos el router por defecto
router.register('recipes',
                views.RecipeViewSet)  # agregamos la ruta de recipes, con esto se permiten todas las acciones HTTP
app_name = 'recipe'  # para identificar a la ruta con el reverse

router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
urlpatterns = [
    path('', include(router.urls))
]
