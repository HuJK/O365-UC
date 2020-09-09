<template>
  <v-app id="keep">
    <v-app-bar
      app
      clipped-left
      color="amber"
    >
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <span class="title ml-3 mr-5">{{appName}}&nbsp;<span class="font-weight-light">Admin Panel</span></span>
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

    <v-main>
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
              <v-list-item-title class="headline mb-1">CAPTCHA Settings</v-list-item-title>
              <v-col>
                <v-switch v-model="CAPTCHA_enable_g" label="Enable CAPTCHA for guest invite code redemption"></v-switch>
                <v-switch v-model="CAPTCHA_enable_p" label="Enable CAPTCHA for admin panel login"></v-switch>
                <v-text-field label="Frontend CAPTCHA form field id"  v-model="CAPTCHA_front_end_response_field" :rules="[ v => v.length !== 0 || 'This field is required']"></v-text-field>
                <v-text-field label="Frontend HTML injection (HEAD)"  v-model="CAPTCHA_frontend_head_html" :rules="[ v => v.length !== 0 || 'This field is required']"></v-text-field>
                <v-text-field label="Frontend HTML injection (FORM)"  v-model="CAPTCHA_frontend_login_html" :rules="[ v => v.length !== 0 || 'This field is required']"></v-text-field>
                <v-textarea auto-grow label="Backend verify api request paramaters" code_text spellcheck="false" v-model="CAPTCHA_verify_api"  @input="CAPTCHA_verify_api_change" :rules="[CAPTCHA_verify_api_pass]"></v-textarea>
                <v-textarea auto-grow label="Backend verify api response check function (ECMAScript 5.1)" code_text spellcheck="false" v-model="CAPTCHA_verify_func" @input="CAPTCHA_verify_func_change" :rules="[CAPTCHA_verify_func_pass] "></v-textarea>
                <v-row justify="end">
                  <v-btn
                    :loading="setCAPTCHA_loading"
                    :disabled="setCAPTCHA_loading || CAPTCHA_front_end_response_field.length === 0 || CAPTCHA_frontend_head_html.length === 0 || CAPTCHA_frontend_login_html.length === 0"
                    :color="setCAPTCHA_color_btn_color"
                    class="ma-2 white--text"
                    @click="setCAPTCHA"
                  >
                    Save
                  <v-icon right >{{setCAPTCHA_icon}}</v-icon>
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
                <v-text-field label="new password" type="password"            v-model="New_password" :rules="[ v => v.length >= 6 || 'Password length must >= 6']"></v-text-field>
                <v-row justify="end">
                  <v-btn
                    :loading="setPassword_loading"
                    :disabled="setPassword_loading || Old_password.length == 0 || New_password.length < 6"
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
                <v-col
                    ma-0 pa-0
                    no-gutters
                    class="CAPTCHAfield"
                    align='center'
                >
                <v-text-field 
                  color="blue" 
                  :error-messages="login_errmsg" 
                  type="password" 
                  v-model="password_in" 
                  outlined 
                  label="Password"
                  @keyup.enter="login"
                ></v-text-field>
                </v-col>
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
    </v-main>
  </v-app>
</template>

<script>
  import axios from "axios"
  import debounce from 'lodash/debounce';
  export default {
    props: {
      source: String,
    },
    data: () => ({
      url_base : location.origin,
      cookie_prefix :"o365_uca",
      form_appinfo : false,
      CAPTCHA_response_name : "" ,
      CAPTCHA_enable_p: false,
      CAPTCHA_enable_g: false,
      CAPTCHA_front_end_response_field : "g-recaptcha-response",
      CAPTCHA_verify_api : JSON.stringify({
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
            }, null, 4),
      CAPTCHA_verify_api_pass : true,
      CAPTCHA_verify_api_pass_btn : true,
      CAPTCHA_verify_func : "function(HTTPResponse) {\n    if(HTTPResponse.code < 200 || HTTPResponse.code >= 400){\n        return \"Bed response code: \" + HTTPResponse.code;\n    }\n    else{\n        response_json = JSON.parse(HTTPResponse.body.decode(\"utf8\"))\n        if(response_json[\"success\"] === true){\n            return true;\n        }\n        return \"CAPTCHA failed: \" + JSON.stringify(response_json[\"error-codes\"]);\n    } \n}",
      CAPTCHA_verify_func_pass : true,
      CAPTCHA_verify_func_pass_btn : true,
      CAPTCHA_frontend_head_html : "<script src='https://www.google.com/recaptcha/api.js'> </ script>" , 
      CAPTCHA_frontend_login_html : "<div class='g-recaptcha' data-sitekey=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI></div>",
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
      setCAPTCHA_loading:false,
      setCAPTCHA_color:"blue",
      setCAPTCHA_icon:"mdi-cloud-upload",
      old_password_type : "password",
      setPassword_loading:false,
      setPassword_color:"blue",
      setPassword_icon:"mdi-cloud-upload",
      
      appName : "Office 365 Account Registration Portal",
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
        { icon: 'mdi-robot', text: 'CAPTCHA Settings' },
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
      },
      setCAPTCHA_color_btn_color(){
        if(this.CAPTCHA_verify_api_pass_btn !== true || this.CAPTCHA_verify_func_pass_btn !== true){
          return "orange";
        }
        else{
          return this.setCAPTCHA_color;
        }
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
        if(this.CAPTCHA_response_name === "" || document.getElementsByName(this.CAPTCHA_response_name)[0].value.length > 0){
          this.login_loading=true;
          let CAPTCHA = document.getElementsByName(this.CAPTCHA_response_name).length > 0?document.getElementsByName(this.CAPTCHA_response_name)[0].value:"undefined";
          axios.post(this.api_path + "login",null,{params : {password : this.password_in,"CAPTCHA":CAPTCHA}}).then(
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
        }
        else{
          self.error_msg_bool = true;
          self.error_msg_title="Captcha Required";
          self.error_msg="Please verify that you are not a robot.";
        }
      },
    logoutAdmin(){
      var self = this;
      axios.delete(self.api_path + "login",{params : {session_id : self.$getCookie(self.cookie_prefix + "session_id")}}).then(
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
      self.$delCookie(self.cookie_prefix + "session_id");
      window.location.reload();
     })

    },
    updatePage(){
      var self = this;
        if (self.CAPTCHA_response_name === ""){
          axios.get(this.api_path + "login",{params : {get_CAPTCHA : "p"}}).then(
            function(res){
              document.getElementsByTagName('head')[0].appendChild( document.createRange().createContextualFragment( res.data["CAPTCHA_frontend_head_html"] ));
              document.getElementsByClassName('CAPTCHAfield')[0].appendChild( document.createRange().createContextualFragment( res.data["CAPTCHA_frontend_login_html"] ));
              
              self.CAPTCHA_response_name = res.data["CAPTCHA_front_end_response_field"];
            }
            
          ).catch(function(error){
            console.log(error);
          })
        }
        if (self.CAPTCHA_response_name !== "" && document.getElementsByName(self.CAPTCHA_response_name).length === 0){
          axios.get(this.api_path + "login",{params : {get_CAPTCHA : "p"}}).then(
            function(res){
              document.getElementsByClassName('CAPTCHAfield')[0].appendChild( document.createRange().createContextualFragment( res.data["CAPTCHA_frontend_login_html"] ));
            }
            
          ).catch(function(error){
            console.log(error);
          })
        }

      axios.get(this.api_path + "CAPTCHA",{params : {session_id : this.$getCookie(self.cookie_prefix + "session_id")}}).then(
        function(res){
          self.CAPTCHA_enable_p = res.data["p"]["CAPTCHA_enable"];
          self.CAPTCHA_enable_g = res.data["g"]["CAPTCHA_enable"];
          self.CAPTCHA_front_end_response_field = res.data["g"]["CAPTCHA_front_end_response_field"];
          self.CAPTCHA_verify_api = JSON.stringify( res.data["g"]["CAPTCHA_verify_api"],null,4);
          self.CAPTCHA_frontend_head_html = res.data["g"]["CAPTCHA_frontend_head_html"];
          self.CAPTCHA_frontend_login_html = res.data["g"]["CAPTCHA_frontend_login_html"];
          self.CAPTCHA_verify_func = res.data["g"]["CAPTCHA_verify_api_check_function"];
        }
      ).catch(function(error){
        console.log(error);
      }).finally(function(){
        self.CAPTCHA_verify_api_change();
        self.CAPTCHA_verify_func_change();
      })

      axios.get(this.api_path + "Info",{params : {session_id : this.$getCookie(self.cookie_prefix + "session_id")}}).then(
        function(res){
          self.appName = res.data["appName"];
          document.title = res.data["appName"];
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
      if(self.secret.indexOf("...(hidden)...") === -1 || self.client_id.indexOf("...(hidden)...") === -1 ){
        let params = {session_id : this.$getCookie(self.cookie_prefix + "session_id")}
        if(self.secret.indexOf("...(hidden)...") === -1){
          params["secret"] = self.secret;
        }
        if(self.client_id.indexOf("...(hidden)...") === -1){
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
      if(self.code.indexOf("...(hidden)...")=== -1 && self.code.length !== 0){
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
    setCAPTCHA(){
      var self = this;
      let new_config_p= {
        "CAPTCHA_enable":this.CAPTCHA_enable_p,
        "CAPTCHA_front_end_response_field":this.CAPTCHA_front_end_response_field,
        "CAPTCHA_frontend_head_html":this.CAPTCHA_frontend_head_html,
        "CAPTCHA_frontend_login_html":this.CAPTCHA_frontend_login_html,
        
      };
      if(self.CAPTCHA_verify_api_pass_btn === true){
        new_config_p["CAPTCHA_verify_api"] = JSON.parse(self.CAPTCHA_verify_api);
      }
      if(self.CAPTCHA_verify_func_pass_btn === true){
        new_config_p["CAPTCHA_verify_api_check_function"] = self.CAPTCHA_verify_func;
      }
      let new_config_g = JSON.parse(JSON.stringify(new_config_p));
      new_config_g["CAPTCHA_enable"] = this.CAPTCHA_enable_g;
      this.setCAPTCHA_loading=true;
      axios.put(this.api_path + "CAPTCHA",null,{params : {
        session_id : self.$getCookie(self.cookie_prefix + "session_id")
        },data:{        new_config: {
          "p":new_config_p,
          "g":new_config_g
        }}
        
        }
      ).then(
        function(){
          self.setCAPTCHA_color = "green";
          self.setCAPTCHA_icon = "mdi-checkbox-marked-circle-outline"
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
        self.setCAPTCHA_loading=false;
        self.updatePage();
      })
    },
    CAPTCHA_verify_api_change(){
      this.CAPTCHA_verify_api_pass_btn = false;
      try{
        JSON.parse(this.CAPTCHA_verify_api);
        this.delay_CAPTCHA_verify_api_change()
      }
      catch(err){
        this.CAPTCHA_verify_api_pass = err.toString();
      }
    },
    delay_CAPTCHA_verify_api_change: debounce(function(){this.CAPTCHA_verify_api_change_server_check()},500),
    CAPTCHA_verify_api_change_server_check(){
      let self=this;
      axios.get(this.api_path + "CAPTCHA",{params : {session_id: this.$getCookie(this.cookie_prefix + "session_id") , test_req_params:"p", test_req_body:self.CAPTCHA_verify_api }}).then(
        function(){
          self.CAPTCHA_verify_api_pass=true;
          self.CAPTCHA_verify_api_pass_btn=true;
        })
      .catch(function (error){
        if (error.response) {
          if (error.response.data["error_description"] != undefined){
            self.CAPTCHA_verify_api_pass=error.response.data["error"] + ": " + error.response.data["error_description"];
          }
          else{
            self.CAPTCHA_verify_api_pass = error.response.data;
          }
        }
        else{
          console.log(error);
          self.CAPTCHA_verify_api_pass = "Network Error."
        }
      })
      .finally(function(){
        
      })
    },
    CAPTCHA_verify_func_change(){
      this.CAPTCHA_verify_func_pass_btn="Waiting for server check...";
      this.delay_check_verify_func();
    },
    delay_check_verify_func: debounce(function(){this.check_verify_func()},100),
    check_verify_func(){
      let self=this;
      axios.get(this.api_path + "CAPTCHA",{params : {session_id: this.$getCookie(this.cookie_prefix + "session_id") , test_func:"p",test_func_body:this.CAPTCHA_verify_func }}).then(
        function(){
          self.CAPTCHA_verify_func_pass=true;
          self.CAPTCHA_verify_func_pass_btn=true;
        })
      .catch(function (error){
        if (error.response) {
          if (error.response.data["error_description"] != undefined){
            self.CAPTCHA_verify_func_pass=error.response.data["error"] + ": " + error.response.data["error_description"];
          }
          else{
            self.CAPTCHA_verify_func_pass = error.response.data;
          }
        }
        else{
          console.log(error);
          self.CAPTCHA_verify_func_pass = "Network Error."
        }
      })
      .finally(function(){
        
      })
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
        self.updatePage();
      })
    }
  }
}
</script>

<style>
#keep .v-navigation-drawer__border {
  display: none
}
[code_text] {
  font-family: Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New !important;
  background: url("/code_line_number.png");
  background-attachment: local;
  background-repeat: no-repeat;
  padding-left: 30px !important;
  padding-top: 11px !important;
  border-color: #ccc;
  white-space: nowrap;
  overflow: auto;
  font-size: 13px !important;
  line-height: 16px !important;
}
</style>