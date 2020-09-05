import secrets
import hashlib
import string
import os
import io
import copy
import time
import json
import js2py
import multiprocessing
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
            "CAPTCHA_verify_api_check_function" : """//HTTPResponse https://www.tornadoweb.org/en/stable/httpclient.html#tornado.httpclient.HTTPResponse
function(HTTPResponse) {
    if(HTTPResponse.code !== 200){
        return "Bed response code: " + HTTPResponse.code;
    }
    else{
        response_json = JSON.parse(HTTPResponse.body.decode("utf8"))
        if(response_json["success"] === true){
            return true;
        }
        return "CAPTCHA failed: " + JSON.stringify(response_json["error-codes"]);
    } 
}
""",
            "CAPTCHA_frontend_head_html" : "<script src='https://www.google.com/recaptcha/api.js'></script>",
            "CAPTCHA_frontend_login_html" : "<div class='g-recaptcha' data-sitekey=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI></div>",
            "_CAPTCHA_api_response_example" : None,
            "_CAPTCHA_api_response_example_timeout" : 0
        }
        
        self.config_path = config_path
        if os.path.isfile(config_path):
            with open(config_path,"r") as config:
                self.__dict__ = {**self.__dict__ , **json.loads(config.read())}
        else:
            self.setPassword("admin")
        with open(config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
    def getCAPTCHAhtml(self):
        return {
            "CAPTCHA_front_end_response_field" : self.CAPTCHA_front_end_response_field if self.CAPTCHA_enable == True else "",
            "CAPTCHA_frontend_head_html" : self.CAPTCHA_frontend_head_html if self.CAPTCHA_enable == True else "",
            "CAPTCHA_frontend_login_html" : self.CAPTCHA_frontend_login_html if self.CAPTCHA_enable == True else ""
        }
    def generateError(self,code,msg,body):
        response = tornado.httpclient.HTTPResponse(request=tornado.httpclient.HTTPRequest(url= ""),code= code, headers= None, buffer= io.StringIO(body))
        return HTTPClientError(code=code, message= msg, response=response)
    def getCAPTCHAsettings(self):
        return { k:v for k,v in self.__dict__.items() if (k.startswith("CAPTCHA_")) }
    def setCAPTCHAsettings(self,newSetting):
        newSetting = { k:v for k,v in newSetting.items() if (k.startswith("CAPTCHA_")) }
        self.__dict__ = {**self.__dict__ , **newSetting}
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
        self._CAPTCHA_api_response_example_timeout=0
    async def check_CAPTCHA_verify_api_check_function(self,jsfuncstr):
        try:
            check_func = js2py.eval_js(jsfuncstr)
        except Exception as e:
            errordict = {
                          "error": "JsException",
                          "error_description": str(e),
                          "error_uri": "See the full API docs at https://github.com/PiotrDabkowski/Js2Py"
                        }
            raise self.generateError(400,"JsException",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        try:
            if self._CAPTCHA_api_response_example_timeout < time.time() or self._CAPTCHA_api_response_example == None:
                client = tornado.httpclient.AsyncHTTPClient()
                CAPTCHA = "undefined"
                request = { k:v for k,v in self.CAPTCHA_verify_api.items() if (v != None) }
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
                self._CAPTCHA_api_response_example_timeout = time.time() + 86400
                self._CAPTCHA_api_response_example = response
        except Exception as e:
            errordict = {
                          "error": "CAPTCHA api error",
                          "error_description": str(e),
                          "error_uri": "See the full API docs at https://github.com/HuJK/O365-UC"
                        }
            raise self.generateError(400,"JsException",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        try:
            func_ret = multiprocessing.Manager().dict()
            func_ret.update({"val":None})
            prcs = multiprocessing.Process(target=lambda p,r:print("P:",p,"C:",check_func(p),"R:",r.update({"val":check_func(p)}),"R2:",r), args=[self._CAPTCHA_api_response_example,func_ret])
            prcs.start()
            prcs.join(timeout=0.1)
            if prcs.is_alive():
                raise TimeoutError("TimeoutError: Maximum execution time exceeded in your code.")
        except Exception as e:
            errordict = {
                          "error": "JsException",
                          "error_description": str(e),
                          "error_uri": "See the full API docs at https://github.com/PiotrDabkowski/Js2Py"
                        }
            raise self.generateError(400,"JsException",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        if func_ret["val"] == True or type(func_ret["val"]) == str:
            return func_ret["val"]
        else:
            errordict = {
                      "error": "Incompatible function",
                      "error_description": "Your function must return true(success) or string(error_msg).",
                      "error_uri": "See the full API docs at https://github.com/HuJK/O365-UC"
                    }
            raise self.generateError(400,"Incompatible function",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
    def check(self,pwdIn):
        return hashlib.pbkdf2_hmac('sha256', pwdIn.encode("utf8"), self.password["salt"].encode("utf8"), 100000).hex() == self.password["pwdHash"]
    def setPassword(self,newPwd):
        salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(32))
        pwdhash = hashlib.pbkdf2_hmac('sha256', newPwd.encode("utf8"), salt.encode("utf8"), 100000).hex()
        self.password = {"salt":salt,"pwdHash":pwdhash}
        for keys in self.loginUser.keys():
            self.loginUser[keys]["expire"] = 0
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
    def checkLogin(self,sid):
        if sid not in self.loginUser:
            return False
        if self.loginUser[sid]["expire"] < time.time():
            del self.loginUser[sid]
            return False
        self.loginUser[sid]["expire"] = self.expire_in + time.time()
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
        return True
    def checkLoginErr(self,reqH,sid,errReasion = "Session expired."):
        if self.checkLogin(sid) == False:
            errordict = {
                          "error": "Permission Denied",
                          "error_description": errReasion,
                          "error_uri": "See the full API docs at https://example.com"
                        }
            raise self.generateError(401,"Permission Denied",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        return self.loginUser[sid]
    def setProperty(self,reqH,sid,key,val):
        self.checkLoginErr(reqH,sid)
        self.loginUser[sid][key] = val
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
        
    async def login(self,reqH,password,CAPTCHA,checkOnly=False):
        if self.CAPTCHA_enable == True and checkOnly == False:
            client = tornado.httpclient.AsyncHTTPClient()
            request = { k:v for k,v in self.CAPTCHA_verify_api.items() if (v != None) }
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
            
            check_func = js2py.eval_js(self.CAPTCHA_verify_api_check_function)
            try:
                func_ret = multiprocessing.Manager().dict()
                func_ret.update({"val":None})
                prcs = multiprocessing.Process(target=lambda p,r:print("P:",p,"C:",check_func(p),"R:",r.update({"val":check_func(p)}),"R2:",r), args=[response,func_ret])
                prcs.start()
                prcs.join(timeout=0.1)
                if prcs.is_alive():
                    raise TimeoutError("TimeoutError: Maximum execution time exceeded in response_check_function.")
            except Exception as e:
                errordict = {
                              "error": "JsException",
                              "error_description": str(e),
                              "error_uri": "See the full API docs at https://github.com/PiotrDabkowski/Js2Py"
                            }
                raise self.generateError(400,"JsException",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
            if func_ret["val"] == True or type(func_ret["val"]) == str:
                check_func_ret = func_ret["val"]
            else:
                errordict = {
                          "error": "Incompatible function",
                          "error_description": "Your function must return true(success) or string(error_msg).",
                          "error_uri": "See the full API docs at https://github.com/HuJK/O365-UC"
                        }
                raise self.generateError(400,"Incompatible function",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
            if check_func_ret==True:
                pass
            else:
                errordict = {
                          "error": "CAPTCHA failed",
                          "error_description": check_func_ret,
                          "error_uri": "See the full API docs at https://example.com"
                        }
                raise self.generateError(401,"CAPTCHA failed",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        if self.check(password):
            sid = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(32))
            self.loginUser = { k:v for k,v in self.loginUser.items() if (v["expire"] > time.time()) }
            if checkOnly == False:
                self.loginUser[sid] = {"expire":time.time() + 3600}
                with open(self.config_path,"w") as config:
                    config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
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
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
    def check(self,password):
        if ".." in password:
            # Security concerns
            return False
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