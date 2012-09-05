# We will be using py2exe to build the binaries.
# You may use other tools, but I know this one.

from distutils.core import setup
import py2exe, sys, os
# Now you need to pass arguments to setup
# windows is a list of scripts that have their own UI and
# thus don't need to run in a console.

#sorta works
includes=['os','scipy.sparse.csgraph._validation','sip','PyQt4.QtNetwork']
excludes=[]
packages=['gzip']
dll_excludes=["MSVCP90.dll","MSWSOCK.dll","mswsock.dll","powrprof.dll"]

setup(
    options={"py2exe":{"compressed":0,
                       "optimize":2,
                       "includes":includes,
                       "excludes":excludes,
                       "packages":packages,
                       "dll_excludes":dll_excludes,
                       "bundle_files":3,
                       "dist_dir":'dist',
                       "xref":False,
                       "skip_archive":True,
                       "ascii":False,
                       "custom_boot_script":'',
                       }
             },
    windows=['SerialReaderInterface.py']
    )
