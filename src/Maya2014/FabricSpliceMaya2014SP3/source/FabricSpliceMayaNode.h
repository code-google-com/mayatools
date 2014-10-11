
#ifndef _CREATIONSPLICEMAYANODE_H_
#define _CREATIONSPLICEMAYANODE_H_

#include "FabricSpliceBaseInterface.h"

#include <maya/MPxNode.h> 
#include <maya/MTypeId.h> 
#include <maya/MNodeMessage.h>
#include <maya/MStringArray.h>

class FabricSpliceMayaNode: public MPxNode, public FabricSpliceBaseInterface{
  //temporarely disabled
  // friend  void onAttributeChanged(MNodeMessage::AttributeMessage msg, MPlug &plug, MPlug &otherPlug, void* userData);

public:
  static void* creator();
  static MStatus initialize();

  FabricSpliceMayaNode();
  void postConstructor();
  ~FabricSpliceMayaNode();

  // implement pure virtual functions
  virtual MObject getThisMObject() { return thisMObject(); }
  virtual MPlug getSaveDataPlug() { return MPlug(thisMObject(), saveData); }

  MStatus compute(const MPlug& plug, MDataBlock& data);
  MStatus setDependentsDirty(MPlug const &inPlug, MPlugArray &affectedPlugs);
  MStatus shouldSave(const MPlug &plug, bool &isSaving);
  void copyInternalData(MPxNode *node);

  // node attributes
  static MTypeId id;
  static MObject saveData;
  static MObject evalID;
};

#endif
