FROM docker-0.unsee.tech/python:3

WORKDIR /usr/src/app

# 安装必要的软件包，包括 cron 和 git
RUN apt-get update && apt-get install -y git git-crypt cron

# ENV http_proxy="http://127.0.0.1:xxxx"
# ENV https_proxy="http://127.0.0.1:xxxx"

# 克隆仓库并安装依赖
RUN --mount=type=secret,id=github_token \
    --mount=type=secret,id=git_crypt_key \
    export GITHUB_TOKEN=$(cat /run/secrets/github_token) && \
    git clone -b master https://${GITHUB_TOKEN}@github.com/yourname/your_bucket.git . && \
    pip install --no-cache-dir -r requirements.txt && \
    # 解密 git-crypt 加密的文件
    git-crypt unlock /run/secrets/git_crypt_key && \
    pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt

# 创建一个脚本用于执行 git pull
RUN echo "#!/bin/bash\n\
# 若有需要，可设置代理\n\   
# export http_proxy=\"http://127.0.0.1:xxxx\" \n\
# export https_proxy=\"http://127.0.0.1:xxxx\" \n\
cd /usr/src/app && \
echo 'git pull' && \
git pull" > /usr/src/app/git_pull.sh && \
    chmod +x /usr/src/app/git_pull.sh

# 设置 cron 任务，每间 6h 执行 git_pull.sh
RUN echo "0 */6 * * * root /usr/src/app/git_pull.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/git-pull-cron && \
    chmod 0644 /etc/cron.d/git-pull-cron && \
    touch /var/log/cron.log

# 暴露端口
EXPOSE 3241

# 启动 cron 服务并运行 fava
CMD cron && tail -f /var/log/cron.log & fava --prefix /fava --host 0.0.0.0 --port 3241 ./ledger/ledger-hbb/main.bean
