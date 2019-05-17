# coding=utf-8
'''
  Created by lyy on 2019-04-04
'''
import smtplib


def send_email():
    sender = 'from@fromdomain.com'
    receivers = ['to@todomain.com']

    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test

    This is a test e-mail message.
    """

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)
        print
        "Successfully sent email"
    except Exception:
        print
        "Error: unable to send email"


if __name__ == '__main__':
    send_email()
