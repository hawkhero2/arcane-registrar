from paramiko import SSHClient
from lib.globals_vars import LOGS_FORMAT, LOGFILE   
from logging.handlers import RotatingFileHandler
from dotenv import dotenv_values
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

    config = dotenv_values(r"C:\Users\User\Documents\Github\arcane-registrar\.env")
    
    handler = RotatingFileHandler(filename=LOGFILE, maxBytes=1000000, backupCount=5, encoding="utf-8")
    handler.setFormatter(logging.Formatter(LOGS_FORMAT))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info(f"Running {__name__} ...")
    logger.info(f"SSH-ing into {config['SSH_HOST']} ")

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=config["SSH_HOST"], username="andrei", password=config["SSH_PASSWORD"])
    print("-"*100)

    print(f"Using the following credentials:\nuser:{config['LDAP_ACC']}\npass:{config['LDAP_PASS']}")
    _, _stdout, _stderr = ssh.exec_command(f"ldapsearch -D \"uid={config['LDAP_ACC']},cn=users,dc={config['DC1']},dc={config['DC2']}\" -w \"{config['LDAP_PASS']}\" -b dc={config['DC1']},dc={config['DC2']} \"({objectClass})\"")
    print("-"*100)
    print(f"ldapsearch -D \"uid={config['LDAP_ACC']},cn=users,dc={config['DC1']},dc={config['DC2']}\" -w \"{config['LDAP_PASS']}\" -b dc={config['DC1']},dc={config['DC2']} \"({objectClass})\"")

    print("-"*100)
    outp = _stdout.read().decode()
    print(outp)
    
    print(_stderr.read().decode())
    ssh.close()

    logger.info(f"Finished running {__name__} ...")
    print("-"*100)

def get_uidNumber() -> int:

    objectClass="uidNumber=*"
    uidNumber=""
    config = dotenv_values(r"C:\Users\User\Documents\Github\arcane-registrar\.env")

    handler = RotatingFileHandler(filename=LOGFILE, maxBytes=1000000, backupCount=5, encoding="utf-8")
    handler.setFormatter(logging.Formatter(LOGS_FORMAT))

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info(f"Running {__name__} ...")
    logger.info(f"SSH-ing into {config['SSH_HOST']} ")

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=config["SSH_HOST"], username="andrei", password=config["SSH_PASSWORD"])
    print("-"*100)

    print(f"Using the following credentials:\nuser:{config['LDAP_ACC']}\npass:{config['LDAP_PASS']}")
    _, _stdout, _stderr = ssh.exec_command(f"ldapsearch -D \"uid={config['LDAP_ACC']},cn=users,dc={config['DC1']},dc={config['DC2']}\" -w \"{config['LDAP_PASS']}\" -b dc={config['DC1']},dc={config['DC2']} \"({objectClass})\"")
    
    print(f"ldapsearch -D \"uid={config['LDAP_ACC']},cn=users,dc={config['DC1']},dc={config['DC2']}\" -w \"{config['LDAP_PASS']}\" -b dc={config['DC1']},dc={config['DC2']} \"({objectClass})\"")
    print("-"*100)

    outp = _stdout.read().decode().split("\n")
    for line in outp:
        if line.__contains__("uidNumber"):
            uidNumber=line.split(":")[1]
    
    print(_stderr.read().decode())
    ssh.close()

    logger.info(f"Finished running {__name__} ...")

    return int(uidNumber)