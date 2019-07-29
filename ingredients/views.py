from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from ingredients.models import Ingredient, IngredientCategory, Recipe
from ingredients.serializers import RecipeSerializer
from ingredients.use_cases import get_possible_recipes


class RecipeViewSet(viewsets.ViewSet):

    def list(self, request):
        user = request.user
        specificity = request.GET.get('specificity')
        recipes = get_possible_recipes(user, specificity=specificity)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
