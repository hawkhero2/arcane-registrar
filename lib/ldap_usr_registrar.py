from paramiko import SSHClient
from dotenv import load_dotenv
import os


def create_ldap_user(username, fullname, password):
    # Define SSH credentials
    load_dotenv()
    ssh = SSHClient()
    ssh.load_system_host_keys()
    print("Attempting to connect to 10.100.0.30")
    print(f"Username: {os.getenv('SSH_USER')}")
    print(f"Password: {os.getenv('SSH_PASSWORD')}")
    ssh.connect(hostname="10.100.0.30", username=os.getenv('SSH_USER'), password=os.getenv('SSH_PASSWORD'))

    _stdin, _stdout, _stderr = ssh.exec_command(f"""cat <<EOF > /tmp/filename.ldif
    # Start of {username}
    dn: uid={username},cn=users,dc=hometest,dc=ro
    objectclass: top
    objectclass: person
    objectclass: organizationalPerson
    objectclass: inetorgPerson
    cn: {username}
    uid: {username}
    gecos: {fullname}
    sn: {username}
    mail: {username}@hometest.ro
    userPassword: {password}
    """)
    print(_stdout.read().decode())
    print(_stderr.read().decode())
    _stdin, _stdout, _stderr = ssh.exec_command("ldapmodify -x -c \"dc=hometest,dc=ro\" -H ldap://10.100.0.30 -D \"uid=andrei123,cn=users,dc=hometest,dc=ro\" -w \"Parola123!\" -a -f /tmp/filename.ldif")
    print(_stdout.read().decode())
    print(_stderr.read().decode())
    ssh.close()
