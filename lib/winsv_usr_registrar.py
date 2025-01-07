from lib.globals_vars import LOGS_FORMAT,LOGFILE
from paramiko import SSHClient
from dotenv import load_dotenv
import logging
import os

logger = logging.getLogger(__name__)

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

    ssh.connect(f"{os.getenv('SSH_HOSTNAME')}", username=os.getenv("SSH_USER"), password=os.getenv("SSH_PASSWORD"))