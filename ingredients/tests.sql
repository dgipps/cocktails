SELECT * FROM ingredients_recipe
INNER JOIN ingredients_recipeingredient on ingredients_recipe.id = ingredients_recipeingredient.recipe_id
INNER JOIN ingredients_ingredient_categories as ic1 on ingredients_recipeingredient.ingredient_id = ic1.ingredient_id
WHERE NOT EXISTS (
    SELECT NULL
    FROM ingredients_ingredient_categories as ic2
    WHERE ic1.ingredientcategory_id = ic2.ingredientcategory_id
    AND ic2.specificity = 1
    AND ic2.ingredientcategory_id NOT IN (
        SELECT DISTINCT("ingredients_ingredientcategory"."id")
        FROM "ingredients_ingredientcategory"
        INNER JOIN "ingredients_ingredient_categories" ON ("ingredients_ingredientcategory"."id" = "ingredients_ingredient_categories"."ingredientcategory_id")
        INNER JOIN "ingredients_ingredient" ON ("ingredients_ingredient_categories"."ingredient_id" = "ingredients_ingredient"."id")
        INNER JOIN "ingredients_inventory" ON ("ingredients_ingredient"."id" = "ingredients_inventory"."ingredient_id")
        WHERE ("ingredients_inventory"."user_id" = 2 AND "ingredients_ingredientcategory"."specificity" = 1)
    )
);

SELECT * FROM ingredients_recipe
INNER JOIN ingredients_recipeingredient on ingredients_recipe.id = ingredients_recipeingredient.recipe_id
INNER JOIN ingredients_ingredient_categories as ic1 on ingredients_recipeingredient.ingredient_id = ic1.ingredient_id
WHERE NOT EXISTS (
    SELECT NULL
    FROM ingredients_ingredientcategory as ic2
    WHERE ic1.ingredientcategory_id = ic2.id
    AND ic2.specificity = 1
    AND ic2.id NOT IN (
        SELECT DISTINCT("ingredients_ingredientcategory"."id")
        FROM "ingredients_ingredientcategory"
        INNER JOIN "ingredients_ingredient_categories" ON ("ingredients_ingredientcategory"."id" = "ingredients_ingredient_categories"."ingredientcategory_id")
        INNER JOIN "ingredients_ingredient" ON ("ingredients_ingredient_categories"."ingredient_id" = "ingredients_ingredient"."id")
        INNER JOIN "ingredients_inventory" ON ("ingredients_ingredient"."id" = "ingredients_inventory"."ingredient_id")
        WHERE ("ingredients_inventory"."user_id" = 2 AND "ingredients_ingredientcategory"."specificity" = 1)
    )
)
GROUP BY ingredients_recipe.id;