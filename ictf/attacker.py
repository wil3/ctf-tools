
__author__ = "Wil Koch"
__contact__= "wfkoch@gmail.com"
import imp
from optparse import OptionParser 
import logging
from os import listdir
from os.path import isfile, join
import time

from ictf.client import iCTF, Team


class Attacker:
    MODULE = 'ictfexploit'

    def __init__(self, exploitdir, email, password):
        self.logger = logging.getLogger("Attacker")
        self.exploitdir = exploitdir
        self.delay = 5 

        i = iCTF()
        self.team = i.login(email, password)

    def run(self):
        tick = self.team.get_tick_info()
        lasttick = tick['tick_id']
        while True:
            tick = self.team.get_tick_info()
            self.logger.debug("Current tick " + str(tick))
            if lasttick != tick:
                self._attackVictims()
                lastick = tick

            time.sleep(self.delay)
            

    def _attackVictims(self):
        for service in self.team.get_service_list():
            service_id = service['service_id']
            for target in self.team.get_targets(service_id):
                self._attackVictim(target)

    def _attackVictim(self, target):

        files = [f for f in listdir(self.exploitdir) if isfile(join(self.exploitdir, f))]
        for exploitFilename in files: 
            exploitFile = join(self.exploitdir, exploitFilename)
            if exploitFile.endswith(".py"):
                try:
                    module_ = imp.load_source(self.MODULE, exploitFile)	
                    e = module_.Exploit()
                    if e.getPort() == target['port']:
                        flags = e.execute(target)
                        if flags and isinstance(list, flags):
                            self.team(flags)
                except Exception as e:
                    self.logger.exception(e)
                    

if __name__ == '__main__':
	usage = "usage: %prog [options] [exploitdir] [username] [password]"
	parser = OptionParser(usage=usage)
	parser.add_option('-v', '--verbose', action="store_true", default=False, help="Set logging to debug, output more stuff.")
	(options, args) = parser.parse_args()
	if len(args) != 3:
		parser.print_help()
		exit()


	logLevel = logging.DEBUG if options.verbose else logging.INFO	
	logging.basicConfig(level=logLevel)

        exploitdir = args[0]
        username = args[1]
        password = args[2]
        a = Attacker(exploitdir, username, password)
        a.run()
