import CAPI
import json

def stringify(obj):
  return json.dumps(normalizeForUnitTests(typeToDict(obj)))

# for unit tests only, make floats use same precision across different
# versions of python which have different repr() implementations and
# change dicts to sorted lists so ordering doesn't change
def normalizeForUnitTests( obj ):
  if type( obj ) is list:
    objlist = []
    for elem in obj:
      objlist.append( normalizeForUnitTests( elem ) )
    return objlist
  elif type( obj ) is dict:
    objdictlist = []
    for member in obj:
      elemobj = {}
      elemobj[ member ] = normalizeForUnitTests( obj[ member ] )
      objdictlist.append( elemobj )
    objdictlist.sort()
    return objdictlist
  elif type( obj ) is float:
    return format( obj, '.3f' )
  else:
    return obj

# take a python class and convert its members down to a hierarchy of
# dictionaries, ignoring methods
def typeToDict(obj):
  if type(obj) is list:
    objlist = []
    for elem in obj:
      objlist.append(typeToDict(elem))
    return objlist

  elif type(obj) is dict:
    objdict = {}
    for member in obj:
      objdict[member] = typeToDict(obj[member])
    return objdict

  elif not hasattr(obj, '__dict__'):
    return obj

  else:
    objdict = {}
    for member in vars(obj):
      attr = getattr(obj, member)
      objdict[member] = typeToDict(attr)
    return objdict

def typeToVariant(obj):
  v = CAPI.Variant()
  CAPI.PyObjectToVariant(obj, v)
  return v

def variantToPyObject(v):
  return CAPI.VariantToPyObject(v)

def rtValToPyObject(context, rtVal):
  return CAPI.RTValToPyObject(context, rtVal)

def pyObjectToRTVal(context, rtVal):
  return CAPI.PyObjectToRTVal(context, rtVal)

def createPyRTTypesObject(context):
  return CAPI.CreatePyRTTypesObject(context)
