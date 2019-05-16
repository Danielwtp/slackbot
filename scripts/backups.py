import subprocess
def checkeo(dia):
    backupsys = "ssh -p 2222 admins@jupiter.ls.fi.upm.es stat /home/backupsys/backup_" + dia + "_01.log"
    if subprocess.call(['bash','-c', backupsys],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 1:
        return("Backups: DOWN\n")
    else:
        return("Backups: UP\n")
