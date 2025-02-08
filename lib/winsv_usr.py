from lib.globals_vars import LOGS_FORMAT,LOGFILE
from paramiko import SSHClient
from dotenv import dotenv_values
import logging

logger = logging.getLogger(__name__)
# Purely for testing name
groupName="group1"

def create_winsv_user(username:str, fullname:str, password:str):
    """
    Creates normal user in a windows server
    Assigns user to a group without privileges

    @username: Username to be created
    @fullname: Full name of the user
    @password: Password for the user

    """

    print("-"*100)
    print(f"Running: {__name__}")
    config = dotenv_values(r"C:\Users\User\Documents\Github\arcane-registrar\.env")
    
    win_ssh_usr = config["W_SSH_USER"]
    win_ssh_pass = config["W_SSH_PASSWORD"]
    win_ssh_host = config["W_SSH_HOST"]
    
    logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    # Define SSH credentials
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=win_ssh_host, username=win_ssh_usr, password=win_ssh_pass)

    # Commands to run: 
    # net user {username} {password} /add
    # net localgroup groupName {username} /add

    try:
        _stdin, _stdout, _stderr= ssh.exec_command(f"powershell net user {username} {password} /add")
        print(_stdout.read().decode())
    except:
        print(_stderr.read().decode())
        logger.log(f"{_stderr.read().decode()}")

    if _stderr.read().decode() == "":
        try:
            _stdin, _stdout, _sterr = ssh.exec_command(f"powershell net localgroup {groupName} {username} /add")
            print(_stdout.read().decode())
        except:
            logger.log(f"{_sterr.read().decode()}")