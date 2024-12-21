from paramiko import SSHClient
from dotenv import load_dotenv
import logging
import os

logger = logging.getLogger(__name__)

def ldap_search(objectClass: str) -> tuple[str, str]:
    """

    Provide objectClass for the dn search
    @objectClass : Specify the base DN to use for the search operation.
    
    Example of parameter: "objectclass=*"
    
    Check documentation:
    https://docs.oracle.com/cd/E22289_01/html/821-1279/ldapsearch.html#scrolltoc

    """
    logger.info('Running a ldap check')
    load_dotenv()
    print(f"SSH-ing into {os.getenv('SSH_HOSTNAME')}")
    ssh = SSHClient()
    ssh.load_system_host_keys()

    ssh.connect(hostname=os.getenv('SSH_HOSTNAME'), username=os.getenv('SSH_USER'), password=os.getenv('SSH_PASSWORD'))

    _, _stdout, _stderr = ssh.exec_command(f"ldapsearch -D \"uid=andrei123,cn=users,dc=hometest,dc=ro\" -w \"Parola123!\" -b dc=hometest,dc=ro \"({objectClass})\"")

    ssh.close()

    if (err := _stderr.readline()) !="":
        return "", err
    else:
        return _stdout.readlines(), ""
    