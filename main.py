from flask import Flask
import os
#from dotenv import load_dotenv
import rbxrequest
import sys
import requests
from time import sleep
import threading
import atexit

class Logger:

    def printMessages(self):
        msgStr = ""
        for m in self.messages:
            msgStr = msgStr + f"{m}\n"
        requests.post(self.webhook, json = {
            "content": f"## console output in last 10 seconds\n```{msgStr}```"
        })
        self.messages = []


    def loop(self):
        while True:
            sleep(1)
            self.timer -= 1
            if self.timer == 0:
                self.timer = -1
                self.printMessages()        


    def __init__(self, webhook):
        self.webhook = webhook
        self.messages = []
        self.suppressed = False
        self.originalStdout = sys.__stdout__
        if self.webhook:
            self.timer = -1
            threading.Thread(target=self.loop).start()

    def write(self, text):
        if not self.suppressed:
            if text != '\n':
                self.originalStdout.write(text + "\n")
                self.timer = 10
                #self.messages.append(text)
                requests.post(self.webhook, json = {
                    "content": text
                })

    def flush(self):
        pass

    def supressOutput(self):
        self.suppressed = True

    def restoreOutput(self):
        self.suppressed = False

#load_dotenv()
webhook = os.getenv("WEBHOOK")

global log
log = Logger(webhook)
atexit.register(log.printMessages)

sys.stdout = log

app = Flask(__name__)
cookie = os.getenv("RBXCOOKIE")

def parseAPIkey(apikey):
    return apikey == os.getenv("APIKEY")

global madeBadges
madeBadges = 0
global timesRan
timesRan = 0

global session
session = rbxrequest.session(cookie)

def read_file_content(fp): 
    #without storing the file contents in a variable, the file would be closed before sending the http request leading to the file content being empty in the request body.
    with open(fp, 'rb') as f:
        content = f.read()
        f.close()
    return content

def getBadgesLeft(session, id):
        badgesLeft = session.get(f"https://badges.roblox.com/v1/universes/{id}/free-badges-quota", decode_json=False)
        return int(badgesLeft)

def createBadge(session, id, name, description, image):
        data = {
            'name': name,
            'description': description,
            'paymentSourceType': 'User',
            'expectedCost': 0,
        }
        files = {'files': image}
        req = session.post(f"https://badges.roblox.com/v1/universes/{id}/badges", data=data, files=files)
        global madeBadges
        madeBadges = madeBadges + 1
        return req["id"]

def createBadgesForGame(session, id, name, desc, image):
    badges = []
    print("creating badges for game: " + str(id))
    badgesQuota = getBadgesLeft(session, id)
    for i in range(badgesQuota):
        output = createBadge(session, id, name, desc, image)
        if output == None:
            continue
        else:
            print("created badge: " + str(output))
            badges.append(output)
    return badges

@app.route("/makebadges/<apikey>/<int:gameid>")
def makebadges(apikey, gameid):
    if parseAPIkey(apikey):
        image = read_file_content('cat.png')
        global session
        global timesRan
        global madeBadges
        badges = createBadgesForGame(session, int(gameid), "temporary badge", "temporary badge", image)
        timesRan = timesRan + 1

        print(f"""
Created {len(badges)} badges for game {gameid}
BADGE IDS: {badges}

TOTAL TIMES RAN: {timesRan}
TOTAL BADGES: {madeBadges}
""")

        return badges
    else:
        return "Invalid APIKEY"

if __name__ == '__main__':
    print("Starting Application")
    #app.run(port=3904)