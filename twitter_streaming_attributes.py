import twitter,json,csv
# endpoints on the Twitter developer platform use the OAuth 1.0a method to act, asking for the API, linked to a specific account of Twitter
# oauth consumer key and secret, can be also seen as user name and password for the twitter developper app for API
# The acces token and the acces token secret authenticate OAuth 1.0a API requests, they are unique credential different for each users. They are used to identify the twitter account they are linked to.
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# here we are preparing a file csv where to write the values w is to create a new file or create one if it does not exist
csvfile = open('brexit_tweets_attributes.csv', 'w')
csvwriter = csv.writer(csvfile, delimiter='|') #in order to easly separate the fields on the csv we can use | a character that is very hard to see in tweets and so it won't create confusion when separating in columns the values.


def getVal(val):
    clean = ""
    if val:
        val = val.replace('|', ' ') #function that allows us to remove the delimiter from the tweet text in order not to get confusion in the csv. we can substitute | with blank space
        val = val.replace('\n', ' ') #The same applies with other signs that are meaningful in the csv
        val = val.replace('\r', ' ')
        clean = val.encode('utf-8')
    return clean


q = "---" # query: word or words separated by commas, that have to be present in the tweet in order to filter them
print 'Filtering the public timeline for track="%s"' % (q,)

#This is OAuth 'Dance', the authentication process needed to identify users using OAuth.
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

#Filtered stream endpoints filter the real-time stream of Tweets.
stream = twitter_stream.statuses.filter(track=q)
#create the list of values
for tweet in stream:
    #write the values into the file: time, user id, tweet, location, number of total tweets since creation day, number of followers and following, account creation date
    csvwriter.writerow([
        tweet['created_at'],
        getVal(tweet['user']['screen_name']),
        getVal(tweet['text']),
        getVal(tweet['user']['location']),
        tweet['user']['statuses_count'],
        tweet['user']['followers_count'],
        tweet['user']['friends_count'],
        tweet['user']['created_at']
        ])
    # print the values on the screen to check everything is working
    print tweet['user']['screen_name'].encode('utf-8'), tweet['text'].encode('utf-8')
