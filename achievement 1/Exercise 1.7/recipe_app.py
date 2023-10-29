from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://cf-python:password@localhost/task_database")
Session = sessionmaker(bind = engine)
session = Session()

Base = declarative_base()



class Recipe(Base):
  __tablename__ = "final_recipes"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  ingredients = Column(String(255))
  cooking_time = Column(Integer)
  difficulty = Column(String(20))

  def __repr__(self):
    return "<Recipe ID: " + str(self.id) + "Name: " + str(self.name) + "Difficulty: " + str(self.difficulty)
  
  def __str__(self):
    output = (
      "Recipe ID: "
      + str(self.id)
      + "\n"
      + "Name: "
      + str(self.name)
      + "\n"
      + "Ingredients: "
      + str(self.ingredients)
      + "\n"
      + "Cooking Time: "
      + str(self.cooking_time)
      + "\n"
      + "Difficulty: "
      + str(self.difficulty)
      + "\n")
    return output
  
  def calculate_difficulty(self, ingredients, cooking_time):   
    if cooking_time < 10 and len(ingredients) < 4:
        self.difficulty = ('easy')
        
    elif cooking_time < 10 and len(ingredients) >= 4:
        self.difficulty = ('medium')
       
    elif cooking_time >= 10 and len(ingredients) < 4:
        self.difficulty = ('intermediate')

    elif cooking_time >=10 and len(ingredients) >= 4:
        self.difficulty = ('hard')
  

  #retrives the ingredients inside Recipe object
  def return_ingredients_as_list(self, ingredients):
     if self.ingredients == "":
      return []
     else:
        return self.ingredients.split(", ")
    

#create table ond database
Base.metadata.create_all(engine)


def create_recipe():
  name = str(input('Enter recipe name: '))
  while(len(name) > 50):
     name = str(input("This name is too long, enter another name again please: "))
  ingredients = []
  noOfIngredients = str(input("How many ingredients would you like to enter: "))
  while(not noOfIngredients.isnumeric()):
     noOfIngredients = str(input("This is not a number, please enter a number: "))
  for i in range(int(noOfIngredients)):
      ingredient = str(input("Please enter one ingredient: "))
      ingredients.append(ingredient)
 
  ingredients_string = ", ".join(ingredients)
  cookingTime_str = str(input("Please enter cooking time: "))
  while(not cookingTime_str.isnumeric()):
     cookingTime_str = str(input("This is not a number, please enter a number: "))
  cooking_time = int(cookingTime_str)
  recipe_entry = Recipe(
            name = name,
            cooking_time = cooking_time,
            ingredients = ingredients_string,
        )
  recipe_entry.calculate_difficulty(ingredients, cooking_time)
  session.add(recipe_entry)
  session.commit()

def view_all_recipes():
   recipes_list = session.query(Recipe).all()
   if len(recipes_list) == 0:
      return None
   for recipe in recipes_list:
      print(recipe)

def search_by_ingredients():
  if(session.query(Recipe).count() == 0):
    return None
  results = session.query(Recipe.ingredients).all()
  all_ingredients = []
  for result in results:
    tmp_list = result[0].split(", ")
    for item in tmp_list:
        if not item in all_ingredients:
          all_ingredients.append(item)
  print("All ingredients: ")
  for position, value in enumerate(all_ingredients):
    print(position, value)
  pick_ingredient = str(input("Pick ingredient(s) by number to begin a search with: "))
  numbers = pick_ingredient.split(", ")
  search_ingredients = []
  for number in numbers:
    if(int(number) > position):
      print("There is no ingredient with number %s", number)
      return None
    search_ingredients.append(all_ingredients[int(number)])
  conditions = []
  for ingredient in search_ingredients:
     like_term = "%" + str(ingredient) + "%"
     condition = Recipe.ingredients.like(like_term)
     conditions.append(condition)
  recipes = session.query(Recipe).filter(*conditions).all()
  print("The following recipes contain the ingredients you have picked: ")
  for recipe in recipes:
     print(recipe)


def edit_recipe():
  if(session.query(Recipe).count() == 0):
    return None
  results = session.query(Recipe.id, Recipe.name).all()
  print("The following recipes exist: ")
  for result in results:
     print("Recipe name: " +  result[1] + " Recipe ID: " + str(result[0]))
  chosenID = int(input("Please choose a recipe by picking an ID: "))
  recipe_exists = False
  for result in results:
     if(chosenID == result[0]):
      recipe_exists = True
  if not recipe_exists:
     return None
  recipe_to_edit = session.query(Recipe).get(chosenID)
  print("Chosen Recipe: ")
  print("1. Name: " + str(recipe_to_edit.name))
  print("2. Ingredients: " + str(recipe_to_edit.ingredients))
  print("3. Cooking time (min): " + str(recipe_to_edit.cooking_time))
  attribute_to_change = int(input("Please choose what you would like to change according to the number: "))
  if(attribute_to_change < 1 or attribute_to_change > 3):
     return None
  if(attribute_to_change == 1):
     new_name = str(input("Please enter the new name: "))  
     recipe_to_edit.name = new_name
  elif(attribute_to_change == 2):
    ingredients = []
    noOfIngredients = str(input("How many ingredients would you like to enter: "))
    while(not noOfIngredients.isnumeric()):
      noOfIngredients = str(input("This is not a number, please enter a number: "))
    for i in range(int(noOfIngredients)):
        ingredient = str(input("Please enter one ingredient: "))
        ingredients.append(ingredient)
    ingredients_string = ", ".join(ingredients)
    recipe_to_edit.ingredients = ingredients_string
    recipe_to_edit.calculate_difficulty(ingredients, recipe_to_edit.cooking_time)
  elif(attribute_to_change == 3):
    new_cooking_time = int(input("Please enter the new cooking time in minutes: "))  
    recipe_to_edit.cooking_time = new_cooking_time
    recipe_to_edit.calculate_difficulty(recipe_to_edit.return_ingredients_as_list(recipe_to_edit.ingredients), new_cooking_time)
  session.commit() 

def delete_recipe():  
  if(session.query(Recipe).count() == 0):
    return None
  results = session.query(Recipe.id, Recipe.name).all()
  print("The following recipes exist: ")
  for result in results:
     print("Recipe name: " +  result[1] + " Recipe ID: " + str(result[0]))
  chosenID = int(input("Please choose a recipe by picking an ID: "))
  recipe_exists = False
  for result in results:
     if(chosenID == result[0]):
      recipe_exists = True
  if not recipe_exists:
     return None
  recipe_to_delete = session.query(Recipe).get(chosenID)
  answer = str(input("Are you sure you want to delete the recipe? If so, enter 'yes': "))
  if (answer == "yes"):
     session.delete(recipe_to_delete)
     session.commit()
   
   

def main_menu():
  
  choice = ''
  while(choice != 'quit'):
    print('MAIN MENU')
    print('=====================================')
    print('Pick a choice:')
    print('1. Create a new recipe')
    print('2. View all recipes')
    print('3. Search for a recipes by ingredient')
    print('4. Update an existing recipe')
    print('5. Delete a recipe')
    print('Type "quit" to exit the program.')
    choice = input('Your choice: ')

    if choice == '1':
      create_recipe()
    elif choice == '2':
      view_all_recipes()
    elif choice == '3':
      search_by_ingredients()
    elif choice == '4':
      edit_recipe()
    elif choice == '5':
      delete_recipe()

main_menu()

