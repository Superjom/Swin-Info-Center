'''
Created on 2012-12-21

@author: superjom
'''
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import chardet
import urllib2  
import StringIO  
import gzip  
import string  
import sys
from pyquery import PyQuery as pq
import xml.dom.minidom as dom
import socket