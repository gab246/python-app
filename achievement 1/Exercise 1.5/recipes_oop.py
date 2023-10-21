class recipe (object):
  def __init__ (self, name, ingredients, cooking_time):
    self.name = name,
    self.ingredients = ingredients,
    self.cooking_time = cooking_time,
    self.difficulty = self.calculate_difficulty()
    self.all_ingredients = []
    
  def calculate_difficulty(self):
    if self.cooking_time < 10 and len(self.ingredients) < 4:
      self.difficulty = "easy"
    elif self.cooking_time < 10 and len(self.ingredients) >= 4:
      self.difficulty = "medium"
    elif self.cooking_time >= 10 and len(self.ingredients) < 4:
      self.difficulty = "intermediate"
    elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
      self.difficulty = "hard"

  def __init__(self, name):
    self.name = name
    self.ingredients = []
    self.cooking_time = 0
    self.difficulty = ""
    self.all_ingredients = []

  def get_name(self):
    output = str(self.name)
    return output
  
  def set_name(self, name):
    self.name = name

  def get_cooking_time(self):
    output = str(self.cooking_time)
    return output

  def set_cooking_time(self, cooking_time):
    self.cooking_time = cooking_time


  def add_ingredients(self, ingredients):
    for ingredient in ingredients:
      self.ingredients.append(ingredient)
    self.update_all_ingredients()

  def get_ingredients(self):
    ingredients = [self.ingredients]
    return ingredients

  def get_difficulty(self):
    if self.difficulty == "":
      self.calculate_difficulty()
    return self.difficulty

  def search_ingredients(self, ingredient):
    if ingredient in self.ingredients:
      return True
    else: 
      return False

  def update_all_ingredients(self):
    for ingredient in self.ingredients:
      if not ingredient in self.all_ingredients:
        self.all_ingredients.append(ingredient)
      
  def __str__(self):
    ingredient_pretty_string = ""
    for ingredient in self.ingredients:
      ingredient_pretty_string = ingredient_pretty_string + " - " + ingredient + "\n" 
    output = "Recipe Name: " + str(self.name) + "\n" + "Ingredients: " + "\n" + ingredient_pretty_string + \
            "Cooking Time (minutes): " + str(self.cooking_time) + "\n" + "Difficulty: " + self.get_difficulty() + "\n" + "--------------------"
    return output
    

def recipe_search(data, search_term):
  for recipe in data:
    if recipe.search_ingredients(search_term):
      print(recipe)


tea = recipe("Tea")
tea.add_ingredients(["tea leaves", "sugar", "water"])
tea.set_cooking_time(5)
print(tea)

coffee = recipe("Coffee")
coffee.add_ingredients(["coffee powder", "sugar", "water"])
coffee.set_cooking_time(5)
print(coffee)

cake = recipe("Cake")
cake.add_ingredients(["sugar", "butter", "eggs", "vanilla essence", "flour", "baking flour", "milk"])
cake.set_cooking_time(50)
print(cake)

banana_smoothie = recipe("Banana Smoothie")
banana_smoothie.add_ingredients(["bananas", "milk", "peanut butter", "sugar", "ice cubes"])
banana_smoothie.set_cooking_time(5)
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]
print("Recipes containing water")
recipe_search(recipes_list, "water")
print("Recipes containing sugar")
recipe_search(recipes_list, "sugar")
print("Recipes containing bananas")
recipe_search(recipes_list, "bananas")