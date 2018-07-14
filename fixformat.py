# Move to the correct format
import os
import sys

try: 
	tid = sys.argv[1]
except:
	print 'TID must be specified!'
	sys.exit()

# This will be used for renaming the calibrated datasets (until the pipeline does so?)
fname = 'cal'

# Get list of files
files = []
cmd = os.popen('ls %s' % fname)
for x in cmd:
	files.append(x.strip())

print files

# Loop through each file and rename
for f in files:

	stem = 'WSRTA%s_' % tid
	beam = int(f.split('_B')[1].split('.')[0])

	# Move to new name
	os.system('mv %s/%s %s/%sB%.3d_CAL.UVFITS' % (fname,f,fname,stem,beam))


