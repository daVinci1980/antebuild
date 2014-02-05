
import os

# -------------------------------------------------------------------------------------------------
def fixpath(_path, _opts):
    return os.path.normpath(os.path.join(_opts.pathPrefix, _path)) 