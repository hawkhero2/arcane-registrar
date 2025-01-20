from lib.ldap_usr import create_ldap_user
from lib.winsv_usr import create_winsv_user
from lib.rocketchat_usr import create_rocketchat_user
from lib.globals_vars import LOGFILE, LOGS_FORMAT
import argparse
import logging
import os

logger = logging.getLogger("Arcane Creator")
parser = argparse.ArgumentParser(description="Utility script for creating users in multiple environments and performing ldapsearch")
parser.add_argument("--username", help="Username to be created",default="")
parser.add_argument("--fullname", help="Full name of the user",default="")
parser.add_argument("--password", help="Password for the user",default="")
parser.add_argument("--file", help="Provide file for creating multiple users; Must be in the format, each user on a new line: user,fullname,pass,email",default="")
parser.add_argument("--email", help="Provide email for the user, needed for chat account", default="")
args = parser.parse_args()

def main():
    logging.basicConfig(filename=LOGFILE, level=logging.INFO, format=LOGS_FORMAT)
    logger.info("Started ...")
    print("Received parameteres...")
    print("Executing script...")
    print("------------------------------------------------")

    if args.file == "":
        if args.username != "" and args.fullname != "" and args.password != "" and args.email !="":
            create_ldap_user(username=args.username, fullname=args.fullname, password=args.password)
            create_winsv_user(username=args.username, fullname=args.fullname, password=args.password) 
            create_rocketchat_user(username=args.username, fullname=args.fullname, password=args.password, email=args.email) 
    elif os.path.exists(args.file):
        with open(args.file, "r") as f:
            for line in f:
                usr,fn,pw, mail = line.split(",")
                create_ldap_user(username=usr, fullname=fn, password=pw)
                create_winsv_user(username=usr, fullname=fn, password=pw)
                create_rocketchat_user(username=usr, fullname=fn, password=pw, email=mail)

    logger.info("Finished running arcane creator")

if __name__=="__main__":
    main()