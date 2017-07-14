from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
             Extension("prun",       ["prun.py"]),
             Extension("prun2",         ["prun2.py"]),
             Extension("prunning",         ["prunning.py"]),
             Extension("prunconnected",         ["prunconnected.py"]),
             ]

setup(
      cmdclass = {'build_ext': build_ext},
      ext_modules = ext_modules,
      )
