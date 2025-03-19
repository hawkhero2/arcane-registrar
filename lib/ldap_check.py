from paramiko import SSHClient
from lib.globals_vars import LOGS_FORMAT, LOGFILE, ENV
import logging

logger = logging.getLogger(__name__)

def ldap_search(objectClass: str = "objectclass=*"):
    """
    Provide objectClass for the dn search
    @objectClass : Specify the base DN to use for the search operation.
    
    Example of parameter: "objectclass=*"
    
    Check documentation:
    https://docs.oracle.com/cd/E22289_01/html/821-1279/ldapsearch.html#scrolltoc

    """

    env=ENV()
    logging.basicConfig(filemode=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    logger.info(f"Running {__name__} ...")
    logger.info(f"SSH-ing into {env.ssh_host} ")

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=env.ssh_host,
                username=env.ssh_user,
                password=env.ssh_pw)

    print("-"*100)

    print(f"Using the following credentials:\nuser:{env.ldap_acc}\npass:{env.ldap_pw}")
    _, _stdout, _stderr = ssh.exec_command(f"ldapsearch -D \"uid={env.ldap_acc},cn=users,dc={env.dc1},dc={env.dc2}\" -w \"{env.ldap_pw}\" -b dc={env.dc1},dc={env.dc2} \"({objectClass})\"")
    print("-"*100)
    print(f"ldapsearch -D \"uid={env.ldap_acc},cn=users,dc={env.dc1},dc={env.dc2}\" -w \"{env.ldap_pw}\" -b dc={env.dc1},dc={env.dc2} \"({objectClass})\"")

    print("-"*100)
    outp = _stdout.read().decode()
    print(outp)
    
    print(_stderr.read().decode())
    ssh.close()

    logger.info(f"Finished running {__name__} ...")
    print("-"*100)

def get_uidNumber() -> int:

    objectClass="uidNumber=*"
    env=ENV()
    uidNumber=""
    logging.basicConfig(filemode=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    logger.setLevel(logging.INFO)
    logger.info(f"Running {__name__} ...")
    logger.info(f"SSH-ing into {env.ssh_host} ")
    print("-"*100)

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=env.ssh_host, username=env.ssh_user, password=env.ssh_pw)

    print(f"Using the following credentials:\nuser:{env.ldap_acc}\npass:{env.ldap_pw}")

    if(env.env == "DEV"):
        cmd = f"ldapsearch -D \"uid={env.ldap_acc},cn=users,dc={env.dc1},dc={env.dc2}\" -w \"{env.ldap_pw}\" -b dc={env.dc1},dc={env.dc2} \"({objectClass})\""
        _, _stdout, _stderr = ssh.exec_command(cmd)
    if(env.env == "PROD"):
        cmd = f"ldapsearch -x -H ldaps://{env.ssh_host} -D \"uid={env.ldap_acc},cn=users,dc={env.dc1},dc={env.dc2}\" -w \"{env.ldap_pw}\" -b dc={env.dc1},dc={env.dc2} \"({objectClass})\""
        _, _stdout, _stderr = ssh.exec_command()

    print(f"ldapsearch -D \"uid={env.ldap_acc},cn=users,dc={env.dc1},dc={env.dc2}\" -w \"{env.ldap_pw}\" -b dc={env.dc1},dc={env.dc2} \"({objectClass})\"")
    print("-"*100)

    outp = _stdout.read().decode().split("\n")
    for line in outp:
        if line.__contains__("uidNumber"):
            uidNumber=line.split(":")[1]
    
    print(_stderr.read().decode())
    ssh.close()

    logger.info(f"Finished running {__name__} ...")

    return int(uidNumber)