Pre-requistics to simulationGFI.py:

a) export path to seq-gen source:
	export PATH=/path/to/seq-gen/source-folder:$PATH

b) export path to jprime jar file:
	PATH=/path/to/jprime-X.X.X.jar:$PATH
	
c) pip install argparse (if not installed on your computer)


Help Options:

$ python simulateGTS.py --help
usage: simulateGTS.py [-h] [-stree speciesTree] [-j jprime] [-d dup] [-l loss]
                      [-tr trans] [-O outdir] [-k shape] [-t theta]
                      [-n ntrees] [-s seed]

Parse input arguments and print output. NOTE: you need to export poath to
jprime jar file and seq-gen exe.

optional arguments:
  -h, --help          show this help message and exit
  -stree speciesTree  Specify path to the species tree file.
  -j jprime           Specify the name of the jprime jar file i.e.
                      jprime-0.3.5.jar.
  -d dup              Specify duplication rate.default=0.5
  -l loss             Specify loss rate.default=0.5
  -tr trans           Specify transfer rate.default=0.5
  -O outdir           Specify path to the output directory.
  -k shape            Specify Shape parameter for IIDGamma distribution for
                      branch relaxation.
  -t theta            Specify Theta parameter for IIDGamma distribution for
                      branch relaxation.
  -n ntrees           Specify the number of gene trees to be generated
  -s seed             Specify seed. default=121