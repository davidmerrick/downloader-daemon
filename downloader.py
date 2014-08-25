#!/usr/bin/python

import subprocess
import Pyro.core
import threading
from daemon import Daemon
import sys

class DownloaderDaemon(Daemon):
    def run(self):
	Pyro.core.initServer()
	downloader = Downloader()
	daemon = Pyro.core.Daemon()
	uri = daemon.connect(downloader, "downloader")
	daemon.requestLoop()

class Downloader(Pyro.core.ObjBase):
    '''Daemon for downloading a queue of files'''

    def __init__(self):
        Pyro.core.ObjBase.__init__(self)

        self.__download_destination_directory = "/tmp/"
        self.__urls_to_download = []

    def add_url(self, url):
        print("Adding URL: " + url)
	self.__urls_to_download.append(url)
	return	
		
    def get_queue(self):
	return self.__urls_to_download    

    def download_files(self):

	print("Downloading files...")

        #Downloads all the files in the list

        for url in self.__urls_to_download:
                self.__download_file(url)

    def __download_file(self, url):
        print("Downloading: " + url)

        # Spawn a process to download the file

        proc = subprocess.Popen('wget ' + url + ' -P ' + self.__download_destination_directory, shell=True, stdout=subprocess.PIPE)
        output = proc.communicate()[0]

        # Wait until subprocess has finished.

        proc.wait()

        # Remove the URL we just downloaded

        self.__urls_to_download.remove(url)


if __name__ == "__main__":
        daemon = DownloaderDaemon('/tmp/downloader-daemon.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
		elif 'start_downloads' == sys.argv[1]:
			print("Starting downloads")
			downloader = Pyro.core.getProxyForURI("PYROLOC://localhost:7766/downloader")
			downloader.download_files
		else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
