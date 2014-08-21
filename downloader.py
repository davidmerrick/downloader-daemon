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

		# Times to do downloading
		
		self.__dl_start_hour = 0
		self.__dl_end_hour = 6

		self.__download_destination_directory = "/home/david/downloads"
                self.__urls_to_download = []
		
		# Thread that does the downloading	
	
		self.__dl_thread = None
	
	def add_url(self, url):
		self.__urls_to_download.append(url)
		return "Currently downloading: " + str(self.__urls_to_download)

	def run(self):

		# Spawn a thread for downloading files and one to monitor the time

		print("Ready")
		
		# Spawn download thread	and stop event (this pauses the thread durin times when it shouldn't be downloading)
		
		dl_stop = threading.Event()
		self.__dl_thread = threading.Thread(target=self.__download_files_thread, args={dl_stop})

		# Go into a loop, checking the time. Start and stop downloads based on this
		
		self.__dl_thread.start()
		
		while True:
			current_hour = time.strftime("%H")
			if int(current_hour) == self.__dl_start_hour:
				# Generate stop event
				dl_stop.set()
			elif int(current_hour) == self.__dl_end_hour:
				# Unset stop event
				dl_stop.clear()
			
			# Sleep for 5 minutes
			
			time.sleep(5 * 60)
	
	def stop(self):

		# Kill the threads

		print("Killing threads and stopping")
		
		if self.__dl_thread:
			self.__dl_thread.join()
		
	def get_time(self):
		return self.__current_time
	
	def __download_files_thread(self, stop_event):
		while True:
			while not stop_event.is_set():
				self.download_files()
			time.sleep(5 * 60)

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
downloader.run()
daemon=Pyro.core.Daemon()
uri=daemon.connect(downloader, "downloader")

print "The daemon runs on port:",daemon.port
print "The object's uri is:",uri

daemon.requestLoop()
