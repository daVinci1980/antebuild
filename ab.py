#!/usr/bin/env python

import inspect
import runpy
import sys

from internals.specs import c, cpp, Solution
from internals.generators.msvs2013 import Msvs2013

# -------------------------------------------------------------------------------------------------
def loadBuildTemplate(_filename):
    initGlobals = { 
        "c": c, 
        "cpp": cpp, 
        "Solution": Solution 
    }

    mod = runpy.run_path("Antebuild", initGlobals)
    return mod, initGlobals

# -------------------------------------------------------------------------------------------------
def processTemplate(_rootModule, _initGlobals):
    ignoreClasses = [c for c in _initGlobals.itervalues() if inspect.isclass(c)]

    usefulClasses = [c for c in _rootModule.itervalues() if inspect.isclass(c) and c not in ignoreClasses]
    for cls in usefulClasses:
        instance = cls()
        specification = instance.FullySpecify()

        # Here's where we would select the generator, but right now I am just hardcoding it.
        print(Msvs2013().Generate(specification)[0]['outputContents'])



# -------------------------------------------------------------------------------------------------
def generate(_buildSpec):
    pass    

# -------------------------------------------------------------------------------------------------
def main(argv=None):
    rootModule, initGlobals = loadBuildTemplate("Antebuild")
    buildSpec = processTemplate(rootModule, initGlobals)
    generate(buildSpec)

    return 0

# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    sys.exit(main())