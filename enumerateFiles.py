#!/usr/bin/env python3

'''
starting point came from http://www.w3resource.com/python-exercises/python-basic-exercise-71.php

enumerate and rename video files based on creation date

'''

from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time

# if path argument not provided then use current directory
dirPath = sys.argv[1] if len(sys.argv) == 2 else r'.'

# creates a generator that yields full filename with path
def createGenerators():

	data = (os.path.join(dirPath, f) for f in os.listdir(dirPath))

	# creates generator that yields statistics and path for each file
	statsAndPath = ((os.stat(path), path) for path in data)

	# regular files, insert creation date
	# creates generator that filters non regular files and yields creation time with path
	creationAndPath = ((stat[ST_CTIME], path)
           for stat, path in statsAndPath if S_ISREG(stat[ST_MODE]))
	return creationAndPath

results = sorted(createGenerators())


def getMp4s(fileTuple):
	return fileTuple[1].endswith('.mp4')

# mp4files = filter(getMp4s, results)
# enumerate(mp4files, start=00)

az = enumerate(filter(getMp4s, results), start=00)

for i in az:
	prefix = '{:#02d}'.format(i[0])
	basename = (prefix + i[1][1]).replace("/", " ")
	os.renames(i[1][1], basename)


'''
when it is current directory the tuple is showing file name as ./filename, then os.renames makes that into a new direcotry on the move
'''