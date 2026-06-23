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



def list_db(sorted = False):
  """ Returns a (sorted descending) list of all db items """
  pass


def add_item(new_item):
  """ Adds an item to db. No validation. """
  pass


def del_item(del_item):
  """ Removes an item from db """
  pass


def update_item():
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


def search_item():
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
    output("Invalid input (Enter 0 - 9. Try again)")
    return True
  
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

    if selection == 9:
      output("Goodbye")
      return False
    #do

    idle_after_input()
    
    





if __name__ == "__main__":
  main()
