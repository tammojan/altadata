# Move to the correct format
import os
import sys

fname = 'cal'

files = []
cmd = os.popen('ls %s' % fname)
for x in cmd:
	files.append(x.strip())

print files