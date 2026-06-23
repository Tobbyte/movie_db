from random import randint

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

def sort_by_value(dic: dict[str, float], reverse = False ):
  return sorted(dic.items(),key=lambda item: item[1], reverse=reverse)


def list_movies(db: dict[str, float], descending = False, by_value = False):
  """ Returns a (optionally sorted descending by value) list of all db items """
  output(f"~~~ {len(db)} items total: ~~~", space_before=True)
  if not by_value:
    for k,v in sorted(db.items(), reverse=descending):
      output(f"{k}: {v}")
  else:
    for k,v in sort_by_value(db, reverse= descending):
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




def update_movie(db: dict[str, float]):
  """ Updates db item. No validation """
  tbupdated = None
  new_rating = None
  while tbupdated is None or tbupdated == "":
    tbupdated = input("\nEnter movie name to update: ")
    if tbupdated == "":
      output("Name required")
    try: 
      db[tbupdated]
    except KeyError:
      output(f"Movie {tbupdated} doesn't exist!", space_before=True, space_after=True)
      return db

  while new_rating is None or new_rating == "":
    new_rating = input("Enter new movies rating (0-10): ")
    if new_rating == "":
      output("Rating required")
    elif not is_num(new_rating):
      new_rating = None
      output("Rating must be a number")
    elif float(new_rating) > 10:
      new_rating = None
      output("Rating must be between 0 - 10")
  
  output(f'Successfully updated: "{tbupdated}": {new_rating}', space_before=True, space_after=True)
  return db


def get_average(nums: list[float]):
  return sum(nums) / len(nums)


def get_median(nums: list[float]):
  sorted_nums = sorted(nums)
  if len(sorted_nums) %2 != 0:
    return sorted_nums[len(sorted_nums)//2]
  else:
    centeri = len(sorted_nums) // 2
    return get_average(sorted_nums[centeri-1:centeri+1])


def get_statistics(db: dict[str, float]):
  """
  Gets statistic about provided data.
  Returns
  - median
  - top-ranked items
  - bottom-ranged items
  """

  val_list = list(db.values())
  avg = get_average(val_list)
  median = get_median(sorted(val_list))
  best_name, best_rat = sort_by_value(db)[-1]
  worst_name, worst_rat = sort_by_value(db)[0]

  output(f"Average rating: {avg}", space_before=True)
  output(f"Median rating: {median}")
  output(f'Best movie: "{best_name}", {best_rat}')
  output(f'Worst movie: "{worst_name}", {worst_rat}', space_after=True)


def get_random(db):
  """ Returns random movie """

  name, rating = list(db.items())[randint(0, len(db)-1)]
  output(f"Your movie for tonight: {name}, it's rated {rating}", space_after=True)


def search_movie(db: dict[str, float]):
  """ Searches for items. Not case sensitive """
  inp = None
  while inp is None or inp == "":
    inp = input("\nEnter part of movie name: ").lower()
    if inp == "":
      output("Name required")
  
  res = [(k, v) for k, v in db.items() if k.lower().find(inp) != -1]

  if not res:
    output(f'No Movie name contains "{inp}":\n', space_before=True)
  else :
    output(f'Movie titles containing "{inp}":\n', space_before=True)
    for r in res:
      output(f"{r[0]}, {r[1]}")

  

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
    elif selection == 4:
      """ update """
      db = update_movie(db)
    elif selection == 5:
      """ stats """
      get_statistics(db)
    elif selection == 6:
      """ random """
      get_random(db)
    elif selection == 7:
      """ search """
      search_movie(db)
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
