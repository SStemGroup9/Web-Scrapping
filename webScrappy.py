import facebook

#generate your access token
app_id=''#your app id
app_secret=''#your app secret
token = app_id+"|"+app_secret

graph = facebook.GraphAPI(token)
person = '/889307941125736'#hillary Clinton facebook ID
profile = graph.get_object(person)
id=profile['id']
print profile

feed = graph.get_connections(id, connection_name='feed')

post_ids = []
count = 0
for i in feed['data']:
    #for c in i:
    print('%s '%i['created_time'])
    print('%10s '%i.get('message',None))
    print('%10s'%i['id'])
    count+=1
    comment=graph.get_connections(i['id'], connection_name='comments')
    for c in comment['data']:
        print('%10s '%c['created_time'])
        print('%15s '%c.get('message',None))
        print('%15s '%c.get('from',None))
        '''
        fromPerson = c.get('from',None)
        if fromPerson != None:
            for f in fromPerson:
                print f['name']
                print f['id']
        '''
        
        print('%15s'%i['id'])
print(count)
