from queries import *
import random
import bcrypt

# html templates
render = web.template.render('templates/')

# All urls
urls = (
    '/', 'index',
    '/login', 'login',
    '/loginFailed', 'login',
    '/questions', 'questions',
    '/main', 'main',
    '/search', 'search',
    '/test', 'test',
    '/logout', 'logout'
)

# Initializing database connector
DB = Database()

class index:
    def GET(SELF):
        return render.index()
    def POST(self):
        i = web.input()
        check = DB.addUserCheck(i.username, i.email)
        # Username/Email not taken
        if check == True:
          DB.addUser(i.username, i.email, i.password)
          return render.userCreated();
        # Username/Email taken
        else:
          return render.signupTaken();

class login:
   def GET(self):
      # Direct to default login page
    	return render.login()
   def POST(self):
      # Querying database
      i = web.input()
      auth = DB.authCheck(i.username, i.password)
      if auth == True:
         token = tokenSet(i.username)
         userId = DB.usernameToId(i.username)
         qCheck = DB.questionsDone(userId)
         print qCheck
         if (qCheck == 1):
            return web.HTTPError('301', {'Location': 'http://www.csdate.me/main'}) 
         else:
            return web.HTTPError('301', {'Location': 'http://www.csdate.me/questions'})
      else:
         # Direct to failed login page
         return render.loginFailed()

# Main page accessed after login with results of our algorithm.
class main:
   def GET(self):
      return render.main()
   def POST(self):
      token = web.cookies().token
      DB.removeToken(token)
      return render.logout()

# Page for getting questions from users  -- is broken for now due to different attribute #s
class questions:
   def GET(self):
      i = web.input(firstName=None)
      if(i.firstName==None):
        return render.questions()
      else:
        token = web.cookies().token
        userId = DB.tokenToId(token)
        print userId
        DB.updateQuestions(userId, i.firstName, i.middleName, i.lastName, 
                                      i.gender, i.state, i.city, i.birthday, 
                                     i.favoriteOS, i.phoneOS, i.relationship, i.gaming, 
                                     i.favLang1, i.favLang2, i.favLang3, i.favHobby1,
                                     i.favHobby2, i.favHobby3, i.wpm)
        return web.HTTPError('301', {'Location': 'http://www.csdate.me/main'}) 

# Searching other users page.
class search:
  def GET(self):
    return render.search()

# Testing Hashing here
class test:
    def GET(self):
        return render.test()

class logout:
   def GET(self):
      token = web.cookies().token
      DB.removeToken(token)
      return render.logout()

def tokenSet(username):
    r = random.randint(0, 2147483647)
    rString = str(r)
    token = bcrypt.hashpw(rString, bcrypt.gensalt())
    validToken = DB.addToken(username, token)
    validToken.replace("'","")
    web.setcookie('token', validToken, domain="csdate.me", secure=False)

# Compare attribute of two users. Works for every attribute except
# wpm and birthday.
def compareTwoUsers(self, attribute, user1, user2):
   if (attribute != "wpm" AND attribute != "birthday"):
      cmd = "SELECT %s FROM Questions Q1 JOIN Questions Q2 ON Q1.%s = Q2.%s WHERE Q1.userid = %d AND Q2.userid = %d" % (attribute, attribute, attribute, user1, user2)
   elif (attribute == "wpm"):
      cmd = "SELECT wpm FROM Questions Q1 JOIN Questions Q2 WHERE Q1.userid = user1 AND Q2.userid = user2 AND (Q1.wpm BETWEEN (Q2.wpm - 10) AND (Q2.wpm + 10))"
   else:
      cmd = "SELECT birthday FROM Questions Q1 JOIN Questions Q2 WHERE Q1.userid = user1 AND Q2.userid = user2 AND (YEAR(Q1.birthday) BETWEEN (YEAR(Q2.birthday) - 5) AND (YEAR(Q2.birthday) + 5)"
   self.cur.execute(cmd)
   res = self.cur.fetchall()
   # If there is a result, the attribute matches.
   if (res[0][0]):
      return True
   return False

# Returns the total number of users currently in the database
def numUsers(self):
   self.cur.execute("SELECT COUNT(*) FROM Users")
   res = self.cur.fetchall()
   return res[0][0]

# Create list of tuples for scores.
def createScores(self):
   currUser = 1
   totalUsers = numUsers()
   scores = []
   while (currUser < totalUsers):
      scores.append((currUser, 0))
      currUser++
   return scores

# Compare attribute of one user against all other users and add to 
# total scores. Returns scores array of tuples (userId, score).
def compareAttribute(self, attribute, weight, userid, scores):
   currUser = 1
   totalUsers = numUsers()
   while (currUser < totalUsers):
      # Do not compare the user with itself.
      if (currUser != userid):
         # If the current user has the same value for this attribute, 
         # add the weight of the attribute to the score.
         if (compareTwoUsers(attribute, userid, currUser)):
            scores = [(uid, score) if (uid != currUser) else (uid, score + weight) for (uid, score) in scores]
      currUser++

# Calculates the score for the user against all other users.
# Returns the scores in an array of tuples (userId, score).
def calculateScores(self, userid):
   scores = createScores()
   stateW = 
   cityW = 
   favoriteOSW = 4
   phoneOSW = 
   gamingW = 
   favLangW = 
   compareAttribute('favoriteOS', favoriteOSW, userid, scores)

# Sorts in order from highest score to lowest score for particular user.
def sortProfiles(self, userid):
   scores = calculateScores(userid)
   scores.sort(key=lambda tup:tup[1])
   # Return an array of users with user data.
   tuples = []
   for (uid, score) in scores:
      self.cur.execute("SELECT * FROM Questions WHERE uid = " + uid + ";")
      res = self.cur.fetchall
      tuples.append(res[0])
   return tuples

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
