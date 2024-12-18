from paramiko import SSHClient
import yaml

def create_ldap_user(username, fullname, password):
    # Define SSH credentials
    with open("ssh_config.yaml") as f:
        config = yaml.safe_load(f)

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname="10.100.0.30", username=config["user"], password=config["password"])

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
    ssh.close()
