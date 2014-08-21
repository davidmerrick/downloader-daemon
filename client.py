#!/usr/bin/python

import Pyro.core

# you have to change the URI below to match your own host/port.
downloader = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/downloader")

print "Time: " + downloader.get_time()

downloader.stop()
