from bs4 import BeautifulSoup
import requests
import tweepy
import getleague
import time

ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = 'YOUR_CONSUMER_KEY_SECRET'

auth = tweepy.OAuth1UserHandler(
   CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

api = tweepy.API(auth)



def get_data(uri):
    print(uri)
    req = requests.get(uri)
    html = req.text
    search_uri = req.url
    s= ""
    if "?search" in search_uri:
        return "Sorry i was unable to process your request"
    else: 
        soup = BeautifulSoup(html,'html.parser')
        jobs = soup.find_all('div',class_='newsfeed')
        i=0
        for job in jobs:
            getd = job.find_all('div',class_='hl')
            for data in getd:
                x = data.a
                # print(x.text + "...")
                s += x.text+"...\n"
                s += x['href']+"\n"
                # print(x['href'])
                # print()

                i+=1
                if i==2:
                    break
            if i==2:
                break
                    # print(job)
    return s

def scrape(s):
    team = s
    team = team.lower()

    if team.startswith("#club"):
        team = team.split(" ")
        team_type = team[0]
        team = team[1:]
        team = '+'.join(team)
        if team in getleague.teams.keys() or team in getleague.abbrs.keys():
            if team in getleague.abbrs.keys():
                team = getleague.abbrs[team]
            sport = getleague.teams[team][0]
            league = getleague.teams[team][1]
            uri = f"https://www.newsnow.co.uk/h/Sport/{sport}/{league}/{team}"
            return get_data(uri)
        else:
            return "Sorry i was unable to process your request"
    elif team.startswith("#cricket"):
        team = team.split(" ")
        team_type = team[0]
        team = team[1:]
        team = '+'.join(team)
        uri = f"https://www.newsnow.co.uk/h/Sport/Cricket/{team}"
        return get_data(uri)
    elif team.startswith("#football"):
        team = team.split(" ")
        team_type = team[0]
        team = team[1:]
        team = '+'.join(team)
        uri = f"https://www.newsnow.co.uk/h/Sport/Football/International/{team}"
        return get_data(uri)
    else:
        return "Sorry i was unable to process your request"

def read_last_seen(FILE_NAME):
    file = open(FILE_NAME,"r")
    id = int(file.read().strip())
    file.close()
    return id

def update_last_seen(FILE_NAME,id):
    file = open(FILE_NAME,"w")
    file.write(str(id)) 
    file.close()

FILE_NAME = "last_seen.txt"

def reply():
    tweets = api.mentions_timeline(since_id=read_last_seen(FILE_NAME),tweet_mode='extended')
    for tweet in reversed(tweets):
        if "#" in tweet.full_text:
            # print(f"{tweet.id} : {tweet.text}")
            text = tweet.full_text
            chunks = text.split(" ")
            chunks = chunks[1:]
            s = " ".join(chunks)
            print(s)
            out = scrape(s)
            print(out)
            api.update_status("@"+ tweet.user.screen_name + "    " +out,in_reply_to_status_id=tweet.id)
            api.create_favorite(tweet.id)
            update_last_seen(FILE_NAME,tweet.id)
            # print()


while True:
    try:
        reply()
        time.sleep(5)
    except Exception as e:
        pass


