#!/usr/bin/python

import Pyro.core
import time

# you have to change the URI below to match your own host/port.
downloader = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/downloader")


url = "http://www.ada.gov/hospcombrprt.pdf"
print("Adding URL to download: " + url)
downloader.add_url(url)

url = "http://www.toplivres.org/i_12247.pdf"
print("Adding URL to download: " + url)
downloader.add_url(url)

print("queue: " + str(downloader.get_queue()))

print("Kicking off download")
downloader.download_files()
