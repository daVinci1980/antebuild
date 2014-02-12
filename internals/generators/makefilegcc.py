
import os
from textwrap import dedent

from base import BaseGenerator
from ..specs import Solution
from ..specs.cpp import DynamicLib, Executable, StaticLib 

class MakefileGCC(BaseGenerator):
    Description = "Makefiles for GCC"

    def GenerateCpp(self, _baseSpec, _opts):
        return [
            {
                'outputFilename': self.getMakefileFilename(_baseSpec),
                'outputContents': self.generateMakefile(_baseSpec, _opts)            
            }
        ]


    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def generateMakefileCommon(self, _baseSpec, _opts):
        MakefileContents = '''
        '''
        MakefileContents = dedent(MakefileContents)

        return MakefileContents

    def generateMakefile(self, _baseSpec, _opts):
        # TODO: This actually needs to come from the spec itself. 
        srcFiles = [s['filename'] for s in _baseSpec['sourcefiles']]
        objFiles = [("$(INTERMEDIATE_DIR)/%s.o" % o['objroot']) for o in _baseSpec['sourcefiles']]

        results = []
        results.append('# This is a generated Makefile. Do not modify by hand!')
        results.append('')

        results.append("PLATFORM ?= %s" % _baseSpec['platforms'][0])
        results.append("CONFIG ?= %s" % _baseSpec['configurations'][0])
        results.append("# TODO: This should be pulled from the project specification.")
        results.append("INTERMEDIATE_DIR := $(PLATFORM)/$(CONFIG)")
        results.append("# TODO: This should be pulled from the project specification.")
        results.append("FINAL_DIR := $(PLATFORM)/$(CONFIG)")
        results.append("FINAL_FILE := %s" % _baseSpec['filename'])
        results.append("FINAL_PATH := $(FINAL_DIR)/$(FINAL_FILE)")
        results.append("")
        results.append('VERBOSE ?= 0')
        results.append('ECHO := @echo ')
        results.append('')
        results.append('ifeq "$(VERBOSE)" "0"')
        results.append('  MAKE_SILENT := @')
        results.append('  MAKE_SILENT_SUFFIX := &> /dev/null')
        results.append('else')
        results.append('  MAKE_SILENT := ')
        results.append('  MAKE_SILENT_SUFFIX := ')
        results.append('endif')
        results.append('')
        results.append('IGNORE_FAILURE := || true')
        results.append('')
        results.append('OBJ_FILES := %s' % " ".join(objFiles))
        results.append('DEP_FILES := $(OBJ_FILES:%.o=%.d)')
        results.append('')
        results.append('LD := $(CC)')
        results.append('LDFLAGS := ')
        results.append('')
        results.append('all: $(FINAL_PATH)')
        results.append('')
        results.append('clean:')
        results.append('\t$(ECHO) ==== Cleaning object files and final target ====')
        results.append('\t$(MAKE_SILENT) rm -f $(INTERMEDIATE_DIR)/*.o $(MAKE_SILENT_SUFFIX)')
        results.append('\t$(MAKE_SILENT) rm -f $(FINAL_PATH) $(MAKE_SILENT_SUFFIX)')
        results.append('')
        results.append('cleandeps:')
        results.append('\t$(ECHO) ==== Cleaning dependency files ====')
        results.append('\t$(MAKE_SILENT) rm -f $(INTERMEDIATE_DIR)/*.d $(MAKE_SILENT_SUFFIX)')
        results.append('')
        results.append('clobber: clean cleandeps')
        results.append('\t$(ECHO) ==== Clobbering output directories ====')
        results.append('\t$(MAKE_SILENT) rmdir -p $(INTERMEDIATE_DIR) $(MAKE_SILENT_SUFFIX) $(IGNORE_FAILURE)')
        results.append('\t$(MAKE_SILENT) rmdir -p $(FINAL_DIR) $(MAKE_SILENT_SUFFIX) $(IGNORE_FAILURE)')
        results.append('')

        makefileFilename = self.getMakefileFilename(_baseSpec)
        for srcFile, objFile in zip(srcFiles, objFiles):
            results.append('%s: %s %s' % (objFile, srcFile, makefileFilename))
            results.append('\t$(ECHO) ==== Compiling $< ====')
            results.append('\t$(MAKE_SILENT) mkdir -p $(INTERMEDIATE_DIR)')
            results.append('\t$(MAKE_SILENT) $(CC) -c -o $@ $< $(CFLAGS) -MMD -MP')
            results.append('')

        results.append('$(FINAL_PATH) : $(OBJ_FILES)')
        results.append('\t$(ECHO) ==== Linking $@ ====')
        results.append('\t$(MAKE_SILENT) mkdir -p $(FINAL_DIR)')
        results.append('\t$(MAKE_SILENT) $(LD) -o $@ $^ $(LDFLAGS) ')
        results.append('')
        results.append('.PHONY: all clean cleandeps clobber')
        results.append('')
        results.append('.DEFAULT: all')
        results.append('')
        results.append('ifeq "$(filter clean cleandeps clobber,$(MAKECMDGOALS))" "$(MAKECMDGOALS)"')
        results.append('-include $(DEP_FILES)')
        results.append('endif')
 
        return "\n".join(results)

    def getMakefileFilename(self, _baseSpec):
        return "Makefile.gcc.%s" % (_baseSpec['filename'])
