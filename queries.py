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
      cmd = "INSERT INTO Users VALUES (NULL, '" + name + "', '" + email + "', '" + password + "', NULL, CURRENT_TIMESTAMP());"
      self.cur.execute(cmd)
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
   def addUserQuestions(self, firstName, middleName, lastName, email, gender, state, city, birthday, favoriteOS):
      cmd = "INSERT INTO user_questions VALUES (NULL, '" + firstName + "', '" + middleName + "','" + lastName + "','" + email + "','" + gender + "','" + state + "','" + city + "','" + birthday + "','" + favoriteOS + "');"
      self.cur.execute("START TRANSACTION;")
      self.cur.execute(cmd)
      self.cur.execute("COMMIT;")
      self.cur.execute("SELECT * FROM user_questions;")
      res = self.cur.fetchall()
      return res 

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
      self.cur.execute("UPDATE Users SET tokenTime = NULL WHERE token = '" + token + "';")
      return