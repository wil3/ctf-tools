import requests
from guerrillamail import GuerrillaMailSession

class CreateTwitterAccount:

    def __init__(self):

        self.mail_session = GuerrillaMailSession()
        email = self.mail_session.get_session_state()['email_address']
    
    
    def check_inbox(self, subject_regex):
        for email in self.mail_session.get_email_list():
            print email.subject

    def register(self):
        register_url='https://twitter.com/account/create'
        fullname=''
        email=''
        password=''
        username=''
        payload = {'user[name]': fullname, 'user[email]': email, 'user[user_password]':password, 'user[screen_name]':username}
        r = requests.post(register_url, data=payload, header=header)






if __name__ == "__main__":
    twitter = CreateTwitterAccount()
    twitter.check_inbox("")
