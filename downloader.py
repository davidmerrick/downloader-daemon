#!/usr/bin/python
# Written by David Merrick on 8-20-14

import subprocess
import Pyro4
import threading
import time

class Downloader(Pyro.core.ObjBase):
        '''Daemon for downloading a queue of files'''

        def __init__(self):
                Pyro.core.ObjBase.__init__(self)

		self.__download_destination_directory = "/media/usbstick/downloads"
                self.__urls_to_download = []
	 	self.__current_time = "None"			

		# Spawn threads
		
		#self.__dl_thread = threading.Thread(target=self.download_files)
                #self.__time_thread = threading.Thread(target=self.__keep_time)

	def add_url(self, url):
		self.__urls_to_download.append(url)
		return "Currently downloading: " + str(self.__urls_to_download)

	def run(self):
		# Spawn a thread for downloading files and one to monitor the time
		print("Ready")
	 	self.__current_time = time.strftime("%H")			
		
		#dl_thread = threading.Thread(target=self.download_files)
		#time_thread = threading.Thread(target=self.keep_time)	

	def __keep_time(self):
		time.sleep(10)
		self.__current_time = time.strftime("%H")

	def get_time(self):
		return self.__current_time
	
        def download_files(self):
                #Downloads all the files in the list

                for url in self.__urls_to_download:
                        self.__download_file(url)

        def __download_file(self, url):
                # Spawn a process to download the file

                proc = subprocess.Popen('wget ' + url + ' -P ' + self.__download_destination_directory, shell=True, stdout=subprocess.PIPE)
                output = proc.communicate()[0]
                
		# Wait until subprocess has finished.
                proc.wait()

                # Remove the URL we just downloaded
                self.__urls_to_download = self.__urls_to_download[1:]

Pyro.core.initServer()
downloader = Downloader()
daemon=Pyro4.Daemon()
uri=daemon.register(downloader)

print "The daemon runs on port:",daemon.port
print "The object's uri is:",uri

daemon.requestLoop()
