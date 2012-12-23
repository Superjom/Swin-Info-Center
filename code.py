# -*- coding: utf-8 -*

'''
Created on 2012-12-19

@author: superjom
'''
import web
web.config.debug = False

import db.ctrl as ctrl

urls = (
    "/", "login",
    "/user_index", "user_index",
    "/profile", "user_profile",
    "/profile_edit", "profile_edit",
    "/profile_select_tags", "profile_select_tags",
    "/profile_join_circles", "profile_join_circles", 
    
    "/login", "login",
    "/signin(.*)", "signin",
    "/items(.*)", "items",
    "/own_messages", "own_messages",

    "/ajax/push_message(.*)", "ajax_push_message",
    "/ajax/get_update_messages(.*)", "ajax_get_update_messages",
    "/ajax/follow(.*)", "ajax_follow",
    
    "/circles", "circles",
    "/add_circle(.*)", "add_circle",
    "/sigle(.*)", "sigle",
    "/hello*", "hello",
    # --------------- ajax ---------------------
    "/ajax/load_more_news(.*)", "load_more_news",
)
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'userid': -1})
#user database ctrl

class hello:
    def GET(self):
        return "Hello, world"
    
class user_index:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        print '@'*50
        print 'session.userid', session.userid
        if session.userid == -1:
            return render.login()

        userinfo = ctrl.userInfo(session.userid)
        messages = ctrl.userGetMessages(session.userid)
        news = ctrl.getAllNewsList(0)
        circles = ctrl.getUserCircle(session.userid)
        tags = ctrl.getTags()
        return render.user_index(userinfo, messages['count'], messages['messages'], news, circles, tags)
       
    
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
        
class load_more_news:
    def GET(self, data):
        data = web.input()
        page = data['page']
        news = ctrl.getAllNewsList(1)
        print '@'*50
        print 'get news page:', news
        render = web.template.frender("templates/ajax_load_more_news.html")
        return render(news)


class own_messages:
    def GET(self):
        userinfo = ctrl.userInfo(session.userid)
        messages = ctrl.getOwnMessages(session.userid)
        print '--'*50
        print 'messages:'
        print messages
        render = web.template.render("templates/", base="template")
        return render.own_messages(userinfo, messages)


#push message and return the filted
#users name and logo
class ajax_push_message:
    def POST(self, data):
        data = web.input()
        print '@' * 50
        print data
        circle = 1
        filter_input = data['filter_input']
        title = data['title']
        summary = data['summary']
        content = data['content']
        user = ctrl.filterUsers(circle, filter_input)
        print 'get ursers', user
        #push message
        ctrl.pushMessage(session.userid, circle, filter_input, title, summary, content)
        render = web.template.frender("templates/ajax_push_message.html")
        return render(user)

class ajax_follow:
    def GET(self, data):
        data = web.input()
        messageid = data['to']
        ctrl.follow(session.userid, messageid)
        return 'ok'

class ajax_get_update_messages:
    def POST(self, data):
        data = web.input()
        user_id = session.userid
        messages = ctrl.userGetUpdateMessages(int(user_id))
        render = web.template.frender("templates/ajax_get_update_messages.html")
        return render(messages)



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
            _user_index = user_index()
            session.userid = user_id
            print '>'*50
            return _user_index.GET()
        print '>'*50
        render = web.template.render("templates/", base="template")
        return render.signin()    

class items:
    def GET(self, data):
        data = web.input()
        station_id = data['station_id']
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        #station_name = ctrl.getStationName(station_id)
        news = ctrl.getNews(int(station_id))
        stations = ctrl.getStations()
        station_name = news['station']
        newslist = news['news']
        return render.items(station_name, newslist, stations)

class sigle:
    def GET(self, data):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        data = web.input()
        news = ctrl.getNewsById(data['id'])
        stations = ctrl.getStations()
        print '@' * 50
        print 'news:', news['title']
        print 'stations:', stations
        return render.sigle(news, stations)    
    
if __name__ == "__main__":
    app.run()
