# encoding=utf8

from slackclient import SlackClient
import imp
import time
import sys
from scripts import backups,hydraServices,VPNCheck
botUserOAuthAccessToken = ""


class slackComunucation(object):
    def __init__(self):
        self.slack_client = SlackClient(botUserOAuthAccessToken)
        self.canal = "C3Y7DDQ2Y"
        self.appName = "monitorationbot"
        self.today = time.strftime("%Y-%m-%d")
        self.lastOne = "2019-04-15"
        self.estadoBackups = backups.checkeo(self.today)
        self.estados =  hydraServices.getStatus()
        self.msgBackups = self.getBackUP()
        print("hola1")
        self.msgRepo = self.getRepo()
        print("hola2")
        self.msgJenk = self.getJenkins()
        print("hola3")
        self.msgArt = self.getArtifac()
        print("hola4")
        self.msgVpn = self.getVPN()
        print("hola5")
        self.mensahito = self.msgBackups + self.msgRepo + self.msgJenk + self.msgArt + self.msgVpn
        print(self.mensahito)

    def getRepo():
        if self.estados[0]:
            return("Repo: UP\n")
        else:
            return("Repo: DOWN\n")

    def getJenkins():
        if self.estados[1]:
            return("Jenkins: UP\n")
        else:
            return("Jenkins: DOWN\n")

    def getArtifac():
        if self.estados[2]:
            return("Artifactory: UP\n")
        else:
            return("Artifactory: DOWN\n")

    def getVPN():
        if VPNCheck.getStatus():#Vpn montado de mensage
            return("VPN: UP\n")
        else:
            return("VPN: DOWN\n")

    def getBackUP():
        self.estadoBackups = backups.checkeo(self.today)
        if backups:
            return("Backups: UP\n")
        else:
            return("Backups: DOWN\n")

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
            if message == "status":
                return self.writeToSlack(channel, self.mensahito)

    def run(self):
        self.slackConnect()
        print("holi")
        BOTID = self.getBotID(self.appName)
        while(True):
            if time.strftime("%M") == "00":#cada hora revisa todo.
                hola = self.mensahito
                self.today = time.strftime("%Y-%m-%d")
                if not self.lastOne == self.today and  time.strftime("%H") == "9":#check del backup solo a las 9
                    self.lastOne=self.today
                    self.msgBackups = self.getBackUP()#FIN backups
                self.estados = hydraServices.getStatus()
                self.msgRepo = self.getRepo()
                self.msgJenk = self.getJenkins()
                self.msgArt = self.getArtifac()
                self.msgVpn = self.getVPN()
                self.mensahito = self.msgBackups + self.msgRepo + self.msgJenk + self.msgArt + self.msgVpn
                if not hola == self.mensahito:
                    self.writeToSlack(self.canal, self.mensahito)
            print(self.mensahito)
            self.decideWheterToRespond(self.parseSlackInput(self.slackReadRTM(), BOTID))
            time.sleep(1)

if __name__ == "__main__":
    instance = mainFuc()
    instance.run()
