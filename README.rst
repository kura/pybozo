======
PyBozo
======

Python implementation of BozoCrack - https://github.com/juuso/BozoCrack

*Note: As of 30 Jan 2012 the format for bozo.cache has changed, please
see `Reformatter` section on how to update you cache file*

Usage
=====

Single hash
-----------

  python bozo.py HASH

Multiple hashes
---------------

  python bozo.py HASHLIST.TXT


Reformatter
===========

  python reformat.py

This will create a file called `bozo.cache.new` which you can
copy over the old cache file.

It will also output a list of hashes that failed to reformat
