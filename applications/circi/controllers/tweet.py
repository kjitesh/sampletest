

@auth.requires_login()
def home():
   '''First point of call, contains all tweets and all tweets of those you follow'''
   #configure defaults, so they not appear on the form
   db.tweets.posted_by.default = me
   db.tweets.posted_on.default = request.now
   #create form with which the user can submit tweets
   crud.settings.formstyle = 'table2cols'
   form = crud.create(db.tweets)
   #determine who the user follows
   my_followees = db(db.followers.follower==me)
   me_and_my_followees = [me]+[row.followee for row in my_followees.select(db.followers.followee)]
   #Pull all tweets to be displayed
   tweets = db(db.tweets.posted_by.belongs(me_and_my_followees)).select(orderby=~db.tweets.posted_on,limitby=(0,100))
   return locals()


def index():
   if auth.user: redirect(URL('home'))
   return locals()


# show user's wall, showing profile and posts
def wall():
   #Determine which user's wall is to be displayed
   user = db.auth_user(request.args(0) or me)
   #If user is invalid, return to the home page
   if not user:
       redirect(URL('home'))
   tweets = db(db.tweets.posted_by==user.id).select(orderby=~db.tweets.posted_on,limitby=(0,100))
   return locals()


# a page for searching for other users
@auth.requires_login()
def search():
   form = SQLFORM.factory(Field('name',requires=IS_NOT_EMPTY()))
   if form.accepts(request):
       tokens = form.vars.name.split()
       query = reduce(lambda a,b:a&b,
                      [db.auth_user.first_name.contains(k)|db.auth_user.last_name.contains(k) \
                           for k in tokens])
       people = db(query).select(orderby=db.auth_user.first_name|db.auth_user.last_name,left=db.followers.on(db.followers.followee==db.auth_user.id))
   else:
       people = []
   return locals()


# this is the Ajax callback
@auth.requires_login()
def follow():
   if request.env.request_method!='POST': raise HTTP(400)
   if request.args(0) =='follow' and not db.followers(follower=me,followee=request.args(1)):
       # insert a new friendship request
       db.followers.insert(follower=me,followee=request.args(1))
   elif request.args(0)=='unfollow':
       # delete a previous friendship request
       db(db.followers.follower==me)(db.followers.followee==request.args(1)).delete()
