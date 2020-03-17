import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import axios from 'axios'
Vue.prototype.$ajax = axios
window._ = require('lodash');
//Vue.prototype.$urlBase = location.origin
Vue.prototype.$urlBase = location.protocol + "//" + location.hostname + ":10000"
Vue.prototype.$setCookie = function(name, value, expireDays){
                              let exdate = new Date();
                              exdate.setDate(exdate.getDate() + expireDays);
                              document.cookie = `${name}=${escape(value)}; expires=${ !expireDays ? '' : exdate.toGMTString()};`;
                            };
Vue.prototype.$getCookie = function(name){
                              var reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)'),
                                arr = document.cookie.match(reg);
                              return arr ? arr[2] : null;
                            };
Vue.prototype.$delCookie = function(name){
                              let exp = new Date();
                              exp.setTime(exp.getTime() - 1);
                              const value = Vue.prototype.$getCookie(name);
                              if (value != null)
                                document.cookie = `${name}=${value}; expires=${exp.toGMTString()}`;
                            };
Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
