from time import sleep
from lib.globals_vars import LOGS_FORMAT,LOGFILE, ENV
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

    env=ENV()
    logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)

    # Define SSH credentials
    ssh = SSHClient()
    ssh.load_system_host_keys()

    print("-"*100)
    print(f"Running: {__name__}")

    logger.info(f"Attempting SSH username: {env.ssh_user} on HOST : {env.ssh_host}")
    print(f"Attempting SSH username: {env.ssh_user} on HOST : {env.ssh_host}")
    print("-"*100)

    try:
        ssh.connect(
            hostname=env.ssh_host,
            username=env.ssh_user,
            password=env.ssh_pw)

        print("Sleeping for 3 seconds...")
        sleep(3)

        try:
            print("-"*100)
            # print(f"""cat <<EOF > /tmp/cr_usr.ldif\ndn: uid={username},cn=users,dc={ldap_dc1},dc={ldap_dc2}\n"""+
            #     f"""changetype: add\nobjectclass: top\nobjectClass: posixAccount\nobjectClass: shadowAccount\nobjectclass: person\nobjectclass: organizationalPerson\nobjectclass: inetorgPerson\nobjectClass: apple-user\nobjectClass: sambaSamAccount\nobjectClass: sambaIdmapEntry\nobjectClass: extensibleObject\ncn: {username}\nuid: {username}\ngidNumber: 1000001\nuidNumber: {uidNumber}\nhomeDirectory: /home/{username}\nloginShell: /bin/sh\ngecos: {fullname}\nsn: {username}\nmail: {username}@hometest.ro\nuserPassword: {password}\nauthAuthority: ;basic;\nsambaSID: S-1-5-21-337860771-1958857223-4022494384-1007""")
            _stdin, _stdout, _stderr = ssh.exec_command(f"""cat <<EOF > /tmp/cr_usr.ldif\ndn: uid={username},cn=users,dc={env.dc1},dc={env.dc2}\nchangetype: add\nobjectclass: top\nobjectClass: posixAccount\nobjectClass: shadowAccount\nobjectclass: person\nobjectclass: organizationalPerson\nobjectclass: inetorgPerson\nobjectClass: apple-user\nobjectClass: sambaSamAccount\nobjectClass: sambaIdmapEntry\nobjectClass: extensibleObject\ncn: {username}\nuid: {username}\ngidNumber: 1000001\nuidNumber: {uidNumber}\nhomeDirectory: /home/{username}\nloginShell: /bin/sh\ngecos: {fullname}\nsn: {username}\nmail: {username}@hometest.ro\nuserPassword: {password}\nauthAuthority: ;basic;\nsambaSID: S-1-5-21-337860771-1958857223-4022494384-1007""")
            sleep(3)

            print("Created LDIF file successfully...")
            out = _stdout.read().decode()
            print(out)
            
            _stdout.close()
            _stderr.close()

            print("-"*100)

            if(env.env == "PROD"):
                command=f"ldapmodify -x -c -V -H ldaps://{env.ssh_host} -D \"uid={env.ldap_acc},cn=users,dc={env.dc1},dc={env.dc2}\" -w \"{env.ldap_pw}\" -f /tmp/cr_usr.ldif"
                print(command)

                _stdin, _stdout, _stderr = ssh.exec_command(command)

                sleep(5)
            
            if(env.env == "DEV"):
                command=f"ldapmodify -x -c -V -H ldaps://{env.ssh_host} -D \"uid={env.ldap_acc},cn=users,dc={env.dc1},dc={env.dc2}\" -w \"{env.ldap_pw}\" -f /tmp/cr_usr.ldif"
                print(command)

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
        
    except Exception as e:
        print(f"Error while attempting ssh conneciton. Error:{e}")
        logger.error(f"Error while attempting ssh conneciton. Error:{e}")

    print("-"*100)
    ssh.close()
    