from time import sleep
from lib.globals_vars import LOGS_FORMAT,LOGFILE
from lib.ldap_check import get_uidNumber
from dotenv import dotenv_values
from paramiko import SSHClient
from paramiko import transport
import logging

logger = logging.getLogger(__name__)

def create_ldap_user(username:str, fullname:str, password:str, uidNumber):
    """
    Creates normal user in a ldap server

    Check documentation: 

    https://docs.oracle.com/cd/E22289_01/html/821-1279/ldapmodify.html
    """

    config = dotenv_values(r"C:\Users\User\Documents\Github\arcane-registrar\.env")

    logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    # Define SSH credentials
    ssh = SSHClient()
    ssh.load_system_host_keys()

    ssh_host = config["SSH_HOST"]
    ssh_acc = config['SSH_USER']
    ssh_pass = config["SSH_PASSWORD"]
    ldap_acc = config["LDAP_ACC"]
    ldap_pass = config["LDAP_PASS"]
    ldap_dc1 = config["DC1"]
    ldap_dc2 = config["DC2"]
    
    print("-"*100)
    print(f"Running: {__name__}")
    logger.info(f"Attempting SSH username: {ssh_acc} on HOST : {ssh_host}")
    print(f"Attempting SSH username: {ssh_acc} on HOST : {ssh_host}")
    print("-"*100)

    ssh.connect(
        hostname=ssh_host,
        username=ssh_acc,
        password=ssh_pass)

    print("Sleeping for 5 seconds...")
    sleep(5)
    logger.info(f"Creating ldif file. for user : {username} and fullname: {fullname}")
    print(f"Loading into ldif file the following:\nusername:{username},\nfullname:{fullname},\npassword:{password}")

    try:
        print("-"*100)
        print(f"""cat <<EOF > /tmp/cr_usr.ldif\ndn: uid={username},cn=users,dc={ldap_dc1},dc={ldap_dc2}\n"""+
              f"""changetype: add\nobjectclass: top\nobjectClass: posixAccount\nobjectClass: shadowAccount\nobjectclass: person\nobjectclass: organizationalPerson\nobjectclass: inetorgPerson\nobjectClass: apple-user\nobjectClass: sambaSamAccount\nobjectClass: sambaIdmapEntry\nobjectClass: extensibleObject\ncn: {username}\nuid: {username}\ngidNumber: 1000001\nuidNumber: {uidNumber}\nhomeDirectory: /home/{username}\nloginShell: /bin/sh\ngecos: {fullname}\nsn: {username}\nmail: {username}@hometest.ro\nuserPassword: {password}\nauthAuthority: ;basic;\nsambaSID: S-1-5-21-337860771-1958857223-4022494384-1007""")
        _stdin, _stdout, _stderr = ssh.exec_command(f"""cat <<EOF > /tmp/cr_usr.ldif\ndn: uid={username},cn=users,dc={config['DC1']},dc={config['DC2']}\nchangetype: add\nobjectclass: top\nobjectClass: posixAccount\nobjectClass: shadowAccount\nobjectclass: person\nobjectclass: organizationalPerson\nobjectclass: inetorgPerson\nobjectClass: apple-user\nobjectClass: sambaSamAccount\nobjectClass: sambaIdmapEntry\nobjectClass: extensibleObject\ncn: {username}\nuid: {username}\ngidNumber: 1000001\nuidNumber: {uidNumber}\nhomeDirectory: /home/{username}\nloginShell: /bin/sh\ngecos: {fullname}\nsn: {username}\nmail: {username}@hometest.ro\nuserPassword: {password}\nauthAuthority: ;basic;\nsambaSID: S-1-5-21-337860771-1958857223-4022494384-1007""")
        sleep(5)

        print("-"*100)
        print("Created LDIF file successfully...")
        out = _stdout.read().decode()
        print(out)
        _stdout.close()
        _stderr.close()

        print("-"*100)
        print("Attempting to create user based on ldif file...")

        if(config['ENV'] == "PROD"):
            print(f"Executing ldapmodify in the following context:\n\"uid={ldap_acc},cn=users,dc={ldap_dc1},dc={ldap_dc2}\"")
            command=f"ldapmodify -x -c -V -H ldaps://{ssh_host} -D \"uid={ldap_acc},cn=users,dc={ldap_dc1},dc={ldap_dc2}\" -w \"{ldap_pass}\" -f /tmp/cr_usr.ldif"
            print(command)
            _stdin, _stdout, _stderr = ssh.exec_command(command)
            sleep(5)
        
        if(config['ENV'] == "DEV"):
            print(f"Executing ldapmodify in the following context:\n\"uid={ldap_acc},cn=users,dc={ldap_dc1},dc={ldap_dc2}\"")
            command=f"ldapmodify -x -c -V -H ldaps://{ssh_host} -D \"uid={ldap_acc},cn=users,dc={ldap_dc1},dc={ldap_dc2}\" -w \"{ldap_pass}\" -f /tmp/cr_usr.ldif"
            _stdin, _stdout, _stderr = ssh.exec_command(command)
            sleep(5)

        print("-"*100)
        out = _stdout.read().decode()
        print(out)
        logger.info(f"{out}")

        err_msg = _stderr.read().decode()
        logger.error(f"{err_msg}")
        print(f"{err_msg}")

        _stdout.close()
        _stderr.close()

    except Exception as e:
        print("-"*100)
        logger.error("Failed to create user",exc_info=True)
        logger.error(f"{_stderr.read().decode()}")
        logger.error(f"{_stdout.read().decode()}")
        print(_stderr.read().decode())

    print("-"*100)
    ssh.close()
    