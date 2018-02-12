from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk
from nltk.corpus import stopwords
from collections import Counter

## SI 206 - HW
## COMMENT WITH:
## Your section day/time: 005 Tues/5:30-7:00
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
CACHE_FNAME = "twitter_cache.json"
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)


def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]


    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, params, auth=auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

baseurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json' #baseurl for fetching
params = {'screen_name':username, 'count':num_tweets}
make_request_using_cache(baseurl, params)
#Finish parts 1 and 2 and then come back to this

#Code for Part 1:Get Tweets
#python hw5_twitter.py umsi 25
baseurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
params = {'screen_name':username, 'count':num_tweets}
response = requests.get(baseurl, params, auth=auth)
tweet_data = json.loads(response.text)

tweet_file = open("tweet.json",'w')
tweet_file.write(json.dumps(tweet_data, indent=2))
tweet_file.close()

#Code for Part 2:Analyze Tweets
h =[]
for x in tweet_data:
    text = x['text']
    cleaned_text = text.replace(',','').replace('.','').replace('"','').replace('\n', ' ').replace('@','').replace(':','').replace('""','')
    cleaned_text = text.lower()
    word_tokens = nltk.word_tokenize(cleaned_text)
    tokens_pos = nltk.pos_tag(word_tokens)
    h.append(tokens_pos)

new = []
for x in h:
    for d in x:
        new.append(d)


# print (new)
stopwords_list = stopwords.words('english')
customized_stopwords = ['http','https','RT','rt','@','#','"',':','.',',','?']

# final_words = new
# for word in new:
#     if word in stopwords_list or customized_stopwords:
#         while word in final_words: final_words.remove(word)
#

Noun_words = []
for word, pos in new:
    if pos.find('NN') >= 0:
        Noun_words.append(word)


unique_Noun_words = set(Noun_words)
final_Noun_words = Noun_words
for word in unique_Noun_words:
    if word in stopwords_list:
        while word in final_Noun_words: final_Noun_words.remove(word)


unique_Noun_words1 = set(final_Noun_words)
for word in unique_Noun_words1:
    if word in customized_stopwords:
        while word in final_Noun_words: final_Noun_words.remove(word)


c = Counter(final_Noun_words)

# c= Counter(final_words)
print(c.most_common(5))



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
