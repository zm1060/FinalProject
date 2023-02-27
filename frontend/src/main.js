import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import {Button, Input, Form, FormItem,} from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';

const  app = createApp(App);
app.config.productionTip = false;

app.use(router)
app.use(Button).use(Input).use(Form).use(FormItem)

app.mount('#app')