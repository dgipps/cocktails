from ingredients.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('name', 'reference', 'ingredients')

    def get_ingredients(self, obj):
        return [r_ing.ingredient.name for r_ing in obj.ingredients.all()]
