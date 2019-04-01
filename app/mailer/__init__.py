import smtplib

EMAIL_ACCOUNT = 'carkodesign@gmail.com'
EMAIL_PASS = '48295620-j'
SENDER = 'carkodesign@gmail.com'
RECEIVER = 'carkodw@gmail.com'

def algo_notify(body):
    print('firewall test mail')
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(EMAIL_ACCOUNT,EMAIL_PASS)

    
    subject = "Algo notification"
    body = content;
    content  = f'Suject: {subject}\n\n{body}'
    mail.sendmail(EMAIL_ACCOUNT, RECEIVER, content)
    mail.close()