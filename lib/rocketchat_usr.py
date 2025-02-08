from lib.globals_vars import LOGFILE,LOGS_FORMAT
from rocketchat_API.rocketchat import RocketChat
from dotenv import dotenv_values
from pprint import pprint
import time
import logging

logger = logging.getLogger(__name__)

def create_rocketchat_user(users_file):
    """
    Creates users on RocketChat server

    @username: Username to be created
    @fullname: Full name of the user
    @password: Password for the user
    @email: Provide an email, it is required;Does not need to be valid
    """

    print("-"*100)
    print(f"Running : {__name__}")

    logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)
    config = dotenv_values(r"C:\Users\User\Documents\Github\arcane-registrar\.env")

    rc_url = config["RC_URL"]
    rc_acc = config["RC_ACC"]
    rc_pass = config["RC_PASS"]
    
    logger.info(f"Accessing user API server URL:{rc_url} using username: {rc_acc}, password: {rc_pass}")
    try:
        rocketAPI = RocketChat(user=rc_acc,password=rc_pass,server_url=rc_url)
        print(f"Status : {rocketAPI.me()}")
        print(f"Connected to RocketChat Server : {rc_url} , acc: {rc_acc}, pass: {rc_pass}")
        with open(users_file) as f:
            for line in f:
                try:
                    username,fullname,password,email = line.split(",")
                    print("-"*100)

                    respo = rocketAPI.users_create(email=email,
                                                name=fullname,
                                                password=password,
                                                username=username)

                    time.sleep(4)

                    print(f"user : {username},\n fullname: {fullname},\n password: {password},\n email: {email}\n")
                    print("-"*100)
                    print(f"Response for user: {username}")
                    print(f"{respo.content.decode()}")
                    print("-"*100)

                except Exception as e:
                    print(f"Error when creating user: {username} \n{e}")
                    logger.error(f"Error when creating user: {username} \n{e}")

    except Exception as e:
        print(f"Error when attempting to login... \n{e}")
        logger.error(f"Error while attempting to login \n{e}", exc_info=e)
