import requests
def getStatus():
    try:
        repo = requests.get('https://repo.conwet.fi.upm.es', timeout=10).status_code
        if repo == 200:
            repo=True
        else:
            repo=False
    except:
        repo=False
    try:
        jenkins = requests.get('https://build.conwet.fi.upm.es/jenkins/', timeout=10).status_code
        if jenkins == 200:
            jenkins=True
        else:
            jenkins=False
    except:
        jenkins=False
    try:
        artifactory = requests.get('https://repo.conwet.fi.upm.es/artifactory', timeout=10).status_code
        if artifactory == 200:
            artifactory=True
        else:
            artifactory=False
    except:
        artifactory=False

    return [repo, jenkins, artifactory]

def getRepo():
    try:
        repo = requests.get('https://repo.conwet.fi.upm.es', timeout=10).status_code
        if repo == 200:
            repo=True
        else:
            repo=False
    except:
        repo=False
    if repo:
        return("Repo: UP\n")
    else:
        return("Repo: DOWN\n")

def getJenkins():
    try:
        jenkins = requests.get('https://build.conwet.fi.upm.es/jenkins/', timeout=10).status_code
        if jenkins == 200:
            jenkins=True
        else:
            jenkins=False
    except:
        jenkins=False
    if jenkins:
        return("Jenkins: UP\n")
    else:
        return("Jenkins: DOWN\n")

def getArtifac():
    try:
        artifactory = requests.get('https://repo.conwet.fi.upm.es/artifactory', timeout=10).status_code
        if artifactory == 200:
            artifactory=True
        else:
            artifactory=False
    except:
        artifactory=False
    if artifactory:
        return("Artifactory: UP\n")
    else:
        return("Artifactory: DOWN\n")
