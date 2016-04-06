import facebook
import datetime
import json
import urllib2
import requests
import csv
import time
import xml.etree.ElementTree as ET

def connect_db():
    try:
        from sqlite3 import dbapi2 as sqlite
    except ImportError:
        from pysqlite2 import dbapi2 as sqlite
    db_connection = sqlite.connect('facebook_data.db')
    return db_connection

def get_comments(comment):
    #created_time= comment['created_time']
    #print comment
    message = comment.get('message',"")
    # data = graph.get_object('/' + comment['id'],fields='from',limits=100)
    from_person = comment.get('from',"")
    from_id = from_person['id'] + "," + from_person['name'] if 'id' in from_person.keys() else ""
    return message + "," + from_id 

def get_post(post):
    post_id = post['id'].split('_')
    created_time = post['created_time'].split('+')[0]
    message = post.get('message',"")
    data = graph.get_object('/' + post['id'],fields='likes.summary(true),shares,comments.summary(true)',limits=100)
    num_likes = data['likes']['summary']['total_count']
    #comments = graph.get_object('/' + post['id'] + "/comments",summary=True)
    num_comments = data['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in data.keys() else data['shares'].get('count',None)
    #print data['sharedposts']
    #comments=""
    #for com in data['comments']['data']:
    #    comments += ',' + get_comments(com)
    '''
    comment=graph.get_connections(i['id'], connection_name='comments')
    for c in comment['data']:
    print('%10s '%c['created_time'])
    print('%15s '%c.get('message',None))
    print('%15s '%c.get('from',None))

    fromPerson = c.get('from',None)
    if fromPerson != None:
    for f in fromPerson:
    print f['name']
    print f['id']
    print('%15s'%i['id'])
    '''
    return (post_id[0],post['id'],created_time,message,num_comments,num_likes,num_shares)


def paging(person):
    db_conn = connect_db()
    db_cursor = db_conn.cursor()
    profile = graph.get_object(person)
    statuses = graph.get_connections('/'+profile['id'], connection_name='feed',limits=100)
    #statuses = request_until_succeed(profile['id'])
    db_cursor.execute("INSERT INTO fb_page VALUES(?,?,?,?,?)",(profile['id'],"\'"+profile['name']+"\'",0,1,"\'"+person+"\'",))
    db_conn.commit()
    has_next_page = True
    scrape_starttime = datetime.datetime.now()
    count = 0
    with open('%s_facebook.csv' % profile['name'].replace(" ","_"), 'wb') as file:
        writer = csv.writer(file)
        #likes = graph.get_object('/' + profile['id'] + "/likes",summary=True)
        #print likes
        #num_likes = likes['summary']['total_count']
        #writer.writerow(num_likes.encode('utf-8'))
        writer.writerow(["status_id", "created_time", "status_message",
            "num_likes", "num_comments", "num_shares"])
        print "Scraping %s Facebook Page: %s\n" % (person,scrape_starttime)
        while has_next_page:
            for post in statuses['data']:
                cur_post = get_post(post)
                db_cursor.execute("INSERT INTO posts VALUES(?,?,?,?,?,?,?)",cur_post)
                db_conn.commit()
                #writer.writerow(cur_post)
                count+=1
            if count % 100 == 0: print "Posts attained: %s" % count 
            # if there is no next page, we're done.
            if 'paging' in statuses.keys():
                nextPage = statuses['paging']['next']
                statuses = requests.get(nextPage).json()
            else:
                has_next_page = False
    print "\nDone!\n %s Feed Processed in %s" % (count,datetime.datetime.now() - scrape_starttime)


#generate your access token
tree = ET.parse('data.xml')
root = tree.getroot()
person=root[0].find('filter').find('person').text
app_id='1553876991589155'
app_secret='86e65d29621b33dd65f0dc6bb1748aa7'
token = app_id+"|"+app_secret

graph = facebook.GraphAPI(token)
page='https://www.facebook.com/' + person
paging(page)
