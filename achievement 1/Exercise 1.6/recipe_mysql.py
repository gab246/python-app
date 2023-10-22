import mysql.connector

def calculate_difficulty(cooking_time, ingredients):     
    if cooking_time < 10 and ingredients < 4:
        difficulty = ('easy')
        
    elif cooking_time < 10 and ingredients >= 4:
        difficulty = ('medium')
       
    elif cooking_time >= 10 and ingredients < 4:
        difficulty = ('intermediate')

    elif cooking_time >=10 and ingredients >= 4:
        difficulty = ('hard')
        
    return difficulty

def create_recipe(conn, cursor):
  name = str(input('Enter recipe name: '))
  ingredients = str(input('Enter ingredients: '))
  ingredients = ingredients.split(", ")
  cooking_time = int(input('Enter cooking time (minutes): '))
  difficulty = calculate_difficulty(cooking_time, len(ingredients))
  ingredients_string = ", ".join(ingredients)
  query_string = "INSERT INTO recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s);"
  val = (name, ingredients_string, cooking_time, difficulty)
  cursor.execute(query_string, val)
  conn.commit()

def search_recipe(conn, cursor):
  cursor.execute("SELECT ingredients FROM recipes")
  results = cursor.fetchall()
  all_ingredients = []
  for element in results:
    ingredients = element[0].split(', ')
    for ingredient in ingredients:
        if not ingredient in all_ingredients:
          all_ingredients.append(ingredient)
  for position, value in enumerate(all_ingredients):
    print(position, value)
  pick_ingredient = int(input("Pick a ingredient by number to begin a search with: "))
  print(pick_ingredient)
  search_ingredient = all_ingredients[pick_ingredient]
  cursor.execute("SELECT name FROM recipes WHERE ingredients LIKE %s", ("%" + search_ingredient + "%", ))
  results = cursor.fetchall()
  print("The following repices contain " + search_ingredient + ": ")
  for recipe_name in results:
     print(recipe_name[0])

def update_recipe(conn, cursor):
  cursor.execute("SELECT * FROM recipes")  
  results = cursor.fetchall()
  print("The following recipes exist: ")
  for result in results:
     print(result)
  recipe_to_change = -1
  while recipe_to_change == -1:
    id = int(input("Pick the ID of the recipe you want to change: "))
    for result in results:
      if result[0] == id:
          recipe_to_change = result
    if recipe_to_change == -1:
        print("The recipe ID you picked does not exist")    
  print("You chose recipe " + str(recipe_to_change))
  print("You can change the following parts of the recipe: ")
  print("1: name")
  print("2: cooking time")
  print("3: ingredients")
  change = int(input("Please pick a number: "))
  if(change == 1):
    new_name = str(input("Please enter the new name: "))
    cursor.execute("UPDATE recipes SET name = %s WHERE id = %s", (new_name, id))
  elif(change == 2):
    new_cooking_time = int(input("Please enter the new cooking time: ")) 
    cursor.execute("UPDATE recipes SET cooking_time = %s WHERE id = %s", (str(new_cooking_time), id))
    ingredients = recipe_to_change[2].split(", ")
    new_difficulty = calculate_difficulty(new_cooking_time, len(ingredients))
    cursor.execute("UPDATE recipes SET difficulty = %s WHERE id = %s", (new_difficulty, id))
  elif(change == 3):
    new_ingredients = str(input("Please enter all ingredients for the recipe: "))     
    cursor.execute("UPDATE recipes SET ingredients = %s WHERE id = %s", (new_ingredients, id))
    cooking_time = int(recipe_to_change[3])
    new_difficulty = calculate_difficulty(cooking_time, len(new_ingredients.split(", ")))
    cursor.execute("UPDATE recipes SET difficulty = %s WHERE id = %s", (new_difficulty, id))    
  conn.commit()

def delete_recipe(conn, cursor):
  cursor.execute("SELECT * FROM recipes")  
  results = cursor.fetchall()
  print("The following recipes exist: ")
  for result in results:
     print(result)
  id = str(input("Pick the ID of the recipe you want to delete: "))
  cursor.execute("DELETE FROM recipes where id = %s", (id, ))
  conn.commit()


def main_menu(conn, cursor):
  choice = ''
  while(choice != 'quit'):
    print('MAIN MENU')
    print('=====================================')
    print('Pick a choice:')
    print('1. Create a new recipe')
    print('2. Search for a recipe by ingredient')
    print('3. Update an existing recipe')
    print('4. Delete a recipe')
    print('Type "quit" to exist the program.')
    choice = input('Your choice: ')

    if choice == '1':
      create_recipe(conn, cursor)
    elif choice == '2':
      search_recipe(conn, cursor)
    elif choice == '3':
      update_recipe(conn, cursor)
    elif choice == '4':
      delete_recipe(conn, cursor)


   

conn = mysql.connector.connect(
          host='localhost', 
          user='cf-python', 
          passwd='password')

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS recipes(
               id             INT PRIMARY KEY AUTO_INCREMENT,
               name           VARCHAR(50),
               ingredients    VARCHAR(255),
               cooking_time   INT,
               difficulty     VARCHAR(20)       
)''')

conn.commit()

main_menu(conn, cursor)

