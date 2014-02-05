from ..specs import Solution
from ..specs.cpp.base import CppBase

def clsname(_obj):
    ''' Returns the class name for an object, whether the object is an instance of the class or the class itself. '''
    try:
        return _obj.__name__
    except AttributeError:
        pass

    return _obj.__class__.__name__


class BaseGenerator(object):
    def Generate(self, _baseSpec, _opts):
        if issubclass(_baseSpec['cls'], CppBase):
            return self.GenerateCpp(_baseSpec, _opts)

        if issubclass(_baseSpec['cls'], Solution):
            return self.GenerateSln(_baseSpec, _opts)

        raise RuntimeError("Unable to run generator for type '%s'. This likely has not yet been implemented." % clsname(_baseSpec['cls']))

    def GenerateCpp(self, _baseSpec, _opts):
        raise NotImplementedError("The selected Generator %s does not yet support specifications of type '%s'." % 
                                  (clsname(self), clsname(_baseSpec['cls'])))

    def GenerateSln(self, _baseSpec, _opts):
        raise NotImplementedError("The selected Generator %s does not yet support specifications of type '%s'." % 
                                  (clsname(self), clsname(_baseSpec['cls'])))
