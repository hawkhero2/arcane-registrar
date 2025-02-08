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
    
    ldap_acc = config["LDAP_ACC"]
    ldap_pass = config["LDAP_PASS"]
    ldap_dc1 = config["DC1"]
    ldap_dc2 = config["DC2"]
    ssh_usr = config["SSH_USER"]
    ssh_pass = config["SSH_PASSWORD"]
    ssh_host = config["SSH_HOST"]

    logging.basicConfig(filemode=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    logger.info(f"Running {__name__} ...")
    logger.info(f"SSH-ing into {config['SSH_HOST']} ")

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=ssh_host,
                username=ssh_usr,
                password=ssh_pass)

    print("-"*100)

    print(f"Using the following credentials:\nuser:{ldap_acc}\npass:{ldap_pass}")
    _, _stdout, _stderr = ssh.exec_command(f"ldapsearch -D \"uid={ldap_acc},cn=users,dc={ldap_dc1},dc={ldap_dc2}\" -w \"{ldap_pass}\" -b dc={ldap_dc1},dc={ldap_dc2} \"({objectClass})\"")
    print("-"*100)
    print(f"ldapsearch -D \"uid={ldap_acc},cn=users,dc={ldap_dc1},dc={ldap_dc2}\" -w \"{ldap_pass}\" -b dc={ldap_dc1},dc={ldap_dc2} \"({objectClass})\"")

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
    logging.basicConfig(filemode=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    ldap_acc = config["LDAP_ACC"]
    ldap_pass = config["LDAP_PASS"]
    ldap_dc1 = config["DC1"]
    ldap_dc2 = config["DC2"]
    ssh_usr = config["SSH_USER"]
    ssh_pass = config["SSH_PASSWORD"]
    ssh_host = config["SSH_HOST"]

    logger.setLevel(logging.INFO)
    logger.info(f"Running {__name__} ...")
    logger.info(f"SSH-ing into {config['SSH_HOST']} ")
    print("-"*100)

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=ssh_host, username=ssh_usr, password=ssh_pass)

    print(f"Using the following credentials:\nuser:{ldap_acc}\npass:{ldap_pass}")

    if(config['ENV'] == "DEV"):
        cmd = f"ldapsearch -D \"uid={ldap_acc},cn=users,dc={ldap_dc1},dc={ldap_dc2}\" -w \"{ldap_pass}\" -b dc={ldap_dc1},dc={ldap_dc2} \"({objectClass})\""
        _, _stdout, _stderr = ssh.exec_command(cmd)
    if(config['ENV'] == "PROD"):
        cmd = f"ldapsearch -x -H ldaps://{ssh_host} -D \"uid={ldap_acc},cn=users,dc={ldap_dc1},dc={ldap_dc2}\" -w \"{ldap_pass}\" -b dc={ldap_dc1},dc={ldap_dc2} \"({objectClass})\""
        _, _stdout, _stderr = ssh.exec_command()

    print(f"ldapsearch -D \"uid={ldap_acc},cn=users,dc={ldap_dc1},dc={ldap_dc2}\" -w \"{ldap_pass}\" -b dc={ldap_dc1},dc={ldap_dc2} \"({objectClass})\"")
    print("-"*100)

    outp = _stdout.read().decode().split("\n")
    for line in outp:
        if line.__contains__("uidNumber"):
            uidNumber=line.split(":")[1]
    
    print(_stderr.read().decode())
    ssh.close()

    logger.info(f"Finished running {__name__} ...")

    return int(uidNumber)