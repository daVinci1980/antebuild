
from base import SpecBase
import uuid

class Solution(SpecBase):
    ''' The base class for all Cpp productions.

    Attributes:
        Projects                A list of child projects--they will be FullySpecified before this.
    '''

    Projects = []

    def FullySpecify(self, _opts):
        retDict = super(Solution, self).FullySpecify(_opts)

        retDict['name'] = self.__class__.__name__        
        retDict['filename'] = self.__class__.__name__.lower()
        retDict['guid'] = str(uuid.uuid4())

        retProjects = []
        configurations = set()
        platforms = set()

        for projSpec in self.Projects:
            inst = projSpec()
            retProjects.append(inst.FullySpecify(_opts))
            configurations.update(retProjects[-1]['configurations'])
            platforms.update(retProjects[-1]['platforms'])

        retDict['projects'] = retProjects
        retDict['configurations'] = list(configurations)
        retDict['platforms'] = list(platforms)

        return retDict
        