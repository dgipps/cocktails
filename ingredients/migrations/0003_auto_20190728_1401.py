# Generated by Django 2.1.4 on 2019-07-28 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0002_inventory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientcategory',
            options={'verbose_name_plural': 'ingredient categories'},
        ),
        migrations.AlterModelOptions(
            name='inventory',
            options={'verbose_name_plural': 'inventories'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name_plural': 'recipe ingredients'},
        ),
        migrations.AlterField(
            model_name='inventory',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventories', to='ingredients.Ingredient'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventories', to=settings.AUTH_USER_MODEL),
        ),
    ]
