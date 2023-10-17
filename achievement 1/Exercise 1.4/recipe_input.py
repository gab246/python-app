import pickle


def take_recipe():
    name = str(input('Recipe name: ' ))
    cooking_time = int(input('Recipe time (min): '))
    ingredients = input('Ingredients: ' )
    ingredients_shopping = ingredients.split()
    
    recipe = { 
        'name': name, 
        'cooking_time': cooking_time, 
        'ingredients': ingredients_shopping, 
        'Difficulty': calc_difficulty(cooking_time, len(ingredients_shopping))
      } 
    return recipe
    
def calc_difficulty(cooking_time, ingredients):     
    if cooking_time < 10 and ingredients < 4:
        difficulty = ('easy')
        
    elif cooking_time < 10 and ingredients >= 4:
        difficulty = ('medium')
       
    elif cooking_time >= 10 and ingredients < 4:
        difficulty = ('intermediate')

    elif cooking_time >=10 and ingredients >= 4:
        difficulty = ('hard')
        
    return difficulty
    
    
    
try: 
    my_file = str(input('Enter a file name: '))
    with open(my_file, 'rb') as my_file_handle:
        data = pickle.load(my_file_handle)
    

    
except FileNotFoundError:
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
    
except:
    data = {
       'recipes_list': [],
       'all_ingredients': []
    }

else:
    my_file_handle.close()

finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']



n = int(input('How many recipes would you like to enter? '))
for i in range(n):
    recipe = take_recipe()
    recipes_list.append(recipe)

    for ingredient in recipe['ingredients']:
        if not ingredient in all_ingredients:
          all_ingredients.append(ingredient)

data = {
    'recipes_list': recipes_list,
    'all_ingredients': all_ingredients
}

with open(my_file, 'wb') as my_file_handle:
    pickle.dump(data, my_file_handle)
    my_file_handle.close()