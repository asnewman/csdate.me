import web
import MySQLdb

# Class for the Database
class Database:

   # Initialize class by connecting to database and creating cursor.
   def __init__(self):
      self.db = MySQLdb.connect(host = "localhost",
                              user = "root",
                              passwd = "knucklepickle",
                              db = "csdateme")
      self.cur = self.db.cursor()

   # Returns true for users that are in the database.
   def authCheck(self, username, password):
      self.cur.close()
      self.cur = self.db.cursor()
      query = "SELECT id FROM Users WHERE username = '" + username + "' AND password = '" + password + "';"
      self.cur.execute(query)
      res = self.cur.fetchall()
      if len(res) == 0:
         return False
      else:
         return True

   # Query for checking login credentials.
   def getUser(self, username, password):
      query = "SELECT * from Users WHERE username = '" + username + "' AND password = '" + password + "';"
      self.cur.execute(query)
      res = self.cur.fetchall()
      return res

   # Query to add a user to the database. Returns a list of users.
   def addUser(self, name, email, password):
      self.cur.execute("START TRANSACTION;")
      cmd = "INSERT INTO Users VALUES (NULL, '" + name + "', '" + password + "', '" + email + "', NULL, NULL);"
      self.cur.execute(cmd)
      cmd2 = "INSERT INTO Questions VALUES (NULL, FALSE, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);"
      self.cur.execute(cmd2)
      self.cur.execute("COMMIT;")
      self.cur.execute("SELECT * FROM Users;")
      res = self.cur.fetchall()
      return res

   # Returns true if username and email is unique
   def addUserCheck(self, username, email):
      query = "SELECT id FROM Users WHERE username = '" + username + "' OR email = '" + email + "';"
      self.cur.execute(query)
      res = self.cur.fetchall()
      if len(res) == 0:
         return True
      else:
         return False

   # Jason testing user_questions
   def updateQuestions(self, userid, fName, mName, lName, gender, state, city, birthday, favoriteOS, phoneOS, relationship, gaming, favLang1, favLang2, favLang3, favHobby1, favHobby2, favHobby3, wpm):
      cmd = "UPDATE Questions SET completed = true, firstName = '" + fName + "', middleName = '" + mName + "', gender = '" + gender + "', state = '" + state + "', city = '" + city + "', birthday = '" + birthday + "', favoriteOS = '" + favoriteOS + "', phoneOS = '" + phoneOS + "', relationship = '" + relationship + "', gaming = '" + gaming + "', favLang1 = '" + favLang1 + "', favLang2 = '" + favLang2 + "', favLang3 = '" + favLang3 + "',  favHobby1 = '" + favHobby1 + "',  favHobby2 = '" + favHobby2 + "', favHobby3 = '" + favHobby3 + "', wpm = " + wpm + " WHERE id = " + str(userid) + ";"
      self.cur.execute("START TRANSACTION;")
      self.cur.execute(cmd)
      self.cur.execute("COMMIT;")

   # Returns a token. Checks if token on file has expired or is still valid. 
   def addToken(self, username, token):
      self.cur.close()
      self.cur = self.db.cursor()
      self.cur.execute("CALL addToken('" + username + "', '" + token + "');")
      res = self.cur.fetchall()
      self.cur.close()
      self.cur = self.db.cursor()
      return res[0][0]

   # Remove token on logout
   def removeToken(self, token):
      self.cur.execute("START TRANSACTION;")
      self.cur.execute("UPDATE Users SET tokenTime = NULL WHERE token = '" + token + "';")
      self.cur.execute("COMMIT;")

   # Returns true if user has finished questions
   def questionsDone(self, userId):
      query = ("SELECT completed FROM Questions WHERE id = " + str(userId) + " LIMIT 1;")
      self.cur.execute(query)
      result = self.cur.fetchall()
      return result[0][0]

   # Returns userId for given username
   def usernameToId(self, username):
      query = ("SELECT id FROM Users WHERE username = '" + username + "';")
      self.cur.execute(query)
      userId = self.cur.fetchall()
      return userId[0][0]

   # Returns userId for given token
   def tokenToId(self, token):
      query = ("SELECT id from Users WHERE token = '" + token + "';")
      self.cur.execute(query)
      userId = self.cur.fetchall()
      return userId[0][0]
