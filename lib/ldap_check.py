from paramiko import SSHClient
from dotenv import load_dotenv
from lib.globals_vars import LOGS_FORMAT, LOGFILE   
import logging
import os


logger = logging.getLogger(__name__)

def ldap_search(objectClass: str = "objectclass=*"):
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
    logger.info(f"SSH-ing into {os.getenv('SSH_HOST')} ")

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=os.getenv("SSH_HOST"), username=os.getenv("SSH_USER"), password=os.getenv("SSH_PASSWORD"))

    _, _stdout, _stderr = ssh.exec_command(f"ldapsearch -x -H ldaps://{os.getenv('SSH_HOST')} -D \"uid={os.getenv('LDAP_ACC')},cn=users,dc={os.getenv('DC1')},dc={os.getenv('DC2')}\" -w \"{os.getenv('LDAP_PASS')}\" -b dc={os.getenv('DC1')},dc={os.getenv('DC2')} {objectClass}")

    outp = _stdout.read().decode()
    print(outp)
    
    print(_stderr.read().decode())
    ssh.close()

    logger.info(f"Finished running {__name__} ...")