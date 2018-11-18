from django.db import models

# Create your models here.

class Ingredient(models.model):
    name = models.charField(length=128)
    categories = models.ManyToManyField(IngredientCategory)


class IngredientCategory(models.model):
    SPECIFICITY_CHOICES = (
        (1, 'Interchangeable'),
        (2, 'Similar'),
        (3, 'Classification')
    )
    name = models.charField(length=128)
    specificity = models.integerField(choices=SPECIFICITY_CHOICES)


class Recipe(models.model):
    name = models.charField(length=128)
    reference = models.charField(length=128)
    instructions = models.charField(length=256)


class RecipeIngredient(models.model):
    recipe = models.foreignKey(Recipe, reverse_name='ingredients')
    ingredient = models.foreignKey(Ingredient, reverse_name='recipes')
