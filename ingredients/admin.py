from django.contrib import admin

from ingredients.models import (
    Ingredient,
    IngredientCategory,
    Recipe,
)

admin.site.register(Ingredient)
admin.site.register(IngredientCategory)
admin.site.register(Recipe)
