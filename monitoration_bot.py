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
        self.msgBackups = backups.checkeo(time.strftime("%Y-%m-%d"))
        self.msgRepo = hydraServices.getRepo()
        self.msgJenk = hydraServices.getJenkins()
        self.msgArt = hydraServices.getArtifac()
        self.msgVpn = VPNCheck.getVPN()
        self.mensahito = self.msgBackups + self.msgRepo + self.msgJenk + self.msgArt + self.msgVpn
        print(self.mensahito)

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
            if message == "help":
                return self.writeToSlack(channel, "\"@Monitoration_Bot status\": devuelve el estado actual de las maquinas")

    def run(self):
        self.slackConnect()
        BOTID = self.getBotID(self.appName)
        while(True):
            if not (time.strftime("%H") == 1 or time.strftime("%H") == 2):
                if time.strftime("%M") == "00":#cada hora revisa todo, excepto el backups
                    hola = self.mensahito
                    if time.strftime("%H") == "9":#check del backup solo a las 9
                        self.msgBackups = backups.checkeo(time.strftime("%Y-%m-%d"))#FIN backups
                    self.estados = hydraServices.getStatus()
                    self.msgRepo = hydraServices.getRepo()
                    self.msgJenk = hydraServices.getJenkins()
                    self.msgArt = hydraServices.getArtifac()
                    self.msgVpn = VPNCheck.getVPN()
                    self.mensahito = self.msgBackups + self.msgRepo + self.msgJenk + self.msgArt + self.msgVpn
                    if not hola == self.mensahito:
                        self.writeToSlack(self.canal, self.mensahito)
            self.decideWheterToRespond(self.parseSlackInput(self.slackReadRTM(), BOTID))
            time.sleep(1)

if __name__ == "__main__":
    instance = mainFuc()
    instance.run()
