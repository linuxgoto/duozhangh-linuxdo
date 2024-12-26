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
要将多个账号和密码添加到 ~/.bashrc 或 ~/.bash_profile 文件中，您可以按照以下步骤进行操作。这里将详细说明如何设置多个环境变量，以便在您的项目中使用。
步骤 1: 编辑 ~/.bashrc 或 ~/.bash_profile
打开终端。
使用文本编辑器（如 nano 或 vim）打开 ~/.bashrc 或 ~/.bash_profile 文件。例如，使用 nano 打开 ~/.bashrc：
```
nano ~/.bashrc

```
添加环境变量：在文件的末尾添加您的账号和密码。为了支持多个账号，您可以使用不同的变量名
```
export LINUXDO_USERNAME1="username1"
export LINUXDO_PASSWORD1="password1"
export LINUXDO_USERNAME2="username2"
export LINUXDO_PASSWORD2="password2"
export LINUXDO_USERNAME3="username3"
export LINUXDO_PASSWORD3="password3"
# 继续添加更多账号...

```
保存并退出：如果您使用的是 nano，可以按 CTRL + X，然后按 Y 确认保存，最后按 Enter 退出。
使更改生效：运行以下命令使更改立即生效：
```
source ~/.bashrc
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
