import secrets
import hashlib
import string
import os
import io
import re
import copy
import time
import json
import js2py
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
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
            "_CAPTCHA_api_response_example" : None ,
            "_CAPTCHA_reused" : {},
            "DEFAULT_usageLocation":"US",
            "GETPWD_show_mail" : False,
            "GETPWD_show_url" : False,
            "GETPWD_redirect_url" : "",
            "GETPWD_valid_mail" : r'.+@example\.com',
            "MAIL_smtp_info" : "smtp.live.com:587",
            "MAIL_smtp_auth_acc" : "username",
            "MAIL_smtp_auth_pwd" : "password",
            "MAIL_msg_from" : "sender@example.com",
            "MAIL_msg_subj" : "Email verification",
            "MAIL_msg_cont" : "<!DOCTYPE html>\n<html>\n<head>\n<title>Email verification</title>\n</head>\n<body>\n<h1>Email verification</h1>\n<p>Dear User:<br>\n&nbsp&nbsp&nbsp&nbsp Your verification code is <font color=\"blue\">__new_code_here__</font> <br>\n&nbsp&nbsp&nbsp&nbsp sincerely<br>\n</p>\n</body>\n</html>",
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
            "CAPTCHA_frontend_login_html" : self.CAPTCHA_frontend_login_html if self.CAPTCHA_enable == True else "",
            "GETPWD_show_mail" : self.GETPWD_show_mail,
            "GETPWD_show_url" : self.GETPWD_show_url,
            "GETPWD_redirect_url" : self.GETPWD_redirect_url,
            "DEFAULT_usageLocation": self.DEFAULT_usageLocation
        }
    def generateError(self,code,msg,body):
        response = tornado.httpclient.HTTPResponse(request=tornado.httpclient.HTTPRequest(url= ""),code= code, headers= None, buffer= io.StringIO(body))
        return HTTPClientError(code=code, message= msg, response=response)
    def generatePwd(self,chars,length):
        return ''.join(secrets.choice(chars) for i in range(length))
    def getCAPTCHAsettings(self):
        return { k:v for k,v in self.__dict__.items() if (k.startswith("CAPTCHA_") or k.startswith("GETPWD_") or k.startswith("MAIL_") or k.startswith("DEFAULT_")) }
    def setCAPTCHAsettings(self,newSetting):
        newSetting = { k:v for k,v in newSetting.items() if (k.startswith("CAPTCHA_") or k.startswith("GETPWD_") or k.startswith("MAIL_") or k.startswith("DEFAULT_")) }
        self.__dict__ = {**self.__dict__ , **newSetting}
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
        self._CAPTCHA_api_response_example_timeout=0
    async def CAPTCHA_check(self,CAPTCHA,request_params):
        try:
            client = tornado.httpclient.AsyncHTTPClient()
            request = { k:v for k,v in request_params.items() if (v != None) }
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
            self._CAPTCHA_api_response_example = response
            return response
        except Exception as e:
            errordict = {
                          "error": "CAPTCHA api fetch error",
                          "error_description": str(e),
                          "error_uri": "See the full API docs at https://www.tornadoweb.org/en/stable/httpclient.html#tornado.httpclient.AsyncHTTPClient.fetch"
                        }
            raise self.generateError(400,"JsException",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
    def check_func_wrapper(self,func,parm,retv):
        try:
            retv["val"] = func(parm)
        except Exception as e:
            retv["err"] = str(e)
    async def CAPTCHA_verify_api_check(self,CAPTCHA,jsfuncstr,use_real=True):
        if CAPTCHA in self._CAPTCHA_reused and self._CAPTCHA_reused[CAPTCHA]["expire"] > time.time():
            self._CAPTCHA_reused = {k:v for (k,v) in self._CAPTCHA_reused.items() if v["expire"] >= time.time()}
            del self._CAPTCHA_reused[CAPTCHA]
            with open(self.config_path,"w") as config:
                config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
            return True
        try:
            check_func = js2py.eval_js(jsfuncstr)
        except Exception as e:
            errordict = {
                          "error": "JsException",
                          "error_description": str(e),
                          "error_uri": "See the full API docs at https://github.com/PiotrDabkowski/Js2Py"
                        }
            raise self.generateError(400,"JsException",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        timeout = 0.1
        if self._CAPTCHA_api_response_example == None or use_real:
            timeout = 0.2
            response = await self.CAPTCHA_check(CAPTCHA,self.CAPTCHA_verify_api)
        else:
            response = self._CAPTCHA_api_response_example
        try:
            func_ret = multiprocessing.Manager().dict()
            func_ret.update({"val":None,"err":None})
            prcs = multiprocessing.Process(target=self.check_func_wrapper(check_func,response,func_ret), args=[response,func_ret])
            prcs.start()
            prcs.join(timeout=timeout)
            if prcs.is_alive():
                prcs.terminate()
                raise TimeoutError("TimeoutError: Maximum execution time exceeded in your response_check_function.")
        except Exception as e:
            errordict = {
                          "error": "JsException",
                          "error_description": str(e),
                          "error_uri": "See the full API docs at https://github.com/PiotrDabkowski/Js2Py"
                        }
            raise self.generateError(400,"JsException",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        if func_ret["err"] != None:
            errordict = {
                      "error": "JsRuntimeError",
                      "error_description": func_ret["err"],
                      "error_uri": "See the full API docs at https://github.com/PiotrDabkowski/Js2Py"
                    }
            raise self.generateError(400,"JsRuntimeError",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        if func_ret["val"] == True:
            return True
        elif type(func_ret["val"]) == str:
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
    def logout(self,sid):
        del self.loginUser[sid]
    def checkLogin(self,sid):
        if sid not in self.loginUser:
            return False
        if self.loginUser[sid]["expire"] < time.time():
            self.logout(sid)
            return False
        self.loginUser[sid]["expire"] = self.expire_in + time.time()
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
        return True
    def checkLoginErr(self,sid,errReasion = "Session expired."):
        if self.checkLogin(sid) == False:
            errordict = {
                          "error": "Permission Denied",
                          "error_description": errReasion,
                          "error_uri": "See the full API docs at https://example.com"
                        }
            raise self.generateError(401,"Permission Denied",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        return self.loginUser[sid]
    def setProperty(self,sid,key,val):
        self.checkLoginErr(sid)
        self.loginUser[sid][key] = val
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
    async def get_pwd_with_CAPTCHA_check(self,email_in,CAPTCHA):
        if self.CAPTCHA_enable == True:
            check_func_ret = await self.CAPTCHA_verify_api_check(CAPTCHA,self.CAPTCHA_verify_api_check_function,use_real=True)
            if check_func_ret==True:
                pass
            else:
                errordict = {
                          "error": "CAPTCHA failed",
                          "error_description": check_func_ret,
                          "error_uri": "See the full API docs at https://example.com"
                        }
                raise self.generateError(401,"CAPTCHA failed",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        ret = self.get_pwd(email_in)
        if self.CAPTCHA_enable == True:
            self._CAPTCHA_reused[CAPTCHA] = {"expire":time.time() + self.expire_in}
            with open(self.config_path,"w") as config:
                config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
        return ret

    def get_pwd(self,email_in):
        errordict = {
              "error": "Not available",
              "error_description": "Not available",
              "error_uri": "See the full API docs at https://example.com"
            }
        raise self.generateError(400,"Not available",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
    async def login(self,password,CAPTCHA,checkOnly=False):
        if self.CAPTCHA_enable == True and checkOnly == False:
            check_func_ret = await self.CAPTCHA_verify_api_check(CAPTCHA,self.CAPTCHA_verify_api_check_function,use_real=True)
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
            if checkOnly == False:
                expired_loginUser = { k:v for k,v in self.loginUser.items() if (v["expire"] < time.time()) }
                list(map(self.logout,expired_loginUser.keys())) # logout all expired user
                self.loginUser[sid] = {"expire":time.time() + self.expire_in}
                if self.modName == "Code":
                    self.loginUser[sid]["invite_code"] = password
                    self.loginUser[sid]["redeemed"] = False
                with open(self.config_path,"w") as config:
                    config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
                return {"session_id":sid,"expore_in":self.expire_in - 1}
            else:
                return {"session_id":"FakeID","expore_in":self.expire_in - 1}
        else:
            self.checkLoginErr("",errReasion= "Invalid " + self.modName + ".")

class pwd_guest(pwd):
    def __init__(self, *args, **kwargs):
        super(pwd_guest, self).__init__(*args, **kwargs)
        self.invite_code_path = "./invite_code"
        self.invite_code_info_path = "./invite_code_info"
        self.modName = "Code"
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
    def get_pwd(self,email_in):
        if re.fullmatch(self.GETPWD_valid_mail,email_in,flags=0) == None:
            errordict = {
                  "error": "Email not allowed",
                  "error_description": "This email not allowed to get a invite code",
                  "error_uri": "See the full API docs at https://example.com"
                }
            raise self.generateError(401,"Not available",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        e_path = os.path.join(self.invite_code_info_path,email_in + ".json")
        if os.path.isfile(e_path):
            errordict = {
                  "error": "Email Registered",
                  "error_description": "This email has been registered",
                  "error_uri": "See the full API docs at https://example.com"
                }
            raise self.generateError(401,"Not available",json.dumps(errordict, indent=2, ensure_ascii=False,default=lambda o:None))
        new_pwd = "email_code_" + self.generatePwd(string.ascii_letters + string.digits , 32)
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.MAIL_msg_subj
        msg['From'] = self.MAIL_msg_from
        msg['To'] = email_in

        # Create the body of the message (a plain-text and an HTML version).
        email_html = self.MAIL_msg_cont.replace("__new_code_here__",new_pwd)

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(MIMEText(email_html, 'plain'))
        msg.attach(MIMEText(email_html, 'html'))
        
        s = smtplib.SMTP(*self.MAIL_smtp_info.split(":"))
        s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
        s.starttls() #Puts connection to SMTP server in TLS mode
        s.ehlo()
        s.login(self.MAIL_smtp_auth_acc, self.MAIL_smtp_auth_pwd)
        s.sendmail(self.MAIL_msg_from, email_in, msg.as_string())
        s.quit()
        i_path = os.path.join(self.invite_code_path,new_pwd)
        with open(e_path,"w") as e_fileHendler:
            e_fileHendler.write(json.dumps({"time":time.time(),"invite_code":new_pwd}, indent=2, ensure_ascii=False,default=lambda o:None))
        with open(i_path,"w") as i_fileHendler:
            i_fileHendler.write(str(1))
        return {"success":True}
        
    def check(self,password):
        if "." in password or "/" in password or "\\" in password:
            # Do not use '.' '\' '/' character in your invite code due to
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
    def logout(self,sid):
        if "redeemed" in self.loginUser[sid] and self.loginUser[sid]["redeemed"] == False:
            i_path = os.path.join(self.invite_code_path,self.loginUser[sid]["invite_code"])
            if os.path.isfile(i_path):
                with open(i_path) as i_fileHendler:
                    use_left = int(i_fileHendler.read())
                if use_left >= 0:
                    with open(i_path,"w") as i_fileHendler:
                        i_fileHendler.write(str(use_left + 1))
            else:
                with open(i_path,"w") as i_fileHendler:
                    i_fileHendler.write(str(1))
        del self.loginUser[sid]