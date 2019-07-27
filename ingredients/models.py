from django.contrib.auth.models import User
from django.db import models


class IngredientCategory(models.Model):
    SPECIFICITY_CHOICES = (
        (1, 'Interchangeable'),
        (2, 'Similar'),
        (3, 'Classification')
    )
    name = models.CharField(max_length=128, unique=True)
    specificity = models.IntegerField(choices=SPECIFICITY_CHOICES)

    class Meta:
        verbose_name_plural = "ingredient categories"


class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    categories = models.ManyToManyField(IngredientCategory, related_name='ingredients')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=128, unique=True)
    reference = models.CharField(max_length=128)
    instructions = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='recipes', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "recipe ingredients"


class Inventory(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='inventories')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventories')

    def __str__(self):
        return str(self.ingredient)

    class Meta:
        verbose_name_plural = "inventories"
