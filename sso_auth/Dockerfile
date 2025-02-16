FROM docker-0.unsee.tech/python:3

WORKDIR /app

COPY requirements.txt .

# 设置环境变量
ENV APP_SECRET_KEY='随意设置你的Flask密钥'
# 群晖 sso OIDC 的 well-known 配置地址 
ENV WELL_KNOWN_URL='修改为你的群晖 sso OIDC 的 well-known 配置地址'
# 群晖 sso OIDC 的 client_id 和 client_secret
ENV OIDC_CLIENT_ID='你的群晖 sso OIDC 的 client_id'
ENV OIDC_CLIENT_SECRET='你的群晖 sso OIDC 的 client_secret'
# 这是登录后的token存放的cookie名，可以根据自己的需求修改
ENV ACCESS_TOKEN_COOKIE_NAME='my_fava_access_token'
# 允许访问Fava的用户名
ENV ALLOWED_USERNAME='允许访问Fava的用户名'

# 克隆仓库并安装依赖
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt
