# -*- coding: utf-8 -*
import web
web.config.debug = False
from datetime import datetime  as dt
import db.table_cr as table
import db.ctrl.user as user
import db.ctrl.tag as tag
import db.ctrl.circle as circle
import db.ctrl.message as message
from db.ctrl.common import getSession

from web.wsgiserver import CherryPyWSGIServer

CherryPyWSGIServer.ssl_certificate = "/etc/ssl/server.crt"
CherryPyWSGIServer.ssl_private_key = "/etc/ssl/server.key"

urls = (    
    # default to login
    "/", "index",
    "/userindex", "userindex",
    "/signin", "signin",
    "/_signin(.*)", "_signin",
    "/ajax/push_message(.*)", "ajax_push_message",
    "/ajax/reply(.*)", "ajax_reply",
    #取得新的记录
    "/ajax/get_new_items", "ajax_get_new_items",
    "/ajax/follow(.*)", "ajax_follow",
    #查看 followers
    "/own_messages", "own_messages",
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'userid': -1})

#--------------- db ctroler--------------------
_session = getSession()
userctrl = user.User()
circlectrl = circle.Circle()
messagectrl = message.Message()


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
            raise web.seeother('/userindex')
            '''
            _user_index = userindex()
            return _user_index.GET()
            '''
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
        #tags = userctrl.getTags(session.userid)
        return render.user_index(userinfo, len(messages), messages, news, circles)


class ajax_push_message:
    def POST(self, data):
        data = web.input()
        print '@' * 50
        print data
        circle = 1
        '''
        filter_input = data['filter_input']
        title = data['title']
        summary = data['summary']
        content = data['content']
        '''
        #user = ctrl.filterUsers(circle, filter_input)
        users = circlectrl.getUserNames(circle)
        #wraper users
        print 'get ursers', user
        #create message
        message = data
        message['ownerid'] = session.userid
        #push message
        messagectrl.push(circle, message)
        render = web.template.frender("templates/ajax_push_message.html")
        return render(users)

class ajax_reply:
    def POST(self, data):
        data = web.input()
        print 'data', '-' * 50
        print data
        _session = getSession()
        #add reply
        reply = table.Reply(dt.today(), -1, data['replyto'])
        item = table.ReplyItem(data['content'])
        reply.item = item
        #get user
        message = _session.query(table.Message).filter(table.Message.id == data['messageid']).first()
        owner_id = message.creator_id
        user = _session.query(table.User).filter(table.User.id == owner_id).first()
        user.replys.append(reply)
        _session.add_all([reply, item, user])
        _session.commit()
        res =  {
            'name':user.name,
            'logo_url':user.logo_url
        }
        render = web.template.frender("templates/ajax_reply.html")
        return render(res)

class ajax_get_new_items:
    def GET(self):
        _session = getSession()
        user = _session.query(table.User).filter(table.User.id == session.userid).first()
        #get new message metas
        #-----------------------------------
        metas = user.messages
        res1 = []
        for m in metas:
            #change status
            #...
            print m.status
            if m.status != -1:
                '''
                只取得status为-1的记录
                '''
                continue
            message = m.message
            item = message.item
            res1.append({
                'id':message.id,
                'title': message.title,
                'summary': message.summary,
                'date': message.date,
                'content': item.content
            })
        #get new reply items
        #-----------------------------------
        res2 = []
        replys = user.replys
        for r in replys:
            print r.replyto
            if r.status != -1:
                continue
            item = r.item
            try:
                res2.append({
                    'id':r.id,
                    'replyto':r.replyto,
                    'date':r.date,
                    'content':item.content
                })
            except:
                print 'none reply'
        render = web.template.frender("templates/ajax_get_update_messages.html")
        print 'res1: res2:'
        print res1, res2
        return render(res1, res2)

class ajax_follow:
    def GET(self, data):
        data = web.input()
        messageid = data['to']
        #get user
        _session = getSession()
        user = _session.query(table.User).filter(table.User.id == session.userid).first()
        message = _session.query(table.Message).filter(table.Message.id == messageid).first()
        print 'follow %s to %s' % (user.name, message.date)
        follower = table.Follower(user.name, dt.today())
        message.followers.append(follower)
        _session.add(follower)
        _session.add(message)
        _session.commit()
        return 'ok'


def getFollowers(session ,messageid):
    message = session.query(table.Message).filter(table.Message.id == messageid).first()
    followers = message.followers
    res = []
    for f in followers:
        res.append({
            'id': f.id,
            'name': f.name, 
            'logo_url': "static/images/user.jpg",
        })
    print 'followers: ', res
    return res


class own_messages:
    def GET(self):
        print 'hello-----' * 50
        userinfo = userctrl.getInfo(session.userid)
        print 'userinfo: ', userinfo
        _session = getSession()
        messages = _session.query(table.Message).filter(table.Message.creator_id == session.userid).all()
        res = []
        for m in messages:
            f = getFollowers(_session, m.id)
            if not f: continue
            res.append({
                'id': m.id,
                'title' : m.title,
                'summary': m.summary,
                'date': m.date,
                'followers': f,
                'followers_num': len(f)
            })
        print '--'*50
        print 'own messages:'
        print res
        render = web.template.render("templates/", base="template")
        return render.own_messages(userinfo, res)



if __name__ == "__main__":
    app.run()
