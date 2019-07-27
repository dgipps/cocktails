import csv
import re

from django.core.management.base import BaseCommand, CommandError

from ingredients.models import (
    Ingredient,
    IngredientCategory,
    Recipe,
    RecipeIngredient,
)


class Command(BaseCommand):
    help = 'Loads csv of Death & Co ingredients'

    def add_arguments(self, parser):
        parser.add_argument('-i', dest='filename', required=True,
                    help='input file with recipes', metavar='FILE')

    def handle(self, *args, **options):
        with open(options['filename'], 'r') as recipes:
            recipes_reader = csv.reader(recipes, delimiter=',')
            line_count = 0
            for row in recipes_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                    continue

                recipe_name = row[1]
                ingredient_name = row[2]
                category_names = row[4]
                page = row[5]
                instructions = row[6]

                if not (recipe_name and ingredient_name):
                    continue
                    ## todo: instructions can trail past recipe_name

                recipe = self.add_or_get_recipe(recipe_name, page)
                categories = self.add_or_get_categories(category_names)
                ingredient = self.add_or_get_ingredient(ingredient_name, categories)

                if not recipe.ingredients.filter(ingredient_id=ingredient.id).exists():
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                    )

                if instructions:
                    if recipe.instructions:
                        recipe.instructions = f'{recipe.instructions} {instructions}'
                    else:
                        recipe.instructions = instructions
                    recipe.save()

                line_count += 1



            print(f'Processed {line_count} lines.')

    def add_or_get_recipe(self, recipe_name, page):
        existing_recipe = Recipe.objects.filter(name=recipe_name).first()
        if existing_recipe:
            return existing_recipe

        reference = f'Death & Co Page: {page}'
        return Recipe.objects.create(name=recipe_name, reference=reference)

    def add_or_get_categories(self, category_names):
        specific_category_name = None
        general_category_name = None
        splits = re.split('(\(|\))', category_names)
        if len(splits) == 1:
            specific_category_name = category_names

        if len(splits) > 2:
            general_category_name = splits[0][:-1]
            if general_category_name not in ('OTHER'):
                specific_category_name = splits[2] + ' ' + general_category_name

        return (
            self.add_or_get_category(general_category_name, 2),
            self.add_or_get_category(specific_category_name, 1)
        )

    def add_or_get_category(self, category_name, specificity):
        if not category_name:
            return None

        existing_category = IngredientCategory.objects.filter(
            name=category_name).first()
        if existing_category:
            return existing_category

        return IngredientCategory.objects.create(name=category_name, specificity=specificity)

    def add_or_get_ingredient(self, ingredient_name, categories):
        existing_ingredient = Ingredient.objects.filter(name=ingredient_name).first()
        if existing_ingredient:
            return existing_ingredient

        ingredient = Ingredient.objects.create(name=ingredient_name)
        for category in categories:
            if category:
                ingredient.categories.add(category)
        ingredient.save()

        return ingredient
