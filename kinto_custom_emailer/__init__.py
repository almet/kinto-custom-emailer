from email.mime.text import MIMEText
from string import Template
import codecs
import smtplib

from kinto.core.listeners import ListenerBase
from pyramid.settings import aslist, asbool


class Listener(ListenerBase):
    def __init__(self, server, tls, username, password, sender, recipients,
                 template, subject_template, bucket, collection, email_field):
        self.server = server
        self.tls = tls
        self.username = username
        self.password = password
        self.sender = sender
        self.recipients = recipients
        self.bucket = bucket
        self.collection = collection
        self.email_field = email_field
        self.subject_template = Template(subject_template)
        with codecs.open(template, 'rb', encoding='utf-8') as f:
            self.template = Template(f.read())

    def __call__(self, event):
        if not (event.payload.get('bucket_id') == self.bucket and
                event.payload.get('collection_id') == self.collection):
            return

        record = event.impacted_records[0]['new']
        text = self.template.substitute(record)

        message = MIMEText(text)
        message['Subject'] = self.subject_template.substitute(record)
        message['From'] = self.sender
        message['To'] = record[self.email_field]
        message['Cc'] = ", ".join(self.recipients)

        server = smtplib.SMTP(self.server)
        if self.tls:
            server.starttls()
        if self.username and self.password:
            server.login(self.username, self.password)
        server.sendmail(self.sender, self.recipients, message.as_string())
        server.quit()


def load_from_config(config, prefix=''):
    settings = config.get_settings()

    return Listener(
        server=settings[prefix + 'server'],
        tls=asbool(settings[prefix + 'tls']),
        username=settings[prefix + 'username'],
        password=settings[prefix + 'password'],
        sender=settings[prefix + 'from'],
        recipients=aslist(settings[prefix + 'recipients']),
        template=settings[prefix + 'template'],
        bucket=settings[prefix + 'bucket'],
        collection=settings[prefix + 'collection'],
        email_field=settings[prefix + 'email_field'],
        subject_template=settings[prefix + 'subject_template']
    )
