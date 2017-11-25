import smtplib
from email.mime.text import MIMEText
from string import Template

FROMADDR = 'telenorbot@gmail.com'
USERNAME = 'telenorbot@gmail.com'
PASSWORD = 'telenorbot12345'
to = "andrej.karadzic@gmail.com"


def send_mail(img, description, call_to_action):
    msg_content = open("email-inlined.html", "r").read()
    s = Template(msg_content).safe_substitute(description=description, call_to_action=call_to_action, img=img)
    message = MIMEText(s, 'html')
    message["subject"] = "Hey, we have a great new event for you!"

    msg_full = message.as_string()

    s = smtplib.SMTP('smtp.gmail.com')
    s.ehlo()
    s.starttls()
    s.login(FROMADDR, PASSWORD)
    s.sendmail(USERNAME, to, msg_full)
    s.quit()
