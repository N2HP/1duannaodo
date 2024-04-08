from fatsecret import Fatsecret

CONSUMER_KEY = '7d84a387593e4412ae6646facc9ddc3f'
CONSUMER_SECRET = '246887260e314652b1fec29f8412ad05'
fs = Fatsecret(CONSUMER_KEY, CONSUMER_SECRET)
#recipe_id = 69320053
#recipe_data = fs.food_get(food_id=recipe_id)

#recipe_data = fs.recipe_types_get()
#recipe_data = fs.recipe_get(recipe_id=recipe_id)
recipe_data =fs.recipes_search(search_expression='', recipe_type='Main Dish', page_number=1, max_results=20)
#recipe_data=fs.foods_search(search_expression='egg')
print(recipe_data)


'''
recipe_types = 'recipe_types'  # Đảm bảo rằng 'recipe_types' đã được định nghĩa trước đó
recipe_type = 'recipe_type'  # Đảm bảo rằng 'recipe_type' đã được định nghĩa trước đó
p=','.join(recipe_data['recipe_types']['recipe_type'])
p = recipe_data[recipe_types][recipe_type]
'''





































