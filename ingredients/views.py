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

        # available_categories = IngredientCategory.objects.filter(
        #     ingredients__inventories__user_id=user.id,
        # )
        recipes = Recipe.objects.raw(
            f'''
            SELECT *
            FROM "ingredients_recipe" as IR
            WHERE NOT EXISTS (
                SELECT V1."ingredient_id" FROM "ingredients_recipeingredient" V1
                    WHERE V1."ingredient_id" NOT IN (
                        SELECT ingredient_id from ingredients_inventory where user_id = {user.id}
                    ) AND
                    IR."id" = V1."recipe_id"
            )
            '''
        )
        print(recipes)
        serializer = RecipeSerializer(recipes, many=True)
        print(serializer)
        return Response(serializer.data)
