#
# Original: https://github.com/juuso/BozoCrack
#

import sys
import os
import hashlib
import urllib2
import time


class Bozo(object):

    def __init__(self, hashes):
        self.hashes = []
        self.cache = []
        self.cracked = {}

        # Assume it's a single hash
        if not os.path.exists(hashes):
                self.hashes.append(hashes)
        else:
            for hash in open(hashes, "r").read().split("\n"):
                if len(hash) == 32: # original uses a regex, I figured I'd just check length and be lazy.
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
            time.sleep(0.1)

    def crack_single(self, hash):
        # Pretend to be Chrome to stop the AWESOME Google 403.
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/17.0.938.0 Safari/535.8"
        # Use the Chrome search URL to pretend to be Chrome.
        url = "http://www.google.co.uk/search?sourceid=chrome&q=%s" % hash
        headers = {'User-Agent': user_agent} 

        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)

        wordlist = response.read().split(" ")
        plain_text = self.dictionary_attack(hash, wordlist)
        if plain_text:
            return plain_text

    def dictionary_attack(self, hash, wordlist):
        for word in wordlist:
            if hashlib.md5(word).hexdigest() == hash.lower():
                return word


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Usage: bozo.py hashes.txt"
        sys.exit(os.EX_USAGE)
    else:
        bozo = Bozo(sys.argv[1])
        bozo.crack()
        sys.exit(os.EX_OK)
