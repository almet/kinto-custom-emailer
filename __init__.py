import smtplib
from email.mime.text import MIMEText

from kinto.core.listeners import ListenerBase
from pyramid.settings import aslist, asbool

class Listener(ListenerBase):
    def __init__(self, server, tls, username, password, sender, recipients):
        self.server = server
        self.tls = tls
        self.username = username
        self.password = password
        self.sender = sender
        self.recipients = recipients

    def __call__(self, event):
        subject = "%s %sd" % (event.payload['resource_name'],
                              event.payload['action'])
        
        text = "User id: %s" % event.request.prefixed_userid

        message = MIMEText(text)
        message['Subject'] = subject
        message['From'] = self.sender
        message['To'] = ", ".join(self.recipients)

        server = smtplib.SMTP(self.server)
        if self.tls:
            server.starttls()
        if self.username and self.password:
            server.login(self.username, self.password)
        server.sendmail(self.sender, self.recipients, message.as_string())
        server.quit()

def load_from_config(config, prefix=''):
    settings = config.get_settings()

    server = settings[prefix + 'server']
    tls = asbool(settings[prefix + 'tls'])
    username = settings[prefix + 'username']
    password = settings[prefix + 'password']
    sender = settings[prefix + 'from']
    recipients = aslist(settings[prefix + 'recipients'])

    return Listener(server, tls, username, password, sender, recipients)
