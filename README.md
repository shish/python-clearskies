python-clearskies
=================

A python library for communicating with the ClearSkies daemon

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
