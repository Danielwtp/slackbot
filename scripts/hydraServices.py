import requests
def getStatus():
    repo = requests.get('https://repo.conwet.fi.upm.es', timeout=10).status_code
    jenkins = requests.get('https://build.conwet.fi.upm.es/jenkins/', timeout=10).status_code
    artifactory = requests.get('https://repo.conwet.fi.upm.es/artifactory', timeout=10).status_code
    if repo == 200:
        repo=True
    else:
        repo=False
    if jenkins == 200:
        jenkins=True
    else:
        jenkins=False
    if artifactory == 200:
        artifactory=True
    else:
        artifactory=False
    return [repo, jenkins, artifactory]

#"https://repo.conwet.fi.upm.es/users/sign_in").getcode()
#respuesta[1] = print(urllib.request.urlopen("https://build.conwet.fi.upm.es/jenkins/").getcode()
#respuesta[2] = urllib.request.urlopen("https://repo.conwet.fi.upm.es/artifactory").getcode()
