// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import VueRouter from 'vue-router'
Vue.config.productionTip = false
import login from './components/Login.vue'
/* eslint-disable no-new */
Vue.use(VueRouter)

const routes = [
  { path: '/login/', component: login, name: 'login' }

]
const router = new VueRouter({
  routes
})

new Vue({
  router,
  el: '#app',
  components: { App },
  render: h => h(App)
})
