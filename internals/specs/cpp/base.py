
from .. import base
import copy
import os
import uuid
from ...utils import fixpath

# -------------------------------------------------------------------------------------------------
class CppBase(base.SpecBase):
    ''' The base class for all Cpp productions.

    Attributes:
        SourceSuffixes          A list of suffixes that identify C/C++ source files

        HeaderSuffixes          A list of suffixes that identify C/C++ header files

        SourceGroups            (Optional) A specification of source (and header files), 
                                separated into groups.

        Configurations          A list of Configurations to be output by the Generator.
        DefaultConfiguration    The value for the default configuration when building.

        Platforms               A list of Platforms (bittedness) to be output as a target.
        DefaultPlatform         The value for the default platform when building.

        IntermediateDirectory   The directory to write intermediate files (.o, .obj, etc) to.

        OutputDirectory         The directory to write final output to.
    '''

    SourceSuffixes = [ ".c", ".cpp" ]
    HeaderSuffixes = [ ".h", ".hpp" ]

    SourceGroups = None

    Configurations = [ "Release", "Debug" ]
    DefaultConfiguration = None

    Platforms = [ "x64", "x86" ]
    DefaultPlatform = None

    IntermediateDirectory = "${Platform}/${Configuration}"
    OutputDirectory = "${Platform}/${Configuration}"

    IncludeDirectories = [ '.' ]

    Defines = [ ]

    DisabledWarnings = [ ]

    PrecompiledHeader = None

    def FullySpecify(self, _opts):
        # TODO TODO TODO
        # TODO: I think this should be a clsmethod that returns an instance of this object, 
        # all filled out. Rather than a dictionary. 

        retDict = super(CppBase, self).FullySpecify(_opts)
        retDict['name'] = self.__class__.__name__        
        retDict['filename'] = self.__class__.__name__.lower()
        retDict['platforms'] = self.Platforms[:]
        retDict['configurations'] = self.Configurations[:]

        sourceFiles = []
        headerFiles = []
        looseFiles = []
        for group, filelist in self.SourceGroups.iteritems():
            for filename in filelist:
                srcFilename = fixpath(filename, _opts)
                objRoot = os.path.splitext(os.path.basename(srcFilename))[0]

                fileDict = { "filename": srcFilename, "objroot": objRoot, "group": group }
                if os.path.splitext(filename)[1] in self.SourceSuffixes:
                    sourceFiles.append(fileDict)
                elif os.path.splitext(filename)[1] in self.HeaderSuffixes:
                    headerFiles.append(fileDict)
                else:
                    looseFiles.append(fileDict)

        includeDirs = [fixpath(incl, _opts) for incl in self.IncludeDirectories]

        retDict['sourcefiles'] = sourceFiles
        retDict['headerfiles'] = headerFiles
        retDict['loosefiles'] = looseFiles
        retDict['guid'] = str(uuid.uuid4())
        retDict['includedirs'] = includeDirs
        retDict['optimizationstrategy'] = "MaximizeSpeed"
        retDict['defines'] = self.Defines[:]
        retDict['disabledwarnings'] = self.DisabledWarnings[:]
        if self.PrecompiledHeader is not None:
            retDict['precompiledheader'] = copy.copy(self.PrecompiledHeader) 
            retDict['precompiledheader']['CompileFrom'] = fixpath(retDict['precompiledheader']['CompileFrom'], _opts)
            retDict['precompiledheader']['Prefix'] = fixpath(retDict['precompiledheader']['Prefix'], _opts)
        else:
            retDict['precompiledheader'] = None

        groups = []
        for name in self.SourceGroups.iterkeys():
            groupDefn = { 'name': name, 'guid': str(uuid.uuid4()) }
            groups.append(groupDefn)

        retDict['groups'] = groups

        return retDict

