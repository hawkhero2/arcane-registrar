from lib.globals_vars import LOGFILE,LOGS_FORMAT, ENV
from rocketchat_API.rocketchat import RocketChat
import time
import logging

logger = logging.getLogger(__name__)

def create_rocketchat_user(username, fullname, password, email):
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
    env = ENV()

    logger.info(f"Accessing RocketChatAPI server URL:{env.rocket_url} using username: {env.rocket_acc}, password: {env.rocket_pw}")
    try:
        rocketAPI = RocketChat(user=env.rocket_acc,
                               password=env.rocket_pw,
                               server_url=env.rocket_url)

        # print(f"Status : {rocketAPI.me()}")
        print(f"Connected to RocketChat Server : {env.rocket_url} , acc: {env.rocket_acc}")
        logger.info(f"Connected to RocketChat Server: {env.rocket_url}")
        try:
            print("-"*100)
            respo = rocketAPI.users_create(email=email,
                                        name=fullname,
                                        password=password,
                                        username=username)

            time.sleep(4)

            print(f"user : {username},\n fullname: {fullname},\n password: {password},\n email: {email}\n")
            logger.info(f"Created user: {username}")
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
