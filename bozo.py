# 
# This is such a rip off of the original that even the method names rename the same
#
# Original: https://github.com/juuso/BozoCrack
#

# TODO
# 
# * single hash lookup
#

import sys
import os
import md5
import urllib
import urllib2


class Bozo(object):

    def __init__(self, file):
        self.hashes = []
        self.cache = []
        self.cracked = {}

        for hash in open(file, "r").read().split("\n"):
            if len(hash) == 32: # original uses a regex, I figured I'd just check length and be lazy
                self.hashes.append(hash)

        self.hashes = list(set(self.hashes))
        print "Loaded %s hashes" % len(self.hashes)

    def crack(self):
        for hash in self.hashes:
            if hash in self.cache:
                print "%s:%s" % (hash, self.cracked[hash])
            plain_text = self.crack_single(hash)
            if plain_text:
                print "%s:%s" % (hash, plain_text)
                self.cache.append(hash)
                self.cracked[hash] = plain_text
            # in the original there was a sleep here, I didn't like it. =D

    def crack_single(self, hash):
        # Pretend to be Firefox to stop the AWESOME Google 403
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        url = "http://www.google.com/search?q=%s" % hash
        headers = {'User-Agent': user_agent} 

        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)

        wordlist = response.read().split(" ")
        plain_text = self.dictionary_attack(hash, wordlist)
        if plain_text:
            return plain_text

    def dictionary_attack(self, hash, wordlist):
        for word in wordlist:
            if md5.new(word).hexdigest() == hash.lower():
                return word


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: bozo.py hashes.txt"
        sys.exit(os.EX_USAGE)
    else:
        bozo = Bozo(sys.argv[1])
        bozo.crack()
        sys.exit(os.EX_OK)