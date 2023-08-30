
"""This module presents samples of usage KlAkOAPIWrapperLib package to add internal user"""

import socket
import uuid
import csv
import os.path
import re
import datetime
from sys import platform
from KlAkOAPI.Params import KlAkArray, paramBinary, strToBin, dateTimeToStr
from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.SecurityPolicy import KlAkSecurityPolicy
from KlAkOAPI.DataProtectionApi import KlAkDataProtectionApi

 
def GetServer():
    """Connects to KSC server"""
    # server details - connect to server installed on current machine, use default port
    server_address = socket.getfqdn()
    server_port = 13299
    server_url = 'https://' + server_address + ':' + str(server_port)

    if platform == "win32":
        username = None # for Windows use NTLM by default
        password = None
    else:
        username = 'klakoapi_test' # for other platform use basic auth, user should be created on KSC server in advance
        password = 'test1234!'
    
    SSLVerifyCert = 'C:\\ProgramData\\KasperskyLab\\adminkit\\1093\\cert\\klserver.cer'

    # create server object
    server = KlAkAdmServer.Create(server_url, username, password, verify = SSLVerifyCert)
    return server

def passwordProtected(server, password):
    # protect User's password
    oDataProtectionApi = KlAkDataProtectionApi(server)
    bPasswordProtected = oDataProtectionApi.ProtectUtf16StringGlobally(password).RetVal()
    return bPasswordProtected

def locationPathFile():
    print("\n********************************************************")
    print("**                Should File CSV                     **")
    print("** Example path like this [C:\\Users\\User\\Data.csv]    **")
    print("********************************************************")
    path = input("** Enter Location File : ")
    check_path = os.path.isfile(path)
    if str(os.path.isfile(path)) == "False":
        print("!!!File Not Found!!!")
        print()
        locationPathFile()
    return path

def userInformation():
    # Get User From CSV File
    try: 
    with open(locationPathFile()) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        userInfo = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            data = {
                "userName": row[0],
                "userDescription": row[1],
                "userFullName": row[2],
                "userEmail": row[3],
                "userPhone":  row[4],
                "userPassword": row[5]
            }
            line_count += 1
            userInfo.append(data)
    except Exception as err:
        print("Double Format CSV file")
        exit()
    return(userInfo)

def addUsers(server, data, status):
    oUsers = KlAkSecurityPolicy(server)
    try:
        nUserID = oUsers.AddUser({
            "KLSPL_USER_NAME": data["userName"],
            "KLSPL_USER_DESCRIPTION": data["userDescription"],
            "KLSPL_USER_FULL_NAME": data["userFullName"],
            "KLSPL_USER_MAIL" : data["userEmail"],
            "KLSPL_USER_PHONE" : data["userPhone"],
            "KLSPL_USER_PWD_ENCRYPTED": paramBinary(passwordProtected(server,(data["userPassword"])))
        }).RetVal()
        status['ID'] = nUserID
        status['Status'] = f'Username {data["userName"]} Successfull Added'
    except Exception as err:
        print("Error In addUsers")
        print(err)
    return status

def validateUsers(server, verified, status):
    oUsers = KlAkSecurityPolicy(server) 
    for x in range(len(verified)):
        # Manually Count Existing UserID
        try:
            find = False
            for v in range(1,500):
                user = oUsers.GetUsers(lUserId=v, lVsId=0).RetVal()
                # Only Filter Username 
                if not user:
                    continue
                cUser = vars(user)
                if verified[x]["userName"] == cUser["data"][0]["value"]["KLSPL_USER_NAME"]:
                    status[x]['Status'] = f'Username {verified[x]["userName"]} Already Exists'
                    find = True
                    break 
            if find:
               continue
            addUsers(server, verified[x], status[x])
        except Exception as err:
            print("Error In validateUsers")
            print(err)
    return(status)

def filterUser(server,data, status):
    verified = []
    for row in range(len(data)):
        # Check Null Data
        if not data[row]["userName"]:
            status[row]['Error'] = 'userName is Missing'
            continue
        elif not data[row]["userPassword"]:
            status[row]['Error'] = 'userPassword is Missing'
            continue
        # Filter Password User
        if sum(map(len, data[row]["userPassword"].split())) in range(8,16):
            if re.search(r'[A-Za-z]', data[row]["userPassword"]):
                if re.search(r'[0-9]',data[row]["userPassword"]):
                    if re.search('[@_!#$%^&*()<>?/\|}{~:]',data[row]["userPassword"]):
                        verified.append(data[row])
                    else:
                        status[row]['Error'] = f'User {data[row]["userName"]} Error Missing Password Special Characters'
                else:
                    status[row]['Error'] = f'User {data[row]["userName"]} Error Missing Password Number'
            else:
                status[row]['Error'] = f'User {data[row]["userName"]} Error Missing Password UpperCase and LowerCase'
        else:
            status[row]['Error'] = f'User {data[row]["userName"]} Must Password 8-16 Characters, No Spaces'
    return validateUsers(server, verified, status)
    
        
 
def main():
    """ /$$   /$$  /$$$$$$   /$$$$$$  /$$$$$$$  /$$$$$$$$ /$$$$$$$   /$$$$$$  /$$   /$$ /$$     /$$      
| $$  /$$/ /$$__  $$ /$$__  $$| $$__  $$| $$_____/| $$__  $$ /$$__  $$| $$  /$$/|  $$   /$$/      
| $$ /$$/ | $$  \ $$| $$  \__/| $$  \ $$| $$      | $$  \ $$| $$  \__/| $$ /$$/  \  $$ /$$/       
| $$$$$/  | $$$$$$$$|  $$$$$$ | $$$$$$$/| $$$$$   | $$$$$$$/|  $$$$$$ | $$$$$/    \  $$$$/        
| $$  $$  | $$__  $$ \____  $$| $$____/ | $$__/   | $$__  $$ \____  $$| $$  $$     \  $$/         
| $$\  $$ | $$  | $$ /$$  \ $$| $$      | $$      | $$  \ $$ /$$  \ $$| $$\  $$     | $$          
| $$ \  $$| $$  | $$|  $$$$$$/| $$      | $$$$$$$$| $$  | $$|  $$$$$$/| $$ \  $$    | $$          
|__/  \__/|__/  |__/ \______/ |__/      |________/|__/  |__/ \______/ |__/  \__/    |__/  by: hokaloh"""
    print (main.__doc__)

    #connect to KSC server using basic auth by default
    server = GetServer()

    # Get Data User From CSV
    dataUser = userInformation()

    # Output Data by Row
    status = [{"Row": x+2} for x in range(len(dataUser))]

    # Filter, Validate and Add User Information  
    result = filterUser(server,dataUser, status)
    print("\n",result)
    
if __name__ == '__main__':
    main()