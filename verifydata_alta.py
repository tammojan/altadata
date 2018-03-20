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
	irange = sys.argv[2]
except:
	print "ID range required! Format: NNN-NNN e.g. 002-010"
	sys.exit()

# Get beams
try: 
	brange = sys.argv[3]
except:
	print "Beam range required! Format: NN-NN e.g. 00-36"
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

		cmd = "irsync -srl i:/altaZone/home/apertif_main/wcudata/WSRTA%s%.3d/WSRTA%s%.3d_B%.3d.MS /data/apertif/temp/WSRTA%s%.3d_B%.3d.MS" % (date,jj,date,jj,ii,date,jj,ii)
		# Don't print command, it clutters it
		#print cmd
		os.system(cmd)

print "###########################"