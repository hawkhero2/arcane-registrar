from paramiko import SSHClient
from dotenv import load_dotenv
from lib.globals_vars import LOGS_FORMAT, LOGFILE   
import logging
import os


logger = logging.getLogger(__name__)

def ldap_search(objectClass: str):
    """

    Provide objectClass for the dn search
    @objectClass : Specify the base DN to use for the search operation.
    
    Example of parameter: "objectclass=*"
    
    Check documentation:
    https://docs.oracle.com/cd/E22289_01/html/821-1279/ldapsearch.html#scrolltoc

    """

    load_dotenv()
    logging.basicConfig(format=LOGS_FORMAT, filename=LOGFILE, level=logging.INFO)
    logger.info(f"Running {__name__} ...")
    logger.info(f"SSH-ing into {os.getenv('SSH_HOSTNAME')} ")

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=os.getenv("SSH_HOSTNAME"), username=os.getenv("SSH_USER"), password=os.getenv("SSH_PASSWORD"))

    _, _stdout, _stderr = ssh.exec_command(f"ldapsearch -D \"uid=andrei123,cn=users,dc=hometest,dc=ro\" -w \"Parola123!\" -b dc=hometest,dc=ro \"({objectClass})\"")

    outp = _stdout.read().decode()
    print(outp)
    
    print(_stderr.read().decode())
    ssh.close()

    logger.info(f"Finished running {__name__} ...")