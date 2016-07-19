import smtplib
from email.mime.text import MIMEText
from multiprocessing import Process


def send(sender, recipient, user_name, user_passwd, message_title, text):
    server = 'smtp.gmail.com'
    port = '25'

    msg = MIMEText(text, '', 'utf-8')
    msg['Subject'] = message_title
    msg['From'] = sender
    msg['To'] = recipient

    s = smtplib.SMTP(server, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(user_name, user_passwd)
    s.sendmail(sender, recipient,msg.as_string())
    s.quit()
    print 'mail to {0} send'.format(recipient)


def send_async(sender, recipient, user_name, user_passwd, message_title, text):
    proc = Process(target=send,
                   args=(sender, recipient, user_name, user_passwd, message_title, text))
    proc.start()


def main():
    send(sender='BoikoAndrei1996@gmail.com',
         recipient='boikoandrei1996@mail.ru',
         user_name='BoikoAndrei1996@gmail.com',
         user_passwd='17131519bsuir',
         message_title='test_send_mail',
         text='Hello from Case.by')


if __name__ == '__main__':
    main()