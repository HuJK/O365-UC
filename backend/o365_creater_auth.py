import os
import io
import re
import copy
import time
import json
import js2py
import socket
import string
import urllib
import secrets
import hashlib
import smtplib
import ipaddress
import tornado.web
import tornado.ioloop
import multiprocessing
import tornado.httpclient
from tornado import httputil
from tornado.escape import _unicode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import urlencode, quote_plus
from tornado.httpclient import HTTPClientError


def check_sock(x):
    s = socket.socket(x[0],x[1])
    s.settimeout(1)
    return s.connect_ex(x[-1])==0

class pwd():
    def __init__(self,config_path = "./config2.json"):
        self.__dict__ = {
            "demo_mode" : False,
            "block_SSRF" : True,
            "block_SSRF_port_whitelist" : [80,443],
            "listen_port" : 12536,
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
            "CAPTCHA_verify_api_check_function" : "//HTTPResponse https://www.tornadoweb.org/en/stable/httpclient.html#tornado.httpclient.HTTPResponse\nfunction(HTTPResponse) {\n    if(HTTPResponse.code !== 200){\n        return \"Bed response code: \" + HTTPResponse.code;\n    }\n    else{\n        response_json = JSON.parse(HTTPResponse.body.decode(\"utf8\"))\n        if(response_json[\"success\"] === true){\n            return true;\n        }\n        return JSON.stringify(response_json[\"error-codes\"]);\n    } \n}",
            "CAPTCHA_frontend_head_html" : "<script src='https://www.google.com/recaptcha/api.js'></script>",
            "CAPTCHA_frontend_login_html" : "<div class='g-recaptcha' data-sitekey=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI></div>",
            "_CAPTCHA_api_response_example" : None ,
            "_CAPTCHA_reused" : {},
            "DEFAULT_usageLocation":"US",
            "GETPWD_show_mail" : False,
            "GETPWD_show_url" : False,
            "GETPWD_redirect_url" : "https://example.com",
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
    def generateError(self,code,error_title,error_description,error_url="https://example.com",add_info={}):
        if type(error_description) == HTTPClientError and "self_generated_use_raw" in error_description.__dict__ and error_description.__dict__["self_generated_use_raw"] == True:
            return error_description
        errordict = {"error":error_title,"error_description":str(error_description),"error_uri":"See the full API docs at "+error_url}
        errordict = {**errordict,**add_info}
        response = tornado.httpclient.HTTPResponse(request=tornado.httpclient.HTTPRequest(url= ""),code= code, headers= None, buffer= io.StringIO(json.dumps(errordict, indent=2, ensure_ascii=False)))
        ret = HTTPClientError(code=code, message= json.dumps(errordict, indent=2, ensure_ascii=False), response=response)
        ret.__dict__["self_generated_use_raw"] = True
        return ret
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
            if self.block_SSRF == True:
                parsed = urllib.parse.urlsplit(_unicode(url))
                if parsed.scheme not in ("http", "https"):
                    raise ValueError("Unsupported url scheme: %s" % url)
                netloc = parsed.netloc
                if "@" in netloc:
                    userpass, _, netloc = netloc.rpartition("@")
                host, port = httputil.split_host_and_port(netloc)
                if port is None:
                    port = 443 if parsed.scheme == "https" else 80
                if re.match(r"^\[.*\]$", host):
                    host = host[1:-1]
                t=time.time()
                host_ips = list(filter(lambda x:x[1]==socket.SOCK_STREAM,socket.getaddrinfo(host,port)))
                host_ips_global = list(filter(lambda x:ipaddress.ip_address(x[-1][0]).is_global,host_ips))
                host_ips_connectable = list(filter(lambda x:check_sock,host_ips_global))
                print(time.time()-t)
                print(host_ips_connectable)
                if len(host_ips_global) == 0:
                    raise self.generateError(400,"SSRF blocked","Request to local network are blocked due to SSRF protection enabled")
                if port not in self.block_SSRF_port_whitelist:
                    raise self.generateError(400,"SSRF blocked","Request port are not in block_SSRF_port_whitelist.")
                if len(host_ips_connectable) == 0:
                    raise self.generateError(500,"CAPTCHA API fetch error","Not connectable")
                if "follow_redirects" in request and request["follow_redirects"] == True:
                    raise self.generateError(400,"SSRF blocked","follow_redirects are not available if SSRF protection enabled")
                request["follow_redirects"] = False
                host_ip = host_ips_connectable[0]
                client = tornado.httpclient.AsyncHTTPClient(hostname_mapping={host:host_ip})
            response = await client.fetch(url,**request)
            self._CAPTCHA_api_response_example = response
            return response
        except Exception as e:
            raise self.generateError(400,"CAPTCHA API fetch error",e,error_url="https://www.tornadoweb.org/en/stable/httpclient.html#tornado.httpclient.AsyncHTTPClient.fetch")
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
            raise self.generateError(400,"JsException",e,error_url="https://github.com/PiotrDabkowski/Js2Py")
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
            raise self.generateError(400,"JsException",e,"https://github.com/PiotrDabkowski/Js2Py")
        if func_ret["err"] != None:
            raise self.generateError(400,"JsRuntimeError",func_ret["err"],"https://github.com/PiotrDabkowski/Js2Py")
        if func_ret["val"] == True:
            return True
        elif type(func_ret["val"]) == str:
            return func_ret["val"]
        else:
            raise self.generateError(400,"Incompatible function","Your function must return true(success) or string(error_msg).","https://github.com/HuJK/O365-UC")
    def check(self,pwdIn):
        return hashlib.pbkdf2_hmac('sha256', pwdIn.encode("utf8"), self.password["salt"].encode("utf8"), 100000).hex() == self.password["pwdHash"]
    def setPassword(self,newPwd):
        if self.demo_mode == True:
            raise self.generateError(400,"Demo mode","Not available in demo mode","https://github.com/HuJK/O365-UC")
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
            raise self.generateError(401,"Permission Denied",errReasion)
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
                raise self.generateError(401,"CAPTCHA failed",check_func_ret)
        ret = self.get_pwd(email_in)
        if self.CAPTCHA_enable == True:
            self._CAPTCHA_reused[CAPTCHA] = {"expire":time.time() + self.expire_in}
            with open(self.config_path,"w") as config:
                config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2,default=lambda o:None))
        return ret

    def get_pwd(self,email_in):
        raise self.generateError(400,"Not Implemented","Not Implemented")
    async def login(self,password,CAPTCHA,checkOnly=False):
        if self.CAPTCHA_enable == True and checkOnly == False:
            check_func_ret = await self.CAPTCHA_verify_api_check(CAPTCHA,self.CAPTCHA_verify_api_check_function,use_real=True)
            if check_func_ret==True:
                pass
            else:
                raise self.generateError(401,"CAPTCHA failed",check_func_ret)
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
        if self.GETPWD_show_mail == False:
            raise self.generateError(401,"Permission Denied","Function not enabled.")
        if re.fullmatch(self.GETPWD_valid_mail,email_in,flags=0) == None:
            raise self.generateError(400,"Permission Denied","This email not allowed.")
        e_path = os.path.join(self.invite_code_info_path,email_in + ".json")
        if os.path.isfile(e_path):
            raise self.generateError(409,"Email Registered","This email has been registered.")
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
