# Push the contents of a folder to ALTA by generating a script
import os
import sys

# Get the folder 
try:
	fname = sys.argv[1]
except:
	print('Folder must be specified!')
	#sys.exit()

# Specify location on ALTA
try:
	dname = sys.argv[2]
except:
	dname = '/altaZone/home/apertif_main/early_results/m51'

fname = 'altadata'

files = []
cmd = os.popen('ls %s/*' % fname)
for x in cmd:
	files.append(x.strip())
print(files)


# Write an out file
out = open('transfer_%s_to_ALTA.sh' % fname,'w')
out.write("""#!/bin/bash
ils imkdir -p %s/%s' 
iput -rkI -X logs/%s-icat.irods-status --lfrestart logs/%s-icat.lf-irods-status --retries 5 -N 4 -R alta-icat-Resc %s %s/%s >> logs/transfer_%s_to_alta_icat.log &
wait #iput
irsync -rsl %s i:%s/%s > logs/transfer_%s_to_alta_verify.log 2>&1
FAILED_FILES=`cat logs/transfer_%s_to_alta_verify.log | wc -l`
if [ $FAILED_FILES -eq 0 ]
then
  curl -X POST --data-urlencode 'payload={"text":"Transfer of %s to ALTA finished."}' https://hooks.slack.com/services/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
else
  curl -X POST --data-urlencode 'payload={"text":"Transfer of %s to ALTA finished incomplete. Check logs!"}' https://hooks.slack.com/services/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
fi
""" % (dname,fname,fname,fname,' '.join(files),dname,fname,fname,' '.join(files),dname,fname,fname,fname,fname,fname))
out.flush()