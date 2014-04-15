python-clearskies
=================

A python library for communicating with the ClearSkies daemon

[![Build Status](https://travis-ci.org/shish/python-clearskies.svg?branch=master)](https://travis-ci.org/shish/python-clearskies)

```
from clearskies.client import ClearSkies

cs = ClearSkies()
cs.connect()

cs.pause()
cs.resume()

print cs.list_shares()
```

The plan is for this to be a pythonic object-y library, because if you just wanted
raw JSON dictionaries, you wouldn't be using a library in the first place.


Also includes simple CLI client for testing:

```
$ ./clearskies/cli.py --help

usage: cli.py [-h] [-v]
              {stop,pause,resume,status,create,list,share,attach,detach} ...

ClearSkies python interface demo

positional arguments:
  {stop,pause,resume,status,create,list,share,attach,detach}
    status              Give program status
    create              Create new share
    list                List all shares and sync status
    share               Make access code to be given to others
    attach              Add access code from someone else, creating new share
                        at [path]
    detach              Stop syncing path

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
```

In particular note that the -v flag will print out the JSON that gets
sent and received through the control socket:

```
$ ./clearskies/cli.py -v list

2014-04-15 19:02:08 DEBU < {"service":"ClearSkies Control","software":"clearskies 0.1pre","protocol":1}
2014-04-15 19:02:08 DEBU > {'type': 'list_shares'}
2014-04-15 19:02:08 DEBU < {"shares":[{"path":"/home/shish/Documents","status":"N/A"},{"path":"/home/shish/Pictures/Unikitty","status":"N/A"}]}

Status Share
~~~~~~ ~~~~~
   N/A /home/shish/Documents
   N/A /home/shish/Pictures/Unikitty
```