#!/usr/bin/env python

import argparse
import inspect
import os
import runpy
import sys
import traceback

from internals import specs, generators

# -------------------------------------------------------------------------------------------------
def loadBuildTemplate(_opts):

    filePath = _opts.inputFile
    if os.path.isdir(filePath):
        filePath = os.path.join(filePath, "Antebuild")

    initGlobals = specs.getProjectGroupDict()
    mod = runpy.run_path(filePath, initGlobals)

    return mod, initGlobals

# -------------------------------------------------------------------------------------------------
def processTemplate(_rootModule, _initGlobals, _opts):
    ignoreClasses = [c for c in _initGlobals.itervalues() if inspect.isclass(c)]

    usefulClasses = [c for c in _rootModule.itervalues() if inspect.isclass(c) and c not in ignoreClasses]
    specs = []
    for cls in usefulClasses:
        instance = cls()
        specs.append(instance.FullySpecify())

    return specs

# -------------------------------------------------------------------------------------------------
def generate(_buildSpecs, _opts):
    generator = generators.getGeneratorDict()[_opts.generator]
    
    for bs in _buildSpecs:
        results = generator().Generate(bs)
        for result in results:
            pathName = os.path.join(_opts.outDir, result["outputFilename"])
            open(pathName, "wb").write(result["outputContents"])

# -------------------------------------------------------------------------------------------------
def parseArgs(_argv):
    description=''' Generates builds for multiple platforms from simple specifications. '''
    parser = argparse.ArgumentParser(description=description, 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("inputFile", default="./Antebuild", nargs="?", 
                        help="The name of the build specification.")

    parser.add_argument("-g", "--generator", default="Msvs2013",
                        help="Which generator to use. A list of valid generators is included below.")

    parser.add_argument("-o", "--outDir", default=".",
                        help="Where to output the results of generation.")

    try:
        return parser.parse_args(_argv)
    except SystemExit:
        print("\nThe generators are as follows:")
        print(generators.getGeneratorListString())
        print("")
        raise

# -------------------------------------------------------------------------------------------------
def main(argv=None):
    try:
        opts = parseArgs(argv)
        rootModule, initGlobals = loadBuildTemplate(opts)
        buildSpecs = processTemplate(rootModule, initGlobals, opts)
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