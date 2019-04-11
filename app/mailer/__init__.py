import smtplib

EMAIL_ACCOUNT = 'carkodesign@gmail.com'
EMAIL_PASS = '48295620-j'
SENDER = 'carkodesign@gmail.com'
RECEIVER = 'carkodw@gmail.com'

def algo_notify(body):
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(EMAIL_ACCOUNT,EMAIL_PASS)

    
    subject = "Algo notification"
    content = body
    content  = f'Suject: {subject}\n\n{body}'
    print('sending mail...')
    mail.sendmail(EMAIL_ACCOUNT, RECEIVER, content)
    mail.close()