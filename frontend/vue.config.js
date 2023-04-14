const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    devServer: {
        host: '0.0.0.0',
        port: 80,     // 端口号
    },
    transpileDependencies: [
        'vue-echarts',
        'resize-detector'
    ]
})
