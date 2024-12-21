from paramiko import SSHClient
from lib.ldap_usr_registrar import create_ldap_user
from lib.ldap_check import ldap_search
import argparse
import logging

logger = logging.getLogger("Arcane Creator")
parser = argparse.ArgumentParser(description='Provide user to be created')
parser.add_argument('--username', help='Username to be created',default="")
parser.add_argument('--fullname', help='Full name of the user',default="")
parser.add_argument('--password', help='Password for the user',default="")
parser.add_argument("--check", help="Perform ldapsearch on ldap, provide a boolean", choices=["y","n"], default="n")
args = parser.parse_args()

def main():
    logging.basicConfig(filename="logs.log", level=logging.INFO)
    logger.info("Started ...")
    if(args.check == "y"):
        output,err=ldap_search("objectclass=*") 
        if(output !=""):
            for line in output:
                print(line)
        else:
            for line in err:
                print(err)
    else:
        print("You didn't provide anything")
    # testing
    # usr ="gog13"
    # fn="gog k"
    # pw="Parola123$"
    # create_ldap_user(usr,fn,pw)
# if args.username is None or args.fullname is None or args.password is None:
#     print("Missing arguments --username, --fullname or --password") 
# else:
#     create_ldap_user(args.username, args.fullname, args.password)
    logger.info("Finished running..")
if __name__=="__main__":
    main()