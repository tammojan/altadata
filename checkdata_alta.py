# ALTA check: check and report on which datasets are in ALTA
# V.A. Moss (vmoss.astro@gmail.com)
__author__ = "V.A. Moss"
__date__ = "$2-oct-2018 17:00:00$"
__version__ = "0.1"

import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

def main():
	"""
    The main program to be run.
    :return:
    """

	# Get arguments
	parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
	parser.add_argument('-p', '--path',
		default='/data/apertif/',
		help='Specify path location of target folder (default: %(default)s)')

	# Parse the arguments above
	args = parser.parse_args()

	# List all folders in that directly
	cmd = os.popen('ls -d %s/*/' % args.path)

	lines = []

	for line in cmd:

		print('Parsing... %s' % line.strip())

		tid = line.split('/')[-2].split('_')[0]
		folder = line.split('/')[-2]
		
		# Check size of that directory in GB
		cmd2 = os.popen('du -s %s/%s*' % (args.path,tid)).read()
		size = float(cmd2.split('\t')[0])/1e6

		# Check ALTA size
		cmd = os.popen('ils -l /altaZone/home/apertif_main/wcudata/WSRTA%s' % tid).read()
		if cmd == '':
			datainalta = 'N'
			total_alta = '-'
		else:
			datainalta = 'Y'

			# Calculate size of data in ALTA
			cmd = os.popen("""iquest "%%s: %%s" "SELECT COLL_NAME, sum(DATA_SIZE) WHERE COLL_NAME like '/altaZone/home/apertif_main/wcudata/WSRTA%s/%%.MS'" """ % tid)
			alta_sizes = []
			for line in cmd:
				col = line.split()
				alta_size = float(col[-1])
				alta_sizes.append(alta_size)

			# Total ALTA size in GB
			total_alta = '%.2f' % (sum(alta_sizes)/1e9)

		# Calc diff if relevant
		if total_alta != '-':
			diff = '%.2f' % (float(total_alta) - size)
		else:
			diff = '-'

		lines.append("%-31s %.2f\t\t\t\t%s\t\t\t\t%s\n" % (folder,size,total_alta,diff))


	# Print results
	print('\n\n')
	print("%-31s Happili(GB)\t\t\tALTA(GB)\t\t\tDifference(GB)" % ('FOLDER'))
	print ''.join(lines)

if __name__ == '__main__':
    main()