import os
import shutil
import json
import pathlib

class UserInfo:
    def __init__(self, value):
        self.id = value[0]
        self.income = value[1]
        self.consumption = value[2]
        self.target = value[3]
        self.monthincome = value[4]
        self.monthconsumption = value[5]
        
def ClearDataFolder():
    folder = str(pathlib.Path(__file__).parent.resolve()) + "\\DataBase\\"
    for path in pathlib.Path(folder).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

def ClearUserData(id):
    path = pathlib.Path(str(pathlib.Path(__file__).parent.resolve()) + "\\DataBase\\{}.json".format(id))
    print(path)
    os.remove(path)

def GetUserData(id):
    id = str(id)
    path = pathlib.Path(__file__).parent.resolve()
    try:
        f = open(str(path)+'\\DataBase\\{0}.json'.format(id))
        data = json.load(f)
        data = data['user_{}'.format(id)]
        value = [int(id)]
        for i in data: value.append(int(data[i]))
        user = UserInfo(value)
        return user
    except: return False



def SetUserData(user):
    path = pathlib.Path(__file__).parent.resolve()
    userdata = {
        'user_{}'.format(user.id) :
        {
            "income" : "{}".format(user.income),
            "consumption" : "{}".format(user.consumption),
            "target" : "{}".format(user.target),
            "monthincome" : "{}".format(user.monthincome),
            "monthconsumption" : "{}".format(user.monthconsumption),
        }
    }
    with open(str(path)+'\\DataBase\\{0}.json'.format(user.id), 'a+', encoding='utf-8') as f:
        f.seek(0)
        f.truncate()
        json.dump(userdata, f, ensure_ascii=False, indent=4)

def SetUserIncome(id, value):
    user = GetUserData(id)
    if user == False:
        user_ = UserInfo([id,value,0,0,0,0,])
        SetUserData(user_)
    else:
        user_ = UserInfo([id, value,user.consumption, user.target, user.monthincome, user.monthconsumption])
        SetUserData(user_)

def SetUserConsumption(id, value):
    user = GetUserData(id)
    if user == False:
        user_ = UserInfo([id,0,value,0,0,0])
        SetUserData(user_)
    else:
        user_ = UserInfo([id, user.income,value, user.target, user.monthincome, user.monthconsumption])
        SetUserData(user_)

def SetUserTarget(id, value):
    user = GetUserData(id)
    if user == False:
        user_ = UserInfo([id, 0,0, value,0,0,])
        SetUserData(user_)
    else:
        user_ = UserInfo([id, user.income, user.consumption, value,user.monthincome, user.monthconsumption])
        SetUserData(user_)

def SetUserMonthIncome(id, value):
    user = GetUserData(id)
    if user == False:
        user_ = UserInfo([id, 0,0,0,value,0])
        SetUserData(user_)
    else:
        user_ = UserInfo([id, user.income, user.consumption, user.target, value, user.monthconsumption])
        SetUserData(user_)

def SetUserMonthConsumption(id, value):
    user = GetUserData(id)
    if user == False:
        user_ = UserInfo([id, 0,0,0,0,value])
        SetUserData(user_)
    else:
        user_ = UserInfo([id, user.income, user.consumption, user.target, user.monthincome, value])
        SetUserData(user_)

