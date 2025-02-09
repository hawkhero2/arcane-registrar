## Arcane Registrar
##### Multiplatform account creation script

Currently it makes use of SSH connection to connect to the target servers/machines to create the provided user.

The logging is done with a python lib and kind of messy for the moment, will improve in future.

It currently works for:
- LDAP Server
- Windows Server
- RocketChat Server

### Usage:

To create multiple users run the following command as in the example:
python.exe arcane_creator.py --file "filepath"

Each user must be placed on a new line and each value separrated by a comma in the following order:
username, fullname, password, mail


For single user creation make use the args --username --fullname --password --email
