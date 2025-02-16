import os
from flask import Flask, redirect, request, session, url_for, make_response
from authlib.integrations.flask_client import OAuth
import requests
import time

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY', '')  # 设置一个安全的密钥

# 群晖 SSO Server 的 well-known URL
WELL_KNOWN_URL = os.getenv('WELL_KNOWN_URL', "")

# 配置 OIDC 客户端
oauth = OAuth(app)

# 获取 OIDC 配置
def fetch_oidc_config():
    try:
        response = requests.get(WELL_KNOWN_URL)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch OIDC configuration: {response.status_code}")
    except requests.RequestException as e:
        raise Exception(f"Error fetching OIDC configuration: {e}")
# 动态注册 OIDC 客户端
oidc_config = fetch_oidc_config()
oidc = oauth.register(
    name='oidc',
    client_id=os.getenv('OIDC_CLIENT_ID', ''),
    client_secret=os.getenv('OIDC_CLIENT_SECRET', ''), 
    authorize_url=oidc_config['authorization_endpoint'],
    access_token_url=oidc_config['token_endpoint'],
    userinfo_endpoint=oidc_config['userinfo_endpoint'],
    client_kwargs={'scope': 'openid profile email'},  # 根据需要调整 Scope
    jwks_uri=oidc_config['jwks_uri'],  # 用于验证 JWT 签名
    server_metadata_url=WELL_KNOWN_URL,  # 动态加载 OIDC 配置
)

@app.route('/auth')
def index():
    if request.cookies.get(os.getenv('ACCESS_TOKEN_COOKIE_NAME')):
      expires_at = session.get('expires_at')
      if expires_at and expires_at > time.time():
          return f'Hello, {session["user"]}!', 200
    return f'Redirecting to login', 403

@app.route('/login')
def login():
    redirect_uri = request.args.get('redirect_uri', '')
    return oidc.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    try:
        # 获取 Token 和用户信息
        token = oidc.authorize_access_token()
        userinfo = token['userinfo']
        if userinfo and userinfo['username'] == os.getenv('ALLOWED_USERNAME'):
            session['user'] = userinfo['email']
            session['expires_at'] = token['expires_at']
            response = make_response(redirect('/'))
            expires_at = token['expires_at']
            response.set_cookie(os.getenv('ACCESS_TOKEN_COOKIE_NAME'), token['access_token'], httponly=True, expires=expires_at)
            return response
        else:
            return "Access denied", 403
    except Exception as e:
        return f"Error during callback: {str(e)}", 401

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6810)
