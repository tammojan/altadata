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

		if int(date) <= 180216:
			cmd = "iget -rfPIT -X WSRTA%s%.2d_B%.3d-icat.irods-status --lfrestart WSRTA%s%.2d_B%.3d-icat.lf-irods-status --retries 5 /altaZone/home/apertif_main/wcudata/WSRTA%s%.2d/WSRTA%s%.2d_B%.3d.MS" % (date,jj,ii,date,jj,ii,date,jj,date,jj,ii)
		else:
			cmd = "iget -rfPIT -X WSRTA%s%.3d_B%.3d-icat.irods-status --lfrestart WSRTA%s%.3d_B%.3d-icat.lf-irods-status --retries 5 /altaZone/home/apertif_main/wcudata/WSRTA%s%.3d/WSRTA%s%.3d_B%.3d.MS" % (date,jj,ii,date,jj,ii,date,jj,date,jj,ii)

		print cmd
		os.system(cmd)

os.system('rm -rf *irods-status')

# Add verification at the end of the transfer 
for ii in range(bstart,bend+1):

	print "###########################"
	
	print 'Verifying Beam %.3d...' % ii

	for jj in range(int(istart),int(iend)+1):
		print 'Processing task ID %.3d...' % jj

		# Toggle for when we started using more digits:
		if int(date) <= 180216:
			cmd = "irsync -srl i:/altaZone/home/apertif_main/wcudata/WSRTA%s%.2d/WSRTA%s%.2d_B%.3d.MS WSRTA%s%.2d_B%.3d.MS >> transfer_WSRTA%s%.2d_to_alta_verify.log 2>&1" % (date,jj,date,jj,ii,date,jj,ii,date,jj)
		else:
			cmd = "irsync -srl i:/altaZone/home/apertif_main/wcudata/WSRTA%s%.3d/WSRTA%s%.3d_B%.3d.MS WSRTA%s%.3d_B%.3d.MS >> transfer_WSRTA%s%.3d_to_alta_verify.log 2>&1" % (date,jj,date,jj,ii,date,jj,ii,date,jj)

		os.system(cmd)

# Identify server details
hostname = os.popen('hostname').read().strip()
path = os.popen('pwd').read().strip() # not using this for now but maybe in future

# Check for failed files
for jj in range(int(istart),int(iend)+1):
	print 'Processing task ID %.3d...' % jj
	
	cmd = os.popen('cat transfer_WSRTA%s%.3d_to_alta_verify.log | wc -l' % (date,jj))
	for x in cmd:
		print 'Failed files:',x.strip()
		failed_files = x.strip()

	if failed_files == '0':
		cmd = """curl -X POST --data-urlencode 'payload={"text":"Transfer of WSRTA%s%.3d (B%.3d-B%.3d) from ALTA to %s finished."}' https://hooks.slack.com/services/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""" % (date,jj,bstart,bend,hostname)
	else:
		cmd = """curl -X POST --data-urlencode 'payload={"text":"Transfer of WSRTA%s%.3d (B%.3d-B%.3d) from ALTA to %s finished incomplete. Check logs!"}' https://hooks.slack.com/services/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""" % (date,jj,bstart,bend,hostname)

	# Execute the command
	os.system(cmd)


print "###########################"

# Time the transfer
end = time.time()

# Print the results
diff = (end-start)/60. # in min
print "Total time to transfer data: %.2f min" % diff