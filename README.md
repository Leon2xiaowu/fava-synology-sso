# 使用群晖SSO为Fava服务添加鉴权

该仓库为使用群晖SSO服务器为本地Fava服务增加鉴权的模板，详情查看[使用说明](https://blog.hbbs.fun/2025/02/16/fava-to-nas-sso/)。

## Fava Dockerfile 配置项

`./Dockerfile` 是fava的容器配置文件，你需要修改`https://${GITHUB_TOKEN}@github.com/yourname/your_bucket.git` 为你自己的`github`仓库地址。


如果遇到拉取速度不理想的情况，可以修改`http_proxy`代理地址。

这一环节有不清楚的可以查看：[在群晖 NAS 上部署 Fava](https://blog.hbbs.fun/2025/02/04/favaToNas)

## SSO Dockerfile 配置项

`sso_auth/Dockerfile` 是SSO鉴权服务的配置

需要修改以下配置

- APP_SECRET_KEY='随意设置你的Flask密钥'
- WELL_KNOWN_URL='修改为你的群晖 sso OIDC 的 well-known 配置地址'
- OIDC_CLIENT_ID='你的群晖 sso OIDC 的 client_id'
- OIDC_CLIENT_SECRET='你的群晖 sso OIDC 的 client_secret'
- ACCESS_TOKEN_COOKIE_NAME='my_fava_access_token'
  
  这是登录后的token存放的cookie名，可以根据自己的需求修改

- ENV ALLOWED_USERNAME='允许访问Fava的用户名'

## SSO_Gateway 配置

`docker-compose.yml` 中配置sso_gateway服务通过暴露8111端口对外提供服务，可自行调整。

使用中遇到问题请提交issue，看到会回复。
