#!/usr/bin/python
# Written by David Merrick on 8-20-14

import subprocess
import Pyro.core
import threading
import time

class Downloader(Pyro.core.ObjBase):
        '''Daemon for downloading a queue of files'''

        def __init__(self):
                Pyro.core.ObjBase.__init__(self)

		self.__download_destination_directory = "/media/usbstick/downloads"
                self.__urls_to_download = []
	 	self.__current_time = "None"			

		# Instantiate threads
		
		self.__dl_thread = None
                self.__time_thread = None
	
	def add_url(self, url):
		self.__urls_to_download.append(url)
		return "Currently downloading: " + str(self.__urls_to_download)

	def run(self):
		# Spawn a thread for downloading files and one to monitor the time
		print("Ready")
	 	self.__current_time = time.strftime("%H")			
		
		# Spawn threads		

		self.__dl_thread = threading.Thread(target=self.__download_files_thread)
		self.__time_thread = threading.Thread(target=self.__keep_time_thread)	

	def stop(self):
		# Kill the threads
		print("Killing threads and stopping")
		self.__dl_thread.join()
		self.__time_thread.join()

	def __keep_time_thread(self):
		while True:
			time.sleep(300)
			self.__keep_time()

	def __keep_time(self):
		self.__current_time = time.strftime("%H")

	def get_time(self):
		return self.__current_time
	
	def __download_files_thread(self):
		while True:
			self.download_files()
	
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
                self.__urls_to_download.remove(url)

Pyro.core.initServer()
downloader = Downloader()
downloader.run()
daemon=Pyro.core.Daemon()
uri=daemon.connect(downloader, "downloader")

print "The daemon runs on port:",daemon.port
print "The object's uri is:",uri

daemon.requestLoop()
