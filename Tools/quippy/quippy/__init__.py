"""quippy package

James Kermode <james.kermode@kcl.ac.uk>

Contains python bindings to the libAtoms/QUIP F95 codes
<http://www.libatoms.org>. """

import _quippy

import sys, cPickle, atexit, os, numpy, logging

from numpy import *

logging.root.setLevel(logging.WARNING)

from oo_fortran import FortranDerivedType, FortranDerivedTypes, fortran_class_prefix, wrap_all

# Read spec file generated by f90doc and construct wrappers for classes
# and routines found therein.

def quippy_cleanup():
   _quippy.system.verbosity_pop()
   _quippy.system.system_finalise()

_quippy.system.system_initialise(-1)
_quippy.system.verbosity_push(0)
atexit.register(quippy_cleanup)

spec = cPickle.load(open(os.path.join(os.path.dirname(__file__),'quippy.spec')))

classes, routines, params = wrap_all(_quippy, spec, spec['wrap_modules'], spec['short_names'])

for name, cls in classes:
   setattr(sys.modules[__name__], name, cls)

for name, routine in routines:
   setattr(sys.modules[__name__], name, routine)

sys.modules[__name__].__dict__.update(params)

AtomsReaders = {}
AtomsWriters = {}

import extras
for name, cls in classes:
   try:
      new_cls = getattr(extras, name[len(fortran_class_prefix):])
   except AttributeError:
      new_cls = type(object)(name[len(fortran_class_prefix):], (cls,), {})
      
   setattr(sys.modules[__name__], name[len(fortran_class_prefix):], new_cls)
   FortranDerivedTypes['type(%s)' % name[len(fortran_class_prefix):].lower()] = new_cls


del classes
del routines
del params
del wrap_all
del extras
del fortran_class_prefix
                      
from farray import *
from atomslist import *

# Convert periodic table arrays
ElementName = farray([s.strip() for s in ElementName[2:]])
ElementMass = dict(zip(ElementName,ElementMass))
ElementCovRad = dict(zip(ElementName,ElementCovRad))

import atomeye, castep

from paramreader import *

