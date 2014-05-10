#!/usr/bin/env python

import argparse
import inspect
import os
import sys
import traceback

from internals import generators, specs, utils

# -------------------------------------------------------------------------------------------------
def loadBuildTemplate(_opts):
    return utils.include(_opts.inputFile)

# -------------------------------------------------------------------------------------------------
def processTemplate(_rootModule, _opts):
    specs = []
    for cls in _rootModule.itervalues():
        if inspect.isclass(cls):
            instance = cls()
            specs.append(instance.FullySpecify(_opts))

    return specs

# -------------------------------------------------------------------------------------------------
def generate(_buildSpecs, _opts):
    generator = generators.getGeneratorDict()[_opts.generator]
    
    for bs in _buildSpecs:
        results = generator().Generate(bs, _opts)
        for result in results:
            pathName = os.path.join(_opts.outDir, result["outputFilename"])
            open(pathName, "wb").write(result["outputContents"])

# -------------------------------------------------------------------------------------------------
def parseArgs(_argv):
    description=''' Generates builds for multiple platforms from simple specifications. '''
    parser = argparse.ArgumentParser(description=description, 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-g", "--generator", default="msvs2013",
                        help="Which generator to use. A list of valid generators is included below.")

    parser.add_argument("-o", "--outDir", default=".",
                        help="Where to output the results of generation.")

    parser.add_argument("inputFile", default="./Antebuild", nargs="?", 
                        help="The name of the build specification.")    

    try:
        retArgs = parser.parse_args(_argv[1:])
        if os.path.isdir(retArgs.inputFile):
            retArgs.inputFile = os.path.join(retArgs.inputFile, "Antebuild")

        retArgs.pathPrefix = os.path.relpath(os.path.dirname(retArgs.inputFile), retArgs.outDir)
        retArgs.argv = _argv[:]
        
        return retArgs
    except SystemExit:
        print("\nThe generators are as follows:")
        print(generators.getGeneratorListString())
        print("")
        raise

# -------------------------------------------------------------------------------------------------
def main(argv=None):
    try:
        argv = argv if argv is not None else sys.argv[:]
        opts = parseArgs(argv)
        rootModule = loadBuildTemplate(opts)
        buildSpecs = processTemplate(rootModule, opts)
        generate(buildSpecs, opts)
    except SystemExit:
        raise
    except:
        traceback.print_exc()
        return -1

    return 0

# -------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())