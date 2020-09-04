import secrets
import hashlib
import string
import os
import copy
import time
import json
from urllib.parse import urlencode, quote_plus
import tornado.web
import tornado.ioloop
import tornado.httpclient
from tornado.httpclient import HTTPClientError

class pwd():
    def __init__(self,config_path = "./config2.json"):
        
        self.__dict__ = {
            "expire_in": 3600,
            "loginUser": {},
            "password": {},
            "modName": "password",
            "CAPTCHA_enable" : False,
            "CAPTCHA_front_end_response_field" : "g-recaptcha-response",
            "CAPTCHA_verify_api" : {
                "url" : "https://www.google.com/recaptcha/api/siteverify",
                "method":"POST",
                "url_params":{
                    "secret":"6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe",
                    "response":"__front_end_response__"
                },
                "body_params":{},
                "headers" : {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            },
            "CAPTCHA_frontend_head_html" : "<script src='https://www.google.com/recaptcha/api.js'></script>",
            "CAPTCHA_frontend_login_html" : "<div class='g-recaptcha' data-sitekey=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI></div>"
        }
        
        self.config_path = config_path
        if os.path.isfile(config_path):
            with open(config_path,"r") as config:
                self.__dict__ = {**self.__dict__ , **json.loads(config.read())}
        else:
            self.setPassword("admin")
        with open(config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
    def getCAPTCHAhtml(self):
        return {
            "CAPTCHA_front_end_response_field" : self.CAPTCHA_front_end_response_field if self.CAPTCHA_enable == True else "",
            "CAPTCHA_frontend_head_html" : self.CAPTCHA_frontend_head_html if self.CAPTCHA_enable == True else "",
            "CAPTCHA_frontend_login_html" : self.CAPTCHA_frontend_login_html if self.CAPTCHA_enable == True else ""
        }

    def getCAPTCHAsettings(self):
        return { k:v for k,v in self.__dict__.items() if (k.startswith("CAPTCHA_")) }
    def setCAPTCHAsettings(self,newSetting):
        newSetting = { k:v for k,v in newSetting.items() if (k.startswith("CAPTCHA_")) }
        print(newSetting)
        self.__dict__ = {**self.__dict__ , **newSetting}
        print(self.__dict__)
        with open(self.config_path,"w") as config:
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
        
    async def login(self,reqH,password,CAPTCHA,checkOnly=False):
        if self.CAPTCHA_enable == True and checkOnly == False:
            client = tornado.httpclient.AsyncHTTPClient()
            request = newSetting = { k:v for k,v in self.CAPTCHA_verify_api.items() if (v != None) }
            request = copy.deepcopy(request)
            if "url_params" in request:
                request["url_params"] = { k:v.replace("__front_end_response__",CAPTCHA) for k,v in request["url_params"].items() }
                request["url"] = request["url"] + "?" + urlencode(request["url_params"])
                del request["url_params"]
            if "body_params" in request:
                request["body_params"] = { k:v.replace("__front_end_response__",CAPTCHA) for k,v in request["body_params"].items() }
                request["body"] = urlencode(request["body_params"])
                del request["body_params"]
            url = request["url"]
            del request["url"]
            response = await client.fetch(url,**request)
            if response.code == 200 and json.loads(response.body)["success"] == False:
                reqH.clear()
                reqH.set_status(401)
                reqH.finish(json.dumps({"error":"CAPTCHA failed","error_description": json.dumps(json.loads(response.body)["error-codes"])}, indent=2, ensure_ascii=False))
                raise KeyError("Unauthorized")
        if self.check(password):
            sid = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(32))
            self.loginUser = { k:v for k,v in self.loginUser.items() if (v["expire"] > time.time()) }
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