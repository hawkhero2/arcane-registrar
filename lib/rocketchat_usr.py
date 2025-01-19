from lib.globals_vars import LOGFILE,LOGS_FORMAT
from dotenv import load_dotenv
from rocketchat.api import RocketChatAPI
import logging
import os

logger = logging.getLogger(__name__)

def create_rocketchat_user(username:str, fullname:str, password:str, email:str):
    """
    Creates users on RocketChat server

    @username: Username to be created
    @fullname: Full name of the user
    @password: Password for the user
    @email: Provide an email, it is required;Does not need to be valid
    """

    logging.basicConfig(filemode=LOGFILE, level=logging.INFO, format=LOGS_FORMAT)
    load_dotenv()
    rocketApi = RocketChatAPI(settings={"username":f"{os.getenv("RC_ACC")}","password":f"{os.getenv("RC_PASS")}","domain":f"{os.getenv("RC_URL")}"})

    rocketApi.create_user(email=email, name=fullname, password=password, username=username, active=True, roles=['user'], join_default_channels=True, send_welcome_email=False, require_password_change=False, verified=True)
