#!/usr/bin/env python
__author__ = "Mehmood Alam Khan"
__email__  = "malagori@kth.se"
__version__= "0.9"
__credits__ = ["Mehmood Alam Khan"]
'''
Created on Apr 4, 2014

@author: malagori
'''
import sys
import argparse
import os
import subprocess
import random
import datetime
import time
import tempfile


def checkExe(exePath):
    return os.path.isfile(exePath) # and os.access(exePath, os.X_OK)
    
def Where(program):
    '''
    input: name of executable
    output: path to executable
    '''
    fpath, fname = os.path.split(program)
    if fpath:
        if checkExe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            pathToProgram = os.path.join(path, program)
            if checkExe(pathToProgram):
                return pathToProgram
    return None

def generateGTreesAndAlignmets(work_dir, outFile, sTree, seed, dup, trans, loss, theta, k, minper, jarFileName):
    '''
    this function will call GenPhyloData to generate gtrees and the call seq-gen to generate sequences
    '''
    # check if path exists
    print jarFileName
    cmd= Where(jarFileName)
    #cmd= '/Users/malagori/Documents/Academic/project/infer-gfamily-project/data/simulation/jars/jprime-0.3.4.d.jar'
    if cmd != None:
        gTree= os.path.join(work_dir, outFile)
        brGTree= os.path.join(work_dir, outFile+".relaxed.tree")
        null = open("/dev/null")
        print "--> GenPhyloData begins..."
        try:
            subprocess.call("java -jar "+cmd+ " GuestTreeGen -s "+ str(seed) + " -minper "+str(minper)+" -max 1000 -a 10000000 "+ sTree+ " "+ str(dup) + " "+ str(loss)+ " "+ str(trans) +" "+ gTree, shell=(sys.platform!="win32"), stdout=True, stderr=True)
            
        except IOError, e:
            print ("Function: generateGTreesAndAlignmets: %s " % e)
        print "--> GenPhyloData ends..."
        print "--> Branch Relaxation begins..."
        try:
            seed += 11
            #varying branch length
            subprocess.call("java -jar "+cmd+ " BranchRelaxer -s "+ str(seed) + " "+ gTree+".pruned.tree " +"IIDGamma "+ str(k)+ " "+ str(theta) +" -o " +brGTree, shell=(sys.platform!="win32"), stdout=True, stderr=True)
            subprocess.call("java -jar "+cmd+ " BranchRelaxer -x -innms -s "+ str(seed) + " "+ gTree+".pruned.tree " +"IIDGamma "+ str(k)+ " "+ str(theta) +" -o " +brGTree+".no.primeid", shell=(sys.platform!="win32"), stdout=True, stderr=True)
            # for constant rates
            #subprocess.call("java -jar "+cmd+ " BranchRelaxer -s "+ str(seed) + " "+ gTree+".pruned.tree " +"Constant "+ str(1)+" -o " +brGTree, shell=(sys.platform!="win32"), stdout=True, stderr=True)
            #subprocess.call("java -jar "+cmd+ " BranchRelaxer -x -innms -s "+ str(seed) + " "+ gTree+".pruned.tree " +"Constant "+ str(1)+" -o " +brGTree+".no.primeid", shell=(sys.platform!="win32"), stdout=True, stderr=True)
            
        except IOError, e:
            print ("Function: generateGTreesAndAlignmets: %s " % e)
        print "--> Branch Relaxation ends..."
        
    else:
        print ("generateGTreesAndAlignmets: Error: Path to JPrIme.jar is not set ") 
        sys.exit()
        
        
    cmd= Where('seq-gen')
    if cmd != None:
        
        null = open("/dev/null")
        seed += 11
        subprocess.call(cmd+ " -mJTT -z "+ str(seed) + " -l 1000 < "+ brGTree +" > "+ work_dir+"/"+outFile+".phylip", shell=(sys.platform!="win32"), stdout=False, stderr=True)
        
    else:
        print ("generateGTreesAndAlignmets: Error: Path to seq-gen is not set ") 
        sys.exit()
        
def main(argv):
    parser = argparse.ArgumentParser(description="Parse input arguments and print output. NOTE: you need to export poath to jprime jar file and seq-gen exe.")
    parser.add_argument('-stree', metavar='speciesTree' ,type=str, help='Specify path to the species tree file. ')
    parser.add_argument('-j', metavar='jprime' ,type=str, help='Specify the name of the jprime jar file i.e. jprime-0.3.5.jar.')
    parser.add_argument('-d', metavar='dup' ,type=float, help='Specify duplication rate.default=0.5', default=0.5)
    parser.add_argument('-l', metavar='loss' ,type=float, help='Specify loss rate.default=0.5', default=0.5)
    parser.add_argument('-tr', metavar='trans' ,type=float, help='Specify transfer rate.default=0.5', default=0.5)
    parser.add_argument('-O', metavar='outdir' ,type=str, help='Specify path to the output directory. ')
    parser.add_argument('-k', metavar='shape' ,type=float, help='Specify Shape parameter for IIDGamma distribution for branch relaxation.', default=2.0)
    parser.add_argument('-t', metavar='theta' ,type=float, help='Specify Theta parameter for IIDGamma distribution for branch relaxation.', default=0.5)
    parser.add_argument('-n', metavar='ntrees' ,type=int, help='Specify the number of gene trees to be generated', default=100)
    parser.add_argument('-s', metavar='seed' ,type=int, help='Specify seed. default=121', default=121)
    
    args = parser.parse_args()
    
    sTree           = args.stree
    workDir        = args.O
    k               = args.k
    theta           = args.t
    nTrees          = args.n
    seed= args.s
    dup= args.d
    loss= args.l
    trans= args.tr
    jarFileName= args.j
    seed= args.s
    
    if workDir == None:
        workDir=tempfile.mkdtemp()
    elif os.path.exists(workDir) == False:
        os.mkdir(workDir)
        
    with open(workDir+"/simulateGTS.py."+str((datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-h%H-m%M-s%S')))+".info", 'w') as wf:
        wf.write("Jar File: %s\n" %(jarFileName))
        wf.write("Directory: %s\n" %(workDir))
        wf.write("Species tree: %s\n" %(sTree))
        wf.write("IIDGamma paramenter K: %f\n" %(k))
        wf.write("IIDGamma paramenter Theta: %f\n" %(theta))
        wf.write("Total gene tree: %d\n" %(nTrees))
        wf.write("Initial Seed: %d\n" %(seed))
        wf.write("Duplication rate: %f\n" %(dup))
        wf.write("Loss rate: %f\n" %(loss))
        wf.write("Loss rate: %f\n" %(trans))
        
    print "-->Simulation starts"
    minper = 0
    for i in xrange(1, nTrees+1):
        seed += 11
        
        if i < (0.1*nTrees):
            minper = 0
        elif i >(0.1*nTrees) and i < (0.3*nTrees):
            minper = 1
        elif i >(0.3*nTrees) and i < (0.6*nTrees):
            minper = 2
        elif i > (0.6*nTrees) and i < nTrees:
            minper = 3
        
        generateGTreesAndAlignmets(workDir, str(i), sTree, seed, dup, trans, loss, theta, k, minper, jarFileName)
    print "-->Simulation Done"

if __name__ == '__main__':
    main(sys.argv[1:])