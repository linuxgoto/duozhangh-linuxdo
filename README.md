如果您希望这些环境变量在每次登录时都可用，可以将它们添加到您的 ~/.bashrc 或 ~/.bash_profile 文件中：
```
echo 'export LINUXDO_USERNAME1="username1"' >> ~/.bashrc
echo 'export LINUXDO_PASSWORD1="password1"' >> ~/.bashrc
echo 'export LINUXDO_USERNAME2="username2"' >> ~/.bashrc
echo 'export LINUXDO_PASSWORD2="password2"' >> ~/.bashrc
# 继续添加更多账号...
```
```
source ~/.bashrc  # 使更改生效
```
配置文件 config.ini
确保您的配置文件（config/config.ini）中包含其他必要的变量，例如：
```
[settings]
like_probability=0.02
reply_probability=0.0
collect_probability=0.02
max_topics=10

[urls]
home_url=https://linux.do/
connect_url=https://connect.linux.do/

[wxpusher]
use_wxpusher=false
app_token=
topic_id=
```
