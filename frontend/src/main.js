import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// import {Menu, Layout, Form, Input, Button, message, Switch, Card, DatePicker, Avatar, Tooltip, Row, Col} from 'ant-design-vue'
import antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css';

import ECharts from "vue-echarts";
import "echarts/lib/chart/bar";
import "echarts/lib/component/tooltip";
import "echarts/lib/component/title";
import "echarts/lib/component/legend";
import 'zrender/lib/canvas/canvas';

const  app = createApp(App);
app.config.productionTip = false;
app.component('v-chart', ECharts)

app.use(router)
app.use(ECharts)
app.use(antd)

// app.use(Button).use(Input).use(Form).use(DatePicker).use(Menu)
// app.use(Card).use(message).use(Layout).use(Switch).use(Avatar).use(Tooltip).use(Row).use(Col)
app.mount('#app')