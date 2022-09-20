#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
import numpy as np
import textwrap

def get_arguments(argv):
	cli = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''\
           Utility to analyze POSCAR/CONTCAR structure file
           By default print all information; unit cell, bonds, atoms ...
           Selectively print info by using optional arguments.
         -----------------------------------------------------------------
         '''),
    epilog=textwrap.dedent('''\
         examples:
         -----------------------------------------------------------------
            %(prog)s POSCAR > structure-data.nfo
            %(prog)s -p POSCAR
            %(prog)s -f POSCAR -bc > bonding-data.nfo 
            %(prog)s --debug --radius=2 --neighbors --save sns2.vasp --primitive
            %(prog)s -vvvvvnacrs 3 --tolerance=1e-3 mos2.contcar 
            %(prog)s -vvnacrs 3 mos2.contcar -t 0.01
            %(prog)s -gnacrs3 mos2.contcar -t0.1
         '''))

	cli.add_argument("FILE",help="input file containig data to process",type=str)
	cli.add_argument("-a","--atoms",dest="printAtoms",help="print atomic scale info. ntotal, types ...",action="store_true")
	cli.add_argument("-b","--bonds",dest="printBonds",help="print bonding info. total, species connectivity",action="store_true")
	cli.add_argument("-c","--cell",dest="printCell",help="print info on the unit cell; a,b,c volume ... ",action="store_true")
	cli.add_argument("-n","--neighbors",dest="printNlist",help="print bonding info and nearest neighbor information. n^2 recursive search for nearest neighbors stop when at least (1) bond is made, use this for assigning all neighbors.",action="store_true")
	cli.add_argument("-p","--primitive=", dest="getPrimitive",help="if possible,reduce convetional cell to primitive unit cell",action="store_true")
	cli.add_argument("-r","--radius=", dest="rcut",help="search radius for considering an atom as nearest neighbor,(default = %(default)s Å)",default=0.0,type=float)
	cli.add_argument("-s","--save",dest="save",help="save the computed data to a file <stoich>.[bonds,atoms,cell]. ex: P1S2H2 -> P1S2H2.bonds P1S2H2.atoms, default == do not save, print to stdout",action="store_true")
	cli.add_argument("-t","--tolerance=", dest="symprec",help="precision in determining crystal symmetry in Cartesian coordinates,(default = %(default)s Å)",default=0.05,type=float)
	cli.add_argument("-v", dest="verb",help="increase output verbosity",default=0,action="count")
	cli.add_argument("--debug", dest="verb",help="extensive info, equivalent to \"-vvvv\"",action="store_true")
	cli.add_argument('--version', action='version', version='%(prog)s 4.0.')
	args = cli.parse_args()

	return args

def get_lines(file):

	l1 = 1
	l2 = 2

	lineNumber = 0

	# f = open(file)
	with open(file) as f:
		nq = 0
		first = True
		second = True
		for line in f:
			lineNumber += 1
			if "distance" in line:
				if first is False and second is True:
					l2 = lineNumber
					second = False
				if first is True:
					l1 = lineNumber
					first = False
				nq += 1
		f.close()

	return l1,l2,nq

def get_occurance(file,occurance,word,position):

	value = None
	recordNumber = 0
	with open(file) as f:
		first = True
		for line in f:
			if recordNumber == occurance:
				break
			if word in line:
				dLine = line.split()
				data = [word for word in dLine]
				recordNumber += 1
				value = data[position-1]
	if value is None:
		print "Warning, the word [%s] was not found in [%s]" % (word,file)

	return value

# def count_occurances(file):
# 	with open(file) as f:
# 		count = sum("distance" in line for line in f)
# 	return count


def main(argv):

	parameters = get_arguments( argv )

	l1,l2,count = get_lines(parameters.FILE)
	

	lineLength = l2 - l1
	nbands = (lineLength-4)/2

	pqx = get_occurance(parameters.FILE,1,"q-position",4)
	pqy = get_occurance(parameters.FILE,1,"q-position",5)
	pqz = get_occurance(parameters.FILE,1,"q-position",6)

	print pqx,pqy,pqz

	# print l1,l2,count,lineLength,nbands


if __name__ == "__main__": main(sys.argv[1:])


