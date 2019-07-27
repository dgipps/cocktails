from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from ingredients.models import Ingredient, IngredientCategory, Recipe
from ingredients.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def list(self, request):
        user = request.user

        available_categories = IngredientCategory.objects.filter(
            ingredients__inventories__user_id=user.id,
        )

        available_ingredients = Ingredient.objects.filter(
            inventories__user_id=user.id,
        ).values_list('id')
        print(available_ingredients)
        recipes = Recipe.objects.filter(
            ingredients__ingredient_id__in=available_ingredients,
        )
        print(recipes)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
