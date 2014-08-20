#!/usr/bin/python

import subprocess

class Downloader:
        'Downloads files using wget'

        def __init__(self):
                self.__download_destination_directory = "/media/usbstick/downloads"
                self.__list_file = "../tmp/download_us.txt"
                self.__urls_to_download = []

                #Initialize the download array
                f = open(self.__list_file)
                lines = f.readlines()
                for line in lines:
                        self.__urls_to_download.append(line.strip())
                f.close()

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


downloader = Downloader()
downloader.download_files()

