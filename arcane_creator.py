from lib.ldap_check import ldap_search, get_uidNumber
from lib.ldap_usr import create_ldap_user
from lib.winsv_usr import create_winsv_user
from lib.rocketchat_usr import create_rocketchat_user
from lib.globals_vars import LOGFILE, LOGS_FORMAT
from time import sleep
import argparse
import logging
import os

logger = logging.getLogger("Arcane Creator")
parser = argparse.ArgumentParser(description="Utility script for creating users in multiple environments and performing ldapsearch")

parser.add_argument("--username", help="Username to be created",default="")
parser.add_argument("--fullname", help="Full name of the user",default="")
parser.add_argument("--password", help="Password for the user",default="")
parser.add_argument("--check", help="Checking info about the LDAP",default="")
parser.add_argument("--file", help="Provide file for creating multiple users; Must be in the format, each user on a new line: user,fullname,pass,email",default="")
parser.add_argument("--email", help="Provide email for the user, needed for chat account", default="")
args = parser.parse_args()

def main():

    logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)
    logger.info("Started ...")

    print("Reading parameters")
    print("-"*100)

    if args.file == "":
        if (args.username != "" and 
            args.fullname != "" and 
            args.password != "" and 
            args.email !=""):
            # Since all args are non empty we proceed with user creation
            print(f"Creating single user provided: {args.username}")
            create_ldap_user(username=f"{args.username}", fullname=f"{args.fullname}", password=f"{args.password}")
            # sleep(5)
            # create_winsv_user(username=args.username, fullname=args.fullname, password=args.password) 
            # sleep(5)
            # create_rocketchat_user(username=args.username, fullname=args.fullname, password=args.password, email=args.email) 
            # sleep(5)
        else:
            print("Missing arguments, checking if file was passed....")
    if(args.file != "" and os.path.exists(args.file)):
        uidNumber = get_uidNumber()
        with open(args.file, "r") as f:
            for line in f:
                uidNumber=uidNumber+1
                print(f"uidNumber: {str(uidNumber)}")
                usr,fn,pw, mail = line.split(",")
                sleep(5)
                create_ldap_user(username=usr, fullname=fn, password=pw, uidNumber=uidNumber)
                sleep(5)
                # create_winsv_user(username=usr, fullname=fn, password=pw)
                # sleep(5)
                # create_rocketchat_user(username=usr, fullname=fn, password=pw, email=mail)
                # sleep(5)
    if(args.check != ""):
        print("You did not provide any user or file...\nRunning a ldap search")
        ldap_search()

    else:
        print("Missing arguments for single user creation, or file for multiple users")
        logger.error("Missing arguments for single user creation, or file for multiple users")
        print("Exiting...")
        logger.info("Exiting...")

    logger.info("Finished running arcane creator")

if __name__=="__main__":
    main()