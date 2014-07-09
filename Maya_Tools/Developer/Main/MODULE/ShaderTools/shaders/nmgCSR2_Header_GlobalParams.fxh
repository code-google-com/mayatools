
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//bool spacerPreMoreParams<string UIName   = "******************************************";> = false;
//bool spacerMoreParams<string UIName      = "***** + (MORE PARAMS) *****";> = false;
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////// Alpha Clip (1 bit)///////////////////////
float clipPoint
<
  float UIMin     = 0.0;
  float UIMax     = 1.0;
  float UIStep    = 0.01;
  string UIName   = "Alpha Clip Value";
> = 0.5;

////////////////////// Global params///////////////////////
float globalTonemap
<
  float UIMin     = 0.0;
  float UIMax     = 1.0;
  float UIStep    = 0.1;
  string UIName   = "Basic Global Tonemapping";
> = 0.0;

float exposure
<
  float UIMin     = -10.0;
  float UIMax     = 10.0;
  float UIStep    = 0.1;
  string UIName   = "Global Exposure";
> = 0.0;

//Ambient
float3 ambientColor
<
  string UIName   = "Global Ambient Color";
  string Type     = "Color";
> = {0.0, 0.0, 0.0};

//Linear Color Math
bool linear
<
  string UIName   = "Linear Color Math?";
> = false;
