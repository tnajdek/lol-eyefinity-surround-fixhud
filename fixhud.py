#!/usr/bin/env python
import os
import shutil

from Tkinter import *
from rafiki.raf.raf import RafInstallation
from rafiki.raf.utils import mkdir_p
from hudfixer.hud import reanchor_centrally_in_raf

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))

def recursive_overwrite(src, dest, ignore=None):
	if os.path.isdir(src):
		if not os.path.isdir(dest):
			os.makedirs(dest)
		files = os.listdir(src)
		if ignore is not None:
			ignored = ignore(src, files)
		else:
			ignored = set()
		for f in files:
			if f not in ignored:
				recursive_overwrite(os.path.join(src, f), 
									os.path.join(dest, f), 
									ignore)
	else:
		shutil.copyfile(src, dest)


class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.userInput = {
			'lol_folder': StringVar(),
			'raf_path': StringVar(),
			'resolution': IntVar()
		}
		self.notification = StringVar()
		self.pack()

		self.ri = RafInstallation()
		self.backup_dir = os.path.join(SCRIPT_ROOT, 'backup')
		self.userInput['lol_folder'].set(self.ri.installation_path)
		self.createWidgets()

	def process(self):
		
		try:
			if(os.path.exists(self.backup_dir)):
				shutil.rmtree(self.backup_dir)
			mkdir_p(self.backup_dir)
		except Exception:
			self.notification.set("Unable to create backup folder dir! Check permissions.")
			self.explanation['bg'] = 'red'
			return

		self.notification.set("Parsing raf files...")
		self.explanation['bg'] = 'green'
		root.update()

		try:
			collection = self.ri.get_raf_collection()
			raffiles = collection.search(self.userInput['raf_path'].get())
		except Exception:
			self.notification.set("Unable to find raf collections. Check your Leagues of Legends path and try again.")
			self.explanation['bg'] = 'red'
			return

		self.notification.set("Creating backups...")
		self.explanation['bg'] = 'green'
		root.update()

		archives = set([raffile.archive for raffile in raffiles])
		for archive in archives:
			target_path = os.path.join(self.backup_dir, archive.relpath)
			mkdir_p(os.path.dirname(target_path))
			shutil.copyfile(archive.path, target_path)

		self.notification.set("Calculating new positions...")
		self.explanation['bg'] = 'green'




	def revert_backup(self):
		try:
			collection = self.ri.get_raf_collection()
		except Exception:
			self.notification.set("Unable to find raf collections. Check your Leagues of Legends path and try again.")
			self.explanation['bg'] = 'red'
			return

		backups = os.listdir(self.backup_dir)
		for backup in backups:
			src = backup
			relpath = os.path.relpath(backup, self.backup_dir)
			dest = os.join(collection.root_path, relpath)
			print("Would copy {} to {}".format(src, dest))



	def createWidgets(self):
		self.explanation = Label(self, textvariable=self.notification, anchor="w", justify="left", bg="blue", fg="white", wraplength=640)
		self.explanation.pack({"side": "top"})

		lol_path_input_label = Label(self, text="Please confirm your Leagues of Legends path:", anchor="w", justify="left")
		lol_path_input_label.pack({"fill": "x"})

		lol_path_input = Entry(self, textvariable=self.userInput['lol_folder'], width=60)
		lol_path_input.pack({"side": "top"})

		res_label = Label(self, text="Resolution of a SINGLE monitor:", anchor="w", justify="left")
		res_label.pack({"fill": "x"})

		res_input = Entry(self, textvariable=self.userInput['resolution'], width=60)
		res_input.pack({"side": "top"})

		raf_path_label = Label(self, text="Please confirm raf poth to modify (default should be ok!):", anchor="w", justify="left")
		raf_path_label.pack({"fill": "x"})

		raf_path_input = Entry(self, textvariable=self.userInput['raf_path'], width=60)
		raf_path_input.pack({"side": "top"})

		# self.userInput['lol_folder'].set(self.ri.installation_path)
		self.userInput['lol_folder'].set("/Users/doppler/tmp/lol-test/")
		#### FIX THIS ^^^
		self.userInput['raf_path'].set('DATA/Menu/HUD/Elements/')
		self.userInput['resolution'].set(1920)
		self.notification.set("This application will OVERRIDE .raf files in your Leauges of Legends directory in order to re-position GUI so playing on on multiple screens such as AMD's eyefinity or NVIDIA's Vision Surround. A BACKUP folder will be created in the same directory as this application where original .raf files will be archived")

		processButton = Button(self, text="Start", command=self.process)
		QUIT.pack({"side": "right"})

		if(os.path.exists(self.backup_dir) and len(os.listdir(self.backup_dir))):




root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()