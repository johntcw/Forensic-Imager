#!/usr/bin/python3
"""
Forensic Imager

A GUI tool on Raspberry Pi for creating Images from digital media. 
Forensic Imager is targeted to be portable, easy to use and forensically sound.

Author: John Wei
Website: instatronic.com
Email: johntcw@gmail.com
Last edited: July 2018
"""
import io
import os
import re
import sys
import time
import pyudev
import hashlib
import subprocess
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from mainwindow import *

#used as a quick way to handle shell commands
def getFromShell(command):
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	result = p.stdout.readlines()
	return str(result[0].strip())

class AppWindow(QMainWindow,Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.imagingBtn.clicked.connect(self.imagingBtnClicked)
		self.ui.hashSrcBtn.clicked.connect(self.hashBtnClickeed)
		self.ui.refreshBtn.clicked.connect(self.refreshDiskList)
		self.show()
		self.refreshDiskList()

	def imagingBtnClicked(self):
		read_size = 0
		last_percent_done = 0
		totalBlocks = 0
		blockSize = 16384
		destFolder = time.strftime("%Y-%m-%d_%I-%M-%S")
		logFile = destFolder+"/logfile.txt"
		imageFile = destFolder+"/"+destFolder+".dd"

		src = self.ui.srcBox.currentText().split()[0]

		#mount target device
		result = getFromShell('sudo mkdir -v /media/targetDisk')
		if re.search('created',result):
			self.ui.logView.append("/media/targetDisk created.")
		else:
			self.ui.logView.append("mkdir /media/targetDisk failed.")
			return

		drive = self.ui.destBox.currentText().split()[0]
		result = getFromShell('sudo mount -v %s /media/targetDisk' % drive)
		if re.search('mounted',result):
			self.ui.logView.append("/media/targetDisk mounted.")
		else:
			self.ui.logView.append("/media/targetDisk cannot be mounted.")
			return

		#create destination folder
		result = getFromShell('sudo mkdir -v /media/targetDisk/'+destFolder)
		if re.search('created',result):
			self.ui.logView.append("Folder '"+destFolder+"' created.")
		else:
			self.ui.logView.append("mkdir /media/targetDisk/+"+destFolder+" failed.")
			return

		#hash source disk
		self.ui.logView.append("Hashing "+src+".")
		md5 = self.checksum_md5(src)
		with open("/media/targetDisk/"+logFile, "a") as myfile:
			myfile.write("Start hasing evidence disk '"+src+"' - ")
			myfile.write(time.strftime("%Y-%m-%d %I:%M:%S")+"\n")
			myfile.write(md5)
			myfile.write("\n\n\n")

		#start imaging
		self.ui.logView.append("Start imaging "+src+".")
		with open("/media/targetDisk/"+logFile, "a") as myfile:
			myfile.write("Start imaging evidence disk '"+src+"' - ")
			myfile.write(time.strftime("%Y-%m-%d %I:%M:%S")+"\n")
		#calculate blocks
		with open(src,'rb') as f:
			self.statusBar().showMessage("Preparing...")
			#calculate size
			for chunk in iter(lambda: f.read(blockSize), b''): 
				totalBlocks += 1
		#imaging
		with open(src,'rb') as f:
			with open("/media/targetDisk/"+imageFile, "wb") as i:
				while True:
					read_size += 1
					# Calculate progress.
					percent_done = (read_size / totalBlocks) * 100
					if percent_done > last_percent_done:
						#print '%d%% done' % percent_done
						self.statusBar().showMessage("{0:.0f}% completed ({1}/{2})".format(percent_done, read_size, totalBlocks))
						last_percent_done = percent_done
					
					if i.write(f.read(blockSize)) == 0:
						with open("/media/targetDisk/"+logFile, "a") as myfile:
							myfile.write("Imaging completed '"+imageFile+"' - ")
							myfile.write(time.strftime("%Y-%m-%d %I:%M:%S")+"\n")
							myfile.write("\n\n\n")
						break

		#hash image
		self.ui.logView.append("Hashing "+imageFile+".")
		md5 = self.checksum_md5("/media/targetDisk/"+imageFile)
		with open("/media/targetDisk/"+logFile, "a") as myfile:
			myfile.write("Start hasing image file '"+imageFile+"' - ")
			myfile.write(time.strftime("%Y-%m-%d %I:%M:%S")+"\n")
			myfile.write(md5)
			myfile.write("\n\n\n")

		#hash source disk
		self.ui.logView.append("Hashing "+src+".")
		md5 = self.checksum_md5(src)
		with open("/media/targetDisk/"+logFile, "a") as myfile:
			myfile.write("Start hasing evidence disk '"+src+"' - ")
			myfile.write(time.strftime("%Y-%m-%d %I:%M:%S")+"\n")
			myfile.write(md5)
			myfile.write("\n\n\n")

		#unmount target device
		result = getFromShell('sudo umount -v /media/targetDisk')
		if re.search('unmounted',result):
			self.ui.logView.append("/media/targetDisk unmounted.")
		else:
			self.ui.logView.append("/media/targetDisk cannot be unmounted.")
			return

		result = getFromShell('sudo rm -v -r /media/targetDisk')
		if re.search('removed',result):
			self.ui.logView.append("/media/targetDisk removed.")
		else:
			self.ui.logView.append("/media/targetDisk remove failed.")
			return

	def hashBtnClickeed(self):
		drive = self.ui.srcBox.currentText().split()[0]
		md5 = self.checksum_md5(drive)
		QMessageBox.about(self, "Hash result", "{0}".format(md5))

	def checksum_md5(self, filename):
		read_size = 0
		last_percent_done = 0
		totalBlocks = 0
		blockSize = 16384
		#get drive size
		disk = os.statvfs(filename)

		md5 = hashlib.md5()
		sha1 = hashlib.sha1()

		with open(filename,'rb') as f:
			self.statusBar().showMessage("Preparing...")
			#calculate size
			for chunk in iter(lambda: f.read(blockSize), b''): 
				totalBlocks += 1

		with open(filename,'rb') as f:		
			for chunk in iter(lambda: f.read(blockSize), b''): 
				read_size += 1
				md5.update(chunk)
				sha1.update(chunk)
				# Calculate progress.
				percent_done = (read_size / totalBlocks) * 100
				if percent_done > last_percent_done:
					#print '%d%% done' % percent_done
					self.statusBar().showMessage("{0:.0f}% completed ({1}/{2})".format(percent_done, read_size, totalBlocks))
					last_percent_done = percent_done
		return md5.hexdigest()+" (md5)\n"+sha1.hexdigest()+" (sha1)"

	def refreshDiskList(self):
		#try:
		#	objProc = subprocess.Popen('lsblk --nodeps %s | grep -v SIZE  | awk \'{ print $4 }\'' % device['DEVNAME'], shell=True, bufsize=0, executable="/bin/bash", stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#except OSError as e:
		#	print(e)

		#  stdOut.communicate() --> dimension [0]: stdout, dimenstion [1]: stderr
		#stdOut = objProc.communicate()
		#stdOut[0].strip()
		self.ui.srcBox.clear()
		self.ui.destBox.clear()

		self.ui.logView.append("Refreshing dirve list.")
		context = pyudev.Context()
		for device in context.list_devices(MAJOR='8'):
			if (device.device_type == 'disk'):
				#print("{0}, ({1})".format(device.device_node, device.device_type))
				self.ui.srcBox.addItem("{0} {1}".format(device['DEVNAME'], device['ID_VENDOR']))

			if (device.device_type == 'partition'):
				#print("{0}, ({1})".format(device.device_node, device.device_type))
				self.ui.destBox.addItem("{0} {1}".format(device['DEVNAME'], device['ID_VENDOR']+"("+device['ID_FS_LABEL']+")"))

		self.ui.logView.append("Dirve list refreshed.")


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())