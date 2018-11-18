from django.db import models

# Create your models here.

class IngredientCategory(models.Model):
    SPECIFICITY_CHOICES = (
        (1, 'Interchangeable'),
        (2, 'Similar'),
        (3, 'Classification')
    )
    name = models.CharField(max_length=128, unique=True)
    specificity = models.IntegerField(choices=SPECIFICITY_CHOICES)


class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    categories = models.ManyToManyField(IngredientCategory, related_name='ingredients')


class Recipe(models.Model):
    name = models.CharField(max_length=128, unique=True)
    reference = models.CharField(max_length=128)
    instructions = models.CharField(max_length=256)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='recipes', on_delete=models.CASCADE)
