import requests
import datetime
import time
import argparse
import logging
import logging.handlers
import getpass
from gmail import SendGmail



class CloudCheck:
    GOOGLE_SEARCH_URL = "https://www.google.com/search?q="
    NOMATCH = 'did not match any documents'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0',
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language':'en-US,en;q=0.5'
               }
    SECONDS_IN_DAY = 60 * 60 * 24
    SLEEPY_TIME = 60 * 60 * 24 #seconds
    LOG_FILENAME='cloudcheck.log'

    def __init__(self, target_file, mailto, from_email, from_password):
        self.target_file = target_file
        self.mailto = mailto 
        self.from_email = from_email
        self.from_password = from_password
        self.logger = logging.getLogger('cloudcheck')
        self.logger.setLevel(logging.INFO)
        h = logging.handlers.RotatingFileHandler(CloudCheck.LOG_FILENAME, maxBytes=20, backupCount=5)
        self.logger.addHandler(h)

    def run(self):
        while True:
            self.check_targets()
            time.sleep(CloudCheck.SLEEPY_TIME)

    def check_targets(self):
        found_targets = []
        targets = self.read_targets()
        for (epoch,key) in targets:
            if self.found(key):
                dt = self.epoch_to_string(self.compute_lapse(epoch))
                found_targets.append((dt, key))
        if found_targets:        
            self.notify(found_targets)
    
    def compute_lapse(self, start):
        """
        How long has passed since the key was added?
    
        return seconds
        """

        return time.time() - start

    def epoch_to_string(self, epoch):
        s = datetime.timedelta(seconds=epoch)
        d = datetime.datetime(1,1,1) + s
        return '%d days %d h %d m' % (d.day-1, d.hour, d.minute)

    def read_targets(self):
        """
        Read the targets from the file

        return pair (epoch,url)
        """

        targets = []
        f = None
        try:
            f = open(self.target_file, 'r')
            for line in f:
                (epoch,key) = line.strip().split(',')
                epoch = int(epoch)
                key = key.strip()
                targets.append((epoch,key))
        except Exception as e:
            print str(e)
        finally:
            if f:
                f.close()

        return targets
    
    def make_url(self,key):
        return CloudCheck.GOOGLE_SEARCH_URL + key
        
    def found(self, key):
        url = self.make_url(key)
        r = requests.get(url, headers=CloudCheck.HEADERS)
        return -1 == r.text.find(CloudCheck.NOMATCH)
    
    def create_message_body(self,targets):
        body = []
        for (dt, key) in targets:
            
            msg = 'Discovered after %s %s %s' % (dt, key, self.make_url(key))
            body.append(msg)
        return '\n'.join(body)

    def notify(self, targets):
        try:
            self.logger.info(str(targets))
            gmail = SendGmail(self.from_email, self.from_password)
            subject = 'CloudCheck: Found %d targets' % len(targets)
            body = self.create_message_body(targets)
            self.logger.info("subject " + subject + " body " + body)        
            gmail.send([self.mailto], subject, body) 
        except Exception as e:
            print "Problem sending notification, wrong credentials?"


if __name__ == "__main__":

    parser = argparse.ArgumentParser("cloud checker")
    parser.add_argument('--db', required=True)
    parser.add_argument('--mailto', required=True)
    parser.add_argument('--mailfrom', required=True)

    args = parser.parse_args()
    pw = getpass.getpass()

    cc = CloudCheck(args.db, args.mailto, args.mailfrom, pw)
    cc.run()

   
