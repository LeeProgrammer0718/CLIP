#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
import os
import requests
from bs4 import BeautifulSoup
import datetime
now = datetime.datetime.now()#시간정보 얻음
app = Flask(__name__)
ACCESS_TOKEN =os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text =lunch(time(now))             #time(now)        
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

def time(time): #서버가 미국에 있으므로 한국에서 사용하려면 시차계산 필요 
    date = [0,1,2,3]
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    khour = hour+9 #한국 시차계산
    kday = day
    kmonth = month
    if khour >24:
        khour = khour-24
        kday +=1
        if month in [1,3,5,7,8,10,12]:
            if kday>31:
                kday = 1
                kmonth +=1
        else:
            if kday>30:
                kday = 1
                kmonth +=1
    date[0] = year
    date[1] = kmonth
    date[2] = kday
    date[3] = khour
    return date

def lunch(time):
    year = str(time[0])
    month = str(time[1])
    if time[2]<10:
        day = '0' + str(time[2])
    else:
        day = str(time[2])
    url = "http://pungduck.hs.kr/lunch.view?date="+year+month+day
    r = requests.get(url)
    c = r.content
    html = BeautifulSoup(c,"html.parser") #html 파싱
    #print(html)
    menu = html.find("div",{"class":"menuName"})
    #print(menu)
    try:
        span = menu.find("span")
        return span.text#메뉴출력
    except:
        return "급식이 없어요!!"




    
if __name__ == "__main__":
    app.run()

