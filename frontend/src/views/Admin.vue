<template>
  <v-app id="keep">
    <v-app-bar
      app
      clipped-left
      color="amber"
    >
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <span class="title ml-3 mr-5">Office 365 Account Registration Portal&nbsp;<span class="font-weight-light">Admin Panel</span></span>
      <v-spacer />





      <v-btn icon color="grey lighten-2" to="/">
        <v-icon>mdi-account-plus</v-icon>
      </v-btn>

      <v-btn 
        icon 
        color="grey lighten-2"
        @click="logoutAdmin"
      >
        <v-icon>mdi-exit-to-app</v-icon>
      </v-btn>

    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
      color="grey lighten-4"
    >
      <v-list
        dense
        class="grey lighten-4"
      >
        <template v-for="(item, i) in items">
          <v-divider
            v-if="item.divider"
            :key="i"
            class="my-4"
          />
          <v-list-item
            v-else
            :key="i"
            link
          >
            <v-list-item-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title class="grey--text">
                {{ item.text }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-content>
      <v-container
        fluid
        class="grey lighten-4"
      >

        <v-card
          class="mx-auto"
          max-width="3440000"
          outlined
        >
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1">Application Infomation</v-list-item-title>
              <v-col>
                <v-form
                  v-model="form_appinfo"
                >
                  <v-text-field label="App Name" v-model="appName"  :rules="[ v => v.length !== 0 || 'This field is required']"></v-text-field>
                  <v-text-field label="Code Receive URI" v-model="redirect_uri" :rules="[checkHTTPS]" ></v-text-field>
                  <v-row justify="end">
                    <v-btn
                      :color="setInfo_color"
                      class="ma-2 white--text"
                      :loading="setInfo_loading"
                      :disabled="setInfo_disabled"
                      @click="setInfo"
                    >
                      Save
                      <v-icon right >{{setInfo_icon}}</v-icon>
                    </v-btn>
                  </v-row>
                </v-form>
              </v-col>
            </v-list-item-content>
          </v-list-item>
        </v-card>

        <v-card
          class="mx-auto"
          max-width="3440000"
          outlined
        >
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1">Client ID and Secret</v-list-item-title>
              <v-col>
                <v-row justify="start">
                  <v-btn
                    rounded 
                    color="primary" 
                    class="ma-2 white--text"
                    @click="prepareRedirect2GetSecretUrl"
                  >
                    Prepare
                  </v-btn>
                  <v-btn
                    rounded 
                    :disabled="redirect2GetSecretUrl_disabled"
                    color="primary" 
                    class="ma-2 white--text"
                    target="_blank"
                    :href="redirect2GetSecretUrl_url"
                  >
                    Get Client ID and Secret
                  </v-btn>
                </v-row>
                <v-text-field label="Secret"        v-model="secret" :rules="[ v => v.length !== 0 || 'This field is required']"></v-text-field>
                <v-text-field label="Client ID"  v-model="client_id" :rules="[ v => v.length !== 0 || 'This field is required']"></v-text-field>
                <v-row justify="end">
                  <v-btn
                    :loading="CIDaS_loading"
                    :disabled="CIDaS_loading"
                    :color="CIDaS_color"
                    class="ma-2 white--text"
                    @click="CIDaS"
                  >
                    Save
                  <v-icon right >{{CIDaS_icon}}</v-icon>
                  </v-btn>
                </v-row>
              </v-col>
            </v-list-item-content>
          </v-list-item>
        </v-card>

        <v-card
          class="mx-auto"
          max-width="3440000"
          outlined
        >
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1">Grant Permission and Get Code</v-list-item-title>
              <v-col>
                <v-row justify="start">
                  <v-btn
                    rounded 
                    :loading="prepareRedirect2GetCodeUrl_loading"
                    :disabled="prepareRedirect2GetCodeUrl_loading"
                    color="primary" 
                    class="ma-2 white--text"
                    @click="prepareRedirect2GetCodeUrl"
                  >
                    Prepare
                  </v-btn>
                  <v-btn
                    rounded 
                    :disabled="redirect2GetCodeUrl_disabled"
                    color="primary" 
                    class="ma-2 white--text"
                    target="_blank"
                    :href="redirect2GetCodeUrl_url"
                  >
                    Grant Permissoins
                  </v-btn>
                </v-row>
                <v-text-field label="Code" v-model="code"></v-text-field>
                <v-row justify="start">
                  <v-btn
                    :loading="InitToken_loading"
                    :disabled="InitToken_disabled"
                    :color="InitToken_color"

                    class="ma-2 white--text"
                    
                    @click="initToken"
                  >
                    Initialize token by this code
                    <v-icon right >{{InitToken_icon}}</v-icon>
                  </v-btn>
                </v-row>
              </v-col>
            </v-list-item-content>
          </v-list-item>
        </v-card>

        <v-card
          class="mx-auto"
          max-width="3440000"
          outlined
        >
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1">Token</v-list-item-title>
              <v-col>
                <v-row justify="start">
                    <v-btn
                      :loading="RefreshToken_loading"
                      :disabled="RefreshToken_loading"
                      color="green" 
                      class="ma-2 white--text"
                      @click="refreshToken"
                    >
                      Force Refresh Token
                    </v-btn>
                </v-row>
                <v-text-field label="Access Token" v-model="access_token"></v-text-field>
                <v-text-field label="Refresh Token" v-model="refresh_token"></v-text-field>
              </v-col>
            </v-list-item-content>
          </v-list-item>
        </v-card>

        <v-card
          class="mx-auto"
          max-width="3440000"
          outlined
        >
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1">Guest Settings</v-list-item-title>
              <v-col>
                    <v-btn
                      color="green" 
                      class="ma-2 white--text"
                      :loading="RefreshRegInfo_loading"
                      :disabled="RefreshRegInfo_loading"
                      @click="refreshRegInfo"
                    >
                      Refresh List
                      <v-icon right >mdi-autorenew</v-icon>
                    </v-btn>
                <v-row justify="start">
                  <v-col>
                    <v-text-field 
                      color="blue" 
                      :error-messages="domain_select_errmsg" 
                      readonly
                      solo
                      flat
                      value="Registerable Domains"
                    ></v-text-field>

                    
                    <v-container fluid v-for="(item, index) in domains" :key="index"> 
                      <v-switch v-model="selected_domains" :label="item" :value="item"></v-switch>
                    </v-container>


                  </v-col>
                  <v-col>
                    <v-text-field 
                      color="blue" 
                      :error-messages="domain_select_errmsg" 
                      readonly
                      solo
                      flat
                      value="Registerable Licences"
                    ></v-text-field>
                    <v-container fluid v-for="(item, index) in licences" :key="index"> 
                      <v-switch v-model="selected_licences" :label="item.skuPartNumber" :value="item" @change="maxAllowedLicense = Math.max(1,Math.min(maxAllowedLicense,selected_licences.length))"></v-switch>
                    </v-container>
                    <v-row>
                      <v-select
                        :items="maxAllowedLicenseList"
                        filled
                        label="Max allowed License"
                        v-model="maxAllowedLicense"
                        
                      ></v-select>
                    </v-row>

                  </v-col>
                </v-row>

                <v-row justify="end">
                  <v-card-actions>
                    <v-btn
                      class="ma-2 white--text"
                      :disabled="setDomainsAndLicences_disable"
                      :loading="setDomainsAndLicences_loading"
                      :color="setDomainsAndLicences_color"
                      @click="setDomainsAndLicences"
                    >
                      Save
                      <v-icon right >{{setDomainsAndLicences_icon}}</v-icon>
                    </v-btn>
                  </v-card-actions>
                </v-row>
              </v-col>
            </v-list-item-content>
          </v-list-item>
        </v-card>




        <v-card
          class="mx-auto"
          max-width="3440000"
          outlined
        >
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1">Settings</v-list-item-title>
              <v-col>
                <v-text-field 
                  color="blue" 
                  :error-messages="domain_select_errmsg" 
                  readonly
                  solo
                  flat
                  value="Change Password"
                ></v-text-field>
                <v-text-field label="Old password" :type="old_password_type"  v-model="Old_password" :rules="[ v => v.length !== 0 || 'This field is required']"></v-text-field>
                <v-text-field label="new password" type="password"            v-model="New_password" :rules="[ v => v.length !== 0 || 'This field is required']"></v-text-field>
                <v-row justify="end">
                  <v-btn
                    :loading="setPassword_loading"
                    :disabled="setPassword_loading"
                    :color="setPassword_color"
                    class="ma-2 white--text"
                    @click="setPassword"
                  >
                    Save
                  <v-icon right >{{setPassword_icon}}</v-icon>
                  </v-btn>
                </v-row>
              </v-col>
            </v-list-item-content>
          </v-list-item>
        </v-card>






          <v-overlay opacity=0.9 color="black" :value="!login_success">
            <v-card       
              class="mx-auto"
              color="white"
              light
              loading=true
              min-width=400
              shaped
            >
              <v-col>
                <v-text-field 
                  color="blue" 
                  :error-messages="login_errmsg" 
                  type="password" 
                  v-model="password_in" 
                  outlined 
                  label="Password"
                  @keyup.enter="login"
                ></v-text-field>
                <v-row justify="center">
                  <v-btn
                    :loading="login_loading"
                    :disabled="login_loading"
                    color="error"
                    @click="login"
                  >
                    Login
                  </v-btn>
                </v-row>
              </v-col>

            </v-card>
          </v-overlay>

          <v-overlay opacity=0.9 color="black" :value="error_msg_bool">
            <v-card       
              class="mx-auto"
              color="red accent-1"
              loading=true
              min-width=400
              shaped
            >
              <v-col>
                <p color="green" class="headline mb-1">{{error_msg_title}}</p>
                <v-card-text color="green" v-html="error_msg"></v-card-text>
                <v-row justify="center">
                  <v-btn
                    color="error"
                    @click="error_msg_bool = false"
                  >
                    OK
                  </v-btn>
                </v-row>
              </v-col>

            </v-card>
          </v-overlay>

      </v-container>
    </v-content>
  </v-app>
</template>

<script>
  import axios from "axios"
  export default {
    props: {
      source: String,
    },
    data: () => ({
      url_base : location.origin,
      cookie_prefix :"o365_uca",
      form_appinfo : false,
      password_in : "",
      Old_password : "",
      New_password : "",
      login_loading : false,
      login_success : false,
      login_errmsg:"",
      setInfo_loading : false,
      setInfo_color : "blue",
      setInfo_icon : "mdi-cloud-upload",
      CIDaS_loading : false,
      CIDaS_color : "red",
      CIDaS_icon : "mdi-cloud-upload",
      redirect2GetSecretUrl_url : undefined,
      prepareRedirect2GetCodeUrl_loading : false,
      redirect2GetCodeUrl_url : undefined,
      InitToken_loading : false,
      InitToken_color : "blue",
      InitToken_icon : "mdi-autorenew",
      RefreshToken_loading : false,
      RefreshRegInfo_loading : false,
      domain_select_errmsg : "",
      setDomainsAndLicences_loading : false,
      setDomainsAndLicences_icon : "mdi-cloud-upload",
      setDomainsAndLicences_color : "blue",
      Admin_setting_loading:false,
      Admin_setting_color:"blue",
      Admin_setting_icon:"mdi-cloud-upload",
      old_password_type : "password",
      setPassword_loading:false,
      setPassword_color:"blue",
      setPassword_icon:"mdi-cloud-upload",
      
      appName : "",
      redirect_uri : "",
      maxAllowedLicense : 1,
      secret : "",
      client_id : "",
      code : "",
      access_token : "",
      refresh_token : "",
      error_msg_bool:false,
      error_msg_title:"Error",
      error_msg:"Error message here!",
      drawer: null,
      items: [
        { icon: 'mdi-information', text: 'App Info' },
        { icon: 'mdi-key', text: 'Client ID and Secret' },
        { divider: true },
        { icon: 'mdi-qrcode-plus', text: 'Grant permission' },
        { icon: 'mdi-ticket', text: 'Token' },
        { divider: true },
        { icon: 'mdi-account-plus', text: 'Guest Settings' },
        { icon: 'mdi-cog', text: 'Settings' }
      ],
      domains:[
        "1.example.com",
        "2.example.com",
        "3.example.com",
        "4.example.com"
      ],
      selected_domains:[
        "1.example.com",
        "2.example.com"
      ],
      licences:[
        { skuPartNumber: "A1" , skuId: "00121"},
        { skuPartNumber: "A2" , skuId: "00122"},
        { skuPartNumber: "A3" , skuId: "00123"}
      ],
      selected_licences:[
        { "skuPartNumber": "A1", "skuId": "00121" }, { "skuPartNumber": "A3", "skuId": "00123" }
      ],
      
      
    }),
    computed: {
      api_path(){ return this.url_base + "/api/"},
      setInfo_disabled(){return !this.form_appinfo || this.setInfo_loading},
      redirect2GetCodeUrl_disabled(){return this.redirect2GetCodeUrl_url === undefined},
      redirect2GetSecretUrl_disabled() {return this.redirect2GetSecretUrl_url === undefined},
      InitToken_disabled() {return this.InitToken_loading || this.code.length === 0},
      setDomainsAndLicences_disable(){return this.setDomainsAndLicences_loading || (this.selected_domains.length === 0) || (this.selected_licences.length === 0) },
      maxAllowedLicenseList() {
          return [...Array(this.selected_licences.length).keys()].map( function (x){return x+1});
      }
    },
    mounted: function(){
      this.updatePage();
    },
    methods: {
      checkHTTPS(v){
        return v.startsWith("https://") ? true : "Redirect URI must start with 'https://' due to Microsoft's GraphAPI restriction.";
      },
      login() {
        var self = this;
        this.login_loading=true;
        axios.post(this.api_path + "login",null,{params : {password : this.password_in}}).then(
          function(res){
            self.$setCookie(self.cookie_prefix + "session_id", res.data["session_id"]);
            self.updatePage();
          })
        .catch(function (error){
          if (error.response) {
            if(error.response.status === 401){
              self.login_errmsg = error.response.data.error_description;
            }
            else{
              self.login_errmsg = "Error code:" + error.response.status;
            }
          }
          else{
            console.log(error);
            self.login_errmsg = "Network Error."
          }
        })
        .finally(function(){
          self.login_loading=false;
        })
      },
    logoutAdmin(){
      this.$delCookie(this.cookie_prefix + "session_id");
      window.location.reload();
    },
    updatePage(){
      var self = this;
      axios.get(this.api_path + "Info",{params : {session_id : this.$getCookie(self.cookie_prefix + "session_id")}}).then(
        function(res){
          self.appName = res.data["appName"];
          self.redirect_uri = res.data["redirect_uri"] === "" ? self.api_path + "setCode" : res.data["redirect_uri"]
          self.maxAllowedLicense =res.data["maxAllowedLicense"];
          self.secret =res.data["secret"];
          self.client_id =res.data["client_id"];
          if(self.secret.length + self.client_id.length > 0){
            self.CIDaS_color = "blue";
          }
          self.code =res.data["code"];
          self.access_token =res.data["access_token"];
          self.refresh_token =res.data["refresh_token"];
          self.login_success=true;

          self.domains = res.data["allDomains"];
          self.selected_domains = res.data["availableDomains"];
          self.licences = res.data["allLicences"];
          self.selected_licences = res.data["availableLicences"];

          if(self.password_in === "admin"){
            self.setPassword_color = "red";
            self.Old_password = self.password_in;
            self.old_password_type = "text";
          }
        }
        
      ).catch(function(error){
        console.log(error);
        self.login_success=false;
      })
    },
    setInfo(){
      var self = this;
      this.setInfo_loading=true;
      axios.put(this.api_path + "Info",null,{params : {session_id : self.$getCookie(self.cookie_prefix + "session_id"),newInfo:{appName:self.appName , redirect_uri : self.redirect_uri}}}).then(
        function(){
          self.setInfo_color = "green";
          self.setInfo_icon = "mdi-checkbox-marked-circle-outline"
          self.updatePage();
        })
      .catch(function (error){
        if (error.response) {
          if (error.response.data["error_description"] != undefined){
            self.error_msg_title = error.response.data["error"];
            self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.response.data;
          }
        }
        else{
          self.error_msg_title = "Error";
          self.error_msg = error.toString();
        }
        self.error_msg_bool = true;
        console.log(error);
      })
      .finally(function(){
        self.setInfo_loading=false;
      })
    },
    CIDaS(){
      let self = this;
      this.CIDaS_loading=true;
      if(self.secret.indexOf("...(not showing)...") === -1 || self.client_id.indexOf("...(not showing)...") === -1 ){
        let params = {session_id : this.$getCookie(self.cookie_prefix + "session_id")}
        if(self.secret.indexOf("...(not showing)...") === -1){
          params["secret"] = self.secret;
        }
        if(self.client_id.indexOf("...(not showing)...") === -1){
          params["client_id"] = self.client_id;
        }
        axios.put(this.api_path + "setSecretId",null,{params : params}).then(
          function(){
            self.CIDaS_color = "green";
            self.CIDaS_icon = "mdi-checkbox-marked-circle-outline"
            self.updatePage();
          })
        .catch(function (error){
          if (error.response) {
            
            if (error.response.data["error_description"] != undefined){
              self.error_msg_title = error.response.data["error"];
              self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
            }
            else{
              self.error_msg_title = "Error";
              self.error_msg = error.response.data;
            }
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.toString();
          }
          self.error_msg_bool = true;
          console.log(error);
        })
        .finally(function(){
          self.CIDaS_loading=false;
        })
      }
      else{
        self.CIDaS_color = "green";
        self.CIDaS_icon = "mdi-checkbox-marked-circle-outline"
        self.CIDaS_loading=false;
      }
    },
    prepareRedirect2GetSecretUrl(){
      let self = this;
      axios.get(this.api_path + "getSecretIdUrl",{params : {session_id : self.$getCookie(self.cookie_prefix + "session_id")}}).then(
          function(res){
            self.redirect2GetSecretUrl_url = res.data;
          })
        .catch(function (error){
          if (error.response) {
            if (error.response.data["error_description"] != undefined){
              self.error_msg_title = error.response.data["error"];
              self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
            }
            else{
              self.error_msg_title = "Error";
              self.error_msg = error.response.data;
            }
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.toString();
          }
          self.error_msg_bool = true;
          console.log(error);
        })
    },
    prepareRedirect2GetCodeUrl(){
      let self = this;
      self.prepareRedirect2GetCodeUrl_loading = true;
      axios.get(this.api_path + "waitCodeSet",{params : {session_id : self.$getCookie(self.cookie_prefix + "session_id")}})
        .then(function(){ 
          self.redirect2GetCodeUrl_url = undefined;
          self.updatePage();
          self.initToken();
        })
        .catch(function (error){
          console.log(error);
          if (error.response) {
            if (error.response.data["error_description"] != undefined){
              self.error_msg_title = error.response.data["error"];
              self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
            }
            else{
              self.error_msg_title = "Error";
              self.error_msg = error.response.data;
            }
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.toString();
          }
          self.redirect2GetCodeUrl_url = undefined;
          self.error_msg_bool = true;
          console.log(error);
        }).finally(function (){
          self.redirect2GetCodeUrl_url = undefined;
          self.prepareRedirect2GetCodeUrl_loading = false;
        })
      axios.get(this.api_path + "getCodeURL",{params : {session_id : self.$getCookie(self.cookie_prefix + "session_id")}}).then(
          function(res){
            self.redirect2GetCodeUrl_url = res.data;
          })
        .catch(function (error){
          if (error.response) {
            if (error.response.data["error_description"] != undefined){
              self.error_msg_title = error.response.data["error"];
              self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
            }
            else{
              self.error_msg_title = "Error";
              self.error_msg = error.response.data;
            }
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.toString();
          }
          self.error_msg_bool = true;
          console.log(error);
        })
    },
    initToken(){
      var self = this;
      this.InitToken_loading=true;
      if(self.code.indexOf("...(not showing)...")=== -1 && self.code.length !== 0){
        axios.put(this.api_path + "Info",null,{params : {session_id : self.$getCookie(self.cookie_prefix + "session_id"),newInfo:{code:self.code}}}).then(
          function(){
            self.setInfo_color = "green";
            self.setInfo_icon = "mdi-checkbox-marked-circle-outline"
            self.updatePage();
          })
        .catch(function (error){
          if (error.response) {
            if (error.response.data["error_description"] != undefined){
              self.error_msg_title = error.response.data["error"];
              self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
            }
            else{
              self.error_msg_title = "Error";
              self.error_msg = error.response.data;
            }
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.toString();
          }
          self.error_msg_bool = true;
          console.log(error);
        })
        .finally(function(){
          self.initToken_step2();
        })
      }
      else{
        self.initToken_step2();
      }
    },
    initToken_step2(){
      var self = this;
      axios.get(this.api_path + "initToken",{params : {session_id : self.$getCookie(self.cookie_prefix + "session_id")}}).then(
        function(){
          self.InitToken_color = "green";
          self.InitToken_icon = "mdi-checkbox-marked-circle-outline"
          self.updatePage();
          self.refreshRegInfo();
        })
      .catch(function (error){
        if (error.response) {
          console.log(error.response)
          if (error.response.data["error_description"] != undefined){
            self.error_msg_title = error.response.data["error"];
            self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.response.data;
          }
        }
        else{
          self.error_msg_title = "Error";
          self.error_msg = error.toString();
        }
        self.error_msg_bool = true;
        console.log(error);
      })
      .finally(function(){
        self.InitToken_loading=false;
      })
    },
    refreshToken(){
      var self = this;
      this.RefreshToken_loading=true;
      axios.get(this.api_path + "testInit",{params : {session_id : self.$getCookie(self.cookie_prefix + "session_id") , force : true }}).then(
        function(){
          self.RefreshToken_icon = "mdi-checkbox-marked-circle-outline"
          self.updatePage();
        })
      .catch(function (error){
        if (error.response) {
          console.log(error.response)
          if (error.response.data["error_description"] != undefined){
            self.error_msg_title = error.response.data["error"];
            self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.response.data;
          }
        }
        else{
          self.error_msg_title = "Error";
          self.error_msg = error.toString();
        }
        self.error_msg_bool = true;
        console.log(error);
      })
      .finally(function(){
        self.RefreshToken_loading=false;
      })
    },
    refreshRegInfo(){
      var self = this;
      this.RefreshRegInfo_loading=true;
      axios.get(this.api_path + "refreshRegInfo",{params : {session_id : self.$getCookie(self.cookie_prefix + "session_id") , force : true }}).then(
        function(){
          self.updatePage();
        })
      .catch(function (error){
        if (error.response) {
          console.log(error.response)
          if (error.response.data["error_description"] != undefined){
            self.error_msg_title = error.response.data["error"];
            self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.response.data;
          }
        }
        else{
          self.error_msg_title = "Error";
          self.error_msg = error.toString();
        }
        self.error_msg_bool = true;
        console.log(error);
      })
      .finally(function(){
        self.RefreshRegInfo_loading=false;
      })
    },
    setDomainsAndLicences(){
      var self = this;
      this.setDomainsAndLicences_loading=true;
      let params = {session_id : self.$getCookie(self.cookie_prefix + "session_id") , availableDomains : JSON.stringify( self.selected_domains), availableLicences : JSON.stringify( self.selected_licences) , maxAllowedLicense : self.maxAllowedLicense };
      console.log(params);
      axios.put(this.api_path + "setDomainsAndLicences",null,{params : params}).then(
        function(){
          self.setDomainsAndLicences_color = "green";
          self.setDomainsAndLicences_icon = "mdi-checkbox-marked-circle-outline"
          self.updatePage();
        })
      .catch(function (error){
        if (error.response) {
          console.log(error.response)
          if (error.response.data["error_description"] != undefined){
            self.error_msg_title = error.response.data["error"];
            self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.response.data;
          }
        }
        else{
          self.error_msg_title = "Error";
          self.error_msg = error.toString();
        }
        self.error_msg_bool = true;
        console.log(error);
      })
      .finally(function(){
        self.setDomainsAndLicences_loading=false;
      })
    },
    Admin_setting(){

    },
    setPassword(){
      var self = this;
      axios.put(this.api_path + "login",null,{params : {session_id : self.$getCookie(self.cookie_prefix + "session_id"),password: self.New_password , password_old : self.Old_password}}).then(
        function(){
          self.Old_password = "";
          self.New_password = "";
          window.location.reload();
        })
      .catch(function (error){
        if (error.response) {
          if (error.response.data["error_description"] != undefined){
            self.error_msg_title = error.response.data["error"];
            self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.response.data;
          }
        }
        else{
          self.error_msg_title = "Error";
          self.error_msg = error.toString();
        }
        self.error_msg_bool = true;
        console.log(error);
      })
      .finally(function(){
        self.initToken_step2();
      })
    }
  }
}
</script>

<style>
#keep .v-navigation-drawer__border {
  display: none
}
</style>