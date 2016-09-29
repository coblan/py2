# -*- encoding:utf8 -*-

# 设置邮箱服务器 ---在settings.py中引入
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = 'coblan@163.com'
EMAIL_PORT = 25
EMAIL_HOST_PASSWORD = 'he123811'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ALLOWED_HOSTS=['127.0.0.1']
EMAIL_USE_TLS=True
SERVER_EMAIL='coblan@163.com'

# 设置邮箱管理员，可以接收到500错误。-----在settings.py中引入
ADMINS=[('HEYULIN','he_yulin@163.com'),]
DEBUG = False

#发送邮件用：
# send_mail('hello','i m heyulin','coblan@163.com',['he_yulin@163.com'])