<template>
  <v-app>
    <v-col>
      <v-app-bar
        app
        color="primary"
        dark
      >
        <div class="d-flex align-center">
          <v-img
            alt="Vuetify Logo"
            class="shrink mr-2"
            contain
            src="logo.ico"
            transition="scale-transition"
            width="40"
          />
        </div>
        <span class="title ml-3 mr-5">{{appName}}</span>
        <v-spacer></v-spacer>
        <v-btn icon color="grey lighten-2" to="/admin">
          <v-icon>mdi-cog</v-icon>
        </v-btn>
        <v-btn 
          icon 
          color="grey lighten-2"
          @click="logoutGuest"
        >
          <v-icon>mdi-exit-to-app</v-icon>
        </v-btn>
      </v-app-bar>
      <v-main>
          <v-card
            class="mx-auto"
            style="max-width: 800px;"
          >

            <v-toolbar
              color="deep-purple accent-4"
              cards
              
              flat
            >
              <v-card-title style="color : white" class="title font-weight-regular">Sign up</v-card-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-form
              ref="form"
              v-model="form"
              class="pa-4 pt-6"
            >
            <v-container>
              <v-row>
              <v-text-field
                v-model="username"
                :rules="[ rules.username_rule, rules.length(1)]"
                :error-messages="username_errormsg"
                filled
                color="deep-purple"
                label="User Name"
                style="min-height: 96px max-width : 300"
                :readonly="username_lock || username_lock_checking || submited"
                :disabled="username_lock_checking"
                @input="usernameChange"
                type="User Name"
              ></v-text-field>
              <v-text-field
                solo
                outlined
                color="white"
                readonly
                background-color="white"
                style="max-width: 40px"
                value="@"
              ></v-text-field>
                <v-select
                  :items="domains"
                  filled
                  :readonly="username_lock || username_lock_checking || submited"
                  :disabled="username_lock_checking"
                  style="min-height: 96px "
                  label="Select Domain"
                  v-model="selected_domain"
                ></v-select>
                  <v-btn
                    :loading="checkBtn_loading"
                    :disabled="checkBtn_disable"
                    :color="checkBtn_color"
                    class="ma-2 white--text"
                    @click="checkName"
                  >
                    {{checkBtn_text}}
                    <v-icon right dark>{{checkBtn_icon}}</v-icon>
                  </v-btn>
              </v-row>
            </v-container>
            <v-container>
              <v-row>
                <v-text-field
                  v-model="givenName"
                  :rules="[rules.requiredStr]"
                  filled
                  @input="FLnameChange"
                  color="deep-purple"
                  label="First Name"
                ></v-text-field>
                <v-text-field
                  v-model="surname"
                  :rules="[rules.requiredStr]"
                  @input="FLnameChange"
                  filled
                  color="deep-purple"
                  label="Last Name"
                ></v-text-field>
                <v-autocomplete
                  :items="locatoinList"
                  filled
                  style="max-width: 120px"
                  label="Location"
                  v-model="usageLocation"
                ></v-autocomplete>
                <v-btn
                  :loading="createBtn_loading"
                  :disabled="createBtn_disable"
                  :color="createBtn_color"
                  class="ma-2 white--text"
                  @click="createUser"
                >
                  {{createBtn_text}}
                </v-btn>
              </v-row>
            </v-container>
              <v-container>
              <v-row>


              <v-text-field
                v-model="displayName"
                :rules="[rules.requiredStr]"
                filled
                color="deep-purple"
                label="Display Name"
              ></v-text-field>

                
                <v-btn
                  :loading="updateBtn_loading"
                  :disabled="updateBtn_disable"
                  :color="updateBtn_color"
                  class="ma-2 white--text"
                  @click="updateUser"
                >
                  {{updateBtn_text}}
                </v-btn>
              </v-row>
              </v-container>
              <v-container>
              <v-row>
                <v-select
                  :items="licences"
                  filled
                  label="Select Licences"
                  item-text="skuFriendlyName"
                  item-value="skuId"
                  v-model="selected_licence"
                ></v-select>
                <v-btn
                  :loading="addLicenceBtn_loading"
                  :disabled="addLicenceBtn_disable"
                  :color="addLicenceBtn_color"
                  @click="addLicenceUser"
                  class="ma-2 white--text"
                >
                  {{addLicenceBtn_text}}
                </v-btn>
              </v-row>
              </v-container>
              <v-checkbox
                v-model="agreement"
                :rules="[rules.required]"
                color="deep-purple"
              >
                <template v-slot:label>
                  I agree to the&nbsp;
                  <a href="https://portal.office.com/Commerce/Mosa.aspx" target="_blank">Terms of Service</a>
                  &nbsp;and&nbsp;
                  <a href="https://privacy.microsoft.com/zh-tw/privacystatement" target="_blank">Privacy Policy</a>*
                </template>
              </v-checkbox>

            </v-form>
            <v-divider></v-divider>
            
            <v-card-actions>
              <v-btn
                :disabled="accInfoBtn_disable"
                class="white--text"
                color="deep-purple accent-4"
                depressed
                @click="dialog=true"
              >Account Info</v-btn>

              <v-btn
                v-if="0==1"
                class="white--text"
                color="deep-purple accent-4"
                depressed
                @click="testFunc"
              >Author_HuJK</v-btn>

              
              <v-spacer></v-spacer>
              <v-btn
                :disabled="!form || !username_checked || submited"
                class="white--text"
                color="deep-purple accent-4"
                depressed
                @click="submitForm"
              >Submit</v-btn>
            </v-card-actions>
            <v-dialog
              v-model="dialog"
              absolute
              max-width="400"
              persistent
            >
              <v-card>
                <v-card-title class="headline grey lighten-3">Account Infomation</v-card-title>
                <v-card-text>
                  This is your account infomaion. This password will expire in 30 days, change it before expiration:
                </v-card-text>
                <v-card-text>
                  Username: {{reg_username}}
                  <br/>
                  Password: {{reg_password}}
                  <br/>
                  <a href="https://www.office.com/?auth=2" target="_blank">Click me to login</a>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    class="white--text"
                    color="deep-purple accent-4"
                    @click="dialog = false"
                  >
                    OK
                  </v-btn>

                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-card>
          <v-overlay opacity=0.6 color="black" :value="!invite_success && server_init_status">
            <v-card       
              class="mx-auto"
              color="white"
              light
              loading=true
              min-width=400
              shaped
            >
              <v-form>
                <v-col>
                  <v-col
                    ma-0 pa-0
                    no-gutters
                    class="CAPTCHAfield"
                    align='center'
                  >
                    <v-row
                      v-if="DEFAULT_HELLO_message"
                    >
                    <div v-html="DEFAULT_HELLO_message.replaceAll('\n', '<br>') +'<br><br>'"> 

                    </div>
                    </v-row>
                    <v-row
                      v-if="GETPWD_show_mail"
                    >
                      <v-text-field 
                        color="blue" 
                        :error-messages="GETPWD_errmsg" 
                        v-model="GETPWD_text" 
                        outlined 
                        label="Your Email"
                        @keyup.enter="SubmitGETPWD"
                      ></v-text-field>
                      <v-btn
                        :loading="GETPWD_loading"
                        :color="GETPWD_color"
                        height=55
                        dark
                        @click="SubmitGETPWD"
                      >
                        {{GETPWD_show_mail_btn_text}}
                        <v-icon v-if="GETPWD_show_mail_btn_icon" right >{{GETPWD_show_mail_btn_icon}}</v-icon>
                      </v-btn>
                    </v-row>
                    <v-row>
                      <v-text-field 
                        color="blue" 
                        :error-messages="invite_errmsg" 
                        v-model="password_in" 
                        outlined 
                        :label='GETPWD_show_mail?"Verification Code":"Invite Code"'
                        @keyup.enter="SubmitInviteCode"
                      ></v-text-field>
                      <v-btn
                        v-if="GETPWD_show_url"
                        color="blue"
                        height=55
                        dark
                        exact
                        :href="GETPWD_redirect_url"
                        target="_blank"
                      >
                        Get
                      </v-btn>
                    </v-row>
                  </v-col>
                  <v-row justify="center">
                    <v-btn
                      :loading="invite_loading"
                      color="error"
                      :disabled="invite_disabled"
                      @click="SubmitInviteCode"
                    >
                      Submit
                    </v-btn>
                  </v-row>
                </v-col>
              </v-form>
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


          <v-overlay opacity=0.6 color="black" :value="!server_init_status" >
            <v-card       
              class="mx-auto"
              light
              :color="server_init_pending ? undefined : 'red'"
              min-width=400
              shaped
              :loading="server_init_pending"
            >
              <v-col>
                <p color="green" class="headline mb-1">{{server_init_status_title}}</p>
                <v-card-text color="green" v-html="server_init_status_text"></v-card-text>
                <v-row justify="center">
                  <v-btn
                    color="error"
                    to="/admin"
                    v-if="!server_init_pending"
                  >
                    admin panel
                  </v-btn>
                </v-row>
              </v-col>

            </v-card>
          </v-overlay>

        </v-main>







        
      </v-col>
  </v-app>
</template>
<script>
  import axios from "axios";
  const axios_retry3 = axios.create();
  axiosRetry(axios_retry3, { retries: 3 , retryDelay: () => {  return 500;} });
  import axiosRetry from 'axios-retry';
  import debounce from 'lodash/debounce';
  export default {
    props: {
      source: String,
    },
    data: () => ({
      url_base : location.origin,
      cookie_prefix: "o365_ucg",
      CAPTCHA_response_name : "" ,
      CAPTCHA_frontend_head_html : "",
      CAPTCHA_frontend_login_html : "",
      GETPWD_show_mail : false,
      GETPWD_show_mail_btn_icon : null,
      GETPWD_show_mail_btn_text : "verify",
      GETPWD_show_url : false,
      GETPWD_redirect_url : "https://example.com",
      GETPWD_text : "",
      GETPWD_loading:false,
      GETPWD_errmsg:"",
      GETPWD_color : "blue",
      DEFAULT_HELLO_message : "",


      invite_success : false,
      invite_loading:false,
      invite_errmsg:"",
      error_msg_bool:false,
      error_msg_title:"Error",
      error_msg:"Error message here!",
      password_in:"anonymous",
      usageLocation:"TW",
      locatoinList:["AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT", "AU", "AW", "AX", "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS", "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM", "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG", "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS", "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO", "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI", "VN", "VU", "WF", "WS", "XK", "YE", "YT", "ZA", "ZM", "ZW"],
      agreement: false,
      dialog: false,
      form: false,
      appName : "Office 365 Account Registration Portal",
      
      username: "",
      username_checked :false,
      username_lock : false,
      username_lock_checking : false,
      username_errormsg : "",

      displayName: "",
      givenName : "",
      surname: "",

      reg_username : "",
      reg_password : "",
      checkBtn_text : "Check",
      checkBtn_icon : "mdi-magnify",
      checkBtn_color : "blue",
      checkBtn_loading:false,

      createBtn_text : "Pending",
      createBtn_color : "green",
      createBtn_loading:false,
      createBtn_disable_1:true,

      updateBtn_text : "Pending",
      updateBtn_color : "green",
      updateBtn_loading:false,
      updateBtn_disable_1:true,

      addLicenceBtn_text : "Pending",
      addLicenceBtn_color : "green",
      addLicenceBtn_loading:false,
      addLicenceBtn_disable_1:true,

      submited : false,

      server_init_pending : true,
      server_init_status : false,
      server_init_status_title : "Connecting to Server",
      server_init_status_text : "Checking server token status.<br/>Please wait....",

      domains:[
        "1.example.com",
        "2.example.com",
        "3.example.com",
        "4.example.com"
      ],
      selected_domain: undefined,
      licences:[
        { skuPartNumber: "A1" , skuId: "00121",skuFriendlyName:"L01"},
        { skuPartNumber: "A2" , skuId: "00122",skuFriendlyName:"L02"},
        { skuPartNumber: "A3" , skuId: "00123",skuFriendlyName:"L03"},
        { skuPartNumber: "A4" , skuId: "00124",skuFriendlyName:"L04"}
      ],
      selected_licence: undefined,

      rules: {
        length: len => v => (v || '').length >= len || `Required length:${len}`,
        username_rule: function(v){return (v || '').match(/^[a-zA-Z0-9]+$/) !== null ? true : 'Only letters and numbers'},
        required: v => !!v || 'This field is required',
        requiredStr: v => v.length !== 0 || 'This field is required',
      },
    }),
    computed: {
      api_path(){ return this.url_base + "/api/"},
      userPrincipalName(){return this.username + "@" + this.selected_domain},
      checkBtn_disable(){return this.checkBtn_loading || this.username.length == 0 || this.rules.username_rule(this.username)!==true || this.submited },
      createBtn_disable(){return this.createBtn_disable_1 || this.createBtn_loading || !this.submited},
      updateBtn_disable(){return this.updateBtn_disable_1 || this.updateBtn_loading || !this.submited},
      addLicenceBtn_disable(){return this.addLicenceBtn_disable_1 || this.addLicenceBtn_loading || !this.submited},
      accInfoBtn_disable(){return this.reg_username.length === 0},
      invite_disabled(){return this.password_in.length === 0}
    },
    mounted: function(){
      this.check_init();
    },
    methods: {
      SubmitGETPWD(){
        var self = this;
        if(self.GETPWD_show_mail_btn_icon !== null){
          return null;
        }
        if(this.CAPTCHA_response_name === "" || document.getElementsByName(this.CAPTCHA_response_name)[0].value.length > 0){
          console.log("do")
          this.GETPWD_loading=true;
          let CAPTCHA = document.getElementsByName(this.CAPTCHA_response_name).length > 0?document.getElementsByName(this.CAPTCHA_response_name)[0].value:"undefined";
          axios.post(this.api_path + "GetPWD",null,{params : {bkend:"g",email : this.GETPWD_text,"CAPTCHA":CAPTCHA}}).then(
            function(){
              self.GETPWD_color = "green";
              self.GETPWD_show_mail_btn_text = "Sent"
              self.GETPWD_show_mail_btn_icon = "mdi-checkbox-marked-circle-outline";
            })
          .catch(function (error){

            if (error.response) {
              if (error.response.data["error_description"] != undefined){
                self.GETPWD_errmsg=error.response.data["error"] + ": " + error.response.data["error_description"];
              }
              else{
                self.GETPWD_errmsg = error.response.data;
              }
            }
            else{
              console.log(error);
              self.GETPWD_errmsg = "Network Error."
            }


          })
          .finally(function(){
            self.GETPWD_loading=false;
          })
        }
        else{
          self.error_msg_bool = true;
          self.error_msg_title="Captcha Required";
          self.error_msg="Please verify that you are not a robot.";
        }
      },
      SubmitInviteCode(){
        var self = this;
        if(this.password_in.length === 0){
          return null;
        }


        if(this.CAPTCHA_response_name === "" || document.getElementsByName(this.CAPTCHA_response_name)[0].value.length > 0){
          this.invite_loading=true;
          let CAPTCHA = document.getElementsByName(this.CAPTCHA_response_name).length > 0?document.getElementsByName(this.CAPTCHA_response_name)[0].value:"undefined";
          axios.post(this.api_path + "guestlogin",null,{params : {password : this.password_in,"CAPTCHA":CAPTCHA}}).then(
            function(res){
              self.$setCookie( self.cookie_prefix + "session_id", res.data["session_id"]);
              self.invite_success=true;
              self.updatePage();
            })
          .catch(function (error){

            if (error.response) {
              if (error.response.data["error_description"] != undefined){
                self.invite_errmsg=error.response.data["error"] + ": " + error.response.data["error_description"];
              }
              else{
                self.invite_errmsg = error.response.data;
              }
            }
            else{
              console.log(error);
              self.invite_errmsg = "Network Error."
            }


          })
          .finally(function(){
            self.invite_loading=false;
          })
        }
        else{
          self.error_msg_bool = true;
          self.error_msg_title="Captcha Required";
          self.error_msg="Please verify that you are not a robot.";
        }
      },
      logoutGuest(){
        var self = this;
        axios.delete(self.api_path + "guestlogin",{params : {session_id : self.$getCookie(self.cookie_prefix + "session_id")}}).then(
          function(res){
            self.$setCookie(self.cookie_prefix + "session_id", res.data["session_id"]);
            window.location.reload();
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
          self.updatePage();
          //self.$delCookie(self.cookie_prefix + "session_id");
          //window.location.reload();
        })
      },
      check_init(){
        var self = this;
        axios.get(this.api_path + "testInit").then(
          function(res){
            document.title = res.data["appName"];
            self.appName = res.data["appName"];
            if(res.data["success"] == true){
              self.server_init_status = true;
              self.updatePage();
            }
            else{
              self.server_init_status = false;
              self.server_init_status_title="Server Token Not Set";
              self.server_init_status_text = "Please contact admin to setup server token.";
            }
          }
          
        ).catch(function(error){
          console.log(error);
          if (error.response.data["appName"] !== undefined) {
            document.title = error.response.data["appName"];
            self.appName = error.response.data["appName"];
            self.server_init_status = false;
            self.server_init_status_title=error.response.data["error"];
            self.server_init_status_text = error.response.data["error_description"].replace(/\n/g, "<br/>");
          }
          else{
            self.server_init_status = false;
            self.server_init_status_title="Connection Error";
            self.server_init_status_text = "Unable to connect to the server.";
          }
        }).finally(function(){
          
          self.server_init_pending = false;
        })
      },
      updateCAPTCHA(){
        // var self = this;
        // // console.log("UPdateC")
        // // console.log(document.getElementsByName(self.CAPTCHA_response_name))
        // // console.log(document.getElementsByClassName('CAPTCHAfield'))
        // if (self.CAPTCHA_response_name !== "" && document.getElementsByName(self.CAPTCHA_response_name).length === 0 && document.getElementsByClassName('CAPTCHAfield').length !== 0){
        //   document.getElementsByClassName('CAPTCHAfield')[0].appendChild( document.createRange().createContextualFragment( self.CAPTCHA_frontend_login_html ));
        // }
        // else{
        //   console.log("Not add due to" + " 1: " + (self.CAPTCHA_response_name === "") + " 2: " + (document.getElementsByName(self.CAPTCHA_response_name).length === 0) + " 3: " + (document.getElementsByClassName('CAPTCHAfield').length !== 0))
        // }
      },
      updatePage(){
        var self = this;
        if (self.CAPTCHA_response_name === ""){
          axios.get(this.api_path + "login",{params : {get_CAPTCHA : "g"}}).then(
            function(res){
              self.CAPTCHA_response_name = res.data["CAPTCHA_front_end_response_field"];
              self.CAPTCHA_frontend_head_html = res.data["CAPTCHA_frontend_head_html"];
              self.CAPTCHA_frontend_login_html = res.data["CAPTCHA_frontend_login_html"];
              self.GETPWD_show_mail = res.data["GETPWD_show_mail"];
              self.GETPWD_show_url = res.data["GETPWD_show_url"];
              self.GETPWD_redirect_url = res.data["GETPWD_redirect_url"];
              self.DEFAULT_HELLO_message = res.data["DEFAULT_HELLO_message"];
              if(self.GETPWD_show_mail){
                self.password_in = "";
              }
              document.getElementsByTagName('head')[0].appendChild( document.createRange().createContextualFragment( self.CAPTCHA_frontend_head_html ));
              document.getElementsByClassName('CAPTCHAfield')[0].appendChild( document.createRange().createContextualFragment( self.CAPTCHA_frontend_login_html ));
            }
            
          ).catch(function(error){
            console.log(error);
          })
        }

        axios.get(this.api_path + "getRegInfo",{params : {guest_session_id : this.$getCookie(self.cookie_prefix + "session_id")}}).then(
          function(res){
            self.invite_success=true;
            self.domains = res.data["availableDomains"]; 
            self.licences = res.data["availableLicences"]; 
            self.selected_domain = self.selected_domain || self.domains[0];
            self.selected_licence = self.selected_licence || self.licences[0]["skuId"];
            self.usageLocation = res.data["DEFAULT_usageLocation"];
            self.updatePage2();
          }
          
        ).catch(function(error){
          console.log(error);
          self.invite_success=false;
          self.updateCAPTCHA()
        })
      },
      updatePage2(){
        var self = this;
        axios.get(this.api_path + "guestlogin",{params : {session_id : this.$getCookie(self.cookie_prefix + "session_id")}}).then(
          function(res){
            if (res.data["userPrincipalName"] !== undefined){
              self.username = res.data["userPrincipalName"].split("@")[0];
              self.selected_domain = res.data["userPrincipalName"].split("@")[1];
              self.displayName = res.data["displayName"];
              self.submited = true;
              self.checkBtn_color = "green";
              self.checkBtn_icon = "mdi-check-outline";
              self.checkBtn_text = "OK";
              self.agreement = true;
              self.createBtn_disable_1=false;
              self.updateBtn_disable_1=false;
              self.addLicenceBtn_disable_1=false;


            }
            if (res.data["regResult"] !== undefined){
              self.reg_username = res.data["regResult"]["username"];
              self.reg_password = res.data["regResult"]["password"];
              self.createBtn_text = "Success";
              if(res.data["infomation"] !== undefined){
                self.givenName = res.data["infomation"]["givenName"];
                self.surname = res.data["infomation"]["surname"];
                self.usageLocation = res.data["infomation"]["usageLocation"];
                self.updateBtn_text = "Success";
              }
              else{
                self.updateBtn_text = "Retry";
                self.updateBtn_color = "red";
              }
              if(res.data["addLicensesID"] !== undefined){
                self.selected_licence = res.data["addLicensesID"];
                self.addLicenceBtn_text = "Success";
              }
              else{
                self.addLicenceBtn_text = "Retry";
                self.addLicenceBtn_color = "red";
              }
            }
          }
          
        ).catch(function(){
          self.invite_success=false;
        })
      },
      checkName(){
        if(this.username.length == 0 || this.rules.username_rule(this.username) != true){
          return;
        }
        var self = this;
        self.checkBtn_loading = true;
        self.username_lock_checking = true;
        axios.get(this.api_path + "canReg",{params : {guest_session_id : this.$getCookie(self.cookie_prefix + "session_id") , userPrincipalName : self.userPrincipalName }}).then(
          function(res){
            if(res.data["success"]===true){
              self.checkBtn_color = "green";
              self.checkBtn_icon = "mdi-check-outline"
              self.checkBtn_text = "OK"
              self.username_errormsg = "";
              self.username_checked = true;
            }
            else{
              self.checkBtn_color = "red";
              self.checkBtn_icon = "mdi-close-outline"
              self.checkBtn_text = "Error"
              self.username_errormsg = "Unknow Error";
              self.username_checked = false;
            }
          }
          
        ).catch(function(error){
          self.username_checked = false;
          if (error.response) {
            if(error.response.status === 409 || error.response.status === 404){
              //username conflict
              self.checkBtn_color = "red";
              self.checkBtn_icon = "mdi-close-outline"
              self.checkBtn_text = "Error"
              self.username_errormsg = error.response.data["error"];
              
            }
            else{
              //normal error hendle
              if (error.response.data["error_description"] != undefined){
                self.error_msg_title = error.response.data["error"];
                self.error_msg = error.response.data["error_description"].replace(/\n/g, "<br/>");
              }
              else{
                self.error_msg_title = "Error";
                self.error_msg = error.response.data;
              }
            }
          }
          else{
            self.error_msg_title = "Error";
            self.error_msg = error.toString();
            self.error_msg_bool = true;
          }
          console.log(error);
        }).finally(function(){
          self.checkBtn_loading = false;
          self.username_lock_checking = false;
        })
      },
      usernameChange(){
        this.username_checked = false;
        this.username_errormsg = "";
        this.delayCheckName();
      },
      delayCheckName: debounce(function(){this.checkName()},2400)
      ,
      FLnameChange(){
        if(this.givenName != "" && this.surname != "" ){
          this.displayName = this.givenName + " " + this.surname;
        }
      },
      createUser(){
      var self = this;
      self.createBtn_disable_1=false;
      this.createBtn_loading=true;
      let params = {guest_session_id : self.$getCookie(self.cookie_prefix + "session_id"),userPrincipalName:self.userPrincipalName,displayName : self.displayName} ;
      axios.post(this.api_path + "createUser",null,{params : params}).then(
        function(res){
          self.createBtn_text= "Success";
          self.createBtn_color = "green",
          self.reg_username = res.data["username"];
          self.reg_password = res.data["password"];
          self.updateUser(event,5,true);
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
        self.createBtn_text= "Retry";
        self.createBtn_color = "red",
        console.log(error);
      })
      .finally(function(){
        self.createBtn_loading=false;
        self.updateBtn_disable_1=false;
      })
      } ,
      updateUser(event,retry_left=0,retry_first=true){
        console.log("retry left:" + retry_left);
        if(retry_first===true){
          this.updateBtn_loading=true;
        }
        var self = this;
        let infomation = {givenName:self.givenName , surname:self.surname , usageLocation:self.usageLocation}
        let params = {guest_session_id : self.$getCookie(self.cookie_prefix + "session_id"),infomation: JSON.stringify(infomation)} ;
        
        axios_retry3.put(this.api_path + "updateUser",null,{params : params}).then(
          function(){
            self.updateBtn_text= "Success";
            self.updateBtn_color = "green";
            self.updateBtn_loading=false;
            self.addLicenceBtn_disable_1=false;
            self.addLicenceUser(event,5,true);
          })
        .catch(function (error){
          if(retry_left > 0){
            setTimeout(self.updateUser, 1000,event,retry_left-1,false);
            return;
          }
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
          self.updateBtn_text= "Retry";
          self.updateBtn_color = "red";
          self.updateBtn_loading=false;
          self.addLicenceBtn_disable_1=false;
          console.log(error);
        })
        .finally(function(){
        })
      },
      addLicenceUser(event,retry_left=0,retry_first=true){
        console.log("retry left:" + retry_left);
        if(retry_first === true){
          this.addLicenceBtn_loading=true;
        }
        var self = this;
        let params = {guest_session_id : self.$getCookie(self.cookie_prefix + "session_id"),addLicensesID: self.selected_licence} ;
        console.log(params);
        axios_retry3.post(this.api_path + "assignLicense",null,{params : params})
        .then(function(){
            self.addLicenceBtn_text= "Success";
            self.addLicenceBtn_color = "green";
            self.addLicenceBtn_loading=false;
            self.dialog=true
          })
        .catch(function (error){
          if(retry_left > 0){
            setTimeout(self.addLicenceUser, 1000,event,retry_left-1,false);
            return;
          }
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
          self.addLicenceBtn_text= "Retry";
          self.addLicenceBtn_color = "red",
          console.log(error);
          self.addLicenceBtn_loading=false;
        })
        .finally(function(){
        })
      },
      submitForm(){
        this.submited = true;
        this.createUser();
      },testFunc(){
        console.log(this.selected_licence);
      }
    }
  }
</script>