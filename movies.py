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

  init()

def present_menu():
  """prints the menu to the user"""
  output("here will be -dragons- menu")
  return False

def output(strg):
  """outputs input"""
  print(strg)

def init():
  """prints welcome and loops menu"""
  output("********** My Movies Database **********")
  while True:
    return present_menu()

if __name__ == "__main__":
  main()
