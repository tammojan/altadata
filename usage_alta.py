# ALTACheck: report on the current usage and status of ALTA
# V.A. Moss 12/10/2018 (vmoss.astro@gmail.com)
# Usage: python usage_alta.py

__author__ = "V.A. Moss"
__date__ = "$12-oct-2018 17:00:00$"
__version__ = "1.0"

import os
import sys

def main():
	"""
	The main program to be run.
	:return:
	"""

	nodes = ['icat','res1','res2','res3']
	lines = []
	
	# Loop through nodes
	for node in nodes:

		# Check status and usage
		cmd = 'ilsresc -l alta-%s-Resc' % node
		data = os.popen(cmd).read()
		status = data.split('status: ')[1].split('\n')[0]
		usage = float(data.split('free space: ')[1].split('\n')[0])/1e12 # in TB

		# Each node has 410.27 TB??, convert to % free
		fullness = (1 - usage/410.27) * 100.0

		# Make a print statement
		lines.append("%s\t\t\t%s\t\t\t%.2f TB\t\t\t%.1f %%\n" % (node,status,usage,fullness))


	# Return the output
	print('\n##########################################################################################')
	print('NODE\t\t\tSTATUS\t\t\tFREE(TB)\t\t\tUSAGE(%)')
	print ''.join(lines).strip('\n')
	print('##########################################################################################\n')


if __name__ == '__main__':
    main()