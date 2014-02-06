
import inspect
import os
import runpy
import specs

# -------------------------------------------------------------------------------------------------
def fixpath(_path, _opts):
    return os.path.normpath(os.path.join(_opts.pathPrefix, _path))

# -------------------------------------------------------------------------------------------------
def include(_path):
    cwd = os.getcwd()

    try:
        os.chdir(os.path.dirname(os.path.abspath(_path)))
        return _includeInternal(_path)
    except IOError:
        return _includeInternal(_path + ".ab")
    finally:
        os.chdir(cwd)

# -------------------------------------------------------------------------------------------------
def _includeInternal(_path):
    initGlobals = specs.getProjectGroupDict()
    initGlobals['include'] = include

    ignoreClasses = [c for c in initGlobals.itervalues() if inspect.isclass(c)]

    mod = runpy.run_path(_path, initGlobals)

    filteredMod = {}
    for k, v in mod.iteritems():
        if not inspect.isclass(v) or v not in ignoreClasses:
            filteredMod[k] = v

    return filteredMod
