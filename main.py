# -*- coding: utf-8 -*-
import os
import time
import random
import logging
import platform
import requests
import html
import io
from datetime import datetime
from configparser import ConfigParser
from tabulate import tabulate
from playwright.sync_api import sync_playwright, TimeoutError

# 创建一个 StringIO 对象用于捕获日志
log_stream = io.StringIO()

# 创建日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建控制台输出的处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建 log_stream 处理器
stream_handler = logging.StreamHandler(log_stream)
stream_handler.setLevel(logging.INFO)

# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 为处理器设置格式化器
console_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# 将处理器添加到日志记录器中
logger.addHandler(console_handler)
logger.addHandler(stream_handler)

# 自动判断运行环境
IS_GITHUB_ACTIONS = 'GITHUB_ACTIONS' in os.environ
IS_SERVER = platform.system() == "Linux" and not IS_GITHUB_ACTIONS

# 从配置文件读取配置信息（如果需要）
def load_config():
    config = ConfigParser()
    if IS_SERVER:
        config_file = './config/config.ini'
    elif IS_GITHUB_ACTIONS:
        config_file = None
    else:
        config_file = 'config/config.ini'
    
    if config_file and os.path.exists(config_file):
        config.read(config_file)
    return config

config = load_config()

LIKE_PROBABILITY = float(config.get('settings', 'like_probability', fallback='0.02'))
REPLY_PROBABILITY = float(config.get('settings', 'reply_probability', fallback='0'))
COLLECT_PROBABILITY = float(config.get('settings', 'collect_probability', fallback='0.02'))
HOME_URL = config.get('urls', 'home_url', fallback="https://linux.do/")
CONNECT_URL = config.get('urls', 'connect_url', fallback="https://connect.linux.do/")
USE_WXPUSHER = config.get('wxpusher', 'use_wxpusher', fallback='false').lower() == 'true'
APP_TOKEN = config.get('wxpusher', 'app_token', fallback=None)
TOPIC_ID = config.get('wxpusher', 'topic_id', fallback=None)
MAX_TOPICS = int(config.get('settings', 'max_topics', fallback='10'))

class LinuxDoBrowser:
    def __init__(self) -> None:
        logging.info("启动 Playwright...")
        self.pw = sync_playwright().start()
        logging.info("以无头模式启动 Firefox...")
        self.browser = self.pw.firefox.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        logging.info(f"导航到 {HOME_URL}...")
        self.page.goto(HOME_URL)
        logging.info("初始化完成。")

    def run_for_accounts(self, accounts):
        for username, password in accounts:
            global USERNAME, PASSWORD  # 使用全局变量更新用户名和密码
            USERNAME, PASSWORD = username, password
            
            logging.info(f"正在处理账号: {USERNAME}")
            if not self.login():
                logging.error(f"账号 {USERNAME} 登录失败，跳过该账号。")
                continue
            
            self.click_topic()  # 执行主题处理等操作
            
            # 登出以准备下一个账号（需要实现 logout 方法）
            self.logout()

    def login(self) -> bool:
        try:
            logging.info("尝试登录...")
            self.page.click(".login-button .d-button-label")
            time.sleep(2)
            self.page.fill("#login-account-name", USERNAME)
            time.sleep(2)
            self.page.fill("#login-account-password", PASSWORD)
            time.sleep(2)
            self.page.click("#login-button")
            time.sleep(10)  # 等待页面加载完成...
            
            user_ele = self.page.query_selector("#current-user")
            if not user_ele:
                logging.error("登录失败，请检查账号密码及是否关闭二次认证")
                return False
            
            logging.info("登录成功")
            return True
        
        except TimeoutError:
            logging.error("登录失败：页面加载超时或元素未找到")
            return False

    def logout(self):
        try:
            logging.info(f"导航到 {HOME_URL}...")
            self.page.goto(HOME_URL)
            time.sleep(2)
            
            # 点击用户菜单按钮以显示下拉菜单
            logging.info("尝试找到并点击用户菜单按钮...")
            user_menu_button = self.page.locator("#current-user .icon").first
            
            if user_menu_button:
                user_menu_button.click()
                logging.info("成功点击用户菜单按钮")

                # 点击“退出”按钮（需要根据实际情况调整选择器）
                logout_button = self.page.locator(".logout .btn").first
                
                if logout_button:
                    logout_button.click()
                    logging.info("成功点击退出按钮")
                else:
                    logging.warning("未找到退出按钮")
                    
        except Exception as e:
            logging.error(f"登出操作失败: {e}")

if __name__ == "__main__":
    accounts = []
    
    while True:
        username = input("请输入用户名（或输入'结束'以停止）：")
        if username.lower() == '结束':
            break
        
        password = input("请输入密码：")
        
        accounts.append((username, password))
    
    ldb = LinuxDoBrowser()
    ldb.run_for_accounts(accounts)
