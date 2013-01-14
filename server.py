# -*- coding: utf-8 -*
import web
web.config.debug = False
from datetime import datetime  as dt
import types
import db.table_cr as table
import db.ctrl.user as user
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
    "/ajax/load_more_news(.*)", "ajax_load_more_news",
    "/sigle(.*)", "sigle",
    "/items(.*)", "items",
    # show circles
    "/circles", "circles",
    #profile
    "/profile", "user_profile",
    "/profile_edit", "profile_edit",
    "/profile_join_circles", "profile_join_circles", 
    "/profile_select_news", "profile_select_news",
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
        replys = userctrl.getReplys(session.userid)
        news = userctrl.getAllNewsList(session.userid)
        circles = userctrl.getCircles(session.userid)
        #tags = userctrl.getTags(session.userid)
        return render.user_index(userinfo, len(messages), messages, news, circles, replys)


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
        print 'get ursers', users
        #create message
        message_dic = data
        message_dic['ownerid'] = session.userid
        #push messages
        '''
        _session = getSession()
        _users = _session.query(table.Circle).filter(table.Circle.id == circle).first().users
        print 'get users: ', _users
        #=---- add new message
        _message = table.Message(
            message_dic['title'],
            message_dic['summary'],
            -1,
            dt.today(),
        )
        _message.creator_id = message_dic['ownerid']
        item = table.MessageItem(message_dic['content'])
        _message.item = item
        _session.add(_message)
        _session.add(item)
        for u in _users:
            #create meat
            meta = table.MessageMeta(_message, -1)
            u.messages.append(meta)
            _session.add(u)
            _session.add(meta)
        _session.commit()
        '''

        #push message
        messagectrl.push(circle, message_dic)
        render = web.template.frender("templates/ajax_push_message.html")
        return render(users)

class ajax_reply:
    def POST(self, data):
        data = web.input()
        print 'data', '-' * 50
        print data
        _session = getSession()
        #add reply
        reply = table.Reply(dt.today(), -1, data['replyto'], session.userid)
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
            if m.status != -1:
                '''
                只取得status为-1的记录
                '''
                continue
            try:
                m.status = 0
                _session.add(m)
                message = m.message
                item = message.item
                res1.append({
                    'id':message.id,
                    'title': message.title,
                    'summary': message.summary,
                    'date': message.date,
                    'content': item.content
                })
            except:
                print 'wrong get new items'
                pass
        #get new reply items
        #-----------------------------------
        res2 = []
        replys = user.replys
        for r in replys:
            print r.replyto
            if r.status != -1:
                continue
            r.status = 0
            _session.add(r)
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
        _session.commit()
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

class ajax_load_more_news:
    def GET(self, data):
        data = web.input()
        #page = int(data['page'])
        news = userctrl.getAllNewsList(session.userid, -1)
        print '@'*50
        print 'get news page:', news
        render = web.template.frender("templates/ajax_load_more_news.html")
        print news
        return render(news)

def getNewsById(id):
    '''
    get news content:
    title
    date
    content
    station
    '''
    session = getSession()
    news = session.query(table.News).filter(table.News.id == id).first()
    res = {}
    res['title'] = news.title
    res['content'] = news.item.content
    res['date'] = news.date
    res['station'] = news.station.name
    return res


def getStations():
    '''
    get stations:
    id
    name
    '''
    session = getSession()
    stations = session.query(table.Station)
    res = []
    for s in stations:
        res.append(
            {'name': s.name,
            'id':s.id,
            'num':len(s.news),
            }
        )
    return res


class sigle:
    def GET(self, data):
        render = web.template.render("templates/", base="template")
        data = web.input()
        news = getNewsById(data['id'])
        stations = getStations()
        print '@' * 50
        print 'news:', news['title']
        print 'stations:', stations
        return render.sigle(news, stations)    


def getNews(station):
    '''
    get staton's all news
    station is id or string name

    title
    date
    '''
    session = getSession()
    res = {}
    if type(station) is types.IntType:
        '''
        get id
        '''
        s = session.query(table.Station).filter(table.Station.id == station).first()
        news = s.news
        res['station'] = s.name
    else:
        res['station'] = station
        s = session.query(table.Station).filter(table.Station.name == station).first()
        news = s.news
    res['news'] = []
    for n in news:
        item = n.item
        res['news'].append(
            {
                'id': n.id,
                'title':n.title,
                'station': n.station.name,
                'date':n.date,
            }
        )
    return res

class items:
    def GET(self, data):
        data = web.input()
        station_id = data['station_id']
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        #station_name = ctrl.getStationName(station_id)
        news = getNews(int(station_id))
        stations = getStations()
        station_name = news['station']
        newslist = news['news']
        return render.items(station_name, newslist, stations)

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
        info = userctrl.getInfo(session.userid)
        return render.profile_edit(info)


class profile_join_circles:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        return render.profile_join_circles()
    
class circles:
    def GET(self):
        #t = web.template.frender('templates/index.html')
        render = web.template.render("templates/", base="template")
        return render.circles()



if __name__ == "__main__":
    app.run()
