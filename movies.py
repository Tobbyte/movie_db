
"""
Disclaimer:
No ai was used
limitation:
passing around db is not fine and reassigning it in run not strictly necessary, but done for clarity

TODO:
  - unify input validation across features, f.e. update and add (out of scope of exercise)
"""

def main():
  # Dictionary to store the movies and the rating
  movies = {
      "The Shawshank Redemption": 9.5,
      "Pulp Fiction": 8.8,
      "The Room": 3.6,
      "The Godfather": 9.2,
      "The Godfather: Part II": 9.0,
      "The Dark Knight": 9.0,
      "12 Angry Men": 8.9,
      "Everything Everywhere All At Once": 8.9,
      "Forrest Gump": 8.8,
      "Star Wars: Episode V": 8.7
  }

  run(movies)



def list_movies(db: dict[str, float], descending = False, by_value = False):
  """ Returns a (optionally sorted descending by value) list of all db items """
  output(f"~~~ {len(db)} items total: ~~~", space_before=True)
  if not by_value:
    for k,v in sorted(db.items(), reverse=descending):
      output(f"{k}: {v}")
  else:
    for k,v in sorted(db.items(),key=lambda item: item[1], reverse=descending):
      output(f"{k}: {v}")

  output("~~~", space_after=True)


def is_num(inp: str):
  """ validates if a sting input is a valid number"""
  if inp == "":
      return False
  try:
    float(inp)
  except ValueError:
    return False
  return True


def add_movie(db):
  """
  Adds an item to db. No validation.
  TODO:
    - check if already exists, present option to update
  """
  name = None
  rating = None

  while name is None or name == "":
    name = input("\nEnter new movie name: ")
    if name == "":
      output("Name required")

  while rating is None or rating == "":
    rating = input("Enter new movies rating (0-10): ")
    if rating == "":
      output("Rating required")
    elif not is_num(rating):
      rating = None
      output("Rating must be a number")
    elif float(rating) > 10:
      rating = None
      output("Rating must be between 0 - 10")

  
  db[name] = float(rating)

  output(f"""Successfully added: "{name}": {rating}""", space_before=True, space_after=True)
  return db



def del_movie(db: dict[str, float]):
  """
  Removes an item from db 
  TODO:
    - implement search_movie()
  """

  tbdeleted = None

  while tbdeleted is None or tbdeleted == "":
    tbdeleted = input("\nEnter movie name to delete: ")
    if tbdeleted == "":
      output("Name required")
    try: 
      del db[tbdeleted]
      output(f'Successfully removed: "{tbdeleted}"', space_before=True, space_after=True)

      return db

    except KeyError:
      output(f"Movie {tbdeleted} doesn't exist!", space_before=True, space_after=True)
      break
  return db




def update_movie():
  """ Updates db item. No validation """
  pass


def get_statistics():
  """
  Gets statistic about provided data.
  Returns
  - median
  - top-ranked items
  - bottom-ranged items
  """


def get_random():
  """ Returns random item """
  pass


def search_movie():
  """ Searches for items. Not case sensitive """
  pass

def idle_after_input():
  """ idles with prompt to continue """
  input("press Enter to continue")
  return


def present_menu():
  """ Prints the menu to the user, asks for input, validates input"""
  output(
    "Menu: \n" \
    "1. List movies \n" \
    "2. Add movie \n" \
    "3. Delete movie \n" \
    "4. Update movie \n" \
    "5. Stats \n" \
    "6. Random movie \n" \
    "7. Search movie \n" \
    "8. Movies sorted by rating \n" \
    "9. Quit \n",
    space_before= True,
  )


  """ Options: 
  1. List movies, no input. Print. Return to menu.
  2. Add movie, single input:
    - str, int:[1-10] (not validated). Print new Entry. Return to menu.
  3. Delete movie, single input:
    - str. Print error or confirmation. Return to menu.
  4. Update movie, multi input:
      1.: str. Print error if not found. Return to menu.
      2.: int:[1-10] (not validated). Print new Entry. Return to menu.
  5. Stats, no input. Print. Return to menu.
  6. Random movie, no input. Print. Return to menu.
  7. Search movie, single input:
    - str. Print error or results. Return to menu.
  8. List movies sorted descending, no input. Print. Return to menu.
  9. Exit.
  """

  selection = input("Enter choice (1-9): ")

  if len(selection) > 1 or not selection.isdecimal():
    output("Invalid input (Enter 0 - 9. Try again)", space_before=True, space_after=True)
    return False
  
  ## TODO
  
  output("\nselected munu item x")
  
  return int(selection)



def output(any, space_after = False, space_before = False):
  """ Outputs para """
  if space_before: print("\n \n")
  print(any)
  if space_after: print("\n \n")


def run(db: dict[str, float]):
  """ Prints welcome and loops menu """
  output("********** My Movies Database **********",space_before=True)
  while True:
    selection = present_menu()

    if selection == 1:
      """ list """
      list_movies(db)
    elif selection == 2:
      """ add """
      db = add_movie(db)
    elif selection == 3:
      """ delete """
      db = del_movie(db)
    elif selection == 8:
      """ list by rating """
      list_movies(db, descending=True, by_value=True)

    elif selection == 9:
      output("Goodbye")
      return False
    #do

    idle_after_input()
    
    





if __name__ == "__main__":
  main()
