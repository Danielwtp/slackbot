import subprocess
def getVPN():
    result=subprocess.run(['echo', '"abcd"', '|', 'nc', '-uvw2', '138.100.12.106', '1194'], stdout=subprocess.PIPE).returncode
    if result == 0:
        return("VPN: UP\n")
    else:
        return("VPN: DOWN\n")
