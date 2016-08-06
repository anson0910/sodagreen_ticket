from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.header         import Header
import smtplib

def generate_email(gmail_user, subject, body, to_list):
    msg = MIMEMultipart('related')
    msg['Subject'] = Header(u'{}'.format(subject), 'utf-8')
    msg['From'] = gmail_user
    msg['To'] = ','.join(to_list)
    msg_alternative = MIMEMultipart('alternative')
    msg_text = MIMEText(u'Image not working - maybe next time', 'plain', 'utf-8')
    msg_alternative.attach(msg_text)
    msg.attach(msg_alternative)
    msg_html = u'<h3>{}</h3>'.format(body)
    msg_html = MIMEText(msg_html, 'html', 'utf-8')
    msg_alternative.attach(msg_html)    
    return msg

def send_email(msg, gmail_user, gmail_pwd, to_list):
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to_list, msg.as_string())
    mailServer.quit()

def notify_email(date):
    gmail_user = "xxxxxx@gmail.com"
    gmail_pwd = "xxxxx"
    subject = date + " tickets!"
    body = "tickets!"

    email_msg = generate_email(gmail_user, subject, body, [gmail_user])
    send_email(email_msg, gmail_user, gmail_pwd, [gmail_user])


if __name__ == '__main__':
    notify_email("Testing")
