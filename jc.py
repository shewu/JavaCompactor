#!/bin/python

import sys
import re

class JavaProgram:
	packages = set()
	mainFile = ""
	javaFiles = []

	class JavaFile:
		def __init__(self, name):
			self.name = name
			self.packages = set()

			f = open(name)
			self.src = f.read()
			f.close()

			# find main file
			if re.search("public[ \t\r\n]+static[ \t\r\n]+void[ \t\r\n]+main", self.src) != None:
				assert JavaProgram.mainFile == ""
				JavaProgram.mainFile = self.name

			# get and strip packages
			self.findAndRemovePackages()

			# replace newlines
			self.carefullyStripWhitespace()

		def __str__(self):
			return self.name
		
		def carefullyStripWhitespace(self):
			class StripState:
				DONT_STRIP, STRIP, INSIDE_STRING = range(3)

			si = 0
			state = StripState.DONT_STRIP

			self.src = self.src.replace('\n', ' ')
			self.src = self.src.replace('\r', ' ')
			while si < len(self.src):
				assert self.src[si] not in "\r\n"
				# if inside string, do not strip whitespace
				# TODO fix bug that strips spaces inside strings, although this doesn't fail on tabs?!
				if state == StripState.INSIDE_STRING:
					if self.src[si] in "\"\'" and self.src[si-1] != '\\':
						state = StripState.DONT_STRIP
					si += 1
				elif state == StripState.DONT_STRIP:
					if self.src[si] in " \t":
						state = StripState.STRIP
					elif self.src[si] == "\"\'":
						state = StripState.INSIDE_STRING
					si += 1
				elif state == StripState.STRIP:
					if self.src[si] in " \t":
						if si+1 < len(self.src):
							self.src = self.src[:si] + self.src[si+1:]
						else:
							self.src = self.src[:si]
					else:
						state = StripState.DONT_STRIP
				else:
					print "Unknown state encountered!"
					raise Exception('spam', 'eggs')

		def findAndRemovePackages(self):
			loc = self.src.find("import")
			while loc != -1:
				semicolon = self.src.find(";", loc)
				assert semicolon != -1
				JavaProgram.packages.add(self.src[loc:semicolon+1])
				self.src = self.src[:loc] + self.src[semicolon+1:]
				loc = self.src.find("import")

		def getSource(self):
			return self.src

	def __init__(self):
		pass
	
	def addFile(self, f):
		self.javaFiles.append(self.JavaFile(f))
	
	def addFiles(self, l):
		for f in l:
			self.addFile(f)
	
	def writeFile(self):
		if self.mainFile == '':
			print "Cannot create file ''. Exiting."
			return

		f = open(self.mainFile+'.new', "w")

		for p in self.packages:
			f.write(p)

		for jf in self.javaFiles:
			f.write(jf.getSource())

		f.close()
		print "File " + self.mainFile + '.new successfully created'

jp = JavaProgram()
jp.addFiles(sys.argv[1:])
jp.writeFile()

