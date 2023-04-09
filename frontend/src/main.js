import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import {Menu, Layout, Form, Input, Button, message, Switch, Card, DatePicker, Avatar} from 'ant-design-vue'

import 'ant-design-vue/dist/antd.css';

const  app = createApp(App);
app.config.productionTip = false;

app.use(router)
app.use(Button).use(Input).use(Form).use(DatePicker).use(Menu).use(Card).use(message).use(Layout).use(Switch).use(Avatar)
app.mount('#app')