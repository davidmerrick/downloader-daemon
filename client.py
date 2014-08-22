#!/usr/bin/python

import Pyro.core

# you have to change the URI below to match your own host/port.
downloader = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/downloader")


url = "http://www.ada.gov/hospcombrprt.pdf"
print("Adding URL to download: " + url)

downloader.add_url(url)
