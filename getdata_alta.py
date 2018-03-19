import os
import sys

# Get date
try:
	date = sys.argv[1]
except:
	print "Date required! Format: YYMMDD e.g. 180309"
	sys.exit()

# Get date
try:
	end = sys.argv[2]
except:
	print "End ID required! Format: NNN e.g. 010"
	sys.exit()

# Get beams
try: 
	brange = sys.argv[3]
except:
	print "Beam range required! Format: NN-NN e.g. 00-37"

# Now with all the information required, loop through beams
bstart = int(brange.split('-')[0])
bend = int(brange.split('-')[1])

print "Start beam:",bstart
print "End beam:",bend

for ii in range(bstart,bend+1):

	print "###########################"
	
	print 'Processing Beam %.3d...' % ii

	for jj in range(1,int(end)+1):
		print 'Processing task ID %.3d...' % jj

		cmd = "iget -rPIT -X WSRTA%s%.3d_B%.3d-icat.irods-status --lfrestart WSRTA%s%.3d_B%.3d-icat.lf-irods-status --retries 5 /altaZone/home/apertif_main/wcudata/WSRTA%s%.3d/WSRTA%s%.3d_B%.3d.MS" % (date,jj,ii,date,jj,ii,date,jj,date,jj,ii)
		print cmd
		os.system(cmd)

os.system('rm -rf *irods-status')
print "###########################"