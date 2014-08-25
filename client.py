#!/usr/bin/python

import Pyro.core
import sys

def add_url(downloader, url):
	print("Adding URL to download: " + url)
	downloader.add_url(url)
	
def start_downloads(downloader):
	print("Starting downloads")
	downloader.start_downloads()


if __name__ == "__main__":

	downloader = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/downloader")
	
	if not downloader:
		print("Error: downloader server is not running. Start the server and then try again.")
		exit(1)

	if len(sys.argv) >= 2:
		if sys.argv[1] == 'add-url':
			url = sys.argv[2]
			add_url(downloader, url)
		if sys.argv[1] == 'start-downloads':
			start_downloads(downloader)		
	else:
		print("Usage: add-url <URL> | start-downloads")

