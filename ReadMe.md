# simulateGTS: a frontend to GenPhyloData and Seq-Gen

Pre-requisites to simulateGTS.py:

1. Add path for seq-gen source:  `export PATH=/path/to/seq-gen/source-folder:$PATH`
2. Add path for jprime jar file: `export PATH=/path/to/jprime-X.X.X.jar:$PATH `
3. If needed, install Python module ArgParse: `pip install argparse`

## Options

``` 
$ python simulateGTS.py --help
usage: simulateGTS.py [-h] [-stree speciesTree] [-j jprime] [-d dup] [-l loss]
                      [-t trans] [-O outdir] [-k shape] [-theta theta]
                      [-n ntrees] [-s seed]
```
Parse input arguments and print output. NOTE: you need to ensure that
jprime jar file and seq-gen exe are in the path, see above.

Run `simulateGTS.py -h` to get details on options!

