import facebook
import datetime
import json
import urllib2
import requests
import csv
import time

def get_post(post):
    #post_id = post['id']
    #created_time = post['created_time']
    message = post.get('message',"")
    #num_likes = post.get('likes',"")
    #num_comments = post.get('comments',None)
    #num_shares = post.get('shares',None)
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
    return [message.encode('utf-8')]#, created_time, message,num_likes, num_comments, num_shares)


def paging(person):
    profile = graph.get_object(person)
    statuses = graph.get_connections(profile['id'], connection_name='feed')
    #statuses = request_until_succeed(profile['id'])
    has_next_page = True
    scrape_starttime = datetime.datetime.now()
    count = 0
    with open('%s_facebook.cvs' % profile['name'].replace(" ","_"), 'wb') as file:
        writer = csv.writer(file)
        #likes= graph.get_connections(profile['id'], connection_name='likes')
        writer.writerow(["status_id", "created_time", "status_message",
            "num_likes", "num_comments", "num_shares"])
        print "Scraping Facebook Page: %s\n" % (scrape_starttime)
        while has_next_page:
            for post in statuses['data']:
                writer.writerow(get_post(post))
                count+=1
            if count % 500 == 0: print "Posts attained: %s" % count 
            # if there is no next page, we're done.
            if 'paging' in statuses.keys():
                nextPage = statuses['paging']['next']
                statuses = requests.get(nextPage).json()
            else:
                has_next_page = False
    print "\nDone!\n %s Feed Processed in %s" % (count,datetime.datetime.now() - scrape_starttime)


#generate your access token
app_id='1553876991589155'
app_secret='86e65d29621b33dd65f0dc6bb1748aa7'
token = app_id+"|"+app_secret

graph = facebook.GraphAPI(token)
page='https://www.facebook.com/DonaldTrump/'
paging(page)
