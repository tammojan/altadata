# ALTA data transfer: Uses the iROD client to transfer data from ALTA
# Example usage: >> python getdata_alta.py 180316 004-010 00-36
# V.A. Moss (vmoss.astro@gmail.com)

__author__ = "V.A. Moss"
__date__ = "$20-mar-2018 16:00:00$"
__version__ = "0.1"

import os
import sys
import time

# Time the transfer
start = time.time()

# Get date
try:
	date = sys.argv[1]
except:
	print "Date required! Format: YYMMDD e.g. 180309"
	sys.exit()

# Get date
try:
	irange = sys.argv[2]
except:
	print "ID range required! Format: NNN-NNN e.g. 002-010"
	sys.exit()

# Get beams
try: 
	brange = sys.argv[3]
except:
	print "Beam range required! Format: NN-NN e.g. 00-37"
	sys.exit()

# Now with all the information required, loop through beams
bstart = int(brange.split('-')[0])
bend = int(brange.split('-')[1])

# Now with all the information required, loop through beams
istart = int(irange.split('-')[0])
iend = int(irange.split('-')[1])

print "Start beam:",bstart
print "End beam:",bend

for ii in range(bstart,bend+1):

	print "###########################"
	
	print 'Processing Beam %.3d...' % ii

	for jj in range(int(istart),int(iend)+1):
		print 'Processing task ID %.3d...' % jj

		cmd = "iget -rfPIT -X WSRTA%s%.3d_B%.3d-icat.irods-status --lfrestart WSRTA%s%.3d_B%.3d-icat.lf-irods-status --retries 5 /altaZone/home/apertif_main/wcudata/WSRTA%s%.3d/WSRTA%s%.3d_B%.3d.MS" % (date,jj,ii,date,jj,ii,date,jj,date,jj,ii)
		print cmd
		os.system(cmd)

os.system('rm -rf *irods-status')
print "###########################"

# Time the transfer
end = time.time()

# Print the results
diff = (end-start)/60. # in min
print "Total time to transfer data: %.2f min" % diff