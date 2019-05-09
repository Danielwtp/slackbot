import requests
def getStatus():
    repo = requests.get('https://repo.conwet.fi.upm.es')
    jenkins = requests.get('https://build.conwet.fi.upm.es/jenkins/')
    artifactory = requests.get('https://repo.conwet.fi.upm.es/artifactory')
    if repo = "<Response [200]>":
        repo=True
    else:
        repo=False
    if jenkins = "<Response [200]>":
        repo=True
    else:
        repo=False
    if artifactory = "<Response [200]>":
        repo=True
    else:
        repo=False
    return [repo, jenkins, artifactory]

#"https://repo.conwet.fi.upm.es/users/sign_in").getcode()
#respuesta[1] = print(urllib.request.urlopen("https://build.conwet.fi.upm.es/jenkins/").getcode()
#respuesta[2] = urllib.request.urlopen("https://repo.conwet.fi.upm.es/artifactory").getcode()
