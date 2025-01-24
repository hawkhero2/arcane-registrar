from lib.globals_vars import LOGS_FORMAT,LOGFILE
from paramiko import SSHClient
from dotenv import load_dotenv
import logging
import os

logger = logging.getLogger(__name__)

def create_ldap_user(username:str, fullname:str, password:str):
    """
    Creates normal user in a ldap server

    Check documentation: 

    https://docs.oracle.com/cd/E22289_01/html/821-1279/ldapmodify.html
    """
    
    logging.basicConfig(filename=LOGFILE, level=logging.INFO, format=LOGS_FORMAT)
    # Define SSH credentials
    load_dotenv()
    ssh = SSHClient()
    ssh.load_system_host_keys()

    logger.info("Attempting SSH...")
    
    print(f"Attempting to connect to {os.getenv('SSH_HOST')}")
    print("------------------------------------------------")
    ssh.connect(hostname=os.getenv("SSH_HOST"), username=os.getenv("SSH_USER"), password=os.getenv("SSH_PASSWORD"))

    logger.info("Creating ldif file")
    print(f"Loading into ldif file the following:\nusername:{username},\nfullname:{fullname},\npassword:{password}")

    try:
        _stdin, _stdout, _stderr = ssh.exec_command(f"""cat <<EOF > /tmp/cr_usr.ldif\ndn: uid={username},cn=users,dc={os.getenv('DC1')},dc={os.getenv('DC2')}\nchangetype: add\nobjectclass: top\nobjectClass: posixAccount\nobjectClass: shadowAccount\nobjectclass: person\nobjectclass: organizationalPerson\nobjectclass: inetorgPerson\nobjectClass: apple-user\nobjectClass: sambaSamAccount\nobjectClass: sambaIdmapEntry\nobjectClass: extensibleObject\ncn: {username}\nuid: {username}\nuidNumber: 100002\ngidNumber: 100003\nhomeDirectory: /home/{username}\nloginShell: /bin/sh\ngecos: {fullname}\nsn: {username}\nmail: {username}@hometest.ro\nuserPassword: {password}\nauthAuthority: ;basic;\nsambaSID: S-1-5-21-337860771-1958857223-4022494384-1007""")

        print("------------------------------------------------")
        print("Created file successfully...")
        print(_stdout.read().decode())
        print("Attempting to create user based on ldif file...")

        _stdin, _stdout, _stderr = ssh.exec_command(f"ldapmodify -x -c -V -H ldap://{os.getenv('SSH_HOST')} -D \"uid={os.getenv('LDAP_ACC')},cn=users,dc={os.getenv('DC1')},dc={os.getenv('DC2')}\" -w \"{os.getenv('LDAP_PASS')}!\" -f /tmp/cr_usr.ldif")
        print(_stdout.read().decode())
    except:
        print("------------------------------------------------")
        print(_stderr.read().decode())

    ssh.close()
