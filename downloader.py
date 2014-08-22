#!/usr/bin/python

import subprocess
import Pyro.core
import threading

class Downloader(Pyro.core.ObjBase):
    '''Daemon for downloading a queue of files'''

    def __init__(self):
        Pyro.core.ObjBase.__init__(self)

        self.__download_destination_directory = "/home/david/downloader-daemon/downloads/"
        self.__urls_to_download = []

    def add_url(self, url):
        print("Adding URL: " + url)
	self.__urls_to_download.append(url)
	return
		
    def get_queue(self):
	return self.__urls_to_download    

    def download_files(self):

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

Pyro.core.initServer()
downloader = Downloader()
daemon = Pyro.core.Daemon()
uri = daemon.connect(downloader, "downloader")
print("The daemon runs on port: " + str(daemon.port))
print("The object's uri is: " + str(uri))
daemon.requestLoop()

