import sqlite3, bcrypt, random
def main(usern, access):
  if access == 0:
    print(f"The account {usern} is banned. You probably did something silly.")
    input('Press enter to make a new account...')
    portal(False, None)
  elif access == 1:
    userType = 'Guest'
  elif access == 2:
    userType = 'User'
  elif access == 3:
    userType = 'VIP'
  elif access == 4:
    userType = 'Moderator'
  input(f"Welcome [{userType}]{usern}! You made it to the main program!")
  return
def portal(loggedIn, usern):
  if not loggedIn:
    while True:
      choice = input('Login, signup or continue as a guest? (L/S/G): ')
      if choice.upper() == 'L':
        login()
      elif choice.upper() == 'S':
        signup()
      elif choice.upper() == 'G':
        usern = guestID()
        permission = 1
        break
      else:
        print("Try again, this time either choose 'L', 'S' or 'G'.")
  else:  # Logged in
    permission = getPermission(usern)
  main(usern, permission)
def guestID():
  while True:
    ID = f'{random.randrange(1, 10**6):03}'
    if ID in used:
      guestID()
  used.append(ID)
  return ID
def login():
  print('Login page:')
  while True:
    usern = input('Enter a username: ')
    duplicate = userExists(usern)
    if usern.upper() == 'CANCEL':
      return
    elif duplicate:
      break
    else:
      print(
        "That user doesn't exist, try something else or type 'CANCEL' to quit."
      )
  passw = input("Enter your password: ")
  connection = sqlite3.connect('users.db')
  c = connection.cursor()
  c.execute("SELECT password FROM users WHERE UPPER(username) = ?",
            (usern.upper(), ))
