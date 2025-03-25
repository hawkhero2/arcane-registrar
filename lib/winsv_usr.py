from lib.globals_vars import LOGS_FORMAT,LOGFILE, ENV
from paramiko import SSHClient
import logging

logger = logging.getLogger(__name__)

def create_winsv_user(username:str, fullname:str, password:str):
    """
    Creates normal user in a windows server
    Assigns user to a group without privileges

    @username: Username to be created
    @fullname: Full name of the user
    @password: Password for the user

    """

    env = ENV()
    logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    print(f"Running: {__name__}")
    logger.info(f"Running: {__name__}")
    
    # Define SSH credentials
    ssh = SSHClient()
    ssh.load_system_host_keys()

    print(f"Attempting SSH username : {env.win_ssh_user} on HOST : {env.win_ssh_host}")
    logger.info(f"Attempting SSH username : {env.win_ssh_user} on HOST : {env.win_ssh_host}")

    ssh.connect(hostname=env.win_ssh_host, 
                username=env.win_ssh_user, 
                password=env.win_ssh_pw)

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
            print(f"{__name__}: Adding user: {username} to group : {env.grp}")
            logger.info(f"{__name__}: Adding user: {username} to group : {env.grp}")
            print("-"*100)

            _stdin, _stdout, _sterr = ssh.exec_command(f"powershell net localgroup {env.grp} {username} /add")
            print(_stdout.read().decode())
        except:
            logger.log(f"{_sterr.read().decode()}")