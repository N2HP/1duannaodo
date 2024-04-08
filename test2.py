from fatsecret import Fatsecret

CONSUMER_KEY = '7d84a387593e4412ae6646facc9ddc3f'
CONSUMER_SECRET = '246887260e314652b1fec29f8412ad05'
fs = Fatsecret(CONSUMER_KEY, CONSUMER_SECRET)
#recipe_id = 478271
#recipe_data = fs.food_get(food_id=recipe_id)

recipe_data = fs.recipe_types_get()
#recipe_data = fs.recipe_get(recipe_id=recipe_id)
#recipe_data=fs.foods_search(search_expression='egg')



print(recipe_data)
