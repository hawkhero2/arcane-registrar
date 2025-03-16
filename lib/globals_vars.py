from dotenv import dotenv_values  
import os

LOGS_FORMAT="%(asctime)s : %(levelname)s :  %(message)s"
LOGFILE="logs.log"

script_path = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_path,"..",".env")
config = dotenv_values(env_path)

class ENV():
    """
    Class containing all the keys in the .env file.
    Created in order to receive autocomplete suggestions.
    """
    ssh_user =  config["SSH_USER"]
    ssh_host = config["SSH_HOST"]
    ssh_pw = config["SSH_PASSWORD"]
    win_ssh_user = config["W_SSH_USER"]
    win_ssh_host = config["W_SSH_HOST"]
    win_ssh_pw = config["W_SSH_PASSWORD"]
    rocket_url = config["RC_URL"]
    rocket_acc = config["RC_ACC"]
    rocket_pw = config["RC_PASSWORD"]
    dc1 = config["DC1"]
    dc2 = config["DC2"]
    ldap_acc = config["LDAP_ACC"]
    ldap_pw = config["LDAP_PASSWORD"]
    env = config["ENV"]
