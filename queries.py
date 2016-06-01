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
      cmd = "INSERT INTO Users VALUES (NULL, '" + name + "', '" + email + "', '" + password + "', NONE);"
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
   
   ######## CHECK FOR TIME!!!!!!!!!!!!!!!!!!!!!!!! #########

   def addToken(self, userid, token):
      self.cur.execute("START TRANSACTION;")
      cmd = """IF EXISTS 
                  (SELECT token 
                   FROM Users
                   WHERE userid = """ + userid + """
                   ) 
               THEN 
                  SELECT token FROM Users WHERE userid = """ + userid + """
               ELSE
                  UPDATE TABLE Users
                  SET token = """ + token + """
                  WHERE
                     userid = """ + userid + """
                  SELECT token
                  FROM Users
                  WHERE
                     userid = """ + userid + """
               END IF """
      self.cur.execute(cmd)
      self.cur.execute("COMMIT;")
      res = self.cur.fetchall()
      return res[0]