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
         tokenSet(i.username)
         return render.main()
      else:
         # Direct to failed login page
         return render.loginFailed()

# Main page accessed after login with results of our algorithm.
class main:
   def GET(self):
      return render.main()

# Page for getting questions from users
class questions:
   def GET(self):
      i = web.input(firstName=None)
      if(i.firstName==None):
        return render.questions()
      else:
        results = DB.add_user_questions(i.firstName, i.middleName, i.lastName, i.email, i.gender, i.state, i.city, i.birthday, i.favoriteOS)
        return render.questions() 

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

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
