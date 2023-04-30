import smtplib
from email.mime.text import MIMEText

from weibospider import settings


def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings.MAIL_FROM
    msg['To'] = ','.join(settings.MAIL_TO)
    s = smtplib.SMTP(settings.MAIL_HOST, settings.MAIL_PORT)
    if settings.MAIL_TLS:
        s.starttls()
    if settings.MAIL_USER and settings.MAIL_PASS:
        s.login(settings.MAIL_USER, settings.MAIL_PASS)
    s.sendmail(settings.MAIL_FROM, settings.MAIL_TO, msg.as_string())
    s.quit()


# subject = f"您的名称为的任务完成，任务号为!"
# body = f"数据收集任务完成，请前往您的任务中心进行下异步操作。  运行状态:"
# send_email(subject, body)
