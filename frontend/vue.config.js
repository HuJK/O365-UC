module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  chainWebpack: config => {
    config.module.rule('images').use('url-loader')
        .loader('url-loader')
        .tap(options => {
          options.limit = 1
          options.fallback = {loader:"file-loader","options":{name: 'img/[name].[hash:8].[ext]'}};
          return options
        })
  },
  "configureWebpack": {
    module: {
          rules: [
            {
              test: /\.(png|jpe?g|gif|ico)$/i,
              use: [
                {
                  loader: 'url-loader',
                  options: {
                    limit: 1,
                    name: 'files/[name].[ext]'
                  }
                },
              ],
            }
          ]
        }
      }
}