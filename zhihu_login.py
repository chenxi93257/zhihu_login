import requests
import time, json, base64
import http.cookiejar as cookielib
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0','HOST':'www.zhihu.com',\
           'Referer':'https://www.zhihu.com/signin?next=%2F','Authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}
url="https://www.zhihu.com/api/v3/oauth/sign_in"

session = requests.Session()
session.cookies = cookielib.LWPCookieJar(filename = 'cookies_res.txt')
    
def zhihu_login(account,password,captcha):
    is_captcha = parse_captcha()
    if is_captcha:
        print("你有验证码")
        is_captcha = parse_captcha()
    else:
        print('没有验证码，我登录')  
 

def zhihu_login1(account,password,captcha):
    post_data={
        'client_id':'c3cef7c66a1843f8b3a9e6a1e3160e20',
        'grant_type':'password',
        'timestamp':'1522175470706',
        'source':'com.zhihu.web',
        'signature':'606ac347840877b5359cdfa463d2f2bddaa7de1c',
        'username':"+86"+account,
        'password':password,
        'captcha':captcha,
        'lang':'en',
        'ref_source':'homepage',
        'utm_source':''
    }
    response = session.post(url,data=post_data,headers=headers,verify=False)
    print(response.cookies)
    session.cookies.save(ignore_expires=True,ignore_discard=True)

        
def parse_captcha():
    response = session.get(
        'https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
        headers=headers, verify=False
        )
    show_captcha = response.json()['show_captcha']
#     print(show_captcha)
    if show_captcha:
        print('有验证码')
        response = session.put(
            'https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
            headers=headers, verify=False
        )
#         print(json.loads(response.content),'1')
        try:
            img = json.loads(response.content)['img_base64']
        except Exception as e:
            print('获取img_base64的值失败，原因:'% e)
        else:
            print('成功获取验证码地址')
            img = img.encode('utf-8')
            img_data = base64.b64decode(img)
            with open('zhihu_captcha.png', 'wb') as f:
                f.write(img_data)            
        captcha = input('请输入识别的验证码：')
        data = {'input_text':captcha}
        response = session.get(
                'https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                data=data, headers=headers, verify=False
            )
        try:
            verify_res = json.loads(response.content)['success']
        except Exception as e:
            print ('关于验证码的post请求响应失败，原因：{}'.format(e))
        else:
            if verify_res:
                zhihu_login('','',captcha=captcha)
            else:
                print ('是错误的验证码')
        return True
    else:
        print("没有验证码")
        zhihu_login1('','',captcha='')
        get_index_page()

def is_login():
    # 判断是否登陆
    inbox_url = 'https://www.zhihu.com/inbox'
    response = session.get(inbox_url, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True
        
        
def get_index_page():
    response = session.get('https://www.zhihu.com',headers=headers,verify = False)
    print(response.cookies,'5555')
    with open('index.html','wb') as f:
        f.write(response.content)
    print ('获取信息成功')

zhihu_login('','',captcha='')