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
                "expires_in": 0,
                "licenses_friendly_name":{
                    "O365_BUSINESS_ESSENTIALS": "Office 365 Business Essentials",
                    "O365_BUSINESS_PREMIUM": "Office 365 Business Premium",
                    "DESKLESSPACK": "Office 365 (Plan K1)",
                    "DESKLESSWOFFPACK": "Office 365 (Plan K2)",
                    "LITEPACK": "Office 365 (Plan P1)",
                    "EXCHANGESTANDARD": "Office 365 Exchange Online Only",
                    "STANDARDPACK": "Enterprise Plan E1",
                    "STANDARDWOFFPACK": "Office 365 (Plan E2)",
                    "ENTERPRISEPACK": "Enterprise Plan E3",
                    "ENTERPRISEPACKLRG": "Enterprise Plan E3",
                    "ENTERPRISEWITHSCAL": "Enterprise Plan E4",
                    "STANDARDPACK_STUDENT": "Office 365 (Plan A1) for Students",
                    "STANDARDWOFFPACKPACK_STUDENT": "Office 365 A1 for students",
                    "ENTERPRISEPACK_STUDENT": "Office 365 (Plan A3) for Students",
                    "ENTERPRISEWITHSCAL_STUDENT": "Office 365 (Plan A4) for Students",
                    "STANDARDPACK_FACULTY": "Office 365 (Plan A1) for Faculty",
                    "STANDARDWOFFPACKPACK_FACULTY": "Office 365 (Plan A2) for Faculty",
                    "ENTERPRISEPACK_FACULTY": "Office 365 (Plan A3) for Faculty",
                    "ENTERPRISEWITHSCAL_FACULTY": "Office 365 (Plan A4) for Faculty",
                    "ENTERPRISEPACK_B_PILOT": "Office 365 (Enterprise Preview)",
                    "STANDARD_B_PILOT": "Office 365 (Small Business Preview)",
                    "VISIOCLIENT": "Visio Pro Online",
                    "POWER_BI_ADDON": "Office 365 Power BI Addon",
                    "POWER_BI_INDIVIDUAL_USE": "Power BI Individual User",
                    "POWER_BI_STANDALONE": "Power BI Stand Alone",
                    "POWER_BI_STANDARD": "Power-BI Standard",
                    "PROJECTESSENTIALS": "Project Lite",
                    "PROJECTCLIENT": "Project Professional",
                    "PROJECTONLINE_PLAN_1": "Project Online",
                    "PROJECTONLINE_PLAN_2": "Project Online and PRO",
                    "ProjectPremium": "Project Online Premium",
                    "ECAL_SERVICES": "ECAL",
                    "EMS": "Enterprise Mobility Suite",
                    "RIGHTSMANAGEMENT_ADHOC": "Windows Azure Rights Management",
                    "MCOMEETADV": "PSTN conferencing",
                    "SHAREPOINTSTORAGE": "SharePoint storage",
                    "PLANNERSTANDALONE": "Planner Standalone",
                    "CRMIUR": "CMRIUR",
                    "BI_AZURE_P1": "Power BI Reporting and Analytics",
                    "INTUNE_A": "Windows Intune Plan A",
                    "PROJECTWORKMANAGEMENT": "Office 365 Planner Preview",
                    "ATP_ENTERPRISE": "Exchange Online Advanced Threat Protection",
                    "EQUIVIO_ANALYTICS": "Office 365 Advanced eDiscovery",
                    "AAD_BASIC": "Azure Active Directory Basic",
                    "RMS_S_ENTERPRISE": "Azure Active Directory Rights Management",
                    "AAD_PREMIUM": "Azure Active Directory Premium",
                    "MFA_PREMIUM": "Azure Multi-Factor Authentication",
                    "STANDARDPACK_GOV": "Microsoft Office 365 (Plan G1) for Government",
                    "STANDARDWOFFPACK_GOV": "Microsoft Office 365 (Plan G2) for Government",
                    "ENTERPRISEPACK_GOV": "Microsoft Office 365 (Plan G3) for Government",
                    "ENTERPRISEWITHSCAL_GOV": "Microsoft Office 365 (Plan G4) for Government",
                    "DESKLESSPACK_GOV": "Microsoft Office 365 (Plan K1) for Government",
                    "ESKLESSWOFFPACK_GOV": "Microsoft Office 365 (Plan K2) for Government",
                    "EXCHANGESTANDARD_GOV": "Microsoft Office 365 Exchange Online (Plan 1) only for Government",
                    "EXCHANGEENTERPRISE_GOV": "Microsoft Office 365 Exchange Online (Plan 2) only for Government",
                    "SHAREPOINTDESKLESS_GOV": "SharePoint Online Kiosk",
                    "EXCHANGE_S_DESKLESS_GOV": "Exchange Kiosk",
                    "RMS_S_ENTERPRISE_GOV": "Windows Azure Active Directory Rights Management",
                    "OFFICESUBSCRIPTION_GOV": "Office ProPlus",
                    "MCOSTANDARD_GOV": "Lync Plan 2G",
                    "SHAREPOINTWAC_GOV": "Office Online for Government",
                    "SHAREPOINTENTERPRISE_GOV": "SharePoint Plan 2G",
                    "EXCHANGE_S_ENTERPRISE_GOV": "Exchange Plan 2G",
                    "EXCHANGE_S_ARCHIVE_ADDON_GOV": "Exchange Online Archiving",
                    "EXCHANGE_S_DESKLESS": "Exchange Online Kiosk",
                    "SHAREPOINTDESKLESS": "SharePoint Online Kiosk",
                    "SHAREPOINTWAC": "Office Online",
                    "YAMMER_ENTERPRISE": "Yammer Enterprise",
                    "EXCHANGE_L_STANDARD": "Exchange Online (Plan 1)",
                    "MCOLITE": "Lync Online (Plan 1)",
                    "SHAREPOINTLITE": "SharePoint Online (Plan 1)",
                    "OFFICE_PRO_PLUS_SUBSCRIPTION_SMBIZ": "Office ProPlus",
                    "EXCHANGE_S_STANDARD_MIDMARKET": "Exchange Online (Plan 1)",
                    "MCOSTANDARD_MIDMARKET": "Lync Online (Plan 1)",
                    "SHAREPOINTENTERPRISE_MIDMARKET": "SharePoint Online (Plan 1)",
                    "OFFICESUBSCRIPTION": "Office ProPlus",
                    "YAMMER_MIDSIZE": "Yammer",
                    "DYN365_ENTERPRISE_PLAN1": "Dynamics 365 Customer Engagement Plan Enterprise Edition",
                    "ENTERPRISEPREMIUM_NOPSTNCONF": "Enterprise E5 (without Audio Conferencing)",
                    "ENTERPRISEPREMIUM": "Enterprise E5 (with Audio Conferencing)",
                    "MCOSTANDARD": "Skype for Business Online Standalone Plan 2",
                    "PROJECT_MADEIRA_PREVIEW_IW_SKU": "Dynamics 365 for Financials for IWs",
                    "STANDARDWOFFPACK_IW_STUDENT": "Office 365 A1 Plus for students",
                    "STANDARDWOFFPACK_IW_FACULTY": "Office 365 A1 Plus for faculty",
                    "EOP_ENTERPRISE_FACULTY": "Exchange Online Protection for Faculty",
                    "EXCHANGESTANDARD_STUDENT": "Exchange Online (Plan 1) for Students",
                    "OFFICESUBSCRIPTION_STUDENT": "Office ProPlus Student Benefit",
                    "STANDARDWOFFPACK_FACULTY": "Office 365 A1 for faculty",
                    "STANDARDWOFFPACK_STUDENT": "Office 365 A1 for students",
                    "DYN365_FINANCIALS_BUSINESS_SKU": "Dynamics 365 for Financials Business Edition",
                    "DYN365_FINANCIALS_TEAM_MEMBERS_SKU": "Dynamics 365 for Team Members Business Edition",
                    "FLOW_FREE": "Microsoft Flow Free",
                    "POWER_BI_PRO": "Power BI Pro",
                    "O365_BUSINESS": "Office 365 Business",
                    "DYN365_ENTERPRISE_SALES": "Dynamics Office 365 Enterprise Sales",
                    "RIGHTSMANAGEMENT": "Rights Management",
                    "PROJECTPROFESSIONAL": "Project Professional",
                    "VISIOONLINE_PLAN1": "Visio Online Plan 1",
                    "EXCHANGEENTERPRISE": "Exchange Online Plan 2",
                    "DYN365_ENTERPRISE_P1_IW": "Dynamics 365 P1 Trial for Information Workers",
                    "DYN365_ENTERPRISE_TEAM_MEMBERS": "Dynamics 365 For Team Members Enterprise Edition",
                    "CRMSTANDARD": "Microsoft Dynamics CRM Online Professional",
                    "EXCHANGEARCHIVE_ADDON": "Exchange Online Archiving For Exchange Online",
                    "EXCHANGEDESKLESS": "Exchange Online Kiosk",
                    "SPZA_IW": "App Connect",
                    "WINDOWS_STORE": "Windows Store for Business",
                    "MCOEV": "Microsoft Phone System",
                    "VIDEO_INTEROP": "Polycom Skype Meeting Video Interop for Skype for Business",
                    "SPE_E5": "Microsoft 365 E5",
                    "SPE_E3": "Microsoft 365 E3",
                    "ATA": "Advanced Threat Analytics",
                    "MCOPSTN2": "Domestic and International Calling Plan",
                    "FLOW_P1": "Microsoft Flow Plan 1",
                    "FLOW_P2": "Microsoft Flow Plan 2",
                    "CRMSTORAGE": "Microsoft Dynamics CRM Online Additional Storage",
                    "SMB_APPS": "Microsoft Business Apps",
                    "MICROSOFT_BUSINESS_CENTER": "Microsoft Business Center",
                    "DYN365_TEAM_MEMBERS": "Dynamics 365 Team Members",
                    "STREAM": "Microsoft Stream Trial",
                    "EMSPREMIUM": "ENTERPRISE MOBILITY + SECURITY E5",
                    "EXCHANGE_STANDARD_ALUMNI" : "Exchange Online (Plan 1) for alumni"
                }
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
        ret_list = [{"skuId":x["skuId"],"skuPartNumber":x["skuPartNumber"],"skuFriendlyName":self.licenses_friendly_name[x["skuPartNumber"]] if x["skuPartNumber"] in self.licenses_friendly_name else x["skuPartNumber"]} for x in licences["value"]]
        ret_list = sorted(ret_list,key = lambda k:k["skuFriendlyName"])
        return ret_list
        #return list(map(lambda x: { need_key : x[need_key] for need_key in need_keys } ,licences["value"]))
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
        if type(error_description) == HTTPClientError and "self_generated_use_raw" in error_description.__dict__ and error_description.__dict__["self_generated_use_raw"] == True:
            return error_description
        errordict = {"error":error_title,"error_description":str(error_description),"error_uri":"See the full API docs at "+error_url}
        errordict = {**errordict,**add_info}
        response = tornado.httpclient.HTTPResponse(request=tornado.httpclient.HTTPRequest(url= ""),code= code, headers= None, buffer= io.StringIO(json.dumps(errordict, indent=2, ensure_ascii=False)))
        ret = HTTPClientError(code=code, message= json.dumps(errordict, indent=2, ensure_ascii=False), response=response)
        ret.__dict__["self_generated_use_raw"] = True
        return ret
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
    