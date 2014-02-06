
from base import BaseGenerator
from ..specs import Solution
from ..specs.cpp import DynamicLib, Executable, StaticLib 

class Msvs2013(BaseGenerator):
    Description = "Visual Studio 2013"

    def GenerateCpp(self, _baseSpec, _opts):
        return [
            { 
                'outputFilename': "%s.vcxproj" % (_baseSpec['filename']),
                'outputContents': self.generateVcxproj(_baseSpec, _opts)
            },
            {
                'outputFilename': "%s.vcxproj.filters" % (_baseSpec['filename']),
                'outputContents': self.generateVcxprojFilters(_baseSpec, _opts)            
            }
        ]

    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def generateVcxproj(self, _baseSpec, _opts):
        results = []
        # First, boilerplate.
        results.append('<?xml version="1.0" encoding="utf-8"?>')
        results.append('<Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schema.microsoft.com/developer/msbuild/2003">')

        # Then the list of build project configurations
        results.append('  <ItemGroup Label="ProjectConfigurations">')
        for platform in _baseSpec['platforms']:
            for config in _baseSpec['configurations']:
                results.append('    <ProjectConfiguration Include="%s|%s">' % (config, platform))
                results.append('      <Configuration>%s</Configuration>' % config)
                results.append('      <Platform>%s</Platform>' % platform)
                results.append('    </ProjectConfiguration>')
        results.append('  </ItemGroup>')

        # Up next are the files.
        # TODO: Libraries
        FileGroups = (
            { "specsrc": "headerfiles", "outattrib": "ClInclude"},
            { "specsrc": "sourcefiles", "outattrib": "ClCompile"},
            { "specsrc": "loosefiles",  "outattrib": "None"},
        )

        for fg in FileGroups:
            if len(_baseSpec[fg['specsrc']]):
                results.append('  <ItemGroup>')
                for incl in _baseSpec[fg['specsrc']]:
                    results.append('    <%s Include="%s" />' % (fg['outattrib'], incl['filename']))
                results.append('  </ItemGroup>')

        # Now, the globals.
        results.append('  <PropertyGroup Label="Globals">')
        results.append('    <ProjectGuid>%s</ProjectGuid>' % _baseSpec['guid'])
        results.append('    <Keyword>Win32Proj</Keyword>')
        results.append('    <RootNamespace>%s</RootNamespace>' % _baseSpec['name'])
        results.append('  </PropertyGroup>')
        results.append('  <Import Project=$(VCTargetsPath)\\Microsoft.Cpp.Default.props" />')

        # Up next, the basic configuration settings.
        for platform in _baseSpec['platforms']:
            for config in _baseSpec['configurations']:
                results.append('''  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='%s|%s'" Label="Configuration">''' % (config, platform))
                results.append('''    <ConfigurationType>%s</ConfigurationType>''' % (self.getConfigurationType(_baseSpec, config, platform)))
                results.append('''    <UseDebugLibraries>%s</UseDebugLibraries>''' % ("true" if config == 'Debug' else "false"))
                results.append('''    <PlatformToolset>v110</PlatformToolset>''')
                if config == 'Release':
                    results.append('''    <WholeProgramOptimization>true</WholeProgramOptimization>''')
                results.append('''    <CharacterSet>NotSet</CharacterSet>''')
                results.append('''  </PropertyGroup>''')

        # A bit more boilerplate.
        results.append('  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.props" />')
        results.append('  <ImportGroup Label="ExtensionSettings">')
        results.append('  </ImportGroup>')

        # Allow for user Property Sheets.
        for platform in _baseSpec['platforms']:
            for config in _baseSpec['configurations']:
                results.append('''  <ImportGroup Condition="'$(Configuration)|$(Platform)'=='%s|%s'" Label="PropertySheets">''' % (config, platform))
                results.append('''    <Import Project="$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props"''' + \
                                       ''' Condition="exists('$(UserRootDir)\\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />''')
                results.append('''  </ImportGroup>''')

        # lol macros. Yeah. Does anyone use this feature? I hates them.
        results.append('  <PropertyGroup Label="UserMacros" />')

        # Now some basic linking settings.
        for platform in _baseSpec['platforms']:
            for config in _baseSpec['configurations']:
                results.append('''  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='%s|%s'">''' % (config, platform))
                results.append('''    <LinkIncremental>%s</LinkIncremental>''' % ("true" if config == 'Debug' else "false"))
                results.append('''    <IncludePath>%s</IncludePath>''' % self.getIncludePath(_baseSpec, config, platform))
                results.append('''  </PropertyGroup>''')

        # Now compile and link settings. I have no idea why VS doesn't include the above linking settings here--it's just
        # what shows up in my exemplar. I'm happy to accept patches in this regard.
        for platform in _baseSpec['platforms']:
            for config in _baseSpec['configurations']:
                results.append('''  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='%s|%s'">''' % (config, platform))
                results.append('''    <ClCompile>''')
                results.append('''      <PrecompiledHeader>''')
                results.append('''      </PrecompiledHeader>''')
                results.append('''      <WarningLevel>%s</WarningLevel>''' % (self.getWarningLevel(_baseSpec, config, platform)))
                results.append('''      <Optimization>%s</Optimization>''' % (self.getOptimizationStrategy(_baseSpec, config, platform)))
                if config == 'Release':
                    results.append('''      <FunctionLevelLinking>true</FunctionLevelLinking>''')
                    results.append('''      <IntrinsicFunctions>true</IntrinsicFunctions>''')
                results.append('''      <PreprocessorDefinitions>%s</PreprocessorDefinitions>''' % (self.getPreprocessorDefines(_baseSpec, config, platform)))
                results.append('''      <AdditionalIncludeDirectories>''')
                results.append('''      </AdditionalIncludeDirectories>''')
                if len(_baseSpec['disabledwarnings']):
                    results.append('''      <DisableSpecificWarnings>%s</DisableSpecificWarnings>''' % (self.getDisabledWarnings(_baseSpec, config, platform)))
                results.append('''    </ClCompile>''')
                results.append('''    <Link>''')
                results.append('''      <SubSystem>%s</SubSystem>''' % (self.getSubSystem(_baseSpec, config, platform)))
                results.append('''      <GenerateDebugInfo>true</GenerateDebugInfo>''')
                if config == 'Release':
                    results.append('''      <EnableCOMDATFolding>true</EnableCOMDATFolding>''')
                    results.append('''      <OptimizeReferences>true</OptimizeReferences>''')
                results.append('''    </Link>''')
                results.append('''  </ItemDefinitionGroup>''')

        # Final boilerplate!
        results.append('  <Import Project="$(VCTargetsPath)\\Microsoft.Cpp.targets" />')
        results.append('  <ImportGroup Label="ExtensionTargets">')
        results.append('  </ImportGroup>')

        # Boom!
        results.append('</Project>\n')

        # Now turn our array of lines into a single string.
        return "\n".join(results)

    # -----------------------------------------------------------------------------------------------------------------
    def generateVcxprojFilters(self, _baseSpec, _opts):
        results = []
        # First, boilerplate.
        results.append('<?xml version="1.0" encoding="utf-8"?>')
        results.append('<Project ToolsVersion="4.0" xmlns="http://schema.microsoft.com/developer/msbuild/2003">')

        if len(_baseSpec['groups']):
            results.append('  <ItemGroup>')
            for group in _baseSpec['groups']:
                results.append('    <Filter Include="%s">' % (group['name']))
                results.append('      <UniqueIdentifier>%s</UniqueIdentifier>' % (group['guid']))
                results.append('    </Filter>')
            results.append('  </ItemGroup>')


        # TODO: This code is copy/pasted from above--we should factor it into something common.
        FileGroups = (
            { "specsrc": "headerfiles", "outattrib": "ClInclude"},
            { "specsrc": "sourcefiles", "outattrib": "ClCompile"},
            { "specsrc": "loosefiles", "outattrib": "None"},
        )

        for fg in FileGroups:
            if len(_baseSpec[fg['specsrc']]):
                results.append('  <ItemGroup>')
                for incl in _baseSpec[fg['specsrc']]:
                    if incl['group'] is not None:
                        results.append('    <%s Include="%s">' % (fg['outattrib'], incl['filename']))
                        results.append('      <Filter>%s</Filter>' % (incl['group']))
                        results.append('    </%s>' % (fg['outattrib']))
                    else:
                        results.append('    <%s Include="%s" />' % (fg['outattrib'], incl['filename']))
                results.append('  </ItemGroup>')

        results.append('</Project>\n')

        # Now turn our array of lines into a single string.
        return "\n".join(results)

    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def getConfigurationType(self, _baseSpec, _config, _platform):
        if issubclass(_baseSpec['cls'], Executable):
            return 'Application'

        raise NotImplementedError("impl")

    # -----------------------------------------------------------------------------------------------------------------
    def getDisabledWarnings(self, _baseSpec, _config, _platform):
        return ":".join(_baseSpec['disabledwarnings'])

    # -----------------------------------------------------------------------------------------------------------------
    def getIncludePath(self, _baseSpec, _config, _platform):
        finalIncludePath = _baseSpec["includedirs"][:]
        finalIncludePath.append("$(IncludePath)")
        return ";".join(finalIncludePath)

    # -----------------------------------------------------------------------------------------------------------------
    def getOptimizationStrategy(self, _baseSpec, _config, _platform):
        return _baseSpec["optimizationstrategy"]

    # -----------------------------------------------------------------------------------------------------------------
    def getPreprocessorDefines(self, _baseSpec, _config, _platform):
        DEBUG_DEFINE = "DEBUG" if _config == 'Debug' else "NDEBUG"
        defineList = [ "WIN32", DEBUG_DEFINE, "_WINDOWS" ]
        defineList.extend(_baseSpec['defines'])
        defineList.append("%(PreprocessorDefinitions)")
        return ";".join(defineList)

    # -----------------------------------------------------------------------------------------------------------------
    def getSubSystem(self, _baseSpec, _config, _platform):
        return "Windows"

    # -----------------------------------------------------------------------------------------------------------------
    def getWarningLevel(self, _baseSpec, _config, _platform):
        # TODO: Something better.
        return "Level3"
