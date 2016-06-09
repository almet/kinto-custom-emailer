# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
from jinja2 import FileSystemLoader, Environment

import smtplib

from kinto.core.listeners import ListenerBase
from pyramid.settings import aslist, asbool


class Listener(ListenerBase):
    def __init__(self, server, tls, username, password, sender, recipients,
                 templates_folder, bucket, collection, email_field):
        self.server = server
        self.tls = tls
        self.username = username
        self.password = password
        self.sender = sender
        self.recipients = recipients
        self.bucket = bucket
        self.collection = collection
        self.email_field = email_field
        self.templates_folder = templates_folder

        simple_loader = FileSystemLoader(self.templates_folder)
        env = Environment(loader=simple_loader)
        self.template = env.get_template("newrecord")
        self.subject_template = env.get_template("subject")

    def __call__(self, event):
        if not (event.payload.get('bucket_id') == self.bucket and
                event.payload.get('collection_id') == self.collection):
            return

        record = {key.replace('-', '_'): value
                  for key, value in event.impacted_records[0]['new'].items()}
        text = self.template.render(record)

        to = record[self.email_field]
        message = MIMEText(text, 'plain', 'UTF-8')
        message['Subject'] = self.subject_template.render(record)
        message['From'] = self.sender
        message['To'] = to
        message['Cc'] = ", ".join(self.recipients)

        server = smtplib.SMTP(self.server)
        if self.tls:
            server.starttls()
        if self.username and self.password:
            server.login(self.username, self.password)
        server.sendmail(self.sender, self.recipients + [to, ],
                        message.as_string())
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
        templates_folder=settings[prefix + 'templates_folder'],
        bucket=settings[prefix + 'bucket'],
        collection=settings[prefix + 'collection'],
        email_field=settings[prefix + 'email_field'],
    )
