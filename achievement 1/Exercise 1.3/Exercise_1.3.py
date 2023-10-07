recipes_list = []
ingredients_list = []

def take_recipe():
    name = str(input('Recipe name: ' ))
    cooking_time = int(input('Recipe time (min): '))
    ingredients = input('Ingredients: ' )
    ingredients_shopping = ingredients.split()
    recipe = { 'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients_shopping}
    return recipe
   

n = int(input('How many recipes would you like to enter? '))
for i in range(n):
    recipe = take_recipe()
    recipes_list.append(recipe)

    for ingredient in recipe['ingredients']:
        if not ingredient in ingredients_list:
          ingredients_list.append(ingredient)

        


for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        difficulty = 'Difficulty Level: ' 'Easy'
        
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        difficulty = 'Difficulty Level: ' 'Medium'

    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        difficulty = 'Difficulty Level: ' 'Intermediate'

    elif recipe['cooking_time'] >=10 and len(recipe['ingredients']) >= 4:
        difficulty = ('Difficulty Level: ' 'Hard')


    print('------------------------------------------')
    print('Recipe: ' + recipe['name'])
    print('Cooking Time (min): ' + str(recipe['cooking_time']))
    print('Ingredients: ')
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print(difficulty)
  
def print_ingredients():
    ingredients_list.sort()
    print('------------------------------------------')
    print('Ingredients Available Across All Recipes')
    for ingredient in ingredients_list:
        print(ingredient)
      
print_ingredients()