#!/usr/bin/python3
import tornado.web
import tornado.ioloop
import tornado.httpclient
import tornado.gen
import secrets
import os
import hashlib
import string
import json
from tornado.httpclient import HTTPClientError
from pathlib import Path

import o365_creater_class
import o365_creater_auth


Path("./config").mkdir(parents=True, exist_ok=True)

o = o365_creater_class.o365("./config/config_o365.json")

p = o365_creater_auth.pwd("./config/config_pwd.json") #admin login

g = o365_creater_auth.pwd_guest("./config/config_guest.json") #guest login


class RequestHandlerWithCROS(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(RequestHandlerWithCROS, self).__init__(*args, **kwargs)
#     def set_default_headers(self):
#         self.set_header("Access-Control-Allow-Origin", "*")
#         self.set_header("Access-Control-Allow-Methods", "*")
#         self.set_header("Access-Control-Allow-Headers", "*")
#     async def options(self, *args, **kwargs): 
#         self.write("OK")

class loginHandler(RequestHandlerWithCROS):
    def __init__(self, *args, **kwargs):
        super(loginHandler, self).__init__(*args, **kwargs)
        self.p = p
    async def get(self, *args, **kwargs): 
        try:
            password = self.get_argument('password', True)
            session_id = self.get_argument('session_id', True)
            self.p.checkLoginErr(self,session_id)
            self.write(json.dumps(self.p.loginUser[session_id], indent=2, ensure_ascii=False))
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
    async def put(self, *args, **kwargs): 
        try:
            password = self.get_argument('password', "")
            password_old = self.get_argument('password_old', "")
            session_id = self.get_argument('session_id', True)
            self.p.checkLoginErr(self,session_id)
            self.p.login(self,password_old,checkOnly=True)
            self.p.setPassword(password)
            self.write("OK")
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
    async def post(self, *args, **kwargs): 
        try:
            password = self.get_argument('password', True)
            self.write(json.dumps(self.p.login(self,password), indent=2, ensure_ascii=False))
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
    async def delete(self, *args, **kwargs): 
        try:
            session_id = self.get_argument('session_id', True)
            self.p.checkLoginErr(self,session_id)
            del self.p.loginUser[session_id]
            self.write("OK")
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class guestloginHandler(loginHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
    def __init__(self, *args, **kwargs):
        super(loginHandler, self).__init__(*args, **kwargs)
        self.p = g
        

        
        
def protect_info(info_in,protected_keys):
    info_out = json.loads(json.dumps(info_in))
    for p in protected_keys:
        if p in info_out and info_out[p] != "":
            try:
                info_out[p] = info_out[p][:5] + "...(not showing)..." + info_out[p][-5:]
            except:
                info_out[p] = info_out[p]
    return info_out
class setInfoHandler(RequestHandlerWithCROS):
    async def get(self, *args, **kwargs): 
        try:
            session_id = self.get_argument('session_id', True)
            p.checkLoginErr(self,session_id)#################Need Login
            self.write(json.dumps(protect_info(o.__dict__,["secret","client_id","access_token","refresh_token","code"]), indent=2, ensure_ascii=False))
        except KeyError as e:
            return
    async def put(self, *args, **kwargs): 
        try:
            session_id = self.get_argument('session_id', True)
            p.checkLoginErr(self,session_id)#################Need Login
            newInfo = self.get_argument('newInfo', True)
            newInfo = json.loads(newInfo)
            o.setInfo(newInfo)
            self.write("OK")
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            print(e)
            return

class getSecretIdUrl(RequestHandlerWithCROS):
    async def get(self, *args, **kwargs): 
        try:
            session_id = self.get_argument('session_id', True)
            p.checkLoginErr(self,session_id)#################Need Login
            ret = o.getSecretIdUrl()
            self.write(ret)
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
        
class setSecretHandler(RequestHandlerWithCROS):
    async def put(self, *args, **kwargs): 
        try:
            session_id = self.get_argument('session_id', True)
            p.checkLoginErr(self,session_id)#################Need Login
            secret = self.get_argument('secret', True)
            client_id = self.get_argument('client_id', True)
            o.setSecret(secret,client_id)
            self.write("OK")
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class getCodeURL(RequestHandlerWithCROS):
    async def get(self, *args, **kwargs): 
        try:
            session_id = self.get_argument('session_id', True)
            p.checkLoginErr(self,session_id)#################Need Login
            ret = o.getCodeURL()
            self.write(ret)
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class setCode(RequestHandlerWithCROS):
    async def get(self, *args, **kwargs): 
        try:
            code = self.get_argument('code', None)
            error = self.get_argument('error', None)
            error_description = self.get_argument('error_description', None)
            session_state = self.get_argument('session_state', "")
            state = self.get_argument('state', "")
            o.setCode(code,session_state,state,error,error_description)
            self.write('<p style="text-align:center">Finished.<br/>This window will close automatically within <span id="counter">3</span> second(s).</p><script type="text/javascript">function countdown() {var i = document.getElementById("counter"); i.innerHTML = parseInt(i.innerHTML)-1;if (parseInt(i.innerHTML)<=0) { window.close();}}setInterval(function(){ countdown(); },1000);</script>')
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class waitCodeSet(RequestHandlerWithCROS):
    async def get(self, *args, **kwargs): 
        try:
            session_id = self.get_argument('session_id', True)
            p.checkLoginErr(self,session_id)#################Need Login
            old_code_update_time = o.code_update_time
            errordict = {
                "error": "Timeout",
                "error_description": "Code not set within 90 seconds",
                "error_uri": "See the full API docs at https://example.com"
            }
            errorcode = 417
            errormsg = "Expectation Failed"
            for wait_sec in range(900):
                if o.code_update_time != old_code_update_time:
                    if o.code_error == None:
                        self.write("OK")
                        return
                    else:
                        errorcode = 403
                        errormsg = "Microsoft didn't return a valid code"
                        errordict["error"] = o.code_error
                        errordict["error_description"] = o.code_error_description
                        break
                else:
                    await tornado.gen.sleep(0.1)   
            raise o.generateError(errorcode,errormsg,json.dumps(errordict, indent=2, ensure_ascii=False))
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class initToken(RequestHandlerWithCROS):
    async def get(self, *args, **kwargs): 
        try:
            session_id = self.get_argument('session_id', True)
            p.checkLoginErr(self,session_id)#################Need Login
            await o.initToken()
            self.write("OK")
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class testInit(RequestHandlerWithCROS):
    async def get(self, *args, **kwargs): 
        try:
            session_id = self.get_argument('session_id', True)
            force = self.get_argument('force', False)
            if force=="true":
                p.checkLoginErr(self,session_id)#################Need Login if force
                ret = await o.testInit(force=True)
            else:
                ret = await o.testInit()
            self.write(json.dumps(ret, indent=2, ensure_ascii=False))
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class refreshRegInfo(RequestHandlerWithCROS):
    async def get(self, *args, **kwargs): 
        try:
            session_id = self.get_argument('session_id', True)
            p.checkLoginErr(self,session_id)#################Need Login
            ret = await o.refreshRegInfo()
            self.write("OK")
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class setDomainsAndLicences(RequestHandlerWithCROS):
    async def put(self, *args, **kwargs): 
        try:
            session_id = self.get_argument('session_id', True)
            p.checkLoginErr(self,session_id)#################Need Login
            availableDomains = json.loads(self.get_argument('availableDomains', True))
            availableLicences = json.loads(self.get_argument('availableLicences', True))
            maxAllowedLicense = int(self.get_argument('maxAllowedLicense', 1))
            o.setDomainsAndLicences(availableDomains,availableLicences,maxAllowedLicense)
            self.write("OK")
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class getRegInfo(RequestHandlerWithCROS):
    async def get(self, *args, **kwargs): 
        try:
            guest_session_id = self.get_argument('guest_session_id', True)
            g.checkLoginErr(self,guest_session_id)################# Guest Login
            ret = o.getRegInfo()
            self.write(json.dumps(ret, indent=2, ensure_ascii=False))
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
        
class canReg(RequestHandlerWithCROS):
    async def get(self, *args, **kwargs): 
        try:
            guest_session_id = self.get_argument('guest_session_id', True)
            g.checkLoginErr(self,guest_session_id)################# Guest Login
            username = self.get_argument('userPrincipalName', True).split("@")[0]
            domain =self.get_argument('userPrincipalName', True).split("@")[1]
            ret = await o.canReg(username,domain)
            self.write(str(ret))
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class createUser(RequestHandlerWithCROS):
    async def post(self, *args, **kwargs): 
        try:
            guest_session_id = self.get_argument('guest_session_id', True)
            g.checkLoginErr(self,guest_session_id)################# Guest Login
            userPrincipalName = self.get_argument('userPrincipalName', True)
            displayName = self.get_argument('displayName', True)
            if g.loginUser[guest_session_id].get("userPrincipalName",userPrincipalName) != userPrincipalName:
                raise o.generateError(409,"Conflict","You already created this account: "+ g.loginUser[guest_session_id].get("userPrincipalName") + ", You can't create another one.")
            ret = await o.createUser(userPrincipalName,displayName)
            g.setProperty(self,guest_session_id,"userPrincipalName",userPrincipalName)
            g.setProperty(self,guest_session_id,"displayName",displayName)
            g.setProperty(self,guest_session_id,"regResult",ret)
            self.write(json.dumps(ret, indent=2, ensure_ascii=False))
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class updateUser(RequestHandlerWithCROS):
    async def put(self, *args, **kwargs): 
        try:
            guest_session_id = self.get_argument('guest_session_id', True)
            g.checkLoginErr(self,guest_session_id)################# Guest Login
            userPrincipalName = g.loginUser[guest_session_id]["userPrincipalName"]
            infomation = json.loads(self.get_argument('infomation', True))
            ret = await o.updateUser(userPrincipalName,infomation)
            g.setProperty(self,guest_session_id,"infomation",infomation)
            self.write("OK")
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
class assignLicense(RequestHandlerWithCROS):
    async def post(self, *args, **kwargs): 
        try:
            guest_session_id = self.get_argument('guest_session_id', True)
            g.checkLoginErr(self,guest_session_id)################# Guest Login
            userPrincipalName = g.loginUser[guest_session_id]["userPrincipalName"]
            addLicensesID = self.get_argument('addLicensesID', "")
            ret = await o.assignLicense(userPrincipalName,addLicensesID)
            g.setProperty(self,guest_session_id,"addLicensesID",addLicensesID)
            self.write(json.dumps(ret, indent=2, ensure_ascii=False))
        except HTTPClientError as e:
            self.clear()
            self.set_status(e.response.code)
            self.finish(e.response.body)
        except KeyError as e:
            return
        
        


if __name__ == '__main__':
    app = tornado.web.Application(handlers=[
        (r'/api/login', loginHandler),
        (r'/api/guestlogin', guestloginHandler),
        (r'/api/Info', setInfoHandler),
        (r'/api/getSecretIdUrl', getSecretIdUrl),
        (r'/api/setSecretId', setSecretHandler),
        (r'/api/getCodeURL', getCodeURL),
        (r'/api/setCode', setCode),
        (r'/api/waitCodeSet', waitCodeSet),
        (r'/api/initToken', initToken),
        (r'/api/testInit', testInit),
        (r'/api/refreshRegInfo', refreshRegInfo),
        (r'/api/setDomainsAndLicences', setDomainsAndLicences),
        (r'/api/getRegInfo', getRegInfo),
        (r'/api/canReg', canReg),
        (r'/api/createUser', createUser),
        (r'/api/updateUser', updateUser),
        (r'/api/assignLicense', assignLicense),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "o365_uc/dist", "default_filename": "index.html"})
    ])
    server = tornado.httpserver.HTTPServer(app, ssl_options={
           "certfile": os.path.join(os.path.abspath("."), "ssl","server.crt"),
           "keyfile": os.path.join(os.path.abspath("."), "ssl","server.key"),
    })
    server.listen(12536)
    tornado.ioloop.IOLoop.current().start()
