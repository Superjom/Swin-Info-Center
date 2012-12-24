# -*- coding: utf-8 -*
'''
Created on 2012-12-20

@author: superjom
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import db.ctrl as ctrl
import db.table_def as db
from sqlalchemy import  create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('sqlite:////home/chunwei/swin2/db/data.db', echo=False)
# create a Session
Session = sessionmaker(bind=engine)
session = Session()


def create_circles():
    circles = [
        {
          "name":u"信息与技术协会",
          "logo_url": "",
          "des": u"北京大学信息与技术协会",
          "kind": u"社团"
         },

        {
          "name":u"青年志愿者协会",
          "logo_url": "",
          "des": u"北京大学青年志愿者协会",
          "kind": u"社团"
         },

        {
          "name":u"橄榄球协会",
          "logo_url": "",
          "des": u"北京大学橄榄球协会",
          "kind": u"社团"
         },
        {
          "name":u"乒乓球协会",
          "logo_url": "",
          "des": u"北京大学乒乓球协会",
          "kind": u"社团"
         },

        {
          "name":u"信息与工程学院",
          "logo_url": "",
          "des": u"北京大学信息与工程学院",
          "kind": u"学校组织"
         },
        {
          "name":u"汇丰商学院",
          "logo_url": "",
          "des": u"北京大学汇丰商学院",
          "kind": u"学校组织"
         },
        {
          "name":u"新材料学院",
          "logo_url": "",
          "des": u"北京大学新材料学院",
          "kind": u"学校组织"
         },
    ]

    for c in  circles:
        circle = db.Circle(c['name'], c['logo_url'], c['des'], c['kind'])
        session.add(circle)
    session.commit()

def show_circles():
    circles = session.query(db.Circle).filter(db.Circle.kind==u"社团")
    print "get circles"
    for c in circles:
        print c.name

def show_circleusers():
    circles = session.query(db.Circle)
    for c in circles:
        print '-'*50
        print 'circle: ', c.name
        print 'users:'
        users = c.users
        for u in users:
            print u.name, u.email
        print '>'*50
  
def create_tags():
    print 'create tags'
    tags = [
        (u"男生", u"性别"),
        (u"女生", u"性别"),

        (u"足球", u"兴趣"),
        (u"篮球", u"兴趣"),
        (u"橄榄球",u"兴趣"),
        (u"看书", u"兴趣"),

        (u"江苏", u"家乡"),
        (u"北京", u"家乡"),
        (u"海南", u"家乡"),
    ]
    for tag in tags:
        t = db.Tag(tag[0], tag[1])
        session.add(t)
    session.commit()

def create_user():
    user = db.User("superjom", "511541", "superjom@gmail.com", \
                        "Shenzhen,Guang dong", "Peking University", 1, "static/images/user.jpg")
    user1 = db.User("shasha", "511541", "shasha@gmail.com", \
                        "Beijin", u"北理工")
    #加入一些社团
    circles = session.query(db.Circle).filter(
                        or_(db.Circle.name == u"信息与技术协会", db.Circle.name == u"青年志愿者协会"))
    for c in circles:
        print c.name
        user.circles.append(c)
        user1.circles.append(c)
    
    tags = session.query(db.Tag).filter(
                or_(db.Tag.name == u"江苏", db.Tag.name == u"橄榄球")
            )
    for tag in tags:
        user.tags.append(tag)
        user1.tags.append(tag)
    session.add(user)
    session.add(user1)
    session.commit()
    
def show_users():
    print "show users"
    users = session.query(db.User)
    for user in users:
        print '-'*50
        print user.name, user.email
        circles = user.circles
        print "circles: ",
        for c in circles:
            print c.name
        print "tags"
        for tag in user.tags:
            print tag.name
        print 'messages:'
        for message in user.messages:
            print message.title
    
def add_messages():
    print 'add messages'
    messages = [
        {
         "title": u"2012年12月份公费医疗报销通知",
         "date": datetime.datetime.today(),
         "summary": u"2012年12月份的学生公费医疗报销工作从今日开始，请大家按以下要求准备好相关材料交到各班生活委员处进行初步审核后，12月24日统一交到我处进行材料二次审核。",
         "content": u'''
         各位同学：
      2012年12月份的学生公费医疗报销工作从今日开始，请大家按以下要求准备好相关材料交到各班生活委员处进行初步审核后，12月24日统一交到我处进行材料二次审核。没有班级编制的可以直接交给我！具体要求如下：
一．报销资格：所有人事档案转入北大的学生均可报销.
二．材料时间要求：所有材料上的日期必须是2012年1月-2012年12月之内，跨年度不可报销，寒暑假产生的费用无法报销。
三．报销指定医院：大学城社康中心（清华食堂旁）、深圳北大医院、西丽人民医院。
四．报销材料：
（1）学生门诊报销需准备的材料：收费单据（发票）、门诊用药清单小白票（西丽医院可能把药品清单打在发票上）、处方、诊断病历。
（2）学生住院报销需准备的材料：院系证明、本人的住院证明、住院病历记录、出院小结（或证明）、住院明细原件及复印件、收费单据。
（3）关于报销材料收集的注意事项请各位同学查看附件《收集报销材料注意事项》
五、材料整理要求：
同一日的材料按门诊收费收据、药品清单、处方笺、门诊费用清单、病例的顺序左上角对齐，然后每个学生自行将报销材料按日期顺序排列并全部用胶水（不能用订书机）粘好（材料不齐全均不可报销），后交与各班生活委员进行初步审查，各班生活委员审查提醒缺材料同学到原就诊医院补材料，初审后用附件的《医疗报销汇总表》的做一份电子版汇总表格，并于24日统一将所有材料交到我处进行二次审核；住院材料整理方式同上（请注意住院是按月报销，可直接交到我处）；
六、以上所有材料报销成功后均不退回，如有需要请同学自行复印留底。
 
祝大家身体健康！
         '''
         },
                        {
         "title": u"讲座通知：讯程实业股份有限公司（台湾）高级经理罗达权先生",
         "date": datetime.datetime.today(),
         "summary": u"我院崔小乐老师邀请讯程实业股份有限公司（台湾）高级经理罗达权先生进行学术讲座",
         "content": u'''
各位同学：
我院崔小乐老师邀请讯程实业股份有限公司（台湾）高级经理罗达权先生进行学术讲座，安排如下：
 
讲座题目：集成电路与系统产品的静电防护与抗栓锁测试方法
 
讲座时间：12月26日（周三）下午 14：00-16：00
 
讲座地点：C-301教室
 
详情见学院网站海报：http://www.ece.pku.edu.cn/index.php?m=content&c=index&a=show&catid=503&id=1390 。欢迎大家参加！

教务 杨柳
         '''
         },
    ]

    for m in messages:
        me = db.Message(m['title'], m['summary'], 0, m['date'])
        item = db.MessageItem(m['content'])
        me.item = item
        session.add(me)
        user = session.query(db.User).filter(db.User.name == 'superjom').first()
        user.messages.append(me)
        user.ownmessages.append(me)
        session.add(user)
    session.commit()

def show_message():
    messages = session.query(db.Message)
    for m in messages:
        print 'm.status', m.status
        print '-' * 50
        print 'title', m.title
        print 'content', m.item.content


#----------------------- news ---------------------------
def addStations():
    stations = [
        u"深圳研究生院官网",
        u"信息工程学院",
    ]
    for station in stations:
        s = db.Station(station)
        session.add(s)
    session.commit()
    print "add stations OK!"

def showStations():
    print "showStations" 
    stations = session.query(db.Station)
    for s in stations:
        print s.id, s.name

def showNews():
    print "showNews" 
    news = session.query(db.News)
    for s in news:
        print s.id, s.item.title
    

def addNews():
    #添加首页新闻
    pass
    
def push_message():
    pass

if __name__ == "__main__":
    
    create_circles()
    create_tags()
    create_user()
    show_circles()
    show_circleusers()
    add_messages()
    addStations()
    showStations()
    showNews()
    show_message()
    show_users()
    
