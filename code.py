from queries import *

# html templates
render = web.template.render('templates/')

# All urls
urls = (
    '/', 'index',
    '/login', 'login',
    '/loginFailed', 'login',
    '/questions', 'questions',
    '/main', 'main',
    '/search', 'search'
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

def tokenSet(self, userId):
    r = random.randint(0, 2147483647)
    token = bcrypt.hashpw(r, bcrypt.gensalt())
    validToken = db.addToken(userId, token)
    web.setcookie('token', validToken, domain="csdate.me", secure=False)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
