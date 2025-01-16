from lib.globals_vars import LOGS_FORMAT,LOGFILE
from paramiko import SSHClient
from dotenv import load_dotenv
import logging
import os

logger = logging.getLogger(__name__)
# Purely for testing name
groupName="group1"

def create_winsv_user(username:str, fullname:str, password:str):
    """
    Creates normal user in a windows server

    """

    logging.basicConfig(filename=LOGFILE, level=logging.INFO, format=LOGS_FORMAT)
    # Define SSH credentials
    load_dotenv()
    ssh = SSHClient()
    ssh.load_system_host_keys()

    # Commands to run: 
    # net user {username} {password} /add
    # net localgroup groupName {username} /add

    ssh.connect(f"{os.getenv('W_SSH_HOST')}", username=os.getenv("W_SSH_USER"), password=os.getenv("W_SSH_PASSWORD"))

    _stdin, _stdout, _sterr = ssh.exec_command(f"powershell net user {username} {password} /add")
    print(_stdout.read().decode())

    _stdin, _stdout, _sterr = ssh.exec_command(f"powershell net localgroup {groupName} {username} /add")
    print(_stdout.read().decode())