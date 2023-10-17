import pickle

def display_recipe(recipe):
    print('Name: ', recipe['name']),
    print('Cooking time (min): ', recipe['cooking_time']),
    print('Ingredients: ', recipe['ingredients']),
    print('Difficulty: ', recipe['Difficulty']),


def search_ingredient(data):
  ingredients = data['all_ingredients']
  
  for position, value in enumerate(ingredients):
    print(position, value)

  try:
    number = int(input('Choose a number from the list: '))
    ingredient_searched = ingredients[number]

  except: 
    print('Input is incorrect')
  
  else: 
    for recipe in data['recipes_list']:
      if ingredient_searched in recipe['ingredients']:
        display_recipe(recipe)


my_file = str(input('Enter the name of the file that contains the recipes: '))
try:
  with open(my_file, 'rb') as my_file_handle:
    data = pickle.load(my_file_handle)

except FileNotFoundError:
  print('File not found')

else:
  search_ingredient(data)

