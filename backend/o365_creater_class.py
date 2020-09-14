import urllib
import json
import time
import os
import io
import secrets
import copy
import string
from urllib.parse import urlencode, quote_plus
import tornado.web
import tornado.ioloop
import tornado.httpclient
from tornado.httpclient import HTTPClientError
class o365():
    def __init__(self,config_path = "./config.json"):
        
        self.__dict__ = {
                "demo_mode" : False,
                "demo_mode_users" : {},
                "newapp_url": "https://apps.dev.microsoft.com/?deepLink=/quickstart/graphIO",
                "api_url": "https://graph.microsoft.com/v1.0",
                "oauth_url": "https://login.microsoftonline.com/common/oauth2/v2.0",
                "appName": "Office 365 Account Registration Portal",
                "redirect_uri": "",
                "maxAllowedLicense": 1,
                "availableDomains": [],
                "allDomains": [],
                "availableLicences": [],
                "allLicences": [],
                "secret": "",
                "client_id": "",
                "code": "",
                "code_update_time": 0,
                "session_state": "",
                "access_token ": "",
                "refresh_token": "",
                "expires_in": 0
            }
        self.config_path = config_path
        if os.path.isfile(config_path):
            with open(config_path,"r") as config:
                self.__dict__ = { **self.__dict__ , **json.loads(config.read())}

        with open(config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
    def setInfo(self,newInfo):
        for key in newInfo.keys():
            self.__dict__[key] = newInfo[key]
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
    def getSecretIdUrl(self):
        if len(self.redirect_uri) == 0 or len(self.appName) == 0:
            raise self.generateError(409,"AppInfo not set","Save application infomation first.")
        newapp_url = "https://apps.dev.microsoft.com/?deepLink=/quickstart/graphIO"
        params = {"publicClientSupport":"false",
                  "appName":self.appName,
                  "redirectUrl":self.redirect_uri,
                  "allowImplicitFlow":"false",
                  "ru":urllib.parse.quote("https://developer.microsoft.com/en-us/graph/quick-start?appID=_appId_&appName=_appName_&redirectUrl="+self.redirect_uri+"/&platform=option-php",safe="")
                 }
        return newapp_url + urllib.parse.quote("?" + urllib.parse.urlencode(params,safe=":/%"),safe="")
    def setSecret(self,secret,client_id):
        if type(secret) == str:
            self.secret=secret
        if type(client_id) == str:
            self.client_id=client_id
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
    def getCodeURL(self):
        scope = "offline_access User.ReadWrite.All Directory.Read.All"
        self.code_state = self.generatePwd(string.ascii_letters + string.digits ,16)
        params = {"client_id":self.client_id,
                  "scope":scope,
                  "response_type":"code",
                  "redirect_uri":self.redirect_uri,
                  "state": self.code_state
                 }
        
        return self.oauth_url + "/authorize?" + urllib.parse.urlencode(params)
    def setCode(self,code,session_state,state,error=None,error_description=None):
        if "code_state" in self.__dict__.keys() and state == self.code_state:
            self.__dict__.pop("code_state",None)
            self.code=code
            self.code_error = error
            self.code_error_description = error_description
            self.code_update_time = time.time()
            self.session_state=session_state
            with open(self.config_path,"w") as config:
                config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
        else:
            raise self.generateError(409,"Challange not pass","The code state not match our generated state")
    def setToken(self,access_token,refresh_token,expires_in):
        self.access_token  = access_token
        self.refresh_token = refresh_token
        self.expires_in = time.time() + expires_in - 30
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
    async def getRefreshToken(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {"client_id":self.client_id,
                  "redirect_uri":self.redirect_uri,
                  "client_secret":self.secret,
                  "code":self.code,
                  "grant_type":"authorization_code"
                 }
        client = tornado.httpclient.AsyncHTTPClient()
        response = await client.fetch(self.oauth_url + "/token", method="POST", body=urllib.parse.urlencode(params),headers=headers)
        self.getCodeURL()
        self.setCode("","",self.code_state)
        return json.loads(response.body)
    async def initToken(self):
        response = await self.getRefreshToken()
        self.setToken(response["access_token"],response["refresh_token"],response["expires_in"])
    async def getAccessToken(self):
        oauth_url = 'https://login.microsoftonline.com/common/oauth2/v2.0'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {"client_id":self.client_id,
                  "redirect_uri":self.redirect_uri,
                  "client_secret":self.secret,
                  "refresh_token":self.refresh_token,
                  "grant_type":"refresh_token"
                 }
        client = tornado.httpclient.AsyncHTTPClient()
        response = await client.fetch(self.oauth_url + "/token", method="POST", body=urllib.parse.urlencode(params),headers=headers)
        return json.loads(response.body)
    async def getToken(self,force=False):
        if(self.expires_in <= time.time() or force == True):
            response = await self.getAccessToken()
            self.setToken(response["access_token"],response["refresh_token"],response["expires_in"])
        return self.access_token
    async def testInit(self,force=False):
        if self.refresh_token == "":
            raise self.generateError(404,"Empty Server Token","Please contact admin to setup server token.",add_info={"appName":self.appName})
        accessToken = await self.getToken(force=force)
        if(accessToken == ""):
            raise self.generateError(404,"Empty Access Token","Empty Server Token","Please contact admin to setup server token.",add_info={"appName":self.appName})
        else:
            return {"success":True,"appName":self.appName}
    async def readLicencesRaw(self):
        headers = {"Authorization":"Bearer " + await self.getToken() }
        client = tornado.httpclient.AsyncHTTPClient()
        response = await client.fetch(self.api_url + "/subscribedSkus", method="GET",headers=headers)
        return json.loads(response.body)
    async def readLicences(self):
        licences = await self.readLicencesRaw()
        need_keys = ["skuId" ,"skuPartNumber"]
        return list(map(lambda x: { need_key : x[need_key] for need_key in need_keys } ,licences["value"]))
    async def readDomainsRaw(self):
        headers = {"Authorization":"Bearer " + await self.getToken() }
        client = tornado.httpclient.AsyncHTTPClient()
        response = await client.fetch(self.api_url + "/domains", method="GET",headers=headers)
        return json.loads(response.body)
    async def readDomains(self):
        domains = await self.readDomainsRaw()
        return list(map(lambda x: x["id"] ,domains["value"]))
    async def refreshRegInfo(self):
        firstRun = (len(self.allLicences) + len(self.allDomains)) == 0
        self.allLicences = await self.readLicences()
        self.allDomains = await self.readDomains()
        if firstRun == True:
            self.setDomainsAndLicences(self.allDomains,self.allLicences)
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
    def setDomainsAndLicences(self,availableDomains,availableLicences,maxAllowedLicense=1):
        self.availableDomains = availableDomains
        self.availableLicences = availableLicences
        self.maxAllowedLicense = maxAllowedLicense
        with open(self.config_path,"w") as config:
            config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
    def getRegInfo(self):
        need_keys = ["availableDomains", "availableLicences"]
        return { need_key : self.__dict__[need_key] for need_key in need_keys } 
    async def getUser(self,userID,raise_error=True):
        headers = {"Authorization":"Bearer " + await self.getToken(),
                   'Content-Type': 'application/json'}
        client = tornado.httpclient.AsyncHTTPClient()
        response = await client.fetch(self.api_url + "/users/" + urllib.parse.quote(userID) , method="GET",headers=headers,raise_error=raise_error)
        return response
    async def checkUser(self,userID):
        headers = {"Authorization":"Bearer " + await self.getToken(),
                   'Content-Type': 'application/json'}
        params = {"$filter":'proxyAddresses/any(x:x eq \'smtp:' + userID + '\')',
                  "$select":"userPrincipalName,proxyAddresses"}
        client = tornado.httpclient.AsyncHTTPClient()
        response = await client.fetch(self.api_url + "/users?" +urllib.parse.urlencode(params) , method="GET",headers=headers)
        return json.loads(response.body)
    def generateError(self,code,error_title,error_description,error_url="https://example.com",add_info={}):
        errordict = {"error":error_title,"error_description":error_description,"error_uri":"See the full API docs at "+error_url}
        errordict = {**errordict,**add_info}
        response = tornado.httpclient.HTTPResponse(request=tornado.httpclient.HTTPRequest(url= ""),code= code, headers= None, buffer= io.StringIO(json.dumps(errordict, indent=2, ensure_ascii=False)))
        return HTTPClientError(code=code, message= json.dumps(errordict, indent=2, ensure_ascii=False), response=response)
    async def canReg(self,username,domain):
        if self.demo_mode == True:
            self.demo_mode_users = {k:v for (k,v) in self.demo_mode_users.items() if v["expire"] >= time.time()}
            if username + "@" + domain in self.demo_mode_users:
                raise self.generateError(409,"Username Exists","The username '" + username + "@" + domain + "' already exists(Demo). Please use a different username.")
        else:
            if len(self.demo_mode_users.keys()) != 0:
                self.demo_mode_users = {}
                with open(self.config_path,"w") as config:
                    config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
        if domain not in self.availableDomains:
            raise self.generateError(404,"Domain Not Available","Domain not in available domains")
        if (await self.getUser(username + "@" + domain,raise_error=False)).code != 404:
            raise self.generateError(409,"Username Exists","The username '" + username + "@" + domain + "' already exists. Please use a different username.")
        checkusers = await self.checkUser(username + "@" + domain)
        if len(checkusers["value"]) != 0:
            raise self.generateError(409,"Username Exists","The username " + username + "@" + domain + " already set as " + checkusers["value"][0]["userPrincipalName"] +"'s alies. Please use a different username.")
        return {"success":True}
    def generatePwd(self,chars,length):
        return ''.join(secrets.choice(chars) for i in range(length))
    async def createUser(self,userPrincipalName,displayName,password = None):
        password = self.generatePwd(string.ascii_letters + string.digits + "@#$%^",12) + self.generatePwd(string.ascii_uppercase,1)+self.generatePwd(string.ascii_lowercase,1)+self.generatePwd(string.digits,1)+self.generatePwd("@#$%^",1) if (password == None) else password
        await self.canReg(*userPrincipalName.split("@"))
        headers = {"Authorization":"Bearer " + await self.getToken(),
                   'Content-Type': 'application/json'}
        params ={
                  "accountEnabled": "true",
                  "displayName": displayName,
                  "mailNickname": userPrincipalName.split("@")[0],
                  "userPrincipalName": userPrincipalName,
                  "passwordProfile" : {
                    "forceChangePasswordNextSignIn": "true",
                    "password": password
                  }
                }
        ret = {}
        ret["username"] = userPrincipalName
        ret["password"] = password
        if self.demo_mode == False:
            client = tornado.httpclient.AsyncHTTPClient()
            response = await client.fetch(self.api_url + "/users" , method="POST",body = json.dumps(params) , headers = headers)
        else:
            await tornado.gen.sleep(3)
            ret["password"] = "DemoModeEnabled_" + password[-4:]
            self.demo_mode_users[userPrincipalName] = ret
            self.demo_mode_users[userPrincipalName]["displayName"] = displayName
            self.demo_mode_users[userPrincipalName]["licenseDetails"] = []
            self.demo_mode_users[userPrincipalName]["expire"] = time.time() + 3600
        return ret
    async def updateUser(self,userPrincipalName,infomation):
        headers = {"Authorization":"Bearer " + await self.getToken(),
                   'Content-Type': 'application/json'}
        allowed_key = {"aboutMe","birthday","businessPhones","city","country","department","displayName","givenName","hireDate","interests","jobTitle","mobilePhone","mySite","officeLocation","pastProjects","postalCode","preferredLanguage","responsibilities","schools","skills","state","streetAddress","surname","usageLocation"}
        if bool(set(infomation.keys()).difference(allowed_key)) == True:
            raise self.generateError(400,"Not allowed key","The update key:" + str(set(infomation.keys()).difference(allowed_key)) + " not in allowed keys:" + str(allowed_key))
        params = infomation
        if self.demo_mode == False:
            client = tornado.httpclient.AsyncHTTPClient()
            response = await client.fetch(self.api_url + "/users/" + urllib.parse.quote(userPrincipalName,safe="") , method="PATCH",body = json.dumps(params) , headers = headers)
        else:
            await tornado.gen.sleep(3)
            self.demo_mode_users[userPrincipalName] = {**self.demo_mode_users[userPrincipalName],**infomation}
        return {"success":True}
    async def ListlicenseDetails(self,userPrincipalName):
        headers = {"Authorization":"Bearer " + await self.getToken(),
                   'Content-Type': 'application/json'}
        if self.demo_mode == False:
            client = tornado.httpclient.AsyncHTTPClient()
            response = await client.fetch(self.api_url + "/users/" + urllib.parse.quote(userPrincipalName,safe="") + "/licenseDetails" , method="GET", headers = headers)
            return json.loads(response.body)
        else:
            return {"value":self.demo_mode_users[userPrincipalName]["licenseDetails"]}
    async def assignLicense(self,userPrincipalName,addLicensesID):
        skuPartNumbers = list(filter(lambda x:x["skuId"]==addLicensesID,self.availableLicences))
        if len(skuPartNumbers) == 0:
            raise self.generateError(401,"SkuId Not Found","SkuId not in availableLicences")
        skuPartNumber = skuPartNumbers[0]
        licenseHave = (await self.ListlicenseDetails(userPrincipalName))["value"]
        if len(licenseHave) >= self.maxAllowedLicense:
            raise self.generateError(409,"Too much Licenses","You already have folling license:" + str(list(map(lambda x:x["skuPartNumber"],licenseHave))) + ".\nBut you can only have " + str(self.maxAllowedLicense) + " licenses.")
        
        headers = {"Authorization":"Bearer " + await self.getToken(),
                   'Content-Type': 'application/json'}
        params = {"addLicenses": [  {
                      "disabledPlans": [  ],
                      "skuId": addLicensesID
                    } ],
                  "removeLicenses": [ ] }
        if self.demo_mode == False:
            client = tornado.httpclient.AsyncHTTPClient()
            response = await client.fetch(self.api_url + "/users/" + urllib.parse.quote(userPrincipalName,safe="") + "/assignLicense" , method="POST",body = json.dumps(params) , headers = headers)
            return json.loads(response.body)
        else:
            await tornado.gen.sleep(3)
            self.demo_mode_users[userPrincipalName]["licenseDetails"] += [skuPartNumber]
            with open(self.config_path,"w") as config:
                config.write(json.dumps(self.__dict__,ensure_ascii=False,indent = 2))
            ret = {**{
                      "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#users/$entity",
                      "businessPhones": [],
                      "givenName": "demo",
                      "jobTitle": None,
                      "mail": userPrincipalName,
                      "mobilePhone": None,
                      "officeLocation": None,
                      "preferredLanguage": None,
                      "id": "demo-mode-fake-id"
                    },**self.demo_mode_users[userPrincipalName]}
            ret = copy.deepcopy(ret)
            del ret["licenseDetails"]
            return ret
    async def createUserWithLicense(self,username,domain,Fname,Lname,displayName,Loc,skuId):
        print("createUser")
        ret = await self.createUser(username + "@" + domain, displayName)
        print("updateUser")
        infomation = {"givenName":Fname,"surname":Lname,"UsageLocation":Loc}
        successU = False
        for i in range(3):
            try:
                await self.updateUser(username + "@" + domain,infomation)
                successU = True
                print("successU")
                break
            except HTTPClientError as e:
                print(e.response.body)
        if successU == False:
            raise "successU == False"
        print("assignLicense")
        successL = False
        for i in range(3):
            try:
                await self.assignLicense(username + "@" + domain,skuId)
                successL = True
                print("successL")
                break
            except HTTPClientError as e:
                print(e.response.body)
        if successL == False:
            raise "successL == False"
        return ret
    