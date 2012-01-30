#
# Python implementation of https://github.com/juuso/BozoCrack
#

import sys
import os
import re


OLD_FORMAT = r"(?P<hash>[a-zA-Z0-9]{32}):(?P<pass>.*)"

class Bozo(object):

    def __init__(self):
        self.failed = []

    def reformat(self):
        if os.stat("bozo.cache").st_size != 0:
            for line in open("bozo.cache", "r").read().strip().split("\n"):
                if re.match(OLD_FORMAT, line):
                    p = re.match(OLD_FORMAT, line)
                    self.write_cache(p.group('hash'), p.group('pass'))
                else:
                    self.failed.append(line)
        print "Wrote out reformatted cache to 'bozo.cache.new'"
        print "rename this file to 'bozo.cache'"
        print 
        print "Failed:"
        print "\n".join(self.failed)
              

    def write_cache(self, hash, plain_text):
        with open("bozo.cache.new", "a") as cache:
            cache.write("%s|@bozo@|%s\n" % (hash, plain_text))


if __name__ == "__main__":
    bozo = Bozo()
    bozo.reformat()
    sys.exit(os.EX_OK)
