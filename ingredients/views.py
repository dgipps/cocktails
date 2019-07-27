from rest_framework import viewsets

from ingredients.models import Ingredient, IngredientCategory, Recipe
from ingredients.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def list(self, request):
        user = request.user

        available_categories = IngredientCategory.objects.filter(
            ingredients__inventories__user_id=user.id
        )

        available_ingredients = Ingredient.objects.filter(

        )
        recipes = Recipe.objects.filter(

        )
        serializer = RecipeSerializer(recipes, many=True)
