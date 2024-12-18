from paramiko import SSHClient
import argparse
from lib.ldap_usr_registrar import create_ldap_user

parser = argparse.ArgumentParser(description='Provide user to be created')
parser.add_argument('--username', help='Username to be created')
parser.add_argument('--fullname', help='Full name of the user')
parser.add_argument('--password', help='Password for the user')
args = parser.parse_args()

create_ldap_user(args.username, args.fullname, args.password)