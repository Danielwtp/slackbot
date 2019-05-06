# encoding=utf8

from slackclient import SlackClient
import imp
import time
import sys
from scripts import backups,hydraServices
botUserOAuthAccessToken = ""


class slackComunucation(object):
    def __init__(self):
        self.slack_client = SlackClient(botUserOAuthAccessToken)
        self.canal = "CJ381CD2Q"
        self.appName = "monitorationbot"
        self.backup = False
        self.today = time.strftime("%Y-%m-%d")
        self.lastOne = "2019-04-15"
        self.estadoBackups = True
        self.mensahito = ""
        self.estados = hydraServices.getStatus()

    def slackConnect(self):
        return self.slack_client.rtm_connect()

    def slackReadRTM(self):
        return self.slack_client.rtm_read()

    def parseSlackInput(self, input, botID):
        botATID = "<@"+botID+">"
        if input and len(input) > 0:
            input = input[0]
            if 'text' in input and botATID in input["text"]:
                user = input["user"]
                message = input["text"].split(botATID)[1].strip(" ")
                channel = input["channel"]
                return [str(user), str(message), str(channel)]
        else:
            return[None, None, None]

    def getBotID(self, botName):
        api_call = self.slack_client.api_call("users.list")
        users = api_call["members"]
        for user in users:
            #print user.get('name')
            if 'name' in user and botName in user.get('name') and not user.get('deleted'):
                return user.get('id')

    def writeToSlack(self, channel, message):
        return self.slack_client.api_call("chat.postMessage", channel = channel, text = message, as_user = True )

class mainFuc(slackComunucation):
    def __init__(self):
        super(mainFuc, self).__init__()
        BOTID = self.getBotID(self.appName)

    def decideWheterToRespond(self, input):
        if input:
            user, message, channel = input
            return self.writeToSlack(channel, message)

    def run(self):
        self.slackConnect()
        BOTID = self.getBotID(self.appName)
        while(True):
        #print(time.strftime("%M"))
        #if time.strftime("%M") == "00":#cada hora revisa todo.
            #if not self.lastOne == time.strftime("%Y-%m-%d") and  time.strftime("%H") == "9":#check del backup solo a las 9
            self.today = time.strftime("%Y-%m-%d")
            estadoBackups = backups.checkeo(self.today)
            if backups:
                self.mensahito = "Backups: UP\n"
            else:
                self.mensahito = "Backups: DOWN\n"#FIN backups
            print(self.estados)

            self.writeToSlack(self.canal, self.mensahito)
            self.decideWheterToRespond(self.parseSlackInput(self.slackReadRTM(), BOTID))
            time.sleep(1)

if __name__ == "__main__":
    instance = mainFuc()
    instance.run()
