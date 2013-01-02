# -*- coding: utf-8 -*
import web
web.config.debug = False

import db.table_cr as table
import db.ctrl.user as user
import db.ctrl.tag as tag
import db.ctrl.circle as circle
from db.ctrl.common import getSession

urls = (    
    # default to login
    "/", "index",
    "/signin", "signin",
    "/_signin(.*)", "_signin",
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'userid': -1})

userctrl = user.User(getSession())

class index:
    def GET(self):
        render = web.template.render("templates/", base="template")
        return render.login()

class signin:
    def GET(self):
        render = web.template.render("templates/", base="template")
        return render.signin()

class _signin:
    def POST(self, data):
        data = web.input()
        #check if user information is true
        res = userctrl.login(data['username'], data['pwd'])
        print '*' * 50
        print 'login res : ', res
        print 'session.id: %d' % session.userid
        if res != -1:
            # success signin
            session.userid = res
            print '*' * 50
            print 'session.id: %d' % session.userid
            _user_index = userindex()
            return _user_index.GET()
        #false signin
        render = web.template.render("templates/", base="template")
        return render.signin()    


class userindex:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        if session.userid == -1:
            return render.login()
        userinfo = userctrl.getInfo(session.userid)
        
        messages = userctrl.getMessages(session.userid)
        news = userctrl.getAllNewsList(session.userid)
        circles = userctrl.getCircles(session.userid)
        tags = userctrl.getTags(session.userid)
        return render.user_index(userinfo, len(messages), messages, news, circles, tags)


if __name__ == "__main__":
    app.run()
