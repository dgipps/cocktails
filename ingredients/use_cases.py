from ingredients.models import Recipe

def get_possible_recipes(user, specificity=None):
    """
        Return a QuerySet of the Recipes possible for the given user with their inventory
    """
    if specificity:
        return Recipe.objects.raw(
            f'''
            SELECT *
            FROM "ingredients_recipe" as IR
            WHERE NOT EXISTS (
                SELECT RI."ingredient_id" FROM "ingredients_recipeingredient" RI
                JOIN "ingredients_ingredient_categories" ON "ingredients_ingredient_categories".ingredient_id = RI."ingredient_id"
                JOIN "ingredients_ingredientcategory" ON "ingredients_ingredientcategory".id = "ingredients_ingredient_categories".ingredientcategory_id
                WHERE specificity = {specificity}
                AND "ingredients_ingredient_categories".ingredientcategory_id NOT IN (
                    SELECT "ingredientcategory_id" FROM "ingredients_ingredient_categories"
                    JOIN "ingredients_inventory" ON "ingredients_inventory".ingredient_id = "ingredients_ingredient_categories".ingredient_id
                    JOIN "ingredients_ingredientcategory" ON "ingredients_ingredientcategory".id = "ingredients_ingredient_categories".ingredientcategory_id
                    WHERE user_id = {user.id} AND specificity = {specificity}
                ) AND
                IR."id" = RI."recipe_id"
            )
            '''
        )

    return Recipe.objects.raw(
        f'''
        SELECT *
        FROM "ingredients_recipe" as IR
        WHERE NOT EXISTS (
            SELECT V1."ingredient_id" FROM "ingredients_recipeingredient" V1
                WHERE V1."ingredient_id" NOT IN (
                    SELECT ingredient_id from ingredients_inventory where user_id = {user.id}
                ) AND
                IR."id" = V1."recipe_id"
        )
        '''
    )