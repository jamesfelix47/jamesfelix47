from ast import dump
import json
from datetime import datetime


def loadJson(filename="signup.json"):
    json_file = open(filename,"r")
    try:
        return json.loads(json.load(json_file))
    except:
        return {}

def dumpJson(data, filename="signup.json"):
    json_file = open(filename,"w")
    data = json.dumps(data)
    json.dump(data, json_file)

def signUp(username, password):
    entries = loadJson()
    entries[username] = {
        "username": username,
        "password": password,
        "waterUsage": 0,
        "waterUsageCost": 0,
        "targetWaterUsage": 0,
        "householdMembers": 1,
        "totalPoints":0,
        "lastUpdated": str(datetime.now()),
    }
    dumpJson(entries)
    return entries[username]

def checkUser(username):
    entries = loadJson()
    if entries.get(username):
        return True
    else:
        return False

def signIn(username, password):
    entries = loadJson()
    if entries.get(username) and entries.get(username)["password"] == password:
        return entries.get(username)
    else:
        return None
        
def forgetPassword(username, newPassword):
    entries = loadJson()
    if entries.get(username):
        entries[username]["password"] = newPassword
        dumpJson(entries)
        return entries.get(username)
    else:
        return False

def updateField(field, value, username):
    entries = loadJson()
    if entries.get(username):
        entries[username][field] = value
        dumpJson(entries)
    else:
        return False
    dumpJson(entries)

def checkCurrentUserStatus():
    userInfo = loadJson("current_user.json")
    return userInfo

def logout():
    userInfo = loadJson("current_user.json")
    userInfo["current_user"] = None
    dumpJson(userInfo)