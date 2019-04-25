import pytest

input = [{u'client_msg_id': u'dcf5f259-d202-40cc-bd9b-a1d5387c6b43', u'event_ts': u'1556016459.000800', u'suppress_notification': False, u'ts': u'1556016459.000800', u'text': u'<@UHS9H41DZ> test01', u'user': u'UG00W891N', u'team': u'T3HLFDTV5', u'type': u'message', u'channel': u'DJ5KC53ST'}]

#####Tests#####
@pytest.fixture
def slackComunucation():
    from monitoration_bot import slackComunucation
    return slackComunucation()

@pytest.fixture
def mainFuc():
    from monitoration_bot import mainFuc
    return mainFuc()

def test_slackConnect(slackComunucation):
    assert slackComunucation.slackConnect() == True

def test_parseSlackInput(slackComunucation):
    assert slackComunucation.parseSlackInput(input, "UHS9H41DZ") == ["UG00W891N","test01","DJ5KC53ST"]

def test_getBotID(slackComunucation):
    assert slackComunucation.getBotID("monitorationbot") == "UHS9H41DZ"

def test_writeToSlack(slackComunucation):
    assert slackComunucation.writeToSlack("CJ381CD2Q", "Hola que ase, soy un bot to flama")["ok"] == True

#@pytest.mark.skip(reason="not implemented")
def test_slackReadRTM(slackComunucation):
    slackComunucation.slackConnect()
    print slackComunucation.slackReadRTM

def test_decideWheterNotToAct(mainFuc):
    input = [None, None, None]
    assert mainFuc.decideWheterToRespond(input)

def test_decideWheterToRespond(mainFuc):
    input = ["UG00W891N","test01","DJ5KC53ST"]
    assert mainFuc.decideWheterToRespond(input)
