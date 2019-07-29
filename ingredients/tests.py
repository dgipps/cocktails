from django.contrib.auth.models import User
from django.test import (Client, TestCase)
from rest_framework import status

from ingredients.models import (
    Ingredient,
    IngredientCategory,
    Recipe,
    RecipeIngredient,
)


class RecipeViewTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='test', password='password')

        self.recipe_have = Recipe.objects.create(name='Have Ingredients')
        self.recipe_exotic = Recipe.objects.create(name='Do Not Have Ingredients')

        self.lemon_juice = IngredientCategory.objects.create(
            name='Lemon Juice', specificity=1)
        self.juice = IngredientCategory.objects.create(
            name='Juice', specificity=2)
        self.london_dry = IngredientCategory.objects.create(
            name='London Dry Gin', specificity=1)
        self.gin = IngredientCategory.objects.create(
            name='Gin', specificity=2)
        self.simple_syrup = IngredientCategory.objects.create(
            name='Simple Syrup', specificity=1)
        self.syrup = IngredientCategory.objects.create(
            name='Syrup', specificity=2)

        self.ing_lemon_juice = Ingredient.objects.create(name='Lemon Juice')
        self.ing_lemon_juice.categories.set([self.lemon_juice, self.juice])
        self.ing_simple_syrup = Ingredient.objects.create(name='Simple Syrup')
        self.ing_simple_syrup.categories.set([self.simple_syrup, self.syrup])
        self.ing_beefeater = Ingredient.objects.create(name='Beefeater')
        self.ing_beefeater.categories.set([self.london_dry, self.gin])

        RecipeIngredient.objects.create(recipe=self.recipe_have, ingredient=self.ing_lemon_juice)
        RecipeIngredient.objects.create(recipe=self.recipe_have, ingredient=self.ing_simple_syrup)
        RecipeIngredient.objects.create(recipe=self.recipe_have, ingredient=self.ing_beefeater)

        self.client = Client()

    def test_get_basic_resume(self):
        self.client.login(username=self.user1.username, password=self.user1.password)
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    