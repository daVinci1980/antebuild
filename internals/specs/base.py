
class SpecBase(object):
    def FullySpecify(self, _opts):
        ''' Called to turn a shorthand Spec into a fully-fleshed specification, suitable for Generation. '''
        return { 
            'cls': self.__class__ 
        }
