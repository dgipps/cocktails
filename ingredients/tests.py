from django.contrib.auth.models import User
from django.test import (Client, TestCase)
from rest_framework import status

from ingredients.models import (
    Ingredient,
    IngredientCategory,
    Inventory,
    Recipe,
    RecipeIngredient,
)
from ingredients.use_cases import get_possible_recipes

class RecipeTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='test', password='password')

        self.recipe_have = Recipe.objects.create(name='Have Ingredients')
        self.recipe_similar_gin = Recipe.objects.create(name='Almost Have Ingredients')
        self.recipe_diff_category_gin = Recipe.objects.create(name='Different Type of Gin')
        self.recipe_exotic = Recipe.objects.create(name='Do Not Have Ingredients')

        self._set_up_ingredients()

        self._add_ingredients_to_recipe(
            self.recipe_have,
            [self.ing_lemon_juice, self.ing_simple_syrup, self.ing_beefeater],
        )
        self._add_ingredients_to_recipe(
            self.recipe_similar_gin,
            [self.ing_lemon_juice, self.ing_simple_syrup, self.ing_tanqueray],
        )
        self._add_ingredients_to_recipe(
            self.recipe_diff_category_gin,
            [self.ing_lemon_juice, self.ing_simple_syrup, self.ing_plymouth],
        )
        self._add_ingredients_to_recipe(
            self.recipe_exotic,
            [self.ing_lemon_juice, self.ing_simple_syrup, self.ing_champagne],
        )

        self._add_inventory_for_user(
            self.user1,
            [self.ing_lemon_juice, self.ing_simple_syrup, self.ing_beefeater],
        )

    def _set_up_ingredients(self):
        self.lemon_juice = IngredientCategory.objects.create(
            name='Lemon Juice', specificity=1)
        self.juice = IngredientCategory.objects.create(
            name='Juice', specificity=2)
        self.london_dry = IngredientCategory.objects.create(
            name='London Dry Gin', specificity=1)
        self.plymouth = IngredientCategory.objects.create(
            name='Plymouth Gin', specificity=1)
        self.gin = IngredientCategory.objects.create(
            name='Gin', specificity=2)
        self.simple_syrup = IngredientCategory.objects.create(
            name='Simple Syrup', specificity=1)
        self.syrup = IngredientCategory.objects.create(
            name='Syrup', specificity=2)
        self.champagne = IngredientCategory.objects.create(
            name='Champagne', specificity=2)
        self.dry_champagne = IngredientCategory.objects.create(
            name='Dry Champagne', specificity=1)

        self.ing_lemon_juice = Ingredient.objects.create(name='Lemon Juice')
        self.ing_lemon_juice.categories.set([self.lemon_juice, self.juice])
        self.ing_simple_syrup = Ingredient.objects.create(name='Simple Syrup')
        self.ing_simple_syrup.categories.set([self.simple_syrup, self.syrup])
        self.ing_beefeater = Ingredient.objects.create(name='Beefeater')
        self.ing_beefeater.categories.set([self.london_dry, self.gin])
        self.ing_tanqueray = Ingredient.objects.create(name='Tanqueray')
        self.ing_tanqueray.categories.set([self.london_dry, self.gin])
        self.ing_plymouth = Ingredient.objects.create(name='Plymouth')
        self.ing_plymouth.categories.set([self.plymouth, self.gin])
        self.ing_champagne = Ingredient.objects.create(name='Fancy Champagne')
        self.ing_champagne.categories.set([self.dry_champagne, self.champagne])

    def _add_ingredients_to_recipe(self, recipe, ingredients):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient)

    def _add_inventory_for_user(self, user, ingredients):
        for ingredient in ingredients:
            Inventory.objects.create(user=user, ingredient=ingredient)

    def test_get_only_recipe_with_all_ingredients(self):
        recipes = get_possible_recipes(self.user1)
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0].id, self.recipe_have.id)

    def test_gets_close_recipes(self):
        recipes = get_possible_recipes(self.user1,specificity=1)
        self.assertEqual(len(recipes), 2)
        recipes_set = { recipe.id for recipe in recipes }
        self.assertEqual(recipes_set, {self.recipe_have.id, self.recipe_similar_gin.id})

    def test_gets_recipe_with_diff_gin(self):
        recipes = get_possible_recipes(self.user1,specificity=2)
        self.assertEqual(len(recipes), 3)
        recipes_set = { recipe.id for recipe in recipes }
        self.assertEqual(
            recipes_set,
            {self.recipe_have.id, self.recipe_similar_gin.id, self.recipe_diff_category_gin.id},
        )

    