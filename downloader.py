#!/usr/bin/python
# Written by David Merrick on 8-20-14

import subprocess
import Pyro.core

class Downloader(Pyro.core.ObjBase):
        'Daemon for downloading a queue of files'

        def __init__(self):
                Pyro.core.ObjBase.__init__(self)

		self.__download_destination_directory = "/media/usbstick/downloads"
                self.__urls_to_download = []

	def add_url(self, url):
		self.__urls_to_download.append(url)
		return "Currently downloading: " + str(self.__urls_to_download)

        def download_files(self):
                #Downloads all the files in the list

                for url in self.__urls_to_download:
                        self.__download_file(url)

        def __download_file(self, url):
                # 1. Spawn a process to download the file

                proc = subprocess.Popen('wget ' + url + ' -P ' + self.__download_destination_directory, shell=True, stdout=subprocess.PIPE)
                output = proc.communicate()[0]
                #Wait until subprocess has finished.
                proc.wait()

                # 2. Clean up the file, leaving only the remaining URLs

                #Remove the URL we just downloaded
                self.__urls_to_download = self.__urls_to_download[1:]
                with open(self.__list_file, "w") as f:
                        for line in self.__urls_to_download:
                                f.write(line)
                        f.close()

Pyro.core.initServer()
daemon=Pyro.core.Daemon()
uri=daemon.connect(Downloader(),"downloader")

print "The daemon runs on port:",daemon.port
print "The object's uri is:",uri

daemon.requestLoop()
