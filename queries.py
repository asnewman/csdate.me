import web
import MySQLdb

# Class for the Database
class Database:

   # Initialize class by connecting to database and creating cursor.
   def __init__(self):
      self.db = MySQLdb.connect(host = "localhost",
                           user = "root",
                           passwd = "knucklepickle",
                           db = "users")
      self.cur = self.db.cursor()

   # TESTING Query to return all users in the database.
   def get_all_users(self):
      query = "SELECT * FROM Users"
      self.cur.execute(query)
      res = self.cur.fetchall()
      return res

   # TESTING Query to return specific user. Returns only username.
   def get_user_test(self, name):
      query = "SELECT username FROM Users WHERE username = '" + name + "';"
      #self.cur = self.db.cursor()
      self.cur.execute(query)
      res = self.cur.fetchall()
      return res

   # Returns true for users that are in the database.
   def authCheck(self, username, password):
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
      cmd = "INSERT INTO Users VALUES (NULL, '" + name + "', '" + email + "', '" + password + "');"
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