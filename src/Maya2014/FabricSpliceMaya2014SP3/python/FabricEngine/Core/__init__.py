#
# Fabric Engine 1.12
# Python FabricEngine.Core __init__.py
#
# Copyright 2010-2013 Fabric Engine Inc. All rights reserved.
#

__version__ = "1.12.0"
__version_info__ = (1, 12, 0, "", 1)

import CAPI
import Util
import atexit
import sys

def createClient(opts=None):
  client = _FabricClient(opts)
  _FabricClient._clients.append(client)
  return client

def enableDebug(runServer=True):
  CAPI.EnableDebug( runServer )

def __closeOutstandingClients():
  for client in _FabricClient._clients:
    client.close()
atexit.register(__closeOutstandingClients)

def stringify(obj):
  return Util.stringify(obj)

class _FabricClient(object):
  _clients = []

  def __init__(self, opts):
    if opts is not None and type(opts) is not dict:
      raise Exception('client options must be a dict')
      
    if opts is not None and 'reportCallback' in opts:
      reportCallback = opts['reportCallback']
    else:
      def reportCallback(msg):
        print msg
    
    if opts is not None and 'contextID' in opts:
      self._client = CAPI.Client.Create(
        reportCallback,
        opts['contextID']
        )
    else:
      createOptions = {}
      
      createOptions['guarded'] = 0
      if opts is not None and 'guarded' in opts:
        createOptions['guarded'] = bool(opts['guarded'])
      
      createOptions['traceOperators'] = 0
      if opts is not None and 'trace' in opts:
        createOptions['traceOperators'] = bool(opts['trace'])
      
      createOptions['extsToLoad'] = []
      if opts is not None and 'exts' in opts:
        if isinstance(opts['exts'], dict):
          for extName, extVersion in opts['exts'].iteritems():
            createOptions['extsToLoad'].append(extName)
        elif isinstance(opts['exts'], list):
          for extName in opts['exts']:
            createOptions['extsToLoad'].append(extName)
        else:
          raise "opts['exts']: must be a list or a dict"
      
      createOptions['extPaths'] = []
      if opts is not None and 'extPaths' in opts:
        for extPath in opts['extPaths']:
          createOptions['extPaths'].append(extPath)
      
      createOptions['optimizationType'] = CAPI.ClientOptimizationType_Background
      if opts is not None and 'optimizeSynchronously' in opts:
        if opts['optimizeSynchronously']:
          createOptions['optimizationType'] = CAPI.ClientOptimizationType_Synchronous
      if opts is not None and 'noOptimization' in opts:
        if opts['noOptimization']:
          createOptions['optimizationType'] = CAPI.ClientOptimizationType_None
      
      self._client = CAPI.Client.Create(
        reportCallback,
        createOptions
        )

    self.DG = _DG(self._client, self)
    self.DependencyGraph = self.DG
    self.RT = _RT(self._client)
    self.RegisteredTypesManager = self.RT
    self.build = _Build()
    
    self.userData = {}

  def close(self):
    if self in _FabricClient._clients:
      _FabricClient._clients.remove(self)
    self.DependencyGraph = None
    self.DG = None
    self.RegisteredTypesManager = None
    self.RT = None
    self.build = None
    self._client = None

  def isClosed(self):
    return self._client == None

  def loadExtension(self, extension):
    return self._client.loadExtension(extension)
    
  # automatically proxy non-existent methods to the client
  def __getattr__(self, attr):
    return getattr(self._client, attr)

  def getMemoryUsage(self):
    v = self._client.getMemoryUsage_Variant()
    return Util.variantToPyObject(v)

  def stopInstrumentation(self, rtype = None):
    if rtype is None:
      v = self._client.stopInstrumentation_Variant()
    else:
      v = self._client.stopInstrumentation_Variant(rtype)
    return Util.variantToPyObject(v)[0]
  
  def adoptCurrentGLContext(self):
    if self._client:
      self._client.adoptCurrentGLContext()

  def registerKLExtension(self, extensionName, sourceFiles):
    CAPI.RegisterKLExtension(
      self._client,
      extensionName,
      sourceFiles
      )

class _DG(object):
  def __init__(self, client, fc):
    self._client = client
    self._fc = fc

  def createBinding(self):
    o = CAPI.DGBinding(self._client)
    CAPI._wrapSceneGraphObject(self._fc, o)
    return o

  def createNode(self, name):
    o = CAPI.DGNode(self._client, str(name))
    CAPI._wrapSceneGraphObject(self._fc, o)
    return o

  def createOperator(self, name):
    o = CAPI.DGOperator(self._client, str(name))
    CAPI._wrapSceneGraphObject(self._fc, o)
    return o

  def createEvent(self, name):
    o = CAPI.DGEvent(self._client, str(name))
    CAPI._wrapSceneGraphObject(self._fc, o)
    return o

  def createEventHandler(self, name):
    o = CAPI.DGEventHandler(self._client, str(name))
    CAPI._wrapSceneGraphObject(self._fc, o)
    return o

  def getNodeByName(self, name):
    o = CAPI.DGNode.GetByName(self._client, name)
    CAPI._wrapSceneGraphObject(self._fc, o)
    return o

  def getOperatorByName(self, name):
    o = CAPI.DGOperator.GetByName(self._client, name)
    CAPI._wrapSceneGraphObject(self._fc, o)
    return o

  def getEventByName(self, name):
    o = CAPI.DGEvent.GetByName(self._client, name)
    CAPI._wrapSceneGraphObject(self._fc, o)
    return o

  def getEventHandlerByName(self, name):
    o = CAPI.DGEventHandler.GetByName(self._client, name)
    CAPI._wrapSceneGraphObject(self._fc, o)
    return o

class _RT(object):
  def __init__(self, client):
    self._client = client
    self._registeredTypes = {}
    self._prototypes = {}
    self.types = Util.createPyRTTypesObject(client.getContext())
  
  def getAggregateMemberInfo(self, aggregateTypeName):
    return Util.variantToPyObject(
      CAPI.GetAggregateMemberInfo_Variant(
        self._client,
        aggregateTypeName
        )
      )
  
  def bindConstructorToRegisteredType(self, typeName, typeConstructor):
    self._prototypes[typeName] = typeConstructor
    
    typeMembers = self.getAggregateMemberInfo(typeName)
    
    self._registeredTypes[typeName] = {
      'name': typeName,
      'members': typeMembers
    }
  
  def registerType(self, name, desc):
    sourceFiles = []
    
    members = []
    if len(desc['members']) > 0:
      typeDefFilename = "_%s-def.kl" % name
      typeDefSourceCode = ""
      for i in range(0, len(desc['members'])):
        member = desc['members'][i]
        memberName, memberType = member.items()[0]
        typeDefSourceCode += "require %s;\n" % memberType
      typeDefSourceCode += "struct %s {\n" % name
      for i in range(0, len(desc['members'])):
        member = desc['members'][i]
        memberName, memberType = member.items()[0]
        m = {"name": memberName, "type": memberType}
        members.append(m)
        typeDefSourceCode += "  %s %s;\n" % (memberType, memberName)
      typeDefSourceCode += "};\n"
      sourceFiles.append({
        "filename": typeDefFilename, "sourceCode": typeDefSourceCode
        })
    
    filename = None
    sourceCode = None
    if 'klBindings' in desc:
      if 'filename' in desc['klBindings']:
        filename = desc['klBindings']['filename']
      if 'sourceCode' in desc['klBindings']:
        sourceCode = desc['klBindings']['sourceCode']
    if filename or sourceCode:
      if not filename:
        filename = "(unknown)"
      if not sourceCode:
        sourceCode = ""
      sourceFiles.append({
        "filename": filename, "sourceCode": sourceCode
        })
    
    CAPI.RegisterKLExtension(
      self._client,
      name,
      sourceFiles
      )
    
    if len(members) > 0:
      if 'constructor' not in desc:
        class anonymous(object):
          pass
        desc['constructor'] = anonymous
      
      self.bindConstructorToRegisteredType(name, desc['constructor'])
  
  def registerObject(self, name, desc):
    sourceFiles = []
    
    members = []
    if len(desc['members']) > 0:
      typeDefFilename = "_%s-def.kl" % name
      typeDefSourceCode = ""
      for i in range(0, len(desc['members'])):
        member = desc['members'][i]
        memberName, memberType = member.items()[0]
        typeDefSourceCode += "require %s;\n" % memberType
      typeDefSourceCode += "object "
      typeDefSourceCode += name
      if 'interfaces' in desc:
        for i in range(0, len(desc['interfaces'])):
          if i == 0:
            typeDefSourceCode += ": "
          else:
            typeDefSourceCode += ", "
        typeDefSourceCode += desc['interfaces'][i]
      typeDefSourceCode += " {\n"
      for i in range(0, len(desc['members'])):
        member = desc['members'][i]
        memberName, memberType = member.items()[0]
        m = {"name": memberName, "type": memberType}
        members.append(m)
        typeDefSourceCode += "  %s %s;\n" % (memberType, memberName)
      typeDefSourceCode += "};\n"
      sourceFiles.append({
        "filename": typeDefFilename, "sourceCode": typeDefSourceCode
        })
    
    filename = None
    sourceCode = None
    if 'klBindings' in desc:
      if 'filename' in desc['klBindings']:
        filename = desc['klBindings']['filename']
      if 'sourceCode' in desc['klBindings']:
        sourceCode = desc['klBindings']['sourceCode']
    if filename or sourceCode:
      if not filename:
        filename = "(unknown)"
      if not sourceCode:
        sourceCode = ""
      sourceFiles.append({
        "filename": filename, "sourceCode": sourceCode
        })
    
    CAPI.RegisterKLExtension(
      self._client,
      name,
      sourceFiles
      )
    
    if len(members) > 0:
      if 'constructor' not in desc:
        class anonymous(object):
          pass
        desc['constructor'] = anonymous
      
      # [andrew 2013-03-13] always require a __type for objects (not needed for structs)
      if not hasattr(desc['constructor'], '_originit_'):
        desc['constructor']._originit_ = desc['constructor'].__init__
        def _newinit_(self, *args, **kwargs):
          self._originit_(*args, **kwargs)
          setattr(self, '__type', name)
        desc['constructor'].__init__ = _newinit_
      
      self.bindConstructorToRegisteredType(name, desc['constructor'])
  
  def getRegisteredTypeSize(self, name):
    return CAPI.GetRegisteredTypeSize(self._client, name) 
  
  def getRegisteredTypeIsShallow(self, name):
    return CAPI.GetRegisteredTypeIsShallow(self._client, name) 
  
  def getRegisteredTypeExtName(self, name):
    return CAPI.GetRegisteredTypeExtName(self._client, name) 
  
  def getRegisteredTypes(self):
    v = CAPI.GetRegisteredTypes_Variant(self._client)
    return Util.variantToPyObject(v)

  def _assignPrototypes(self, data, typeName):
    if type(data) is dict and '__type' in data:
      typeName = data['__type']

    openBraceIdx = typeName.find('[')
    if openBraceIdx > 0:
      closeBraceIdx = typeName.find(']')
      keyType = ''
      if closeBraceIdx > openBraceIdx+1:
        keyType = typeName[openBraceIdx+1:closeBraceIdx]
        try:
          constInt = int(keyType)
          constIntKey = True
        except:
          constIntKey = False

      # remove the braces and keytype from the typeName, giving the typeName for the elements
      typeName = typeName.replace('['+keyType+']', '', 1)

      if closeBraceIdx == openBraceIdx+1 or constIntKey:
        obj = []
        for i in range(0, len(data)):
          obj.append(self._assignPrototypes(data[i], typeName))
        return obj
        
      # check for a key value defined between square brackets that would indicate a dictionary
      if closeBraceIdx > openBraceIdx+1:
        obj = {}
        for key, value in data.iteritems():
          obj[self._assignPrototypes(key, keyType)] = (self._assignPrototypes(data[key], typeName))
        return obj

    if typeName in self._prototypes:
      if not data:
        # [pzion 20121106] a null value for an object
        obj = None
      else:
        obj = self._prototypes[typeName]()
        if 'members' in self._registeredTypes[typeName]:
          members = self._registeredTypes[typeName]['members']
          for i in range(0, len(members)):
            member = members[i]
            memberName = member['name']
            setattr(obj, memberName,
              self._assignPrototypes(data[memberName], member['type'])
            )
      return obj
    else:
      return data

class _Build(object):
  def getName(self):
    return "Fabric Engine"

  def getPureVersion(self):
    return "1.12.0"

  def getFullVersion(self):
    return "1.12"

  def getDesc(self):
    return "Dedicated Platform for High-Performance Graphics Applications"

  def getCopyright(self):
    return "Copyright 2010-2013 Fabric Engine Inc. All rights reserved."

  def getURL(self):
    return "http://fabricengine.com/"

  def getOS(self):
    return "Windows"

  def getArch(self):
    return "x86_64"
