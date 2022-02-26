

import traceback
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ff_utils.tools.logger import LogHelper
from si_utils.config import base_config as con

logger = LogHelper().logger


def send_email(mail_to, subject, text):
    email_from = "3351206873@qq.com"
    email_to = mail_to #接收邮箱 
    hostname = "smtp.qq.com" #不变，QQ邮箱的smtp服务器地址 
    login = "3351206873@qq.com" #发送邮箱的用户名 
    password = "jxelxnrfzkvjcibg" #发送邮箱的密码，即开启smtp服务得到的授权码。注：不是QQ密码。 
    subject = subject #邮件主题 
    text = text #邮件正文内容 
    smtp = smtplib.SMTP_SSL(hostname)#SMTP_SSL默认使用465端口 
    smtp.login(login, password) 
    msg = MIMEText(text, "plain", "utf-8") 
    msg["Subject"] = Header(subject, "utf-8") 
    msg["from"] = email_from 
    msg["to"] = email_to 
    smtp.sendmail(email_from, email_to, msg.as_string()) 
    smtp.quit()

def init_mime_email(subject, receiver_list, mime_email_params=con.mime_email_params):
    receivers = ', '.join(receiver_list)
    message =  MIMEMultipart('related')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = mime_email_params['mail_sender']
    message['To'] = receivers
    return message

def send_mime_email(receiver_list, message, mime_email_params=con.mime_email_params):
    try:
        server=smtplib.SMTP_SSL(mime_email_params['smtp_server'], mime_email_params['smtp_port'])
        server.login(mime_email_params['mail_sender'], mime_email_params['password'])
        server.sendmail(mime_email_params['mail_sender'], receiver_list, message.as_string())
        server.quit()
        logger.info("邮件发送成功")
    except Exception as ex:
        logger.error(traceback.format_exc())


