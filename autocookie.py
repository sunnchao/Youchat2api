import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time

# 获取当前工作目录的路径
current_dir = os.getcwd()

# 设置Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 打开目标网站的登录页面
driver.get("https://you.com")

# 检查precookie.json文件是否存在且不为空
precookie_path = os.path.join(current_dir, 'precookie.json')
if os.path.exists(precookie_path) and os.path.getsize(precookie_path) > 0:
    with open(precookie_path, 'r') as file:
        try:
            cookies = json.load(file)
            # 如果文件不为空，仅添加特定Cookie到浏览器
            for cookie in cookies:
                if cookie['name'] in ['stytch_session', 'stytch_session_jwt']:  # 检查cookie名称
                    if 'expiry' in cookie:
                        cookie['expiry'] = int(cookie['expirationDate'])
                    cookie.pop('expirationDate', None)  # 删除不需要的字段
                    cookie.pop('http_only', None)  # 删除不需要的字段
                    cookie.pop('session', None)  # 删除不需要的字段
                    # 确保sameSite属性合法
                    if 'sameSite' not in cookie or cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                        cookie['sameSite'] = "None"  # 设置默认值
                    driver.add_cookie(cookie)
            # 再次加载网页以应用Cookie
            driver.get("https://you.com")
        except json.JSONDecodeError:
            print("JSON data in 'precookie.json' is invalid. Please log in manually.")
else:
    print("No cookies found. Please log in manually.")

# 等待页面加载
time.sleep(1)  # 等待足够时间让JS渲染页面

# 从页面提取__NEXT_DATA__脚本内容
script_element = driver.find_element(By.ID, '__NEXT_DATA__')
script_text = script_element.get_attribute('innerHTML')
data = json.loads(script_text)
buildId = data.get('buildId', '')

# 提取当前浏览器中的所有cookie
current_cookies = driver.get_cookies()

# 将cookie处理为{name: value}的格式
simple_cookies = {cookie['name']: cookie['value'] for cookie in current_cookies}
simple_cookies['buildId'] = buildId

# 完成后关闭浏览器
driver.quit()

# 将包括buildId的cookie数据写入cookie.json文件
auto_cookie_path = os.path.join(current_dir, 'cookie.json')
with open(auto_cookie_path, 'w') as f:
    json.dump([simple_cookies], f, indent=4)  # 将simple_cookies包装在列表中

print("Updated auto_cookie.json with buildId and cookies.")