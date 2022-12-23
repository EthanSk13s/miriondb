import { createApp } from "vue";
import VueLazyLoad from 'vue3-lazyload'
import axios from 'axios'
import VueAxios from 'vue-axios'

import App from "./App.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(App);

app.use(VueAxios, axios)
app.use(VueLazyLoad);
app.provide('axios', app.config.globalProperties.axios)
app.use(router);

app.mount("#app");
