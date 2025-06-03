import requests
from bs4 import BeautifulSoup

# 论坛相关信息
base_url = 'http://10.2.91.91:40023'
login_url = f'{base_url}/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
post_url = f'{base_url}/forum.php?mod=post&action=newthread&fid=2&extra=&topicsubmit=yes'

# 登录信息
login_data = {
    'username': 'admin',
    'password': 'admin',
    'quickforward': 'yes',
    'handlekey': 'ls'
}

# 会话对象，用于保持登录状态
session = requests.Session()

# 登录操作
response = session.post(login_url, data=login_data)
if response.status_code == 200:
    print("登录成功")
else:
    print("登录失败")

# 获取发帖所需的 formhash
formhash_response = session.get(post_url)
soup = BeautifulSoup(formhash_response.text, 'html.parser')
formhash = soup.find('input', {'name': 'formhash'})['value']

# 发帖信息
post_data = {
    'formhash': formhash,
    'subject': '这是帖子标题',
    'message': '这是帖子内容',
    'topicsubmit': 'true'
}

# 发帖操作
post_response = session.post(post_url, data=post_data)
if post_response.status_code == 200:
    print("发帖成功")
else:
    print("发帖失败")
