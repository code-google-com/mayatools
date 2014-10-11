
#include "FabricSpliceConversion.h"
#include "FabricSpliceMayaData.h"
#include "plugin.h"

#include <maya/MGlobal.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFloatVector.h>
#include <maya/MFnIntArrayData.h>
#include <maya/MFnDoubleArrayData.h>
#include <maya/MFnVectorArrayData.h>
#include <maya/MFnPointArrayData.h>
#include <maya/MIntArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MVectorArray.h>
#include <maya/MPointArray.h>
#include <maya/MFloatVector.h>
#include <maya/MMatrix.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MAngle.h>
#include <maya/MDistance.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MFnPluginData.h>
#include <maya/MFnMesh.h>
#include <maya/MFnMeshData.h>
#include <maya/MFnNurbsCurve.h>
#include <maya/MFnNurbsCurveData.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MFnAnimCurve.h>

typedef std::map<std::string, SplicePlugToPortFunc> SplicePlugToPortFuncMap;
typedef std::map<std::string, SplicePortToPlugFunc> SplicePortToPlugFuncMap;
typedef SplicePlugToPortFuncMap::iterator SplicePlugToPortFuncIt;
typedef SplicePortToPlugFuncMap::iterator SplicePortToPlugFuncIt;

struct KLEuler{
  float x;
  float y;
  float z;
  int32_t order;
};

double getFloat64FromRTVal(FabricCore::RTVal rtVal)
{
  FabricCore::RTVal::SimpleData simpleData;
  if(!rtVal.maybeGetSimpleData(&simpleData))
    return DBL_MAX;
  if(simpleData.type == FEC_RTVAL_SIMPLE_TYPE_FLOAT32)
    return simpleData.value.float32;
  if(simpleData.type == FEC_RTVAL_SIMPLE_TYPE_FLOAT64)
    return simpleData.value.float64;
  if(simpleData.type == FEC_RTVAL_SIMPLE_TYPE_SINT32)
    return simpleData.value.sint32;
  if(simpleData.type == FEC_RTVAL_SIMPLE_TYPE_UINT32)
    return simpleData.value.uint32;
  if(simpleData.type == FEC_RTVAL_SIMPLE_TYPE_UINT8)
    return simpleData.value.uint8;
  if(simpleData.type == FEC_RTVAL_SIMPLE_TYPE_UINT16)
    return simpleData.value.uint16;
  if(simpleData.type == FEC_RTVAL_SIMPLE_TYPE_UINT64)
    return simpleData.value.uint64;
  if(simpleData.type == FEC_RTVAL_SIMPLE_TYPE_SINT8)
    return simpleData.value.sint8;
  if(simpleData.type == FEC_RTVAL_SIMPLE_TYPE_SINT16)
    return simpleData.value.sint16;
  if(simpleData.type == FEC_RTVAL_SIMPLE_TYPE_SINT64)
    return simpleData.value.sint64;
  return DBL_MAX;
}

void plugToPort_compound_convertMat44(const MMatrix & matrix, FabricCore::RTVal & rtVal)
{
  rtVal = FabricSplice::constructRTVal("Mat44", 0, 0);
  FabricCore::RTVal dataRTVal = rtVal.callMethod("Data", "data", 0, 0);
  float * data = (float*)dataRTVal.getData();

  unsigned int offset = 0;
  data[offset++] = (float)matrix[0][0];
  data[offset++] = (float)matrix[1][0];
  data[offset++] = (float)matrix[2][0];
  data[offset++] = (float)matrix[3][0];
  data[offset++] = (float)matrix[0][1];
  data[offset++] = (float)matrix[1][1];
  data[offset++] = (float)matrix[2][1];
  data[offset++] = (float)matrix[3][1];
  data[offset++] = (float)matrix[0][2];
  data[offset++] = (float)matrix[1][2];
  data[offset++] = (float)matrix[2][2];
  data[offset++] = (float)matrix[3][2];
  data[offset++] = (float)matrix[0][3];
  data[offset++] = (float)matrix[1][3];
  data[offset++] = (float)matrix[2][3];
  data[offset++] = (float)matrix[3][3];
}

void plugToPort_compound_convertCompound(MFnCompoundAttribute & compound, MDataHandle & handle, FabricCore::RTVal & rtVal)
{
  std::vector<FabricCore::RTVal> args(5);

  // treat special cases
  if(compound.numChildren() == 3)
  {
    MString compoundName = compound.name();
    FabricCore::RTVal compoundNameRTVal = FabricSplice::constructStringRTVal(compoundName.asChar());

    MFnAttribute x(compound.child(0));
    MFnAttribute y(compound.child(1));
    MFnAttribute z(compound.child(2));

    if(x.name() == compoundName+"X" && y.name() == compoundName+"Y" && z.name() == compoundName+"Z")
    {
      MStatus attrStatus;
      MFnNumericAttribute nx(x.object(), &attrStatus);
      if(attrStatus == MS::kSuccess)
      {
        if(!compound.isArray())
        {
          MDataHandle xHandle(handle.child(x.object()));
          MDataHandle yHandle(handle.child(y.object()));
          MDataHandle zHandle(handle.child(z.object()));
          args[0] = FabricSplice::constructFloat32RTVal(xHandle.asDouble());
          args[1] = FabricSplice::constructFloat32RTVal(yHandle.asDouble());
          args[2] = FabricSplice::constructFloat32RTVal(zHandle.asDouble());
          FabricCore::RTVal value = FabricSplice::constructRTVal("Vec3", 3, &args[0]);
          args[0] = compoundNameRTVal;
          args[1] = value;
          rtVal = FabricSplice::constructObjectRTVal("Vec3Param", 2, &args[0]);
        }
        else
        {
          MArrayDataHandle arrayHandle(handle);

          rtVal = FabricSplice::constructObjectRTVal("Vec3ArrayParam", 1, &compoundNameRTVal);
          args[0] = FabricSplice::constructUInt32RTVal(arrayHandle.elementCount());
          rtVal.callMethod("", "resize", 1, &args[0]);

          for(unsigned int j=0;j<arrayHandle.elementCount();j++)
          {
            MDataHandle elementHandle = arrayHandle.inputValue();
            MDataHandle xHandle(elementHandle.child(x.object()));
            MDataHandle yHandle(elementHandle.child(y.object()));
            MDataHandle zHandle(elementHandle.child(z.object()));
            args[0] = FabricSplice::constructFloat32RTVal(xHandle.asDouble());
            args[1] = FabricSplice::constructFloat32RTVal(yHandle.asDouble());
            args[2] = FabricSplice::constructFloat32RTVal(zHandle.asDouble());
            FabricCore::RTVal value = FabricSplice::constructRTVal("Vec3", 3, &args[0]);

            args[0] = FabricSplice::constructUInt32RTVal(j);
            args[1] = value;
            rtVal.callMethod("", "setValue", 2, &args[0]);
            arrayHandle.next();
          }
        }

        return;
      }
      else
      {
        MFnUnitAttribute ux(x.object(), &attrStatus);
        if(attrStatus == MS::kSuccess)
        {
          if(!compound.isArray())
          {
            MDataHandle xHandle(handle.child(x.object()));
            MDataHandle yHandle(handle.child(y.object()));
            MDataHandle zHandle(handle.child(z.object()));
            args[0] = FabricSplice::constructFloat32RTVal(xHandle.asAngle().as(MAngle::kRadians));
            args[1] = FabricSplice::constructFloat32RTVal(yHandle.asAngle().as(MAngle::kRadians));
            args[2] = FabricSplice::constructFloat32RTVal(zHandle.asAngle().as(MAngle::kRadians));
            FabricCore::RTVal value = FabricSplice::constructRTVal("Euler", 3, &args[0]);
            args[0] = compoundNameRTVal;
            args[1] = value;
            rtVal = FabricSplice::constructObjectRTVal("EulerParam", 2, &args[0]);
          }
          else
          {
            MArrayDataHandle arrayHandle(handle);

            rtVal = FabricSplice::constructObjectRTVal("EulerArrayParam", 1, &compoundNameRTVal);
            args[0] = FabricSplice::constructUInt32RTVal(arrayHandle.elementCount());
            rtVal.callMethod("", "resize", 1, &args[0]);

            for(unsigned int j=0;j<arrayHandle.elementCount();j++)
            {
              MDataHandle elementHandle = arrayHandle.inputValue();
              MDataHandle xHandle(elementHandle.child(x.object()));
              MDataHandle yHandle(elementHandle.child(y.object()));
              MDataHandle zHandle(elementHandle.child(z.object()));
              args[0] = FabricSplice::constructFloat32RTVal(xHandle.asAngle().as(MAngle::kRadians));
              args[1] = FabricSplice::constructFloat32RTVal(yHandle.asAngle().as(MAngle::kRadians));
              args[2] = FabricSplice::constructFloat32RTVal(zHandle.asAngle().as(MAngle::kRadians));
              FabricCore::RTVal value = FabricSplice::constructRTVal("Euler", 3, &args[0]);

              args[0] = FabricSplice::constructUInt32RTVal(j);
              args[1] = value;
              rtVal.callMethod("", "setValue", 2, &args[0]);
              arrayHandle.next();
            }
          }

          return;
        }
      }
    }
  }

  for(unsigned int i=0;i<compound.numChildren();i++)
  {
    MFnAttribute child(compound.child(i));
    MString childName = child.name();
    FabricCore::RTVal childNameRTVal = FabricSplice::constructStringRTVal(childName.asChar());
    FabricCore::RTVal childRTVal;
    MStatus attrStatus;

    MFnNumericAttribute nAttr(child.object(), &attrStatus);
    if(attrStatus == MS::kSuccess)
    {
      if(nAttr.unitType() == MFnNumericData::kBoolean)
      {
        if(!nAttr.isArray())
        {
          MDataHandle childHandle(handle.child(child.object()));
          args[0] = childNameRTVal;
          args[1] = FabricSplice::constructBooleanRTVal(childHandle.asBool());
          childRTVal = FabricSplice::constructObjectRTVal("BooleanParam", 2, &args[0]);
        }
        else
        {
          MArrayDataHandle childHandle(handle.child(child.object()));
          childRTVal = FabricSplice::constructObjectRTVal("BooleanArrayParam", 1, &childNameRTVal);
          args[0] = FabricSplice::constructUInt32RTVal(childHandle.elementCount());
          childRTVal.callMethod("", "resize", 1, &args[0]);

          for(unsigned int j=0;j<childHandle.elementCount();j++)
          {
            args[0] = FabricSplice::constructUInt32RTVal(j);
            args[1] = FabricSplice::constructBooleanRTVal(childHandle.inputValue().asBool());
            childRTVal.callMethod("", "setValue", 2, &args[0]);
            childHandle.next();
          }
        }
      }
      else if(nAttr.unitType() == MFnNumericData::kInt)
      {
        if(!nAttr.isArray())
        {
          MDataHandle childHandle(handle.child(child.object()));
          args[0] = childNameRTVal;
          args[1] = FabricSplice::constructSInt32RTVal(childHandle.asInt());
          childRTVal = FabricSplice::constructObjectRTVal("SInt32Param", 2, &args[0]);
        }
        else
        {
          MArrayDataHandle childHandle(handle.child(child.object()));
          childRTVal = FabricSplice::constructObjectRTVal("SInt32ArrayParam", 1, &childNameRTVal);
          args[0] = FabricSplice::constructUInt32RTVal(childHandle.elementCount());
          childRTVal.callMethod("", "resize", 1, &args[0]);

          for(unsigned int j=0;j<childHandle.elementCount();j++)
          {
            args[0] = FabricSplice::constructUInt32RTVal(j);
            args[1] = FabricSplice::constructSInt32RTVal(childHandle.inputValue().asInt());
            childRTVal.callMethod("", "setValue", 2, &args[0]);
            childHandle.next();
          }
        }
      }
      else if(nAttr.unitType() == MFnNumericData::kFloat)
      {
        if(!nAttr.isArray())
        {
          MDataHandle childHandle(handle.child(child.object()));
          args[0] = childNameRTVal;
          args[1] = FabricSplice::constructFloat64RTVal(childHandle.asFloat());
          childRTVal = FabricSplice::constructObjectRTVal("Float64Param", 2, &args[0]);
        }
        else
        {
          MArrayDataHandle childHandle(handle.child(child.object()));
          childRTVal = FabricSplice::constructObjectRTVal("Float64ArrayParam", 1, &childNameRTVal);
          args[0] = FabricSplice::constructUInt32RTVal(childHandle.elementCount());
          childRTVal.callMethod("", "resize", 1, &args[0]);

          for(unsigned int j=0;j<childHandle.elementCount();j++)
          {
            args[0] = FabricSplice::constructUInt32RTVal(j);
            args[1] = FabricSplice::constructFloat64RTVal(childHandle.inputValue().asFloat());
            childRTVal.callMethod("", "setValue", 2, &args[0]);
            childHandle.next();
          }
        }
      }
      else if(nAttr.unitType() == MFnNumericData::kDouble)
      {
        if(!nAttr.isArray())
        {
          MDataHandle childHandle(handle.child(child.object()));
          args[0] = childNameRTVal;
          args[1] = FabricSplice::constructFloat64RTVal(childHandle.asDouble());
          childRTVal = FabricSplice::constructObjectRTVal("Float64Param", 2, &args[0]);
        }
        else
        {
          MArrayDataHandle childHandle(handle.child(child.object()));
          childRTVal = FabricSplice::constructObjectRTVal("Float64ArrayParam", 1, &childNameRTVal);
          args[0] = FabricSplice::constructUInt32RTVal(childHandle.elementCount());
          childRTVal.callMethod("", "resize", 1, &args[0]);

          for(unsigned int j=0;j<childHandle.elementCount();j++)
          {
            args[0] = FabricSplice::constructUInt32RTVal(j);
            args[1] = FabricSplice::constructFloat64RTVal(childHandle.inputValue().asDouble());
            childRTVal.callMethod("", "setValue", 2, &args[0]);
            childHandle.next();
          }
        }
      }
      else if(nAttr.unitType() == MFnNumericData::k3Double) // vec3
      {
        if(!nAttr.isArray())
        {
          MDataHandle childHandle(handle.child(child.object()));
          args[0] = childNameRTVal;
          args[1] = FabricSplice::constructRTVal("Vec3", 0, 0);
          MFloatVector v = childHandle.asFloatVector();
          args[1].setMember("x", FabricSplice::constructFloat64RTVal(v.x));
          args[1].setMember("y", FabricSplice::constructFloat64RTVal(v.y));
          args[1].setMember("z", FabricSplice::constructFloat64RTVal(v.z));
          childRTVal = FabricSplice::constructObjectRTVal("Vec3Param", 2, &args[0]);
        }
        else
        {
          MArrayDataHandle childHandle(handle.child(child.object()));
          childRTVal = FabricSplice::constructObjectRTVal("Vec3ArrayParam", 1, &childNameRTVal);
          args[0] = FabricSplice::constructUInt32RTVal(childHandle.elementCount());
          childRTVal.callMethod("", "resize", 1, &args[0]);

          for(unsigned int j=0;j<childHandle.elementCount();j++)
          {
            args[0] = FabricSplice::constructUInt32RTVal(j);
            args[1] = FabricSplice::constructRTVal("Vec3", 0, 0);
            MFloatVector v = childHandle.inputValue().asFloatVector();
            args[1].setMember("x", FabricSplice::constructFloat64RTVal(v.x));
            args[1].setMember("y", FabricSplice::constructFloat64RTVal(v.y));
            args[1].setMember("z", FabricSplice::constructFloat64RTVal(v.z));
            childRTVal.callMethod("", "setValue", 2, &args[0]);
            childHandle.next();
          }
        }
      }
      else if(nAttr.unitType() == MFnNumericData::k3Float) // color
      {
        if(!nAttr.isArray())
        {
          MDataHandle childHandle(handle.child(child.object()));
          args[0] = childNameRTVal;
          args[1] = FabricSplice::constructRTVal("Color", 0, 0);
          MFloatVector v = childHandle.asFloatVector();
          args[1].setMember("r", FabricSplice::constructFloat64RTVal(v.x));
          args[1].setMember("g", FabricSplice::constructFloat64RTVal(v.y));
          args[1].setMember("b", FabricSplice::constructFloat64RTVal(v.z));
          args[1].setMember("a", FabricSplice::constructFloat64RTVal(1.0));
          childRTVal = FabricSplice::constructObjectRTVal("ColorParam", 2, &args[0]);
        }
        else
        {
          MArrayDataHandle childHandle(handle.child(child.object()));
          childRTVal = FabricSplice::constructObjectRTVal("ColorArrayParam", 1, &childNameRTVal);
          args[0] = FabricSplice::constructUInt32RTVal(childHandle.elementCount());
          childRTVal.callMethod("", "resize", 1, &args[0]);

          for(unsigned int j=0;j<childHandle.elementCount();j++)
          {
            args[0] = FabricSplice::constructUInt32RTVal(j);
            args[1] = FabricSplice::constructRTVal("Color", 0, 0);
            MFloatVector v = childHandle.inputValue().asFloatVector();
            args[1].setMember("r", FabricSplice::constructFloat64RTVal(v.x));
            args[1].setMember("g", FabricSplice::constructFloat64RTVal(v.y));
            args[1].setMember("b", FabricSplice::constructFloat64RTVal(v.z));
            args[1].setMember("a", FabricSplice::constructFloat64RTVal(1.0));
            childRTVal.callMethod("", "setValue", 2, &args[0]);
            childHandle.next();
          }
        }
      }
      else
      {
        MFnNumericData::Type unitType = nAttr.unitType();
        mayaLogErrorFunc("Unsupported numeric attribute '"+childName+"'.");
        return;
      }
    }
    else
    {
      MFnTypedAttribute tAttr(child.object(), &attrStatus);
      if(attrStatus == MS::kSuccess)
      {
        if(tAttr.attrType() == MFnData::kString)
        {
          if(!tAttr.isArray())
          {
            MDataHandle childHandle(handle.child(child.object()));
            args[0] = childNameRTVal;
            args[1] = FabricSplice::constructStringRTVal(childHandle.asString().asChar());
            childRTVal = FabricSplice::constructObjectRTVal("StringParam", 2, &args[0]);
          }
          else
          {
            MArrayDataHandle childHandle(handle.child(child.object()));
            childRTVal = FabricSplice::constructObjectRTVal("StringArrayParam", 1, &childNameRTVal);
            args[0] = FabricSplice::constructUInt32RTVal(childHandle.elementCount());
            childRTVal.callMethod("", "resize", 1, &args[0]);

            for(unsigned int j=0;j<childHandle.elementCount();j++)
            {
              args[0] = FabricSplice::constructUInt32RTVal(j);
              args[1] = FabricSplice::constructStringRTVal(childHandle.inputValue().asString().asChar());
              childRTVal.callMethod("", "setValue", 2, &args[0]);
              childHandle.next();
            }
          }
        }
        else
        {
          mayaLogErrorFunc("Unsupported typed attribute '"+childName+"'.");
          return;
        }
      }
      else
      {
        MFnMatrixAttribute mAttr(child.object(), &attrStatus);
        if(attrStatus == MS::kSuccess)
        {
          if(!mAttr.isArray())
          {
            MDataHandle childHandle(handle.child(child.object()));
            const MMatrix& mayaMat = childHandle.asMatrix();

            childRTVal = FabricSplice::constructObjectRTVal("Mat44Param", 1, &childNameRTVal);
            FabricCore::RTVal matrixRTVal;
            plugToPort_compound_convertMat44(childHandle.asMatrix(), matrixRTVal);
            childRTVal.callMethod("", "setValue", 1, &matrixRTVal);
          }
          else
          {
            MArrayDataHandle childHandle(handle.child(child.object()));
            childRTVal = FabricSplice::constructObjectRTVal("Mat44ArrayParam", 1, &childNameRTVal);
            args[0] = FabricSplice::constructUInt32RTVal(childHandle.elementCount());
            childRTVal.callMethod("", "resize", 1, &args[0]);

            for(unsigned int j=0;j<childHandle.elementCount();j++)
            {
              args[0] = FabricSplice::constructUInt32RTVal(j);
              plugToPort_compound_convertMat44(childHandle.inputValue().asMatrix(), args[1]);
              childRTVal.callMethod("", "setValue", 2, &args[0]);
              childHandle.next();
            }
          }
        }
        else
        {
          MFnCompoundAttribute cAttr(child.object(), &attrStatus);
          if(attrStatus == MS::kSuccess)
          {
            MFnCompoundAttribute cAttr(compound.child(i));
            if(!cAttr.isArray())
            {
              MDataHandle childHandle(handle.child(child.object()));
              childRTVal = FabricSplice::constructObjectRTVal("CompoundParam", 1, &childNameRTVal);
              plugToPort_compound_convertCompound(cAttr, childHandle, childRTVal);
            }
          }
        }
      }
    }

    if(childRTVal.isValid())
      rtVal.callMethod("", "addParam", 1, &childRTVal);
  }
}

void plugToPort_compound(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){
  if(plug.isArray())
    return;

  MDataHandle handle = data.inputValue(plug);
  FabricCore::RTVal rtVal = FabricSplice::constructObjectRTVal("CompoundParam");
  MFnCompoundAttribute compound(plug.attribute());
  plugToPort_compound_convertCompound(compound, handle, rtVal);
  port.setRTVal(rtVal);
}

void plugToPort_bool(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.inputArrayValue(plug);

    unsigned int elements = arrayHandle.elementCount();
    MAYASPLICE_MEMORY_ALLOCATE(bool, elements);

    for(unsigned int i = 0; i < elements; ++i){
      arrayHandle.jumpToArrayElement(i);
      MDataHandle handle = arrayHandle.inputValue();
      MAYASPLICE_MEMORY_SETITEM(i, handle.asBool());
    }

    MAYASPLICE_MEMORY_SETPORT(port);
    MAYASPLICE_MEMORY_FREE();
  }
  else{
    MDataHandle handle = data.inputValue(plug);
    port.setRTVal(FabricSplice::constructBooleanRTVal(handle.asBool()));
  }
}

void plugToPort_integer(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.inputArrayValue(plug);

    unsigned int elements = arrayHandle.elementCount();
    MAYASPLICE_MEMORY_ALLOCATE(int32_t, elements);

    for(unsigned int i = 0; i < elements; ++i){
      arrayHandle.jumpToArrayElement(i);
      MDataHandle handle = arrayHandle.inputValue();
      MAYASPLICE_MEMORY_SETITEM(i, handle.asLong());
    }

    MAYASPLICE_MEMORY_SETPORT(port);
    MAYASPLICE_MEMORY_FREE();
  }else{
    MDataHandle handle = data.inputValue(plug);
    if(handle.type() == MFnData::kIntArray) {
      MIntArray arrayValues = MFnIntArrayData(handle.data()).array();
      unsigned int elements = arrayValues.length();
      MAYASPLICE_MEMORY_ALLOCATE(int32_t, elements);

      for(unsigned int i = 0; i < elements; ++i){
        MAYASPLICE_MEMORY_SETITEM(i, arrayValues[i]);
      }

      MAYASPLICE_MEMORY_SETPORT(port);
      MAYASPLICE_MEMORY_FREE();
    }else{
      if(!port.isArray())
        port.setRTVal(FabricSplice::constructSInt32RTVal(handle.asLong()));
    }
  }
}

void plugToPort_scalar(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){

  std::string scalarUnit = port.getStringOption("scalarUnit");
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.inputArrayValue(plug);

    unsigned int elements = arrayHandle.elementCount();
    MAYASPLICE_MEMORY_ALLOCATE(float, elements);

    for(unsigned int i = 0; i < elements; ++i){
      arrayHandle.jumpToArrayElement(i);
      MDataHandle handle = arrayHandle.inputValue();

      if(scalarUnit == "time")
        MAYASPLICE_MEMORY_SETITEM(i, handle.asTime().as(MTime::kSeconds));
      else if(scalarUnit == "angle")
        MAYASPLICE_MEMORY_SETITEM(i, handle.asAngle().as(MAngle::kRadians));
      else if(scalarUnit == "distance")
        MAYASPLICE_MEMORY_SETITEM(i, handle.asDistance().as(MDistance::kMillimeters));
      else
      {
        if(handle.numericType() == MFnNumericData::kFloat){
          MAYASPLICE_MEMORY_SETITEM(i, handle.asFloat());
        }else{
          MAYASPLICE_MEMORY_SETITEM(i, handle.asDouble());
        }
      }
    }

    MAYASPLICE_MEMORY_SETPORT(port);
    MAYASPLICE_MEMORY_FREE();
  }else{
    MDataHandle handle = data.inputValue(plug);
    if(handle.type() == MFnData::kDoubleArray){
      MDoubleArray arrayValues = MFnDoubleArrayData(handle.data()).array();
      unsigned int elements = arrayValues.length();
      MAYASPLICE_MEMORY_ALLOCATE(float, elements);

      for(unsigned int i = 0; i < elements; ++i){
        MAYASPLICE_MEMORY_SETITEM(i, arrayValues[i]);
      }

      MAYASPLICE_MEMORY_SETPORT(port);
      MAYASPLICE_MEMORY_FREE();
    }else{
      if(port.isArray())
        return;

      if(scalarUnit == "time")
        port.setRTVal(FabricSplice::constructFloat64RTVal(handle.asTime().as(MTime::kSeconds)));
      else if(scalarUnit == "angle")
        port.setRTVal(FabricSplice::constructFloat64RTVal(handle.asAngle().as(MAngle::kRadians)));
      else if(scalarUnit == "distance")
        port.setRTVal(FabricSplice::constructFloat64RTVal(handle.asDistance().as(MDistance::kMillimeters)));
      else
      {
        if(handle.numericType() == MFnNumericData::kFloat)
          port.setRTVal(FabricSplice::constructFloat64RTVal(handle.asFloat()));
        else
          port.setRTVal(FabricSplice::constructFloat64RTVal(handle.asDouble()));
      }
    }
  }
}

void plugToPort_string(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.inputArrayValue(plug);
    unsigned int elements = arrayHandle.elementCount();
    FabricCore::RTVal stringArrayVal = FabricSplice::constructVariableArrayRTVal("String");
    FabricCore::RTVal elementsVal = FabricSplice::constructUInt32RTVal(elements);
    stringArrayVal.callMethod("", "resize", 1, &elementsVal);
    for(unsigned int i = 0; i < elements; ++i){
      arrayHandle.jumpToArrayElement(i);
      MDataHandle handle = arrayHandle.inputValue();
      MString stringVal = handle.asString();
      stringArrayVal.setArrayElement(i, FabricSplice::constructStringRTVal(stringVal.asChar()));
    }

    port.setRTVal(stringArrayVal);
  }
  else{
    if(port.isArray())
      return;
    MDataHandle handle = data.inputValue(plug);
    port.setRTVal(FabricSplice::constructStringRTVal(handle.asString().asChar()));
  }
}

void plugToPort_color(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.inputArrayValue(plug);

    unsigned int elements = arrayHandle.elementCount();
    FabricCore::RTVal arrayVal = FabricSplice::constructVariableArrayRTVal("Color");
    FabricCore::RTVal color = FabricSplice::constructRTVal("Color");
    FabricCore::RTVal arraySizeVal = FabricSplice::constructUInt32RTVal(elements);
    arrayVal.callMethod("", "resize", 1, &arraySizeVal);
    for(unsigned int i = 0; i < elements; ++i){
      arrayHandle.jumpToArrayElement(i);
      MDataHandle handle = arrayHandle.inputValue();

      if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
        MFloatVector v = handle.asFloatVector();
        color.setMember("r", FabricSplice::constructFloat64RTVal(v.x));
        color.setMember("g", FabricSplice::constructFloat64RTVal(v.y));
        color.setMember("b", FabricSplice::constructFloat64RTVal(v.z));
      } else{
        MVector v = handle.asVector();
        color.setMember("r", FabricSplice::constructFloat64RTVal(v.x));
        color.setMember("g", FabricSplice::constructFloat64RTVal(v.y));
        color.setMember("b", FabricSplice::constructFloat64RTVal(v.z));
      }
      color.setMember("a", FabricSplice::constructFloat64RTVal(1.0));
      arrayVal.setArrayElement(i, color);
    }

    port.setRTVal(arrayVal);
  }
  else {
    if(port.isArray())
      return;
    MDataHandle handle = data.inputValue(plug);

    FabricCore::RTVal color = FabricSplice::constructRTVal("Color");
    if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
      MFloatVector v = handle.asFloatVector();
      color.setMember("r", FabricSplice::constructFloat64RTVal(v.x));
      color.setMember("g", FabricSplice::constructFloat64RTVal(v.y));
      color.setMember("b", FabricSplice::constructFloat64RTVal(v.z));
    } else{
      MVector v = handle.asVector();
      color.setMember("r", FabricSplice::constructFloat64RTVal(v.x));
      color.setMember("g", FabricSplice::constructFloat64RTVal(v.y));
      color.setMember("b", FabricSplice::constructFloat64RTVal(v.z));
    }
    color.setMember("a", FabricSplice::constructFloat64RTVal(1.0));

    port.setRTVal(color);
  }
}

void plugToPort_vec3(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.inputArrayValue(plug);

    unsigned int elements = arrayHandle.elementCount();
    MAYASPLICE_MEMORY_ALLOCATE(float, elements * 3);

    unsigned int offset = 0;
    for(unsigned int i = 0; i < elements; ++i){
      arrayHandle.jumpToArrayElement(i);
      MDataHandle handle = arrayHandle.inputValue();
      if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
        const float3& mayaVec = handle.asFloat3();
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaVec[0]);
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaVec[1]);
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaVec[2]);
      } else {
        const double3& mayaVec = handle.asDouble3();
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaVec[0]);
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaVec[1]);
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaVec[2]);
      }
    }

    MAYASPLICE_MEMORY_SETPORT(port);
    MAYASPLICE_MEMORY_FREE();
  }else{
    MDataHandle handle = data.inputValue(plug);
    if(handle.type() == MFnData::kVectorArray){
      MVectorArray arrayValues = MFnVectorArrayData(handle.data()).array();
      unsigned int elements = arrayValues.length();
      MAYASPLICE_MEMORY_ALLOCATE(float, elements * 3);

      size_t offset = 0;
      for(unsigned int i = 0; i < elements; ++i){
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)arrayValues[i].x);
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)arrayValues[i].y);
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)arrayValues[i].z);
      }

      MAYASPLICE_MEMORY_SETPORT(port);
      MAYASPLICE_MEMORY_FREE();
    }else if(handle.type() == MFnData::kPointArray){
      MPointArray arrayValues = MFnPointArrayData(handle.data()).array();
      unsigned int elements = arrayValues.length();
      MAYASPLICE_MEMORY_ALLOCATE(float, elements * 3);

      size_t offset = 0;
      for(unsigned int i = 0; i < elements; ++i){
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)arrayValues[i].x);
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)arrayValues[i].y);
        MAYASPLICE_MEMORY_SETITEM(offset++, (float)arrayValues[i].z);
      }

      MAYASPLICE_MEMORY_SETPORT(port);
      MAYASPLICE_MEMORY_FREE();
    }else{
      if(port.isArray())
        return;
      FabricCore::RTVal spliceVec = FabricSplice::constructRTVal("Vec3");
      if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
        const float3& mayaVec = handle.asFloat3();
        spliceVec.setMember("x", FabricSplice::constructFloat64RTVal(mayaVec[0]));
        spliceVec.setMember("y", FabricSplice::constructFloat64RTVal(mayaVec[1]));
        spliceVec.setMember("z", FabricSplice::constructFloat64RTVal(mayaVec[2]));
      } else{
        const double3& mayaVec = handle.asDouble3();
        spliceVec.setMember("x", FabricSplice::constructFloat64RTVal(mayaVec[0]));
        spliceVec.setMember("y", FabricSplice::constructFloat64RTVal(mayaVec[1]));
        spliceVec.setMember("z", FabricSplice::constructFloat64RTVal(mayaVec[2]));
      }
      port.setRTVal(spliceVec);
    }
  }
}

void plugToPort_euler(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.inputArrayValue(plug);

    unsigned int elements = arrayHandle.elementCount();
    FabricCore::RTVal arrayVal = FabricSplice::constructVariableArrayRTVal("Euler");
    FabricCore::RTVal euler = FabricSplice::constructRTVal("Euler");
    FabricCore::RTVal arraySizeVal = FabricSplice::constructUInt32RTVal(elements);
    arrayVal.callMethod("", "resize", 1, &arraySizeVal);
    for(unsigned int i = 0; i < elements; ++i){
      arrayHandle.jumpToArrayElement(i);
      MDataHandle handle = arrayHandle.inputValue();

      if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
        const float3& mayaVec = handle.asFloat3();
        euler.setMember("x", FabricSplice::constructFloat64RTVal(mayaVec[0]));
        euler.setMember("y", FabricSplice::constructFloat64RTVal(mayaVec[1]));
        euler.setMember("z", FabricSplice::constructFloat64RTVal(mayaVec[2]));
      } else{
        const double3& mayaVec = handle.asDouble3();
        euler.setMember("x", FabricSplice::constructFloat64RTVal(mayaVec[0]));
        euler.setMember("y", FabricSplice::constructFloat64RTVal(mayaVec[1]));
        euler.setMember("z", FabricSplice::constructFloat64RTVal(mayaVec[2]));
      }
      arrayVal.setArrayElement(i, euler);
    }

    port.setRTVal(arrayVal);
  }
  else {
    if(port.isArray())
      return;
    MDataHandle handle = data.inputValue(plug);

    FabricCore::RTVal euler = FabricSplice::constructRTVal("Euler");
    if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
      const float3& mayaVec = handle.asFloat3();
      euler.setMember("x", FabricSplice::constructFloat64RTVal(mayaVec[0]));
      euler.setMember("y", FabricSplice::constructFloat64RTVal(mayaVec[1]));
      euler.setMember("z", FabricSplice::constructFloat64RTVal(mayaVec[2]));
    } else{
      const double3& mayaVec = handle.asDouble3();
      euler.setMember("x", FabricSplice::constructFloat64RTVal(mayaVec[0]));
      euler.setMember("y", FabricSplice::constructFloat64RTVal(mayaVec[1]));
      euler.setMember("z", FabricSplice::constructFloat64RTVal(mayaVec[2]));
    }

    port.setRTVal(euler);
  }
}

void plugToPort_mat44(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.inputArrayValue(plug);

    unsigned int elements = arrayHandle.elementCount();
    MAYASPLICE_MEMORY_ALLOCATE(float, elements * 16);

    unsigned int offset = 0;
    for(unsigned int i = 0; i < elements; ++i){
      arrayHandle.jumpToArrayElement(i);
      MDataHandle handle = arrayHandle.inputValue();
      const MMatrix& mayaMat = handle.asMatrix();

      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[0][0]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[1][0]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[2][0]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[3][0]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[0][1]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[1][1]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[2][1]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[3][1]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[0][2]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[1][2]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[2][2]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[3][2]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[0][3]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[1][3]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[2][3]);
      MAYASPLICE_MEMORY_SETITEM(offset++, (float)mayaMat[3][3]);
    }

    MAYASPLICE_MEMORY_SETPORT(port);
    MAYASPLICE_MEMORY_FREE();
  }
  else{
    if(port.isArray())
      return;
    MDataHandle handle = data.inputValue(plug);
    const MMatrix& mayaMat = handle.asMatrix();

    FabricCore::RTVal spliceMat = FabricSplice::constructRTVal("Mat44");
    FabricCore::RTVal spliceMatRow = FabricSplice::constructRTVal("Vec4");

    spliceMatRow.setMember("x", FabricSplice::constructFloat64RTVal(mayaMat.matrix[0][0]));
    spliceMatRow.setMember("y", FabricSplice::constructFloat64RTVal(mayaMat.matrix[1][0]));
    spliceMatRow.setMember("z", FabricSplice::constructFloat64RTVal(mayaMat.matrix[2][0]));
    spliceMatRow.setMember("t", FabricSplice::constructFloat64RTVal(mayaMat.matrix[3][0]));
    spliceMat.setMember("row0", spliceMatRow);

    spliceMatRow.setMember("x", FabricSplice::constructFloat64RTVal(mayaMat.matrix[0][1]));
    spliceMatRow.setMember("y", FabricSplice::constructFloat64RTVal(mayaMat.matrix[1][1]));
    spliceMatRow.setMember("z", FabricSplice::constructFloat64RTVal(mayaMat.matrix[2][1]));
    spliceMatRow.setMember("t", FabricSplice::constructFloat64RTVal(mayaMat.matrix[3][1]));
    spliceMat.setMember("row1", spliceMatRow);

    spliceMatRow.setMember("x", FabricSplice::constructFloat64RTVal(mayaMat.matrix[0][2]));
    spliceMatRow.setMember("y", FabricSplice::constructFloat64RTVal(mayaMat.matrix[1][2]));
    spliceMatRow.setMember("z", FabricSplice::constructFloat64RTVal(mayaMat.matrix[2][2]));
    spliceMatRow.setMember("t", FabricSplice::constructFloat64RTVal(mayaMat.matrix[3][2]));
    spliceMat.setMember("row2", spliceMatRow);

    spliceMatRow.setMember("x", FabricSplice::constructFloat64RTVal(mayaMat.matrix[0][3]));
    spliceMatRow.setMember("y", FabricSplice::constructFloat64RTVal(mayaMat.matrix[1][3]));
    spliceMatRow.setMember("z", FabricSplice::constructFloat64RTVal(mayaMat.matrix[2][3]));
    spliceMatRow.setMember("t", FabricSplice::constructFloat64RTVal(mayaMat.matrix[3][3]));
    spliceMat.setMember("row3", spliceMatRow);

    port.setRTVal(spliceMat);
  }
}

void plugToPort_PolygonMesh(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){

  std::vector<MDataHandle> handles;
  std::vector<FabricCore::RTVal> rtVals;
  FabricCore::RTVal portRTVal;

  try
  {
    if(plug.isArray())
    {
      portRTVal = port.getRTVal();

      MArrayDataHandle arrayHandle = data.inputArrayValue(plug);

      unsigned int elements = arrayHandle.elementCount();
      for(unsigned int i = 0; i < elements; ++i){
        arrayHandle.jumpToArrayElement(i);
        handles.push_back(arrayHandle.inputValue());

        FabricCore::RTVal polygonMesh;
        if(portRTVal.getArraySize() <= i)
        {
          polygonMesh = FabricSplice::constructObjectRTVal("PolygonMesh");
          portRTVal.callMethod("", "push", 1, &polygonMesh);
        }
        else
        {
          polygonMesh = portRTVal.getArrayElement(i);
          if(!polygonMesh.isValid() || polygonMesh.isNullObject())
          {
            polygonMesh = FabricSplice::constructObjectRTVal("PolygonMesh");
            portRTVal.setArrayElement(i, polygonMesh);
          }
        }
        rtVals.push_back(polygonMesh);
      }
    }
    else
    {
      handles.push_back(data.inputValue(plug));

      if(port.getMode() == FabricSplice::Port_Mode_IO)
        portRTVal = port.getRTVal();
      if(!portRTVal.isValid() || portRTVal.isNullObject())
        portRTVal = FabricSplice::constructObjectRTVal("PolygonMesh");
      rtVals.push_back(portRTVal);
    }

    for(size_t handleIndex=0;handleIndex<handles.size();handleIndex++) 
    {
      MObject meshObj = handles[handleIndex].asMesh();
      MFnMesh mesh(meshObj);
      FabricCore::RTVal polygonMesh = rtVals[handleIndex];

      // determine if we need a topology update
      bool requireTopoUpdate = false;
      if(!requireTopoUpdate)
      {
        unsigned int nbPolygons = polygonMesh.callMethod("UInt64", "polygonCount", 0, 0).getUInt64();
        requireTopoUpdate = nbPolygons != mesh.numPolygons();
      }
      if(!requireTopoUpdate)
      {
        unsigned int nbSamples = polygonMesh.callMethod("UInt64", "polygonPointsCount", 0, 0).getUInt64();
        requireTopoUpdate = nbSamples != mesh.numFaceVertices();
      }

      MPointArray mayaPoints;
      MIntArray mayaCounts, mayaIndices;

      mesh.getPoints(mayaPoints);

      if(requireTopoUpdate)
      {
        // clear the mesh
        polygonMesh.callMethod("", "clear", 0, NULL);
      }

      if(mayaPoints.length() > 0)
      {
        std::vector<FabricCore::RTVal> args(2);
        args[0] = FabricSplice::constructExternalArrayRTVal("Float64", mayaPoints.length() * 4, &mayaPoints[0]);
        args[1] = FabricSplice::constructUInt32RTVal(4); // components
        polygonMesh.callMethod("", "setPointsFromExternalArray_d", 2, &args[0]);
        mayaPoints.clear();
      }

      if(requireTopoUpdate)
      {
        mesh.getVertices(mayaCounts, mayaIndices);
        std::vector<FabricCore::RTVal> args(2);
        args[0] = FabricSplice::constructExternalArrayRTVal("UInt32", mayaCounts.length(), &mayaCounts[0]);
        args[1] = FabricSplice::constructExternalArrayRTVal("UInt32", mayaIndices.length(), &mayaIndices[0]);
        polygonMesh.callMethod("", "setTopologyFromCountsIndicesExternalArrays", 2, &args[0]);
      }

      if(mesh.numUVSets() > 0)
      {
        MFloatArray u, v, values;
        mesh.getUVs(u, v);
        unsigned int offset = 0;

        MIntArray counts, indices;
        mesh.getAssignedUVs(counts, indices);
        counts.clear();
        values.setLength(indices.length() * 2);
        if(values.length() > 0)
        {
          for(unsigned int i=0;i<indices.length(); i++)
          {
            values[offset++] = u[indices[i]];
            values[offset++] = v[indices[i]];
          }
          u.clear();
          v.clear();

          std::vector<FabricCore::RTVal> args(2);
          args[0] = FabricSplice::constructExternalArrayRTVal("Float32", values.length(), &values[0]);
          args[1] = FabricSplice::constructUInt32RTVal(2); // components
          polygonMesh.callMethod("", "setUVsFromExternalArray", 2, &args[0]);
          values.clear();
        }
      }

      if(mesh.numColorSets() > 0)
      {
        MColorArray faceValues;

        MStringArray colorSetNames;
        mesh.getColorSetNames(colorSetNames);
        MString colorSetName = colorSetNames[0];

        mesh.getFaceVertexColors(faceValues, &colorSetName);
        if(faceValues.length() > 0)
        {
          std::vector<FabricCore::RTVal> args(2);
          args[0] = FabricSplice::constructExternalArrayRTVal("Float32", faceValues.length() * 4, &faceValues[0]);
          args[1] = FabricSplice::constructUInt32RTVal(4); // components
          polygonMesh.callMethod("", "setVertexColorsFromExternalArray", 2, &args[0]);
          faceValues.clear();
        }
      }

      mayaCounts.clear();
      mayaIndices.clear();
    }

    port.setRTVal(portRTVal);
  }
  catch(FabricCore::Exception e)
  {
    mayaLogErrorFunc(e.getDesc_cstr());
    return;
  }
  catch(FabricSplice::Exception e)
  {
    mayaLogErrorFunc(e.what());
    return;
  }
}

void plugToPort_Lines(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){

  std::vector<MDataHandle> handles;
  std::vector<FabricCore::RTVal> rtVals;
  FabricCore::RTVal portRTVal;

  try
  {
    if(plug.isArray())
    {
      portRTVal = port.getRTVal();

      MArrayDataHandle arrayHandle = data.inputArrayValue(plug);

      unsigned int elements = arrayHandle.elementCount();
      for(unsigned int i = 0; i < elements; ++i){
        arrayHandle.jumpToArrayElement(i);
        handles.push_back(arrayHandle.inputValue());

        FabricCore::RTVal rtVal;
        if(portRTVal.getArraySize() <= i)
        {
          rtVal = FabricSplice::constructObjectRTVal("Lines");
          portRTVal.callMethod("", "push", 1, &rtVal);
        }
        else
        {
          rtVal = portRTVal.getArrayElement(i);
          if(!rtVal.isValid() || rtVal.isNullObject())
          {
            rtVal = FabricSplice::constructObjectRTVal("Lines");
            portRTVal.setArrayElement(i, rtVal);
          }
        }
        rtVals.push_back(rtVal);
      }
    }
    else
    {
      handles.push_back(data.inputValue(plug));

      if(port.getMode() == FabricSplice::Port_Mode_IO)
        portRTVal = port.getRTVal();
      if(!portRTVal.isValid() || portRTVal.isNullObject())
        portRTVal = FabricSplice::constructObjectRTVal("Lines");
      rtVals.push_back(portRTVal);
    }

    for(size_t handleIndex=0;handleIndex<handles.size();handleIndex++) 
    {
      MObject curveObj = handles[handleIndex].asNurbsCurve();
      MFnNurbsCurve curve(curveObj);
      FabricCore::RTVal rtVal = rtVals[handleIndex];

      MPointArray mayaPoints;
      curve.getCVs(mayaPoints);
      std::vector<double> mayaDoubles(mayaPoints.length() * 3);

      size_t nbSegments = (mayaPoints.length() - 1);
      if(curve.form() == MFnNurbsCurve::kClosed)
        nbSegments++;

      std::vector<uint32_t> mayaIndices(nbSegments * 2);

      size_t voffset = 0;
      size_t coffset = 0;
      for(unsigned int i=0;i<mayaPoints.length();i++)
      {
        mayaDoubles[voffset++] = mayaPoints[i].x;
        mayaDoubles[voffset++] = mayaPoints[i].y;
        mayaDoubles[voffset++] = mayaPoints[i].z;
        if(i < mayaPoints.length() - 1)
        {
          mayaIndices[coffset++] = i;
          mayaIndices[coffset++] = i + 1;
        }
        else if(curve.form() == MFnNurbsCurve::kClosed)
        {
          mayaIndices[coffset++] = i;
          mayaIndices[coffset++] = 0;
        }
      }

      FabricCore::RTVal mayaDoublesVal = FabricSplice::constructExternalArrayRTVal("Float64", mayaDoubles.size(), &mayaDoubles[0]);
      rtVal.callMethod("", "_setPositionsFromExternalArray_d", 1, &mayaDoublesVal);

      FabricCore::RTVal mayaIndicesVal = FabricSplice::constructExternalArrayRTVal("UInt32", mayaIndices.size(), &mayaIndices[0]);
      rtVal.callMethod("", "_setTopologyFromExternalArray", 1, &mayaIndicesVal);
    }

    port.setRTVal(portRTVal);
  }
  catch(FabricCore::Exception e)
  {
    mayaLogErrorFunc(e.getDesc_cstr());
    return;
  }
  catch(FabricSplice::Exception e)
  {
    mayaLogErrorFunc(e.what());
    return;
  }
}

void plugToPort_KeyframeTrack_helper(MFnAnimCurve & curve, FabricCore::RTVal & trackVal) {

  // find the usage of this plug
  // with this we might be able to determine color
  MString curveName = curve.name();
  double red, green, blue;
  red = green = blue = 0.0;
  if(curveName.indexW("_translateX") > -1 || curveName.indexW("_rotateX") > -1 || curveName.indexW("_scaleX") > -1)
    red = 1.0;
  else if(curveName.indexW("_translateY") > -1 || curveName.indexW("_rotateY") > -1 || curveName.indexW("_scaleY") > -1)
    green = 1.0;
  else if(curveName.indexW("_translateZ") > -1 || curveName.indexW("_rotateZ") > -1 || curveName.indexW("_scaleZ") > -1)
    blue = 1.0;

  trackVal = FabricSplice::constructObjectRTVal("KeyframeTrack");
  FabricCore::RTVal keysVal = trackVal.maybeGetMember("keys");
  FabricCore::RTVal colorVal = FabricSplice::constructRTVal("Color");
  FabricCore::RTVal numKeysVal = FabricSplice::constructUInt32RTVal(curve.numKeys());
  keysVal.callMethod("", "resize", 1, &numKeysVal);

  trackVal.setMember("name", FabricSplice::constructStringRTVal(curveName.asChar()));
  colorVal.setMember("r", FabricSplice::constructFloat64RTVal(red));
  colorVal.setMember("g", FabricSplice::constructFloat64RTVal(green));
  colorVal.setMember("b", FabricSplice::constructFloat64RTVal(blue));
  colorVal.setMember("a", FabricSplice::constructFloat64RTVal(1.0));
  trackVal.setMember("color", colorVal);
  trackVal.setMember("defaultInterpolation", FabricSplice::constructSInt32RTVal(2));
  trackVal.setMember("defaultValue", FabricSplice::constructFloat64RTVal(0.0));

  bool weighted = curve.isWeighted();

  for(unsigned int i=0;i<curve.numKeys();i++)
  {
	FabricCore::RTVal keyVal = FabricSplice::constructRTVal("Keyframe");
	FabricCore::RTVal inTangentVal = FabricSplice::constructRTVal("Vec2");
	FabricCore::RTVal outTangentVal = FabricSplice::constructRTVal("Vec2");

    // Integer interpolation;
    double keyTime = curve.time(i).as(MTime::kSeconds);
    double keyValue = curve.value(i);
    keyVal.setMember("time", FabricSplice::constructFloat64RTVal(keyTime));
    keyVal.setMember("value", FabricSplice::constructFloat64RTVal(keyValue));

    if(i > 0)
    {
	  double prevKeyValue = curve.value(i-1);
      double prevKeyTime = curve.time(i-1).as(MTime::kSeconds);
      double valueDelta = keyValue - prevKeyValue;
      double timeDelta = keyTime - prevKeyTime;
	  
      float x,y;
      curve.getTangent(i, x, y, true);
	  
      float weight = 1.0/3.0;
	  float gradient = 0.0;
	  
	  // Weighted out tangents are defined as 3*(P4 - P3),
	  // So multiplly by 1/3 to get P3, and then divide by timeDelta
	  // to get the ratio stored by the Fabric Engine keyframes.
	  // Also note that the default value of 1/3 for the handle weight 
	  // will create equally spaced handles, effectively the same as
	  // Maya's non-weighted curves.
      if(weighted && abs(timeDelta) > 0.0001)
		weight = (x*-1.0/3.0)/timeDelta;
      if(abs(x) > 0.0001)
		gradient = y/x;
		//gradient = ((y*1.0/3.0)/valueDelta)/((x*1.0/3.0)/timeDelta);

	  inTangentVal.setMember("x", FabricSplice::constructFloat64RTVal(weight));
      inTangentVal.setMember("y", FabricSplice::constructFloat64RTVal(gradient));
    }

    if(i < curve.numKeys()-1)
    {
	  double nextKeyValue = curve.value(i+1);
      double nextKeyTime = curve.time(i+1).as(MTime::kSeconds);
      double valueDelta = nextKeyValue - keyValue;
      double timeDelta = nextKeyTime - keyTime;
	  
      float x,y;
      curve.getTangent(i, x, y, false);
	  
      float weight = 1.0/3.0;
	  float gradient = 0.0;
	  
	  // Weighted out tangents are defined as 3*(P2 - P1),
	  // So multiplly by 1/3 to get P2, and then divide by timeDelta
	  // to get the ratio stored by the Fabric Engine keyframes.
	  // Also note that the default value of 1/3 for the handle weight 
	  // will create equally spaced handles, effectively the same as
	  // Maya's non-weighted curves.
      if(weighted && abs(timeDelta) > 0.0001)
		weight = (x*1.0/3.0)/timeDelta;
      if(abs(x) > 0.0001)
		gradient = y/x;
		//gradient = ((y*1.0/3.0)/valueDelta)/((x*1.0/3.0)/timeDelta);
	  
	  outTangentVal.setMember("x", FabricSplice::constructFloat64RTVal(weight));
      outTangentVal.setMember("y", FabricSplice::constructFloat64RTVal(gradient));
    }

    keyVal.setMember("inTangent", inTangentVal);
    keyVal.setMember("outTangent", outTangentVal);
    int interpolation = 2;
    if(curve.outTangentType(i) == MFnAnimCurve::kTangentFlat)
      interpolation = 0;
    else if(curve.outTangentType(i) == MFnAnimCurve::kTangentLinear)
      interpolation = 1;
    keyVal.setMember("interpolation", FabricSplice::constructSInt32RTVal(interpolation));
    keysVal.setArrayElement(i, keyVal);
  }

  trackVal.setMember("keys", keysVal);

}

void plugToPort_KeyframeTrack(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){
  if(!plug.isArray()){
    
    MPlugArray plugs;
    plug.connectedTo(plugs,true,false);
    MFnAnimCurve curve;
    for(unsigned int i=0;i<plugs.length();i++)
    {
      MFnDependencyNode fcurveNode(plugs[i].node());
      MString nodeTypeStr = fcurveNode.typeName();
      if(nodeTypeStr.substring(0,8) == "animCurve")
      {
        curve.setObject(plugs[i].node());
        break;
      }
    }
    if(curve.object().isNull())
      return;

    FabricCore::RTVal trackVal;
    plugToPort_KeyframeTrack_helper(curve, trackVal);
    port.setRTVal(trackVal);
  } else {

    FabricCore::RTVal trackVals = FabricSplice::constructRTVal("KeyframeTrack[]");
    trackVals.setArraySize(plug.numElements());

    for(unsigned int j=0;j<plug.numElements();j++) {

      MPlug element = plug.elementByPhysicalIndex(j);

      MPlugArray plugs;
      element.connectedTo(plugs,true,false);
      MFnAnimCurve curve;
      for(unsigned int i=0;i<plugs.length();i++)
      {
        MFnDependencyNode fcurveNode(plugs[i].node());
        MString nodeTypeStr = fcurveNode.typeName();
        if(nodeTypeStr.substring(0,8) == "animCurve")
        {
          curve.setObject(plugs[i].node());
          break;
        }
      }
      if(curve.object().isNull())
        continue;

      FabricCore::RTVal trackVal;
      plugToPort_KeyframeTrack_helper(curve, trackVal);

      trackVals.setArrayElement(j, trackVal);
    }

    port.setRTVal(trackVals);
  }
}

void plugToPort_spliceMayaData(MPlug &plug, MDataBlock &data, FabricSplice::DGPort & port){
  try{
    if(!plug.isArray()){
      MDataHandle handle = data.inputValue(plug);
      MObject spliceMayaDataObj = handle.data();
      MFnPluginData mfn(spliceMayaDataObj);
      FabricSpliceMayaData *spliceMayaData = (FabricSpliceMayaData*)mfn.data();
      if(!spliceMayaData)
        return;

      port.setRTVal(spliceMayaData->getRTVal());
    }else{
      MArrayDataHandle arrayHandle = data.inputArrayValue(plug);
      unsigned int elements = arrayHandle.elementCount();

      FabricCore::RTVal value = port.getRTVal();
      if(!value.isArray())
        return;
      value.setArraySize(elements);

      for(unsigned int i = 0; i < elements; ++i){
        arrayHandle.jumpToArrayElement(i);
        MDataHandle childHandle = arrayHandle.inputValue();

        childHandle.asMatrix();
        MObject spliceMayaDataObj = childHandle.data();
        MFnPluginData mfn(spliceMayaDataObj);
        FabricSpliceMayaData *spliceMayaData = (FabricSpliceMayaData*)mfn.data();
        if(!spliceMayaData)
          return;
        value.setArrayElement(i, spliceMayaData->getRTVal());
      }

      port.setRTVal(value);
    }
  }
  catch(FabricCore::Exception e)
  {
    mayaLogErrorFunc(e.getDesc_cstr());
    return;
  }
}

void portToPlug_compound_convertMat44(MMatrix & matrix, FabricCore::RTVal & rtVal)
{
  FabricCore::RTVal dataRTVal = rtVal.callMethod("Data", "data", 0, 0);
  float * data = (float*)dataRTVal.getData();

  double vals[4][4] ={
    data[0], data[4], data[8], data[12], 
    data[1], data[5], data[9], data[13], 
    data[2], data[6], data[10], data[14], 
    data[3], data[7], data[11], data[15]
  };
  matrix = MMatrix(vals);
}

void portToPlug_compound_convertCompound(MFnCompoundAttribute & compound, MDataHandle & handle, FabricCore::RTVal & rtVal)
{
  std::vector<FabricCore::RTVal> args(5);
  std::string valueType;

  valueType = rtVal.callMethod("String", "getValueType", 0, 0).getStringCString();

  // treat special cases
  if(compound.numChildren() == 3)
  {
    MString compoundName = compound.name();
    FabricCore::RTVal compoundNameRTVal = FabricSplice::constructStringRTVal(compoundName.asChar());

    MFnAttribute x(compound.child(0));
    MFnAttribute y(compound.child(1));
    MFnAttribute z(compound.child(2));

    if(x.name() == compoundName+"X" && y.name() == compoundName+"Y" && z.name() == compoundName+"Z")
    {
      MStatus attrStatus;
      MFnNumericAttribute nx(x.object(), &attrStatus);
      if(attrStatus == MS::kSuccess)
      {
        if(!compound.isArray())
        {
          if(valueType != "Vec3")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a Vec3Param.");
            return;
          }

          FabricCore::RTVal value = rtVal.callMethod("Vec3", "getValue", 0, 0);
          if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
            handle.set3Float(
              (float)getFloat64FromRTVal(value.maybeGetMember("x")),
              (float)getFloat64FromRTVal(value.maybeGetMember("y")),
              (float)getFloat64FromRTVal(value.maybeGetMember("z")));
          } else {
            handle.set3Double(
              getFloat64FromRTVal(value.maybeGetMember("x")),
              getFloat64FromRTVal(value.maybeGetMember("y")),
              getFloat64FromRTVal(value.maybeGetMember("z")));
          }
        }
        else
        {
          if(valueType != "Vec3[]")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a Vec3ArrayParam.");
            return;
          }

          MArrayDataHandle arrayHandle(handle);
          FabricCore::RTVal arrayValue = rtVal.maybeGetMember("values");
          unsigned int arraySize = arrayValue.getArraySize();

          MArrayDataBuilder arraybuilder = arrayHandle.builder();

          for(unsigned int i = 0; i < arraySize; ++i){
            FabricCore::RTVal value = rtVal.getArrayElement(i);
            MDataHandle elementHandle = arraybuilder.addElement(i);
            if(elementHandle.numericType() == MFnNumericData::k3Float || elementHandle.numericType() == MFnNumericData::kFloat){
              elementHandle.set3Float(
                (float)getFloat64FromRTVal(value.maybeGetMember("x")),
                (float)getFloat64FromRTVal(value.maybeGetMember("y")),
                (float)getFloat64FromRTVal(value.maybeGetMember("z")));
            } else {
              elementHandle.set3Double(
                getFloat64FromRTVal(value.maybeGetMember("x")),
                getFloat64FromRTVal(value.maybeGetMember("y")),
                getFloat64FromRTVal(value.maybeGetMember("z")));
            }
          }
          arrayHandle.set(arraybuilder);
          arrayHandle.setAllClean();
        }

        return;
      }
      else
      {
        MFnUnitAttribute ux(x.object(), &attrStatus);
        if(attrStatus == MS::kSuccess)
        {
          if(!compound.isArray())
          {
            if(valueType != "Euler")
            {
              mayaLogErrorFunc("Incompatible param for compound attribute - expected a EulerParam.");
              return;
            }

            FabricCore::RTVal value = rtVal.callMethod("Euler", "getValue", 0, 0);
            if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
              handle.set3Float(
                (float)getFloat64FromRTVal(value.maybeGetMember("x")),
                (float)getFloat64FromRTVal(value.maybeGetMember("y")),
                (float)getFloat64FromRTVal(value.maybeGetMember("z")));
            } else {
              handle.set3Double(
                getFloat64FromRTVal(value.maybeGetMember("x")),
                getFloat64FromRTVal(value.maybeGetMember("y")),
                getFloat64FromRTVal(value.maybeGetMember("z")));
            }
          }
          else
          {
            if(valueType != "Euler[]")
            {
              mayaLogErrorFunc("Incompatible param for compound attribute - expected a EulerArrayParam.");
              return;
            }

            MArrayDataHandle arrayHandle(handle);
            FabricCore::RTVal arrayValue = rtVal.maybeGetMember("values");
            unsigned int arraySize = arrayValue.getArraySize();

            MArrayDataBuilder arraybuilder = arrayHandle.builder();

            for(unsigned int i = 0; i < arraySize; ++i){
              FabricCore::RTVal value = rtVal.getArrayElement(i);
              MDataHandle elementHandle = arraybuilder.addElement(i);
              if(elementHandle.numericType() == MFnNumericData::k3Float || elementHandle.numericType() == MFnNumericData::kFloat){
                elementHandle.set3Float(
                  (float)getFloat64FromRTVal(value.maybeGetMember("x")),
                  (float)getFloat64FromRTVal(value.maybeGetMember("y")),
                  (float)getFloat64FromRTVal(value.maybeGetMember("z")));
              } else {
                elementHandle.set3Double(
                  getFloat64FromRTVal(value.maybeGetMember("x")),
                  getFloat64FromRTVal(value.maybeGetMember("y")),
                  getFloat64FromRTVal(value.maybeGetMember("z")));
              }
            }
            arrayHandle.set(arraybuilder);
            arrayHandle.setAllClean();
          }

          return;
        }
      }
    }
  }

  for(unsigned int i=0;i<compound.numChildren();i++)
  {
    MFnAttribute child(compound.child(i));
    MString childName = child.name();
    FabricCore::RTVal childNameRTVal = FabricSplice::constructStringRTVal(childName.asChar());
    FabricCore::RTVal childRTVal = rtVal.callMethod("Param", "getParam", 1, &childNameRTVal);
    valueType = childRTVal.callMethod("String", "getValueType", 0, 0).getStringCString();

    if(!rtVal.callMethod("Boolean", "hasParam", 1, &childNameRTVal).getBoolean())
    {
      mayaLogFunc("Compound attribute child '"+childName+"' exists, but not found as child KL parameter.");
      continue;
    }

    MStatus attrStatus;

    MFnNumericAttribute nAttr(child.object(), &attrStatus);
    if(attrStatus == MS::kSuccess)
    {
      if(nAttr.unitType() == MFnNumericData::kBoolean)
      {
        if(!nAttr.isArray())
        {
          if(valueType != "Boolean")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a BooleanParam.");
            return;
          }

          childRTVal = rtVal.callMethod("BooleanParam", "getParam", 1, &childNameRTVal);
          MDataHandle childHandle(handle.child(child.object()));
          childHandle.setBool(childRTVal.callMethod("Boolean", "getValue", 0, 0).getBoolean());
        }
        else
        {
          if(valueType != "Boolean[]")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a BooleanArrayParam.");
            return;
          }

          childRTVal = rtVal.callMethod("BooleanArrayParam", "getParam", 1, &childNameRTVal);
          FabricCore::RTVal arrayValues = childRTVal.maybeGetMember("values");
          MArrayDataHandle childHandle(handle.child(child.object()));
          MArrayDataBuilder arraybuilder = childHandle.builder();

          for(unsigned int j=0;j<arrayValues.getArraySize();j++)
          {
            MDataHandle elementHandle = arraybuilder.addElement(i);
            elementHandle.setBool(arrayValues.getArrayElement(i).getBoolean());
          }

          childHandle.set(arraybuilder);
          childHandle.setAllClean();
        }
      }
      else if(nAttr.unitType() == MFnNumericData::kInt)
      {
        if(!nAttr.isArray())
        {
          if(valueType != "SInt32")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a SInt32Param.");
            return;
          }

          childRTVal = rtVal.callMethod("SInt32Param", "getParam", 1, &childNameRTVal);
          MDataHandle childHandle(handle.child(child.object()));
          childHandle.setInt(childRTVal.callMethod("SInt32", "getValue", 0, 0).getSInt32());
        }
        else
        {
          if(valueType != "SInt32[]")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a SInt32ArrayParam.");
            return;
          }

          childRTVal = rtVal.callMethod("SInt32ArrayParam", "getParam", 1, &childNameRTVal);
          FabricCore::RTVal arrayValues = childRTVal.maybeGetMember("values");
          MArrayDataHandle childHandle(handle.child(child.object()));
          MArrayDataBuilder arraybuilder = childHandle.builder();

          for(unsigned int j=0;j<arrayValues.getArraySize();j++)
          {
            MDataHandle elementHandle = arraybuilder.addElement(i);
            elementHandle.setInt(arrayValues.getArrayElement(i).getSInt32());
          }

          childHandle.set(arraybuilder);
          childHandle.setAllClean();
        }
      }
      else if(nAttr.unitType() == MFnNumericData::kFloat)
      {
        if(!nAttr.isArray())
        {
          if(valueType != "Float64")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a Float64Param.");
            return;
          }

          childRTVal = rtVal.callMethod("Float64Param", "getParam", 1, &childNameRTVal);
          MDataHandle childHandle(handle.child(child.object()));
          childHandle.setFloat(childRTVal.callMethod("Float64", "getValue", 0, 0).getFloat64());
        }
        else
        {
          if(valueType != "Float64[]")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a Float64ArrayParam.");
            return;
          }

          childRTVal = rtVal.callMethod("Float64ArrayParam", "getParam", 1, &childNameRTVal);
          FabricCore::RTVal arrayValues = childRTVal.maybeGetMember("values");
          MArrayDataHandle childHandle(handle.child(child.object()));
          MArrayDataBuilder arraybuilder = childHandle.builder();

          for(unsigned int j=0;j<arrayValues.getArraySize();j++)
          {
            MDataHandle elementHandle = arraybuilder.addElement(i);
            elementHandle.setFloat(arrayValues.getArrayElement(i).getFloat64());
          }

          childHandle.set(arraybuilder);
          childHandle.setAllClean();
        }
      }
      else if(nAttr.unitType() == MFnNumericData::kDouble)
      {
        if(!nAttr.isArray())
        {
          if(valueType != "Float64")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a Float64Param.");
            return;
          }

          childRTVal = rtVal.callMethod("Float64Param", "getParam", 1, &childNameRTVal);
          MDataHandle childHandle(handle.child(child.object()));
          childHandle.setDouble(childRTVal.callMethod("Float64", "getValue", 0, 0).getFloat64());
        }
        else
        {
          if(valueType != "Float64[]")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a Float64ArrayParam.");
            return;
          }

          childRTVal = rtVal.callMethod("Float64ArrayParam", "getParam", 1, &childNameRTVal);
          FabricCore::RTVal arrayValues = childRTVal.maybeGetMember("values");
          MArrayDataHandle childHandle(handle.child(child.object()));
          MArrayDataBuilder arraybuilder = childHandle.builder();

          for(unsigned int j=0;j<arrayValues.getArraySize();j++)
          {
            MDataHandle elementHandle = arraybuilder.addElement(i);
            elementHandle.setDouble(arrayValues.getArrayElement(i).getFloat64());
          }

          childHandle.set(arraybuilder);
          childHandle.setAllClean();
        }
      }
      else if(nAttr.unitType() == MFnNumericData::k3Double) // vec3
      {
        if(!nAttr.isArray())
        {
          if(valueType != "Vec3")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a Vec3Param.");
            return;
          }

          childRTVal = rtVal.callMethod("Vec3Param", "getParam", 1, &childNameRTVal);
          MDataHandle childHandle(handle.child(child.object()));

          FabricCore::RTVal value = childRTVal.maybeGetMember("value");
          MFloatVector v(
            getFloat64FromRTVal(value.maybeGetMember("x")),
            getFloat64FromRTVal(value.maybeGetMember("y")),
            getFloat64FromRTVal(value.maybeGetMember("z"))
          );
          childHandle.setMFloatVector(v);
        }
        else
        {
          if(valueType != "Vec3[]")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a Vec3ArrayParam.");
            return;
          }

          childRTVal = rtVal.callMethod("Vec3ArrayParam", "getParam", 1, &childNameRTVal);
          FabricCore::RTVal arrayValues = childRTVal.maybeGetMember("values");
          MArrayDataHandle childHandle(handle.child(child.object()));
          MArrayDataBuilder arraybuilder = childHandle.builder();

          for(unsigned int j=0;j<arrayValues.getArraySize();j++)
          {
            FabricCore::RTVal value = childRTVal.maybeGetMember("value");
            MFloatVector v(
              getFloat64FromRTVal(value.maybeGetMember("x")),
              getFloat64FromRTVal(value.maybeGetMember("y")),
              getFloat64FromRTVal(value.maybeGetMember("z"))
            );
            MDataHandle elementHandle = arraybuilder.addElement(i);
            elementHandle.setMFloatVector(v);
          }

          childHandle.set(arraybuilder);
          childHandle.setAllClean();
        }
      }
      else if(nAttr.unitType() == MFnNumericData::k3Float) // color
      {
        if(!nAttr.isArray())
        {
          if(valueType != "Color")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a ColorParam.");
            return;
          }

          childRTVal = rtVal.callMethod("ColorParam", "getParam", 1, &childNameRTVal);
          MDataHandle childHandle(handle.child(child.object()));

          FabricCore::RTVal value = childRTVal.maybeGetMember("value");
          MFloatVector v(
            getFloat64FromRTVal(value.maybeGetMember("r")),
            getFloat64FromRTVal(value.maybeGetMember("g")),
            getFloat64FromRTVal(value.maybeGetMember("b"))
          );
          childHandle.setMFloatVector(v);
        }
        else
        {
          if(valueType != "Color[]")
          {
            mayaLogErrorFunc("Incompatible param for compound attribute - expected a ColorArrayParam.");
            return;
          }

          childRTVal = rtVal.callMethod("ColorArrayParam", "getParam", 1, &childNameRTVal);
          FabricCore::RTVal arrayValues = childRTVal.maybeGetMember("values");
          MArrayDataHandle childHandle(handle.child(child.object()));
          MArrayDataBuilder arraybuilder = childHandle.builder();

          for(unsigned int j=0;j<arrayValues.getArraySize();j++)
          {
            FabricCore::RTVal value = childRTVal.maybeGetMember("value");
            MFloatVector v(
              getFloat64FromRTVal(value.maybeGetMember("r")),
              getFloat64FromRTVal(value.maybeGetMember("g")),
              getFloat64FromRTVal(value.maybeGetMember("b"))
            );
            MDataHandle elementHandle = arraybuilder.addElement(i);
            elementHandle.setMFloatVector(v);
          }

          childHandle.set(arraybuilder);
          childHandle.setAllClean();
        }
      }
      else
      {
        MFnNumericData::Type unitType = nAttr.unitType();
        mayaLogErrorFunc("Unsupported numeric attribute '"+childName+"'.");
        return;
      }
    }
    else
    {
      MFnTypedAttribute tAttr(child.object(), &attrStatus);
      if(attrStatus == MS::kSuccess)
      {
        if(tAttr.attrType() == MFnData::kString)
        {
          if(!tAttr.isArray())
          {
            if(valueType != "String")
            {
              mayaLogErrorFunc("Incompatible param for compound attribute - expected a String=Param.");
              return;
            }

            childRTVal = rtVal.callMethod("StringParam", "getParam", 1, &childNameRTVal);
            MDataHandle childHandle(handle.child(child.object()));

            FabricCore::RTVal value = childRTVal.maybeGetMember("value");
            childHandle.setString(value.getStringCString());
          }
          else
          {
           if(valueType != "String[]")
            {
              mayaLogErrorFunc("Incompatible param for compound attribute - expected a StringArrayParam.");
              return;
            }

            childRTVal = rtVal.callMethod("StringArrayParam", "getParam", 1, &childNameRTVal);
            FabricCore::RTVal arrayValues = childRTVal.maybeGetMember("values");
            MArrayDataHandle childHandle(handle.child(child.object()));
            MArrayDataBuilder arraybuilder = childHandle.builder();

            for(unsigned int j=0;j<arrayValues.getArraySize();j++)
            {
              FabricCore::RTVal value = childRTVal.maybeGetMember("value");
              MDataHandle elementHandle = arraybuilder.addElement(i);
              elementHandle.setString(value.getStringCString());
            }

            childHandle.set(arraybuilder);
            childHandle.setAllClean();
          }
        }
        else
        {
          mayaLogErrorFunc("Unsupported typed attribute '"+childName+"'.");
          return;
        }
      }
      else
      {
        MFnMatrixAttribute mAttr(child.object(), &attrStatus);
        if(attrStatus == MS::kSuccess)
        {
          if(!mAttr.isArray())
          {
            if(valueType != "Mat44")
            {
              mayaLogErrorFunc("Incompatible param for compound attribute - expected a Mat44Param.");
              return;
            }

            childRTVal = rtVal.callMethod("Mat44Param", "getParam", 1, &childNameRTVal);
            MDataHandle childHandle(handle.child(child.object()));

            FabricCore::RTVal value = childRTVal.maybeGetMember("value");
            MMatrix m;
            portToPlug_compound_convertMat44(m, value);
            childHandle.setMMatrix(m);
          }
          else
          {
            if(valueType != "Mat44[]")
            {
              mayaLogErrorFunc("Incompatible param for compound attribute - expected a Mat44ArrayParam.");
              return;
            }

            childRTVal = rtVal.callMethod("Mat44ArrayParam", "getParam", 1, &childNameRTVal);
            FabricCore::RTVal arrayValues = childRTVal.maybeGetMember("values");
            MArrayDataHandle childHandle(handle.child(child.object()));
            MArrayDataBuilder arraybuilder = childHandle.builder();

            for(unsigned int j=0;j<arrayValues.getArraySize();j++)
            {
              FabricCore::RTVal value = childRTVal.maybeGetMember("value");
              MDataHandle elementHandle = arraybuilder.addElement(i);
              MMatrix m;
              portToPlug_compound_convertMat44(m, value);
              elementHandle.setMMatrix(m);
            }

            childHandle.set(arraybuilder);
            childHandle.setAllClean();
          }
        }
        else
        {
          MFnCompoundAttribute cAttr(child.object(), &attrStatus);
          if(attrStatus == MS::kSuccess)
          {
            MFnCompoundAttribute cAttr(compound.child(i));
            if(!cAttr.isArray())
            {
              if(valueType != "Compound")
              {
                mayaLogErrorFunc("Incompatible param for compound attribute - expected a CompoundParam.");
                return;
              }

              MDataHandle childHandle(handle.child(child.object()));
              childRTVal = rtVal.callMethod("CompoundParam", "getParam", 1, &childNameRTVal);
              portToPlug_compound_convertCompound(cAttr, childHandle, childRTVal);
            }
          }
        }
      }
    }
  }
}

void portToPlug_compound(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  if(plug.isArray())
    return;

  MDataHandle handle = data.outputValue(plug);
  FabricCore::RTVal rtVal = port.getRTVal();
  MFnCompoundAttribute compound(plug.attribute());
  portToPlug_compound_convertCompound(compound, handle, rtVal);
  handle.setClean();
}

void portToPlug_bool(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.outputArrayValue(plug);
    MArrayDataBuilder arraybuilder = arrayHandle.builder();

    unsigned int elements = port.getArrayCount();

    MAYASPLICE_MEMORY_ALLOCATE(bool, elements);
    MAYASPLICE_MEMORY_GETPORT(port);

    for(unsigned int i = 0; i < elements; ++i){
      MDataHandle handle = arraybuilder.addElement(i);

      handle.setBool(MAYASPLICE_MEMORY_GETITEM(i));
    }

    MAYASPLICE_MEMORY_FREE();

    arrayHandle.set(arraybuilder);
    arrayHandle.setAllClean();
  }
  else{
    MDataHandle handle = data.outputValue(plug);
    handle.setBool(port.getRTVal().getBoolean());
  }
}

void portToPlug_integer(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.outputArrayValue(plug);
    MArrayDataBuilder arraybuilder = arrayHandle.builder();

    unsigned int elements = port.getArrayCount();

    MAYASPLICE_MEMORY_ALLOCATE(int32_t, elements);
    MAYASPLICE_MEMORY_GETPORT(port);

    for(unsigned int i = 0; i < elements; ++i){
      MDataHandle handle = arraybuilder.addElement(i);

      handle.setInt(MAYASPLICE_MEMORY_GETITEM(i));
    }

    MAYASPLICE_MEMORY_FREE();

    arrayHandle.set(arraybuilder);
    arrayHandle.setAllClean();
  }else{
    MDataHandle handle = data.outputValue(plug);
    if(handle.type() == MFnData::kIntArray) {
      unsigned int elements = port.getArrayCount();

      MIntArray arrayValues;
      arrayValues.setLength(elements);

      MAYASPLICE_MEMORY_ALLOCATE(int32_t, elements);
      MAYASPLICE_MEMORY_GETPORT(port);

      for(unsigned int i = 0; i < elements; ++i){
        arrayValues[i] = MAYASPLICE_MEMORY_GETITEM(i);
      }

      MAYASPLICE_MEMORY_FREE();
      handle.set(MFnIntArrayData().create(arrayValues));
    }else{
      FabricCore::RTVal rtVal = port.getRTVal();
      handle.setInt((int)getFloat64FromRTVal(rtVal));
    }
  }
}

void portToPlug_scalar(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  std::string scalarUnit = port.getStringOption("scalarUnit");
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.outputArrayValue(plug);
    MArrayDataBuilder arraybuilder = arrayHandle.builder();

    unsigned int elements = port.getArrayCount();

    MAYASPLICE_MEMORY_ALLOCATE(float, elements);
    MAYASPLICE_MEMORY_GETPORT(port);

    for(unsigned int i = 0; i < elements; ++i){
      MDataHandle handle = arraybuilder.addElement(i);

      if(scalarUnit == "time")
        handle.setMTime(MTime(MAYASPLICE_MEMORY_GETITEM(i), MTime::kSeconds));
      else if(scalarUnit == "angle")
        handle.setMAngle(MAngle(MAYASPLICE_MEMORY_GETITEM(i), MAngle::kRadians));
      else if(scalarUnit == "distance")
        handle.setMDistance(MDistance(MAYASPLICE_MEMORY_GETITEM(i), MDistance::kMillimeters));
      else
      {
        if(handle.numericType() == MFnNumericData::kFloat)
          handle.setFloat(MAYASPLICE_MEMORY_GETITEM(i));
        else
          handle.setDouble(MAYASPLICE_MEMORY_GETITEM(i));
      }
    }

    MAYASPLICE_MEMORY_FREE();

    arrayHandle.set(arraybuilder);
    arrayHandle.setAllClean();
  }
  else{
    MDataHandle handle = data.outputValue(plug);
    if(handle.type() == MFnData::kDoubleArray) {
      unsigned int elements = port.getArrayCount();

      MDoubleArray arrayValues;
      arrayValues.setLength(elements);
      port.getArrayData(&arrayValues[0], sizeof(double) * arrayValues.length());

      handle.set(MFnDoubleArrayData().create(arrayValues));
    }else{
      FabricCore::RTVal rtVal = port.getRTVal();
      double value = getFloat64FromRTVal(rtVal);
      if(value == DBL_MAX)
        return;
      if(scalarUnit == "time")
        handle.setMTime(MTime(value, MTime::kSeconds));
      else if(scalarUnit == "angle")
        handle.setMAngle(MAngle(value, MAngle::kRadians));
      else if(scalarUnit == "distance")
        handle.setMDistance(MDistance(value, MDistance::kMillimeters));
      else
      {
        if(handle.numericType() == MFnNumericData::kFloat)
          handle.setFloat(value);
        else
          handle.setDouble(value);
      }
    }
  }
}

void portToPlug_string(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.outputArrayValue(plug);
    MArrayDataBuilder arraybuilder = arrayHandle.builder();

    FabricCore::RTVal arrayVal = port.getRTVal();
    unsigned int elements = port.getArrayCount();
    for(unsigned int i = 0; i < elements; ++i){
      MDataHandle handle = arraybuilder.addElement(i);
      handle.setString(arrayVal.getArrayElement(i).getStringCString());
    }

    arrayHandle.set(arraybuilder);
    arrayHandle.setAllClean();
  }
  else{
    MDataHandle handle = data.outputValue(plug);
    handle.setString(MString(port.getRTVal().getStringCString()));
  }
}

void portToPlug_color(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.outputArrayValue(plug);
    MArrayDataBuilder arraybuilder = arrayHandle.builder();

    FabricCore::RTVal arrayVal = port.getRTVal();
    unsigned int elements = port.getArrayCount();
    for(unsigned int i = 0; i < elements; ++i){
      MDataHandle handle = arraybuilder.addElement(i);
      FabricCore::RTVal rtVal = arrayVal.getArrayElement(i);
      if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
        handle.setMFloatVector(MFloatVector(
          (float)getFloat64FromRTVal(rtVal.maybeGetMember("r")),
          (float)getFloat64FromRTVal(rtVal.maybeGetMember("g")),
          (float)getFloat64FromRTVal(rtVal.maybeGetMember("b"))
        ));
      }else{
        handle.setMVector(MVector(
          getFloat64FromRTVal(rtVal.maybeGetMember("r")),
          getFloat64FromRTVal(rtVal.maybeGetMember("g")),
          getFloat64FromRTVal(rtVal.maybeGetMember("b"))
        ));
      }
    }

    arrayHandle.set(arraybuilder);
    arrayHandle.setAllClean();
  }
  else{
    MDataHandle handle = data.outputValue(plug);

    FabricCore::RTVal rtVal = port.getRTVal();
    if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
      MFloatVector v(
        (float)getFloat64FromRTVal(rtVal.maybeGetMember("r")),
        (float)getFloat64FromRTVal(rtVal.maybeGetMember("g")),
        (float)getFloat64FromRTVal(rtVal.maybeGetMember("b"))
      );
      handle.setMFloatVector(v);
    }else{
      MVector v(
        getFloat64FromRTVal(rtVal.maybeGetMember("r")),
        getFloat64FromRTVal(rtVal.maybeGetMember("g")),
        getFloat64FromRTVal(rtVal.maybeGetMember("b"))
      );
      handle.setMVector(v);
    }
  }
}

void portToPlug_vec3(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.outputArrayValue(plug);
    MArrayDataBuilder arraybuilder = arrayHandle.builder();

    unsigned int elements = port.getArrayCount();

    MAYASPLICE_MEMORY_ALLOCATE(float, elements * 3);
    MAYASPLICE_MEMORY_GETPORT(port);

    unsigned int offset = 0;
    for(unsigned int i = 0; i < elements; ++i){
      MDataHandle handle = arraybuilder.addElement(i);

      if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
        handle.set3Float(
          (float)MAYASPLICE_MEMORY_GETITEM(offset), 
          (float)MAYASPLICE_MEMORY_GETITEM(offset+1), 
          (float)MAYASPLICE_MEMORY_GETITEM(offset+2)
        );
      } else {
        handle.set3Double(
          MAYASPLICE_MEMORY_GETITEM(offset), 
          MAYASPLICE_MEMORY_GETITEM(offset+1), 
          MAYASPLICE_MEMORY_GETITEM(offset+2)
        );
      }
      offset+=3;
    }

    MAYASPLICE_MEMORY_FREE();

    arrayHandle.set(arraybuilder);
    arrayHandle.setAllClean();
  }
  else{
    MDataHandle handle = data.outputValue(plug);
    if(handle.type() == MFnData::kVectorArray) {
      unsigned int elements = port.getArrayCount();

      MVectorArray arrayValues;
      arrayValues.setLength(elements);

      MAYASPLICE_MEMORY_ALLOCATE(float, elements * 3);
      MAYASPLICE_MEMORY_GETPORT(port);

      size_t offset = 0;
      for(unsigned int i = 0; i < elements; ++i){
        arrayValues[i].x = MAYASPLICE_MEMORY_GETITEM(offset++);
        arrayValues[i].y = MAYASPLICE_MEMORY_GETITEM(offset++);
        arrayValues[i].z = MAYASPLICE_MEMORY_GETITEM(offset++);
      }

      MAYASPLICE_MEMORY_FREE();
      handle.set(MFnVectorArrayData().create(arrayValues));
    }else if(handle.type() == MFnData::kPointArray) {
      unsigned int elements = port.getArrayCount();

      MPointArray arrayValues;
      arrayValues.setLength(elements);

      MAYASPLICE_MEMORY_ALLOCATE(float, elements * 3);
      MAYASPLICE_MEMORY_GETPORT(port);

      size_t offset = 0;
      for(unsigned int i = 0; i < elements; ++i){
        arrayValues[i].x = MAYASPLICE_MEMORY_GETITEM(offset++);
        arrayValues[i].y = MAYASPLICE_MEMORY_GETITEM(offset++);
        arrayValues[i].z = MAYASPLICE_MEMORY_GETITEM(offset++);
      }

      MAYASPLICE_MEMORY_FREE();
      handle.set(MFnPointArrayData().create(arrayValues));
    }else{
      FabricCore::RTVal rtVal = port.getRTVal();
      if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
        handle.set3Float(
          getFloat64FromRTVal(rtVal.maybeGetMember("x")),
          getFloat64FromRTVal(rtVal.maybeGetMember("y")),
          getFloat64FromRTVal(rtVal.maybeGetMember("z"))
        );
      }else{
        handle.set3Double(
          getFloat64FromRTVal(rtVal.maybeGetMember("x")),
          getFloat64FromRTVal(rtVal.maybeGetMember("y")),
          getFloat64FromRTVal(rtVal.maybeGetMember("z"))
        );
      }
    }
  }
}

void portToPlug_euler(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.outputArrayValue(plug);
    MArrayDataBuilder arraybuilder = arrayHandle.builder();

    FabricCore::RTVal arrayVal = port.getRTVal();
    unsigned int elements = port.getArrayCount();
    for(unsigned int i = 0; i < elements; ++i){
      MDataHandle handle = arraybuilder.addElement(i);
      FabricCore::RTVal rtVal = arrayVal.getArrayElement(i);
      if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
        handle.set3Float(
          getFloat64FromRTVal(rtVal.maybeGetMember("x")),
          getFloat64FromRTVal(rtVal.maybeGetMember("y")),
          getFloat64FromRTVal(rtVal.maybeGetMember("z"))
        );
      }else{
        handle.set3Double(
          getFloat64FromRTVal(rtVal.maybeGetMember("x")),
          getFloat64FromRTVal(rtVal.maybeGetMember("y")),
          getFloat64FromRTVal(rtVal.maybeGetMember("z"))
        );
      }
    }

    arrayHandle.set(arraybuilder);
    arrayHandle.setAllClean();
  }
  else{
    MDataHandle handle = data.outputValue(plug);

    FabricCore::RTVal rtVal = port.getRTVal();
    if(handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat){
      handle.set3Float(
        getFloat64FromRTVal(rtVal.maybeGetMember("x")),
        getFloat64FromRTVal(rtVal.maybeGetMember("y")),
        getFloat64FromRTVal(rtVal.maybeGetMember("z"))
      );
    }else{
      handle.set3Double(
        getFloat64FromRTVal(rtVal.maybeGetMember("x")),
        getFloat64FromRTVal(rtVal.maybeGetMember("y")),
        getFloat64FromRTVal(rtVal.maybeGetMember("z"))
      );
    }
  }
}

void portToPlug_mat44(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  if(plug.isArray()){
    MArrayDataHandle arrayHandle = data.outputArrayValue(plug);
    MArrayDataBuilder arraybuilder = arrayHandle.builder();

    unsigned int elements = port.getArrayCount();

    MAYASPLICE_MEMORY_ALLOCATE(float, elements * 16);
    MAYASPLICE_MEMORY_GETPORT(port);

    unsigned int offset = 0;
    for(unsigned int i = 0; i < elements; ++i){
      MDataHandle handle = arraybuilder.addElement(i);

      double vals[4][4] ={
        MAYASPLICE_MEMORY_GETITEM(offset), MAYASPLICE_MEMORY_GETITEM(offset+4), MAYASPLICE_MEMORY_GETITEM(offset+8), MAYASPLICE_MEMORY_GETITEM(offset+12), 
        MAYASPLICE_MEMORY_GETITEM(offset+1), MAYASPLICE_MEMORY_GETITEM(offset+5), MAYASPLICE_MEMORY_GETITEM(offset+9), MAYASPLICE_MEMORY_GETITEM(offset+13), 
        MAYASPLICE_MEMORY_GETITEM(offset+2), MAYASPLICE_MEMORY_GETITEM(offset+6), MAYASPLICE_MEMORY_GETITEM(offset+10), MAYASPLICE_MEMORY_GETITEM(offset+14), 
        MAYASPLICE_MEMORY_GETITEM(offset+3), MAYASPLICE_MEMORY_GETITEM(offset+7), MAYASPLICE_MEMORY_GETITEM(offset+11), MAYASPLICE_MEMORY_GETITEM(offset+15)
      };
      offset += 16;

      MMatrix mayaMat(vals);
      handle.setMMatrix(mayaMat);
    }

    MAYASPLICE_MEMORY_FREE();

    arrayHandle.set(arraybuilder);
    arrayHandle.setAllClean();
  }
  else{
    MDataHandle handle = data.outputValue(plug);

    FabricCore::RTVal rtVal = port.getRTVal();
    FabricCore::RTVal row0 = rtVal.maybeGetMember("row0");
    FabricCore::RTVal row1 = rtVal.maybeGetMember("row1");
    FabricCore::RTVal row2 = rtVal.maybeGetMember("row2");
    FabricCore::RTVal row3 = rtVal.maybeGetMember("row3");

    double vals[4][4] = {
      getFloat64FromRTVal(row0.maybeGetMember("x")), getFloat64FromRTVal(row1.maybeGetMember("x")), getFloat64FromRTVal(row2.maybeGetMember("x")), getFloat64FromRTVal(row3.maybeGetMember("x")),
      getFloat64FromRTVal(row0.maybeGetMember("y")), getFloat64FromRTVal(row1.maybeGetMember("y")), getFloat64FromRTVal(row2.maybeGetMember("y")), getFloat64FromRTVal(row3.maybeGetMember("y")),
      getFloat64FromRTVal(row0.maybeGetMember("z")), getFloat64FromRTVal(row1.maybeGetMember("z")), getFloat64FromRTVal(row2.maybeGetMember("z")), getFloat64FromRTVal(row3.maybeGetMember("z")),
      getFloat64FromRTVal(row0.maybeGetMember("t")), getFloat64FromRTVal(row1.maybeGetMember("t")), getFloat64FromRTVal(row2.maybeGetMember("t")), getFloat64FromRTVal(row3.maybeGetMember("t"))
    };

    MMatrix mayaMat(vals);

    handle.setMMatrix(mayaMat);
  }
}

void portToPlug_PolygonMesh_singleMesh(MDataHandle handle, FabricCore::RTVal rtMesh)
{
  unsigned int nbPoints = 0;
  unsigned int nbPolygons = 0;
  unsigned int nbSamples = 0;
  if(!rtMesh.isNullObject())
  {
    nbPoints = rtMesh.callMethod("UInt64", "pointCount", 0, 0).getUInt64();
    nbPolygons = rtMesh.callMethod("UInt64", "polygonCount", 0, 0).getUInt64();
    nbSamples = rtMesh.callMethod("UInt64", "polygonPointsCount", 0, 0).getUInt64();
  }

  MPointArray mayaPoints;
  MVectorArray mayaNormals;
  MIntArray mayaCounts, mayaIndices;

  mayaPoints.setLength(nbPoints);
  if(mayaPoints.length() > 0)
  {
    std::vector<FabricCore::RTVal> args(2);
    args[0] = FabricSplice::constructExternalArrayRTVal("Float64", mayaPoints.length() * 4, &mayaPoints[0]);
    args[1] = FabricSplice::constructUInt32RTVal(4); // components
    rtMesh.callMethod("", "getPointsAsExternalArray_d", 2, &args[0]);
  }

  mayaNormals.setLength(nbSamples);
  if(mayaNormals.length() > 0)
  {
    FabricCore::RTVal normalsVar = 
    FabricSplice::constructExternalArrayRTVal("Float64", mayaNormals.length() * 3, &mayaNormals[0]);
    rtMesh.callMethod("", "getNormalsAsExternalArray_d", 1, &normalsVar);
  }

  mayaCounts.setLength(nbPolygons);
  mayaIndices.setLength(nbSamples);
  if(mayaCounts.length() > 0 && mayaIndices.length() > 0)
  {
    std::vector<FabricCore::RTVal> args(2);
    args[0] = FabricSplice::constructExternalArrayRTVal("UInt32", mayaCounts.length(), &mayaCounts[0]);
    args[1] = FabricSplice::constructExternalArrayRTVal("UInt32", mayaIndices.length(), &mayaIndices[0]);
    rtMesh.callMethod("", "getTopologyAsCountsIndicesExternalArrays", 2, &args[0]);
  }

  MFnMeshData meshDataFn;
  MObject meshObject;
  MFnMesh mesh;
  meshObject = meshDataFn.create();
  if(mayaPoints.length() == 0 || mayaCounts.length() == 0 || mayaIndices.length() == 0)
  {
    mayaPoints.setLength(0);
    mayaCounts.setLength(0);
    mayaIndices.setLength(0);
    
    mayaPoints.append(MPoint(0,0,0));
    mayaPoints.append(MPoint(0,0,0));
    mayaPoints.append(MPoint(0,0,0));
    mayaCounts.append(3);
    mayaIndices.append(0);
    mayaIndices.append(1);
    mayaIndices.append(2);
    mesh.create(mayaPoints.length(), mayaCounts.length(), mayaPoints, mayaCounts, mayaIndices, meshObject);  
    mesh.updateSurface();
  }
  else
  {
    MIntArray normalFace, normalVertex;
    normalFace.setLength(mayaIndices.length());
    normalVertex.setLength(mayaIndices.length());        

    int face = 0;
    int vertex = 0;
    int offset = 0;

    if(mayaCounts[face] != 3 && mayaCounts[face] != 4)
    {
      MString mayaCountStr;
      mayaCountStr.set(mayaCounts[face]);
      mayaLogErrorFunc("PolygonMesh: Polygon with "+mayaCountStr+" vertices not supported.");
      return;
    }

    for(unsigned int i=0;i<mayaIndices.length();i++) {
      normalFace[i] = face;
      normalVertex[i] = mayaIndices[offset + vertex];

      if(vertex == 0)
      {
        int v0 = mayaIndices[offset];
        int v1 = mayaIndices[offset+1];
        int v2 = mayaIndices[offset+2];
        if(v0 >= mayaPoints.length())
        {
          MString indexStr;
          indexStr.set(v0);
          mayaLogErrorFunc("PolygonMesh: Point "+indexStr+" out of range.");
          return;
        }
        if(v1 >= mayaPoints.length())
        {
          MString indexStr;
          indexStr.set(v1);
          mayaLogErrorFunc("PolygonMesh: Point "+indexStr+" out of range.");
          return;
        }
        if(v2 >= mayaPoints.length())
        {
          MString indexStr;
          indexStr.set(v2);
          mayaLogErrorFunc("PolygonMesh: Point "+indexStr+" out of range.");
          return;
        }
        if(v0 == v1 || v0 == v2 || v1 == v2)
        {
          MString indexStr;
          indexStr.set(face);
          mayaLogErrorFunc("PolygonMesh: Polygon corrupt polygon ["+indexStr+"].");
          return;
        }
        if(mayaCounts[face] > 3)
        {
          int v3 = mayaIndices[offset+3];
          if(v3 >= mayaPoints.length())
          {
            MString indexStr;
            indexStr.set(v3);
            mayaLogErrorFunc("PolygonMesh: Point "+indexStr+" out of range.");
            return;
          }
          if(v3 == v0 || v3 == v1 || v3 == v2)
          {
            MString indexStr;
            indexStr.set(face);
            mayaLogErrorFunc("PolygonMesh: Polygon corrupt polygon ["+indexStr+"].");
            return;
          }
        }
      }

      vertex++;

      if(vertex == mayaCounts[face])
      {
        offset += mayaCounts[face];
        face++;
        vertex = 0;

        if(face == mayaCounts.length())
        {
          if(i != mayaIndices.length() - 1)
          {
            mayaLogErrorFunc("PolygonMesh: Corrupt mayaCounts vs mayaIndices.");
            return;
          }
        }
        else if(mayaCounts[face] != 3 && mayaCounts[face] != 4)
        {
          MString mayaCountStr;
          mayaCountStr.set(mayaCounts[face]);
          mayaLogErrorFunc("PolygonMesh: Polygon with "+mayaCountStr+" vertices not supported.");
          return;
        }
      }
    }
  
    mesh.create(mayaPoints.length(), mayaCounts.length(), mayaPoints, mayaCounts, mayaIndices, meshObject);  
    mesh.updateSurface();
    mayaPoints.clear();
    mesh.setFaceVertexNormals( mayaNormals, normalFace, normalVertex );

    if(rtMesh.callMethod("Boolean", "hasUVs", 0, 0).getBoolean())
    {
      MFloatArray values(nbSamples*2);
      std::vector<FabricCore::RTVal> args(2);
      args[0] = FabricSplice::constructExternalArrayRTVal("Float32", values.length(), &values[0]);
      args[1] = FabricSplice::constructUInt32RTVal(2); // components
      rtMesh.callMethod("", "getUVsAsExternalArray", 2, &args[0]);

      MFloatArray u, v;
      u.setLength(nbSamples);      
      v.setLength(nbSamples);      
      unsigned int offset = 0;
      for(unsigned int i=0;i<u.length();i++)
      {
        u[i] = values[offset++];
        v[i] = values[offset++];
      }
      values.clear();
      MString setName("map1");
      mesh.createUVSet(setName);
      mesh.setCurrentUVSetName(setName);

      mesh.setUVs(u, v);

      MIntArray indices(nbSamples);
      for(unsigned int i=0;i<nbSamples;i++)
        indices[i] = i;
      mesh.assignUVs(mayaCounts, indices);
    }

    if(rtMesh.callMethod("Boolean", "hasVertexColors", 0, 0).getBoolean())
    {
      MColorArray values(nbSamples);
      std::vector<FabricCore::RTVal> args(2);
      args[0] = FabricSplice::constructExternalArrayRTVal("Float32", values.length() * 4, &values[0]);
      args[1] = FabricSplice::constructUInt32RTVal(4); // components
      rtMesh.callMethod("", "getVertexColorsAsExternalArray", 2, &args[0]);

      MString setName("colorSet");
      mesh.createColorSet(setName);
      mesh.setCurrentColorSetName(setName);

      MIntArray face(nbSamples);

      unsigned int offset = 0;
      for(unsigned int i=0;i<mayaCounts.length();i++)
      {
        for(unsigned int j=0;j<mayaCounts[i];j++,offset++)
        {
          face[offset] = i;
        }
      }

      mesh.setFaceVertexColors(values, face, mayaIndices);
    }

    handle.set(meshObject);
    handle.setClean();
  }

}

void portToPlug_PolygonMesh(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  try
  {
    if(plug.isArray())
    {
      MArrayDataHandle arrayHandle = data.outputArrayValue(plug);
      MArrayDataBuilder arraybuilder = arrayHandle.builder();

      unsigned int elements = port.getArrayCount();
      FabricCore::RTVal polygonMeshArray = port.getRTVal();
      for(unsigned int i = 0; i < elements; ++i)
        portToPlug_PolygonMesh_singleMesh(arraybuilder.addElement(i), polygonMeshArray.getArrayElement(i));

      arrayHandle.set(arraybuilder);
      arrayHandle.setAllClean();
    }
    else
    {
      MDataHandle handle = data.outputValue(plug.attribute());
      portToPlug_PolygonMesh_singleMesh(handle, port.getRTVal());
    }
  }
  catch(FabricCore::Exception e)
  {
    mayaLogErrorFunc(e.getDesc_cstr());
    return;
  }
  catch(FabricSplice::Exception e)
  {
    mayaLogErrorFunc(e.what());
    return;
  }
}

void portToPlug_Lines_singleLines(MDataHandle handle, FabricCore::RTVal rtVal)
{
  unsigned int nbPoints = 0;
  unsigned int nbSegments = 0;
  if(!rtVal.isNullObject())
  {
    nbPoints = rtVal.callMethod("UInt64", "pointCount", 0, 0).getUInt64();
    nbSegments = rtVal.callMethod("UInt64", "lineCount", 0, 0).getUInt64();
  }

  MPointArray mayaPoints(nbPoints);
  std::vector<double> mayaDoubles(nbPoints * 3);
  std::vector<uint32_t> mayaIndices(nbSegments*2);
  MDoubleArray mayaKnots(nbPoints);

  if(nbPoints > 0)
  {
    FabricCore::RTVal mayaDoublesVal = FabricSplice::constructExternalArrayRTVal("Float64", mayaDoubles.size(), &mayaDoubles[0]);
    rtVal.callMethod("", "_getPositionsAsExternalArray_d", 1, &mayaDoublesVal);
  }

  if(nbSegments > 0)
  {
    FabricCore::RTVal mayaIndicesVal = FabricSplice::constructExternalArrayRTVal("UInt32", mayaIndices.size(), &mayaIndices[0]);
    rtVal.callMethod("", "_getTopologyAsExternalArray", 1, &mayaIndicesVal);
  }

  size_t nbCurves = 1;
  size_t offset = 0;
  for(unsigned int i=0;i<nbPoints;i++) {
    mayaPoints[i].x = mayaDoubles[offset++];
    mayaPoints[i].y = mayaDoubles[offset++];
    mayaPoints[i].z = mayaDoubles[offset++];
    mayaPoints[i].w = 1.0;
    mayaKnots[i] = (double)i;
  }

  MFnNurbsCurveData curveDataFn;
  MObject curveObject;
  MFnNurbsCurve curve;
  curveObject = curveDataFn.create();

  curve.create(
    mayaPoints, mayaKnots, 1, 
    mayaIndices[0] == mayaIndices[mayaIndices.size()-1] ? MFnNurbsCurve::kClosed : MFnNurbsCurve::kOpen, 
    false,
    false,
    curveObject);

  handle.set(curveObject);
  handle.setClean();
}

void portToPlug_Lines(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  try
  {
    if(plug.isArray())
    {
      MArrayDataHandle arrayHandle = data.outputArrayValue(plug);
      MArrayDataBuilder arraybuilder = arrayHandle.builder();

      unsigned int elements = port.getArrayCount();
      FabricCore::RTVal rtVal = port.getRTVal();
      for(unsigned int i = 0; i < elements; ++i)
        portToPlug_Lines_singleLines(arraybuilder.addElement(i), rtVal.getArrayElement(i));

      arrayHandle.set(arraybuilder);
      arrayHandle.setAllClean();
    }
    else
    {
      MDataHandle handle = data.outputValue(plug.attribute());
      portToPlug_Lines_singleLines(handle, port.getRTVal());
    }
  }
  catch(FabricCore::Exception e)
  {
    mayaLogErrorFunc(e.getDesc_cstr());
    return;
  }
  catch(FabricSplice::Exception e)
  {
    mayaLogErrorFunc(e.what());
    return;
  }
}

void portToPlug_spliceMayaData(FabricSplice::DGPort & port, MPlug &plug, MDataBlock &data){
  MStatus status;
  try{
    if(!plug.isArray()){
      MFnFabricSpliceMayaData mfnpd;
      MObject spliceMayaDataObj = mfnpd.create(&status);
      FabricSpliceMayaData *spliceMayaData =(FabricSpliceMayaData *)mfnpd.data();
      spliceMayaData->setRTVal(port.getRTVal());

      MDataHandle handle = data.outputValue(plug);
      handle.set(spliceMayaDataObj);
    } else {
      if(!port.isArray())
        return;
      FabricCore::RTVal value = port.getRTVal();

      MArrayDataHandle arrayHandle = data.outputArrayValue(plug);
      MArrayDataBuilder arraybuilder = arrayHandle.builder();

      unsigned int elements = value.getArraySize();
      for(unsigned int i = 0; i < elements; ++i)
      {
        MDataHandle handle = arraybuilder.addElement(i);
        MFnFabricSpliceMayaData mfnpd;
        MObject spliceMayaDataObj = mfnpd.create(&status);
        FabricSpliceMayaData *spliceMayaData =(FabricSpliceMayaData *)mfnpd.data();
        spliceMayaData->setRTVal(value.getArrayElement(i));
        handle.set(spliceMayaDataObj);
      }

      arrayHandle.set(arraybuilder);
      arrayHandle.setAllClean();
    }
  }
  catch(FabricCore::Exception e)
  {
    mayaLogErrorFunc(e.getDesc_cstr());
    return;
  }
}

SplicePlugToPortFunc getSplicePlugToPortFunc(const std::string & dataType, const FabricSplice::DGPort * port)
{
  if(dataType == "CompoundParam")
    return plugToPort_compound;
  if(dataType == "Boolean")
    return plugToPort_bool;
  if(dataType == "Integer")
    return plugToPort_integer;
  if(dataType == "Scalar")
    return plugToPort_scalar;
  if(dataType == "String")
    return plugToPort_string;
  if(dataType == "Color")
    return plugToPort_color;
  if(dataType == "Vec3")
    return plugToPort_vec3;
  if(dataType == "Euler")
    return plugToPort_euler;
  if(dataType == "Mat44")
    return plugToPort_mat44;
  if(dataType == "PolygonMesh")
    return plugToPort_PolygonMesh;
  if(dataType == "Lines")
    return plugToPort_Lines;
  if(dataType == "KeyframeTrack")
    return plugToPort_KeyframeTrack;
  if(dataType == "SpliceMayaData")
    return plugToPort_spliceMayaData;

  return NULL;  
}

SplicePortToPlugFunc getSplicePortToPlugFunc(const std::string & dataType, const FabricSplice::DGPort * port)
{
  if(dataType == "CompoundParam")
    return portToPlug_compound;
  if(dataType == "Boolean")
    return portToPlug_bool;
  if(dataType == "Integer")
    return portToPlug_integer;
  if(dataType == "Scalar")
    return portToPlug_scalar;
  if(dataType == "String")
    return portToPlug_string;
  if(dataType == "Color")
    return portToPlug_color;
  if(dataType == "Vec3")
    return portToPlug_vec3;
  if(dataType == "Euler")
    return portToPlug_euler;
  if(dataType == "Mat44")
    return portToPlug_mat44;
  if(dataType == "PolygonMesh")
    return portToPlug_PolygonMesh;
  if(dataType == "Lines")
    return portToPlug_Lines;
  if(dataType == "SpliceMayaData")
    return portToPlug_spliceMayaData;

  return NULL;  
}

MString getSpliceDataTypeFromMPlug(const MPlug &plug){
  MString dataType = "";
  MStatus handleStat;
  MDataHandle dataHandle = plug.asMDataHandle(MDGContext::fsNormal, &handleStat);

  if(handleStat == MStatus::kSuccess){
    if(dataHandle.isNumeric()){
      if(dataHandle.numericType() == MFnNumericData::kFloat ||
        dataHandle.numericType() == MFnNumericData::kDouble){
        dataType = "Scalar";
      }
      else if(dataHandle.numericType() == MFnNumericData::kLong){
        dataType = "Integer";
      }
      else if(dataHandle.numericType() == MFnNumericData::k3Float ||
        dataHandle.numericType() == MFnNumericData::k3Double){
        dataType = "Vec3";
      }
      else{
        MStatus stat;
        MFnMatrixAttribute mattr(plug.attribute(), &stat);
        
        if(stat == MStatus::kSuccess){
          dataType = "Mat44";
        }
      }
    }
    else{
      // avoid string multi attr causing a crash!
      if(!plug.isArray() && dataHandle.type() & MFnData::kString){ 
        dataType = "String";
      }
    }

    if(plug.isArray() && dataType.length() > 0){
      dataType += "[]";
    }
  } else if(!plug.isArray()){
    if(dataHandle.type() == MFnData::kDoubleArray){
      dataType = "Scalar[]";
    } else if(dataHandle.type() == MFnData::kIntArray){
      dataType = "Integer[]";
    } else if(dataHandle.type() == MFnData::kVectorArray){
      dataType = "Vec3[]";
    } else if(dataHandle.type() == MFnData::kPointArray){
      dataType = "Vec3[]";
    } else{
      mayaLogErrorFunc("MDataHandle invalid!");
    }
  } 
  else{
    mayaLogErrorFunc("MDataHandle invalid!");
  }

  return dataType;
}
