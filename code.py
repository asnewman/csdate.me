from queries import *

# html templates
render = web.template.render('templates/')

# All urls
urls = (
    '/', 'index',
    '/signup', 'signup',
    '/login', 'login',
    '/loginFailed', 'login',
    '/questions', 'questions',
    '/main', 'main'
)

# Initializing database connector
DB = Database()

class index:
    def GET(self):
        i = web.input(name=None)
        return render.index(i.name)

class signup:
    def GET(SELF):
        return render.signup()
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

class main:
   def GET(self):
      return render.main()

# Page for getting questions from users
class questions:
   def GET(self):
      i = web.input(firstName=None)
      if(i.firstName==None):
        return render.questions(None)
      else:
        results = DB.add_user_questions(i.firstName, i.middleName, i.lastName, i.email, i.gender, i.state, i.city, i.birthday, i.favoriteOS)
        return render.questions(results) 

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
