# coding=utf-8
import sendgrid
import os
from sendgrid.helpers.mail import *

import smtplib

FROMADDR = 'telenorbot@gmail.com'
USERNAME = 'telenorbot@gmail.com'
PASSWORD = 'telenorbot12345'
to = "filipdanic7@gmail.com"


def send_mail(msg):
    s = smtplib.SMTP('smtp.gmail.com')
    s.ehlo()
    s.starttls()
    s.login(FROMADDR, PASSWORD)
    s.sendmail(USERNAME, to, msg)
    s.quit()
