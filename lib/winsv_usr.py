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

    logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    print("-"*100)
    print(f"Running: {__name__}")
    logger.info(f"Running: {__name__}")

    config = dotenv_values(r"C:\Users\User\Documents\Github\arcane-registrar\.env")
    
    win_ssh_usr = config["W_SSH_USER"]
    win_ssh_pass = config["W_SSH_PASSWORD"]
    win_ssh_host = config["W_SSH_HOST"]

    # Define SSH credentials
    ssh = SSHClient()
    ssh.load_system_host_keys()

    print(f"SSH-ing into\nHost: {win_ssh_host}")
    logger.info(f"SSH-ing into\nHost: {win_ssh_host}")

    ssh.connect(hostname=win_ssh_host, username=win_ssh_usr, password=win_ssh_pass)

    # Commands to run: 
    # net user {username} {password} /add
    # net localgroup groupName {username} /add

    try:
        print(f"{__name__}: Creating user: {username}")
        logger.info(f"{__name__}: Creating user: {username}")
        print("-"*100)

        _stdin, _stdout, _stderr= ssh.exec_command(f"powershell net user {username} {password} /add")
        print(_stdout.read().decode())
    except:
        print(_stderr.read().decode())
        logger.log(f"{_stderr.read().decode()}")

    if _stderr.read().decode() == "":
        try:
            print(f"{__name__}: Adding user: {username} to basic group")
            logger.info(f"{__name__}: Adding user: {username} to basic group")
            print("-"*100)

            _stdin, _stdout, _sterr = ssh.exec_command(f"powershell net localgroup {groupName} {username} /add")
            print(_stdout.read().decode())
        except:
            logger.log(f"{_sterr.read().decode()}")