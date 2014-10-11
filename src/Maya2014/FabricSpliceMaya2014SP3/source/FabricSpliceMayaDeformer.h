

#ifndef _CREATIONSPLICEMAYADEFORMER_H_
#define _CREATIONSPLICEMAYADEFORMER_H_

#include "FabricSpliceBaseInterface.h"

#include <maya/MPxDeformerNode.h> 
#include <maya/MTypeId.h> 
#include <maya/MItGeometry.h>

class FabricSpliceMayaDeformer: public MPxDeformerNode, public FabricSpliceBaseInterface{
public:
  static void* creator();
  static MStatus initialize();

  FabricSpliceMayaDeformer();
  void postConstructor();
  ~FabricSpliceMayaDeformer();

  // implement pure virtual functions
  virtual MObject getThisMObject() { return thisMObject(); }
  virtual MPlug getSaveDataPlug() { return MPlug(thisMObject(), saveData); }

  MStatus deform(MDataBlock& block, MItGeometry& iter, const MMatrix&, unsigned int multiIndex);
  MStatus setDependentsDirty(MPlug const &inPlug, MPlugArray &affectedPlugs);
  MStatus shouldSave(const MPlug &plug, bool &isSaving);
  void copyInternalData(MPxNode *node);
  
  // node attributes
  static MTypeId id;
  static MObject saveData;
  static MObject evalID;

protected:
  virtual void invalidateNode();

private:
  int initializePolygonMeshPorts(MString &meshId, MPlug &meshPlug, MDataBlock &data);
  // void initializeGeometry(MObject &meshObj);
  int mGeometryInitialized;
};

#endif

