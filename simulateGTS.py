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

def generateGTreesAndAlignmets(work_dir, outFile, sTree, seed, dup, trans, loss, theta, k, minper, msa_len, jarFileName):
    '''
    this function will call GenPhyloData to generate gtrees and the call seq-gen to generate sequences
    '''

    logfilename=os.path.join(work_dir, outFile + ".log")
    logfile=open(logfilename, "w") or die("Could not create file '" + logfilename + "'")
    # check if path exists
    cmd= Where(jarFileName)
    if cmd != None:
        gTree= os.path.join(work_dir, outFile)
        brGTree= os.path.join(work_dir, outFile+".relaxed.tree")
        print "--> GenPhyloData " + outFile
        try:
            subprocess.call("java -jar "+cmd+ " GuestTreeGen -s "+ str(seed) + " -minper "+str(minper)+" -max 1000 -a 10000000 "+ sTree+ " "+ str(dup) + " "+ str(loss)+ " "+ str(trans) +" "+ gTree, shell=(sys.platform!="win32"), stdout=True, stderr=logfile)
            
        except IOError, e:
            print ("Function: generateGTreesAndAlignmets: %s " % e)
        print "--> Branch Relaxation"
        try:
            seed += 11
            #varying branch length
            subprocess.call("java -jar "+cmd+ " BranchRelaxer -s "+ str(seed) + " "+ gTree+".pruned.tree " +"IIDGamma "+ str(k)+ " "+ str(theta) +" -o " +brGTree, shell=(sys.platform!="win32"), stdout=True, stderr=logfile)
            subprocess.call("java -jar "+cmd+ " BranchRelaxer -x -innms -s "+ str(seed) + " "+ gTree+".pruned.tree " +"IIDGamma "+ str(k)+ " "+ str(theta) +" -o " +brGTree+".no.primeid", shell=(sys.platform!="win32"), stdout=True, stderr=logfile)
            # for constant rates
            #subprocess.call("java -jar "+cmd+ " BranchRelaxer -s "+ str(seed) + " "+ gTree+".pruned.tree " +"Constant "+ str(1)+" -o " +brGTree, shell=(sys.platform!="win32"), stdout=True, stderr=logfile)
            #subprocess.call("java -jar "+cmd+ " BranchRelaxer -x -innms -s "+ str(seed) + " "+ gTree+".pruned.tree " +"Constant "+ str(1)+" -o " +brGTree+".no.primeid", shell=(sys.platform!="win32"), stdout=True, stderr=logfile)
            
        except IOError, e:
            print ("Function: generateGTreesAndAlignmets: %s " % e)
        
    else:
        print("generateGTreesAndAlignments: Error: Path to JPrIme.jar is not set ") 
        sys.exit()
        
        
    cmd= Where('seq-gen')
    if cmd != None:
        seed += 11
        subprocess.call(cmd+ " -mJTT -z "+ str(seed) + " -l " + str(msa_len) + " < "+ brGTree +" > "+ work_dir+"/"+outFile+".phylip", shell=(sys.platform!="win32"), stdout=False, stderr=logfile)
        
    else:
        print ("generateGTreesAndAlignmets: Error: Path to seq-gen is not set ") 
        sys.exit()
    logfile.close()
        
def main(argv):
    parser = argparse.ArgumentParser(description="Parse input arguments and print output. NOTE: you need to export poath to jprime jar file and seq-gen exe.")
    parser.add_argument('-H', metavar='treefile' ,type=str, help='Specify path to the host (species) tree file. ')
    parser.add_argument('-j', metavar='jprime' ,type=str, help='Specify the name of the jprime jar file i.e. jprime-0.3.5.jar.')
    parser.add_argument('-d', metavar='dup' ,type=float, help='Specify duplication rate.default=0.5', default=0.5)
    parser.add_argument('-l', metavar='loss' ,type=float, help='Specify loss rate. Default=0.5', default=0.5)
    parser.add_argument('-t', metavar='trans' ,type=float, help='Specify transfer rate. Default=0.5', default=0.5)
    parser.add_argument('-m', metavar='msa_len', type=int, help='Specify alignment (sequence) length', default=1000)
    parser.add_argument('-O', metavar='outdir' ,type=str, help='Specify path to the output directory. ')
    parser.add_argument('-k', metavar='shape' ,type=float, help='Specify Shape parameter for IIDGamma distribution for branch relaxation.', default=2.0)
    parser.add_argument('-theta', metavar='theta' ,type=float, help='Specify Theta parameter for IIDGamma distribution for branch relaxation.', default=0.5)
    parser.add_argument('-n', metavar='ntrees' ,type=int, help='Specify the number of gene trees to be generated', default=100)
    parser.add_argument('-s', metavar='seed' ,type=int, help='Specify seed. default=121', default=121)
    parser.add_argument('-mingenesperleaf', metavar='n', type=int, help='Minimum number of genes per leaf in the host tree.', default=1)
    
    args = parser.parse_args()
    
    sTree           = args.H
    workDir        = args.O
    k               = args.k
    theta           = args.theta
    nTrees          = args.n
    seed= args.s
    dup= args.d
    loss= args.l
    trans= args.t
    msa_len= args.m
    jarFileName= args.j
    seed= args.s
    min_per_leaf=args.mingenesperleaf
    
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
        wf.write("Trans rate: %f\n" %(trans))
        wf.write("MSA length: %d\n" %(msa_len))        
        
#    print "-->Simulation starts"
    for i in xrange(1, nTrees+1):
        seed += 11
        generateGTreesAndAlignmets(workDir, str(i), sTree, seed, dup, trans, loss, theta, k, min_per_leaf, msa_len, jarFileName)
#    print "-->Simulation Done"

if __name__ == '__main__':
    main(sys.argv[1:])
