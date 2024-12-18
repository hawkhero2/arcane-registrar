from paramiko import SSHClient
import yaml
import argparse
from lib.ldap_usr_registrar import create_ldap_user

parser = argparse.ArgumentParser(description='Provide user to be created')
parser.add_argument('--username', type=str, help='Username to be created')
parser.add_argument('--fullname', type=str, help='Full name of the user')
parser.add_argument('--password', type=str, help='Password for the user')
args = parser.parse_args()

create_ldap_user(args.username, args.fullname, args.password)