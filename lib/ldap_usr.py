from lib.globals_vars import LOGS_FORMAT,LOGFILE
from lib.ldap_check import get_uidNumber
from dotenv import dotenv_values
from paramiko import SSHClient
from logging.handlers import RotatingFileHandler
import logging
import os

logger = logging.getLogger(__name__)

def create_ldap_user(username:str, fullname:str, password:str, uidNumber):
    """
    Creates normal user in a ldap server

    Check documentation: 

    https://docs.oracle.com/cd/E22289_01/html/821-1279/ldapmodify.html
    """

    config = dotenv_values(r"C:\Users\User\Documents\Github\arcane-registrar\.env")

    handler = RotatingFileHandler(filename=LOGFILE, maxBytes=1000000, backupCount=5, encoding="utf-8")
    handler.setFormatter(logging.Formatter(LOGS_FORMAT))

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    # Define SSH credentials
    ssh = SSHClient()
    ssh.load_system_host_keys()

    logger.info(f"Attempting SSH username: "+config['SSH_USER'])
    logger.info(f"Attempting SSH to HOST: "+config['SSH_HOST'])
    print(f"Attempting SSH username: "+config['SSH_USER'])
    print(f"Attempting to connect to "+config['SSH_HOST'])
    print("-"*100)
    ssh.connect(
        hostname=config["SSH_HOST"],
        username=config["SSH_USER"],
        password=config["SSH_PASSWORD"])

    logger.info(f"Creating ldif file on: {config['SSH_HOST']}")
    print(f"Loading into ldif file the following:\nusername:{username},\nfullname:{fullname},\npassword:{password}")

    try:
        print(f"""cat <<EOF > /tmp/cr_usr.ldif\ndn: uid={username},cn=users,dc={config['DC1']},dc={config['DC2']}\nchangetype: add\nobjectclass: top\nobjectClass: posixAccount\nobjectClass: shadowAccount\nobjectclass: person\nobjectclass: organizationalPerson\nobjectclass: inetorgPerson\nobjectClass: apple-user\nobjectClass: sambaSamAccount\nobjectClass: sambaIdmapEntry\nobjectClass: extensibleObject\ncn: {username}\nuid: {username}\nuidNumber:{uidNumber}\nhomeDirectory: /home/{username}\nloginShell: /bin/sh\ngecos: {fullname}\nsn: {username}\nmail: {username}@hometest.ro\nuserPassword: {password}\nauthAuthority: ;basic;\nsambaSID: S-1-5-21-337860771-1958857223-4022494384-1007""")
        _stdin, _stdout, _stderr = ssh.exec_command(f"""cat <<EOF > /tmp/cr_usr.ldif\ndn: uid={username},cn=users,dc={config['DC1']},dc={config['DC2']}\nchangetype: add\nobjectclass: top\nobjectClass: posixAccount\nobjectClass: shadowAccount\nobjectclass: person\nobjectclass: organizationalPerson\nobjectclass: inetorgPerson\nobjectClass: apple-user\nobjectClass: sambaSamAccount\nobjectClass: sambaIdmapEntry\nobjectClass: extensibleObject\ncn: {username}\nuid: {username}\nuidNumber:{uidNumber}\nhomeDirectory: /home/{username}\nloginShell: /bin/sh\ngecos: {fullname}\nsn: {username}\nmail: {username}@hometest.ro\nuserPassword: {password}\nauthAuthority: ;basic;\nsambaSID: S-1-5-21-337860771-1958857223-4022494384-1007""")

        print("-"*100)
        print("Created LDIF file successfully...")
        print(_stdout.read().decode())
        print("Attempting to create user based on ldif file...")

        _stdin, _stdout, _stderr = ssh.exec_command(f"ldapmodify -x -c -V -H ldap://{config['SSH_HOST']} -D \"uid={config['LDAP_ACC']},cn=users,dc={config['DC1']},dc={config['DC2']}\" -w \"{config['LDAP_PASS']}!\" -f /tmp/cr_usr.ldif")
        print(_stdout.read().decode())

    except Exception as e:
        print("-"*100)
        logger.error("Failed to create user",exc_info=True)
        print(_stderr.read().decode())

    ssh.close()
