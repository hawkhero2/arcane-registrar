from lib.ldap_usr_registrar import create_ldap_user
from lib.ldap_check import ldap_search
from lib.globals_vars import LOGFILE, LOGS_FORMAT
from paramiko import SSHClient
import argparse
import logging

logger = logging.getLogger("Arcane Creator")
parser = argparse.ArgumentParser(description="Utility script for creating users in multiple environments and performing ldapsearch")
parser.add_argument("--username", help="Username to be created",default="")
parser.add_argument("--fullname", help="Full name of the user",default="")
parser.add_argument("--password", help="Password for the user",default="")
parser.add_argument("--check", help="Perform ldapsearch on ldap, provide y/n", choices=["y","n"], default="n")
args = parser.parse_args()

def main():
    logging.basicConfig(filename=LOGFILE, level=logging.INFO, format=LOGS_FORMAT)
    logger.info("Started ...")

    if(args.check == "y"):
        ldap_search("objectclass=*") 
    else:
        # Just for testing
        if args.username == "" or args.fullname == "" or args.password == "":
            print("Didnt' provide values for either --username, --fullname or password.\nUsing some values for testing...") 
            usr ="gog13"
            fn="gog k"
            pw="Parola123$"
            create_ldap_user(usr,fn,pw)

        else:
            create_ldap_user(args.username, args.fullname, args.password)

    logger.info("Finished running arcane creator")

if __name__=="__main__":
    main()