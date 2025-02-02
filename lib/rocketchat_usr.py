from lib.globals_vars import LOGFILE,LOGS_FORMAT
from rocketchat.api import RocketChatAPI
from dotenv import dotenv_values
import logging

logger = logging.getLogger(__name__)

def create_rocketchat_user(username:str, fullname:str, password:str, email:str):
    """
    Creates users on RocketChat server

    @username: Username to be created
    @fullname: Full name of the user
    @password: Password for the user
    @email: Provide an email, it is required;Does not need to be valid
    """

    config = dotenv_values(r"C:\Users\User\Documents\Github\arcane-registrar\.env")
    logging.basicConfig(filename=LOGFILE, format=LOGS_FORMAT, level=logging.INFO)
    
    logger.info(f"Accessing user API server URL: {config['RC_URL']} using username: {config['RC_ACC']}")
    try:
        rocketApi = RocketChatAPI(settings={"username":f"{config['RC_ACC']}","password":f"{config['RC_PASS']}","domain":f"{config['RC_URL']}"})
    except Exception as e:
        print("Error when attempting to login...")
        logger.error("Error while attempting to login", exc_info=e)

    try:    
        rocketApi.create_user(email=email, name=fullname, password=password, username=username, active=True, roles=['user'], join_default_channels=True, send_welcome_email=False, require_password_change=False, verified=True)
    except:
        print("-"*100)
        print("Error while attempting to create user...")
        logger.error("Error while attempting to create user...")
