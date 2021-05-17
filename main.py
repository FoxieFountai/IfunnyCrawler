import threading
from bs4 import BeautifulSoup
import json

from utils.schedule import SimpleTasking
from utils.data import RetrieveHtml

scheduling = SimpleTasking()

###########################################################
#                  ______   __  __     ______                            
#                 /\  ___\ /\_\_\_\   /\__  _\                           
#                 \ \  __\ \/_/\_\/_  \/_/\ \/                           
#                  \ \_\     /\_\/\_\    \ \_\                           
#                   \/_/     \/_/\/_/     \/_/                           
#   ______   ______     __  __     __   __     ______   ______     __    
#  /\  ___\ /\  __ \   /\ \/\ \   /\ "-.\ \   /\__  _\ /\  __ \   /\ \   
#  \ \  __\ \ \ \/\ \  \ \ \_\ \  \ \ \-.  \  \/_/\ \/ \ \  __ \  \ \ \  
#   \ \_\    \ \_____\  \ \_____\  \ \_\\"\_\    \ \_\  \ \_\ \_\  \ \_\ 
#    \/_/     \/_____/   \/_____/   \/_/ \/_/     \/_/   \/_/\/_/   \/_/ 
#                                                                                      
# Not final version.
#  
#                                               v: 1.0.0                             
##############################################################

#execution routine
def MakePostList(LastPost = None , domain = 'https://br.ifunny.co'):
    #post
    PostList = []

    #get site html
    html = RetrieveHtml(domain)

    #working with the html
    soup = BeautifulSoup(html, "lxml")
    Posts = soup.find_all('li', attrs={'class' : ['stream__item js-playlist-item']})

    for post in Posts:
        #the post
        CardImage = post.find_all('img', attrs={'class': 'media__image'})

        #author data
        CardAuthorDiv = post.find_all('a', attrs={'class': ['metapanel__user-nick js-goalcollector-action js-dwhcollector-actionsource']})
        CardAuthorName = CardAuthorDiv[0].getText()
        CardAuthorLink = domain + CardAuthorDiv[0]['href']

        #post reactions and comments
        CardReactions = post.find_all('span', attrs={'class': ['post-actions__text']})[0].getText()
        CardComments = post.find_all('span', attrs={'class': ['post-actions__text']})[0].getText()

        #post date
        CardDate = post.find_all('span', attrs={'class': ['metapanel__time']})[0].getText()

        #post image link 
        CardImageLink = post.find_all('img', attrs={'class': ['media__image']})[0]['data-src']

        #post original link 
        CardOriginalLink = domain + post.find_all('a', attrs={'class': ['media__preview js-goalcollector-action js-dwhcollector-actionsource']})[0]['href']

        #building post structure
        ThisPost = {}
        ThisPost['author-name']   = CardAuthorName
        ThisPost['author-link']   = CardAuthorLink
        ThisPost['reactions']     = CardReactions
        ThisPost['comments']      = CardComments
        ThisPost['date']          = CardDate
        ThisPost['src-link']      = CardImageLink
        ThisPost['original-link'] =  CardOriginalLink

        #verification if this post has been saved before
        if LastPost == None:
            #adding this post to post list
            PostList.append(ThisPost)
        else:
            if ThisPost['author-link'] == LastPost['author-link'] and ThisPost['original-link'] == LastPost['original-link']:
                break
            else:
                PostList.append(ThisPost)


    return PostList

#get lastpost from db
def GetDbLast(path = 'database/db.json'):
    DbReader = open(path, 'r+')
    DbReaderData = DbReader.read()
    LastPost = json.loads(DbReaderData) if not DbReaderData == '' else None
    DbReader.close()

    return (LastPost[0] if not LastPost == None else None)

#saving post 
def SavePosts(Posts, path = 'database/db.json'):
    if Posts == []:
        return
    Db = open(path, 'w+')
    json.dump(Posts, Db)
    Db.close()

#execute
def Routine():
    #feedback 
    #print(">>Running crawler...")

    #get last post
    LastSavedPost = GetDbLast()

    #get posts 
    Posts = MakePostList(LastSavedPost)

    #saving posts on db
    SavePosts(Posts)

    #feedback
    #print(">>Done!")
    #print("=-"* 10)
    
#setup execution time to tasking manager
scheduling.on('08:02:00', Routine)
scheduling.on('10:02:00', Routine)
scheduling.on('12:02:00', Routine)
scheduling.on('15:02:00', Routine)
scheduling.on('18:02:00', Routine)
scheduling.on('20:02:00', Routine)
scheduling.on('22:02:00', Routine)

scheduling.start()

#realize routine
Routine()

#main loop(keep script open)
while True:
    pass
