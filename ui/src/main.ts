import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from 'axios'
import VueAxios from 'vue-axios'

import "./assets/main.css";

const app = createApp(App);

app.use(VueAxios, axios)
app.provide('axios', app.config.globalProperties.axios)
app.use(router);

app.mount("#app");
