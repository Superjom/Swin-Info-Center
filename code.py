# -*- coding: utf-8 -*

'''
Created on 2012-12-19

@author: superjom
'''
import web
web.config.debug = False

import db.ctrl as ctrl

urls = (
    "/", "index",
    "/profile", "user_profile",
    "/profile_edit", "profile_edit",
    "/profile_select_tags", "profile_select_tags",
    "/profile_join_circles", "profile_join_circles", 
    
    "/login", "login",
    "/signin(.*)", "signin",
    "/items", "items",
    
    "/circles", "circles",
    "/add_circle(.*)", "add_circle",
    "/sigle", "sigle",
    "/hello*", "hello",
)
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'userid': 1})
#user database ctrl

class hello:
    def GET(self):
        return "Hello, world"
    
class index:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        assert session.userid != -1
        userinfo = ctrl.userInfo(session.userid)
        messages = ctrl.userGetMessages(session.userid)
        news = ctrl.getAllNewsList()
        return render.user_index(userinfo, messages['count'], messages['messages'], news)
       
    
class user_profile:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        return render.user_profile()


class profile_edit:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        assert session.userid != -1
        info = ctrl.userGetInfo(session.userid)
        return render.profile_edit(info)
    
class profile_select_tags:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        return render.profile_select_tags()
    
class profile_join_circles:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        return render.profile_join_circles()
    
    
class login:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        return render.login()

class circles:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        return render.circles()
    
class add_circle:
    def POST(self, data):
        data = web.input()
        if data:
            circle = ctrl.Circle()
            circle.addNew(data['name'], data['url'], data['des'])
            return "Succeed add circle"
        render = web.template.render("templates/", base="template")
        return render.circles()
        

class signin:
    def GET(self, data):
        #t = web.template.frender('templates/index.html')
        data = web.data()
        print 'get data:', data
        render = web.template.render("templates/", base="template")
        return render.signin()  
      
    def POST(self, data):
        print '-'*50
        data = web.input()
        print 'web data',data
        
        #check if user information is true
        user = ctrl.User()
        user_id = user.login(data['username'], data['pwd'])
        if user_id!= -1:
            _login = login()
            session.userid = user_id
            print '>'*50
            return _login.GET()
        print '>'*50
        render = web.template.render("templates/", base="template")
        return render.signin()    

class items:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        return render.items()

class sigle:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        return render.sigle()    
    
if __name__ == "__main__":
    app.run()
