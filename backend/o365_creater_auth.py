import secrets
import hashlib
import string
import os
import time
import json

def filterTheDict(dictObj, callback):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition then add to new dict
        if callback(value):
            newDict[key] = value
    return newDict

class pwd():
    def __init__(self,config_path = "./config2.json"):
        self.config_path = config_path
        if os.path.isfile(config_path):
            with open(config_path,"r") as config:
                self.__dict__ = json.loads(config.read())
        else:
            self.expire_in = 3600
            self.loginUser = {}
            self.password = {}
            self.modName = "password"
            self.setPassword("admin")
        if not os.path.isfile(config_path):
            with open(config_path,"w") as config:
                config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))

    def check(self,pwdIn):
        return hashlib.pbkdf2_hmac('sha256', pwdIn.encode("utf8"), self.password["salt"].encode("utf8"), 100000).hex() == self.password["pwdHash"]
    def setPassword(self,newPwd):
        salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(32))
        pwdhash = hashlib.pbkdf2_hmac('sha256', newPwd.encode("utf8"), salt.encode("utf8"), 100000).hex()
        self.password = {"salt":salt,"pwdHash":pwdhash}
        for keys in self.loginUser.keys():
            self.loginUser[keys]["expire"] = 0
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
    def checkLogin(self,sid):
        if sid not in self.loginUser:
            return False
        if self.loginUser[sid]["expire"] < time.time():
            del self.loginUser[sid]
            return False
        self.loginUser[sid]["expire"] = self.expire_in + time.time()
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
        return True
    def checkLoginErr(self,reqH,sid,errReasion = "Session expired."):
        if self.checkLogin(sid) == False:
            reqH.clear()
            reqH.set_status(401)
            reqH.finish(json.dumps({"error":"Permission Denied","error_description": errReasion}, indent=2, ensure_ascii=False))
            raise KeyError("Unauthorized")
        return self.loginUser[sid]
    def setProperty(self,reqH,sid,key,val):
        self.checkLoginErr(reqH,sid)
        self.loginUser[sid][key] = val
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
    def login(self,reqH,password,checkOnly=False):
        if self.check(password):
            sid = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(32))
            self.loginUser = filterTheDict(self.loginUser,lambda x:x["expire"] < time.time())
            if checkOnly == False:
                self.loginUser[sid] = {"expire":time.time() + 3600}
                with open(self.config_path,"w") as config:
                    config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
                return {"session_id":sid,"expore_in":self.expire_in - 1}
            else:
                return {"session_id":"FakeID","expore_in":self.expire_in - 1}
        else:
            self.checkLoginErr(reqH,"",errReasion= "Invalid " + self.modName + ".")

class pwd_guest(pwd):
    def __init__(self, *args, **kwargs):
        super(pwd_guest, self).__init__(*args, **kwargs)
        self.invite_code_path = "./invite_code"
        self.modName = "invite Code"
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
    def check(self,password):
        i_path = os.path.join(self.invite_code_path,password)
        if os.path.isfile(i_path):
            with open(i_path) as i_fileHendler:
                use_left = int(i_fileHendler.read())
            if use_left < 0:
                return True
            elif use_left == 0:
                os.remove(i_path)
                return False
            elif use_left == 1:
                os.remove(i_path)
                return True
            else:
                with open(i_path,"w") as i_fileHendler:
                    i_fileHendler.write(str(use_left - 1))
                return True
        return False