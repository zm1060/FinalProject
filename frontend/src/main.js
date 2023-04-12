import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import echarts from 'echarts';

// import {Menu, Layout, Form, Input, Button, message, Switch, Card, DatePicker, Avatar, Tooltip, Row, Col} from 'ant-design-vue'
import antd from 'ant-design-vue'

import 'ant-design-vue/dist/antd.css';

const  app = createApp(App);
app.config.productionTip = false;

app.use(router)
app.use(echarts)
app.use(antd)
// app.use(Button).use(Input).use(Form).use(DatePicker).use(Menu)
// app.use(Card).use(message).use(Layout).use(Switch).use(Avatar).use(Tooltip).use(Row).use(Col)
app.mount('#app')