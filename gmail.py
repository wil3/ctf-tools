#!/usr/bin/env python

"""Send an email with your Gmail account
"""

import smtplib

__author__ = "William Koch"

class SendGmail:
    SMTP_ENDPOINT ='smtp.gmail.com:587' 

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def send(self, to_addrs, subject, body):
        """Send email to the recepients specified by to_addrs

        to_addrs: array of email address
        subject: email subject
        body: email body

        """
        from_addr = self._make_email()

        message = self._make_message(", ".join(to_addrs), from_addr, subject, body)
        server = smtplib.SMTP(SendGmail.SMTP_ENDPOINT)
        server.ehlo()
        server.starttls()
        server.login(self.__username, self.__password)
        #from address is ignored...
        server.sendmail(from_addr, to_addrs, message)
        server.quit()
    
    def _make_email(self):
        return "%s@gmail.com"%(self.__username)

    def _make_message(self, to_addr, from_addr, subject, body):
        return '\r\n'.join([
            "From: " + from_addr,
            "To: " + to_addr, 
            "Subject: " + subject,
            "",
            body
            ])  



