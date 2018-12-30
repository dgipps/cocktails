from django.contrib import admin

from ingredients.models import (
    Ingredient,
    IngredientCategory,
    Inventory,
    Recipe,
)

admin.site.register(Ingredient)
admin.site.register(IngredientCategory)
admin.site.register(Recipe)
admin.site.register(Inventory)
