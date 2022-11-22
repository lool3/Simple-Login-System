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
    break
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
  if bcrypt.checkpw(passw.encode(), c.fetchone()[0]):
    portal(True, usern)
    exit()
  else:
    print("Wrong password!")
    login()


def signup():
  print('Signup page:')

  while True:
    usern = input('Enter a new username: ')
    duplicate = userExists(usern)
    if duplicate:
      print('Username already exists')
      continue
    elif len(usern) < 5:
      print('Username must be more than 5 characters')
      continue
    elif any(not c.isalnum() for c in usern):
      print('Your username must be made of alphanumeric characters only')
      continue
    else:
      break

  while True:
    passw = input('Enter a password: ')
    if not any(x.isupper() for x in passw):
      print('Your password must contain an uppercase character')
      continue
    elif not any(x.islower() for x in passw):
      print('Your password must contain a lowercase character')
      continue
    elif not any(c.isalnum() for c in usern):
      print('Your password must contain at least one digit')
      continue
    elif len(passw) < 6:
      print('Your password must be 6 characters or more')
      continue
    verifyPassw = input('Verify your password: ')
    if passw != verifyPassw:
      print('Passwords do not match!')
      continue
    else:
      break

  passw.encode()
  hashed = bcrypt.hashpw(passw.encode(), bcrypt.gensalt(rounds = 13))
  connection = sqlite3.connect('users.db')
  c = connection.cursor()
  c.execute("INSERT INTO users VALUES (?, ?, ?)", (
    usern,
    hashed,
    2,
  ))  # Create user
  connection.commit()
  connection.close()
  portal(True, usern)
  exit()  # Account made, logged in automatically


def userExists(usern):
  connection = sqlite3.connect('users.db')
  c = connection.cursor()

  while True:
    for row in c.execute('SELECT username FROM users'):
      if usern.upper() in (item.upper() for item in row):
        connection.close()
        return True  #Already exists
    connection.close()
    return False  #Unique


def getPermission(usern):
  connection = sqlite3.connect('users.db')
  c = connection.cursor()

  c.execute("SELECT permission FROM users WHERE username = ?", (usern, ))
  return (c.fetchone()[0])


def checkDB():
  connection = sqlite3.connect('users.db')
  c = connection.cursor()

  try:  #Check if database already exists
    c.execute("""CREATE TABLE users (
                      username text,
                      password text,
                      permission integer
                      )""")
    connection.commit()
    print("Table created")
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (
      'admin',
      bcrypt.hashpw(b'aDmin002', bcrypt.gensalt(rounds = 13)),
      0,
    ))
    connection.commit()
    print("Default account created")
    connection.close()
    checkDB()
  except sqlite3.OperationalError:
    return True
  except:
    raise Exception("Database corrupt, whoops!")


if __name__ == "__main__":
  checkDB()
  used = []
  portal(False, None)
